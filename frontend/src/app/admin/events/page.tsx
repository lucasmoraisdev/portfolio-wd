"use client";

import React, { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import {
  Plus,
  Trash2,
  Edit2,
  ToggleLeft,
  ToggleRight,
  Loader2,
  X,
  AlertCircle,
  Upload as UploadIcon,
  Calendar as CalendarIcon,
  MapPin,
  Star,
} from "lucide-react";

import api from "../../../services/api";
import { Event } from "../../../types";

export default function EventsAdminPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form Modal States
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingEvent, setEditingEvent] = useState<Event | null>(null);
  const [formTitle, setFormTitle] = useState("");
  const [formCity, setFormCity] = useState("");
  const [formClient, setFormClient] = useState("");
  const [formDate, setFormDate] = useState("");
  const [formDescription, setFormDescription] = useState("");
  const [formOrder, setFormOrder] = useState(0);
  const [formIsActive, setFormIsActive] = useState(true);
  const [formIsFeatured, setFormIsFeatured] = useState(false);
  
  // Images
  const [formCoverId, setFormCoverId] = useState<string | null>(null);
  const [formCoverUrl, setFormCoverUrl] = useState<string | null>(null);
  const [formGalleryIds, setFormGalleryIds] = useState<string[]>([]);
  const [formGalleryUrls, setFormGalleryUrls] = useState<string[]>([]);
  const [selectedGalleryIds, setSelectedGalleryIds] = useState<string[]>([]);
  const [deletingImages, setDeletingImages] = useState(false);

  const [uploadingCover, setUploadingCover] = useState(false);
  const [uploadingGallery, setUploadingGallery] = useState(false);
  const [formSubmitting, setFormSubmitting] = useState(false);

  const searchParams = useSearchParams();

  // Load Events
  const loadEvents = async () => {
    setLoading(true);
    try {
      const res = await api.events.listAdmin();
      if (res?.data?.items) {
        setEvents(res.data.items);
      }
    } catch (err: any) {
      setError(err.message || "Erro ao carregar eventos.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  // Handle action parameter from dashboard (e.g. ?action=new)
  useEffect(() => {
    if (searchParams.get("action") === "new" && !loading) {
      handleOpenCreateModal();
    }
  }, [searchParams, loading]);

  const handleOpenCreateModal = () => {
    setEditingEvent(null);
    setFormTitle("");
    setFormCity("");
    setFormClient("");
    setFormDate(new Date().toISOString().split("T")[0]);
    setFormDescription("");
    setFormOrder(0);
    setFormIsActive(true);
    setFormIsFeatured(false);
    setFormCoverId(null);
    setFormCoverUrl(null);
    setFormGalleryIds([]);
    setFormGalleryUrls([]);
    setSelectedGalleryIds([]);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (event: Event) => {
    setEditingEvent(event);
    setFormTitle(event.title);
    setFormCity(event.city);
    setFormClient(event.client);
    setFormDate(event.event_date);
    setFormDescription(event.description || "");
    setFormOrder(event.display_order);
    setFormIsActive(event.is_active);
    setFormIsFeatured(event.is_featured);
    setFormCoverId(event.cover_image_id);
    setFormCoverUrl(event.cover_image_url || null);
    setFormGalleryIds(event.gallery_image_ids || []);
    setFormGalleryUrls(event.gallery_urls || []);
    setSelectedGalleryIds([]);
    setIsModalOpen(true);
  };

  const handleCoverUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadingCover(true);
    try {
      const res = await api.upload.file(file);
      if (res?.data?.id) {
        setFormCoverId(res.data.id);
        setFormCoverUrl(res.data.public_url);
      }
    } catch (err: any) {
      alert(err.message || "Erro ao enviar capa.");
    } finally {
      setUploadingCover(false);
    }
  };

  const handleGalleryUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setUploadingGallery(true);
    try {
      const res = await api.upload.files(Array.from(files));
      if (res?.data) {
        const newIds = res.data.map((item) => item.id);
        const newUrls = res.data.map((item) => item.public_url);

        const updatedIds = [...formGalleryIds, ...newIds];
        const updatedUrls = [...formGalleryUrls, ...newUrls];

        setFormGalleryIds(updatedIds);
        setFormGalleryUrls(updatedUrls);

        if (editingEvent) {
          await api.events.update(editingEvent.id, {
            gallery_image_ids: updatedIds,
          });
          loadEvents();
        }
      }
    } catch (err: any) {
      alert(err.message || "Erro ao enviar imagens.");
    } finally {
      setUploadingGallery(false);
    }
  };

  const handleToggleSelectImage = (id: string) => {
    if (selectedGalleryIds.includes(id)) {
      setSelectedGalleryIds(selectedGalleryIds.filter((item) => item !== id));
    } else {
      setSelectedGalleryIds([...selectedGalleryIds, id]);
    }
  };

  const handleDeleteSelectedImages = async () => {
    if (selectedGalleryIds.length === 0) return;

    const confirmMsg = selectedGalleryIds.length === 1
      ? "Tem certeza que deseja deletar permanentemente esta imagem do servidor?"
      : `Tem certeza que deseja deletar permanentemente as ${selectedGalleryIds.length} imagens selecionadas do servidor?\n\nEsta ação irá remover as mídias de forma definitiva.`;

    if (!confirm(confirmMsg)) return;

    setDeletingImages(true);
    try {
      await Promise.all(selectedGalleryIds.map((id) => api.upload.delete(id)));

      const remainingIndices = formGalleryIds.reduce<number[]>((acc, id, index) => {
        if (!selectedGalleryIds.includes(id)) {
          acc.push(index);
        }
        return acc;
      }, []);

      setFormGalleryIds(remainingIndices.map((idx) => formGalleryIds[idx]));
      setFormGalleryUrls(remainingIndices.map((idx) => formGalleryUrls[idx]));
      setSelectedGalleryIds([]);
    } catch (err: any) {
      const errMsg = (err.message || "").toLowerCase();
      const isFileNotFound = 
        errMsg.includes("not found") || 
        errMsg.includes("não encontrado") || 
        errMsg.includes("404") || 
        errMsg.includes("file_not_found");

      if (!isFileNotFound) {
        alert(err.message || "Erro ao deletar imagens do servidor.");
      }
      window.location.reload();
    } finally {
      setDeletingImages(false);
    }
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formTitle || !formCity || !formClient || !formDate) return;

    // Validate display order uniqueness locally
    const orderConflict = events.some((event) => 
      event.display_order === formOrder && 
      (!editingEvent || event.id !== editingEvent.id)
    );
    if (orderConflict) {
      alert(`A ordem de exibição ${formOrder} já está sendo usada por outro evento.`);
      return;
    }

    setFormSubmitting(true);
    try {
      const payload = {
        title: formTitle,
        city: formCity,
        client: formClient,
        event_date: formDate,
        description: formDescription || null,
        display_order: formOrder,
        is_active: formIsActive,
        is_featured: formIsFeatured,
        cover_image_id: formCoverId,
        gallery_image_ids: formGalleryIds,
      };

      if (editingEvent) {
        // Edit Mode
        await api.events.update(editingEvent.id, payload);
      } else {
        // Create Mode
        await api.events.create(payload);
      }
      setIsModalOpen(false);
      loadEvents();
    } catch (err: any) {
      alert(err.message || "Erro ao salvar evento.");
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Tem certeza que deseja excluir permanentemente este evento do portfólio?")) return;

    try {
      await api.events.delete(id);
      loadEvents();
    } catch (err: any) {
      alert(err.message || "Erro ao deletar evento.");
    }
  };

  const handleToggleActive = async (event: Event) => {
    try {
      await api.events.toggleStatus(event.id);
      setEvents(
        events.map((e) => (e.id === event.id ? { ...e, is_active: !e.is_active } : e))
      );
    } catch (err: any) {
      alert(err.message || "Erro ao alterar status.");
    }
  };

  const handleToggleFeatured = async (event: Event) => {
    try {
      await api.events.toggleFeatured(event.id);
      setEvents(
        events.map((e) => (e.id === event.id ? { ...e, is_featured: !e.is_featured } : e))
      );
    } catch (err: any) {
      alert(err.message || "Erro ao alterar destaque.");
    }
  };

  if (loading && events.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="animate-spin text-rose-500" size={32} />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
        <div className="flex flex-col gap-2">
          <h2 className="text-2xl font-black text-slate-100">Eventos & Shows</h2>
          <p className="text-sm text-slate-400">
            Gerencie a vitrine de eventos realizados para atrair mais clientes.
          </p>
        </div>
        <button
          onClick={handleOpenCreateModal}
          className="px-5 py-3 rounded-xl bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black text-sm flex items-center justify-center gap-2 cursor-pointer transition-all hover:scale-[1.02]"
        >
          <Plus size={18} />
          Novo Evento
        </button>
      </div>

      {/* Error alert */}
      {error && (
        <div className="p-4 bg-rose-950/20 border border-rose-950/30 rounded-2xl text-rose-400 text-sm flex items-center gap-2">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Events Table / List */}
      {events.length === 0 ? (
        <div className="p-16 border border-dashed border-slate-800 rounded-3xl text-center text-slate-500">
          Nenhum evento cadastrado. Clique em "Novo Evento" para começar.
        </div>
      ) : (
        <div className="bg-slate-900 border border-slate-800/80 rounded-3xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-widest bg-slate-900/50">
                  <th className="px-6 py-4">Evento</th>
                  <th className="px-6 py-4">Localização</th>
                  <th className="px-6 py-4">Cliente</th>
                  <th className="px-6 py-4">Data</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40 text-sm">
                {events.map((event) => (
                  <tr key={event.id} className="hover:bg-slate-800/20 transition-colors">
                    <td className="px-6 py-4 font-bold text-slate-200">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-slate-950 border border-slate-850 flex items-center justify-center font-bold text-slate-400 text-xs overflow-hidden shrink-0">
                          {event.cover_image_url ? (
                            <img
                              src={event.cover_image_url}
                              alt={event.title}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <span>🎉</span>
                          )}
                        </div>
                        <span className="truncate max-w-xs">{event.title}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-slate-450">
                      <div className="flex items-center gap-1.5">
                        <MapPin size={12} className="text-slate-550" />
                        <span>{event.city}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-slate-450">{event.client}</td>
                    <td className="px-6 py-4 text-slate-450">
                      <div className="flex items-center gap-1.5">
                        <CalendarIcon size={12} className="text-slate-550" />
                        <span>{event.event_date}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleToggleActive(event)}
                          className={`px-3 py-1 rounded-full text-xs font-bold transition-all cursor-pointer ${
                            event.is_active
                              ? "bg-emerald-500/10 text-emerald-400"
                              : "bg-slate-800 text-slate-500"
                          }`}
                        >
                          {event.is_active ? "Ativo" : "Inativo"}
                        </button>
                        <button
                          onClick={() => handleToggleFeatured(event)}
                          className={`p-1.5 rounded-full transition-all cursor-pointer ${
                            event.is_featured
                              ? "bg-amber-500/10 text-amber-400"
                              : "bg-slate-800 text-slate-500"
                          }`}
                          title="Destaque"
                        >
                          <Star size={12} fill={event.is_featured ? "currentColor" : "none"} />
                        </button>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-3">
                        <button
                          onClick={() => handleOpenEditModal(event)}
                          className="p-2 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-xl"
                          title="Editar"
                        >
                          <Edit2 size={16} />
                        </button>
                        <button
                          onClick={() => handleDelete(event.id)}
                          className="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-xl"
                          title="Excluir"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Form Modal Dialog */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-2xl w-full max-h-[90vh] flex flex-col overflow-hidden shadow-2xl relative">
            <div className="flex justify-between items-center px-8 py-6 border-b border-slate-800/80 shrink-0">
              <h3 className="font-extrabold text-slate-100">
                {editingEvent ? "Editar Evento" : "Novo Evento"}
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="p-2 text-slate-400 hover:text-slate-100 rounded-xl"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleFormSubmit} className="p-8 flex flex-col gap-6 overflow-y-auto flex-1">
              {/* Cover Photo selector */}
              <div className="flex items-center gap-6 p-4 bg-slate-950 border border-slate-800 rounded-2xl">
                <div className="w-20 h-16 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center font-bold text-slate-500 overflow-hidden shrink-0 text-xs">
                  {formCoverUrl ? (
                    <img src={formCoverUrl} alt="Cover Preview" className="w-full h-full object-cover" />
                  ) : (
                    "CAPA"
                  )}
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Foto de Capa</label>
                  <div className="relative">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleCoverUpload}
                      className="hidden"
                      id="cover-upload-input"
                    />
                    <label
                      htmlFor="cover-upload-input"
                      className="px-4 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 font-bold text-xs rounded-xl flex items-center gap-2 cursor-pointer transition-colors animate-fade-in"
                    >
                      {uploadingCover ? (
                        <>
                          <Loader2 size={14} className="animate-spin" /> Enviando...
                        </>
                      ) : (
                        <>
                          <UploadIcon size={14} /> Selecionar Foto
                        </>
                      )}
                    </label>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Título do Evento</label>
                  <input
                    type="text"
                    required
                    value={formTitle}
                    onChange={(e) => setFormTitle(e.target.value)}
                    placeholder="Ex: Aniversário Tema Vingadores"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Cliente</label>
                  <input
                    type="text"
                    required
                    value={formClient}
                    onChange={(e) => setFormClient(e.target.value)}
                    placeholder="Ex: Família Santos"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Cidade</label>
                  <input
                    type="text"
                    required
                    value={formCity}
                    onChange={(e) => setFormCity(e.target.value)}
                    placeholder="Ex: São Paulo"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Data de Realização</label>
                  <input
                    type="date"
                    required
                    value={formDate}
                    onChange={(e) => setFormDate(e.target.value)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none font-bold"
                  />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Descrição Completa</label>
                <textarea
                  rows={4}
                  value={formDescription}
                  onChange={(e) => setFormDescription(e.target.value)}
                  placeholder="Escreva como foi realizado o evento, quais atrações e brinquedos montados..."
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none resize-none"
                />
              </div>

              {/* Photos Gallery uploads */}
              <div className="flex flex-col gap-3">
                <div className="flex justify-between items-center h-8">
                  <label className="text-xs text-slate-400 font-bold uppercase">Galeria de Fotos do Evento</label>
                  {selectedGalleryIds.length > 0 && (
                    <button
                      type="button"
                      disabled={deletingImages}
                      onClick={handleDeleteSelectedImages}
                      className="px-3 py-1 bg-rose-950 hover:bg-rose-900 text-rose-200 hover:text-rose-100 border border-rose-800 text-xs font-bold rounded-lg flex items-center gap-1.5 transition-colors duration-200 cursor-pointer disabled:opacity-50"
                    >
                      {deletingImages ? (
                        <>
                          <Loader2 size={12} className="animate-spin text-rose-500" />
                          <span>Deletando...</span>
                        </>
                      ) : (
                        <>
                          <Trash2 size={12} />
                          <span>Deletar Selecionadas ({selectedGalleryIds.length})</span>
                        </>
                      )}
                    </button>
                  )}
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  {formGalleryUrls.map((url, index) => {
                    const imageId = formGalleryIds[index];
                    const isSelected = selectedGalleryIds.includes(imageId);
                    return (
                      <div
                        key={index}
                        onClick={() => handleToggleSelectImage(imageId)}
                        className={`relative h-24 bg-slate-950 rounded-xl border overflow-hidden cursor-pointer group/img transition-all duration-200 ${
                          isSelected 
                            ? "border-rose-500 ring-2 ring-rose-500/20" 
                            : "border-slate-850 hover:border-slate-700"
                        }`}
                      >
                        <img src={url} alt="Gallery item" className="w-full h-full object-cover select-none" />
                        {/* Checkbox overlay */}
                        <div className={`absolute top-2 left-2 w-5 h-5 rounded-md border flex items-center justify-center transition-all duration-250 ${
                          isSelected 
                            ? "bg-rose-500 border-rose-500 text-slate-100" 
                            : "bg-slate-950/80 border-slate-750 opacity-0 group-hover/img:opacity-100"
                        }`}>
                          {isSelected && (
                            <svg className="w-3 h-3 fill-current font-bold" viewBox="0 0 20 20">
                              <path d="M0 11l2-2 5 5L18 3l2 2L7 18z" />
                            </svg>
                          )}
                        </div>
                      </div>
                    );
                  })}
                  <div className="relative h-24">
                    <input
                      type="file"
                      multiple
                      accept="image/*"
                      id="event-gallery-upload-input"
                      className="hidden"
                      onChange={handleGalleryUpload}
                    />
                    <label
                      htmlFor="event-gallery-upload-input"
                      className="w-full h-full border border-dashed border-slate-800 hover:border-slate-700 bg-slate-950 hover:bg-slate-900 rounded-xl flex flex-col items-center justify-center gap-1.5 text-[10px] text-slate-500 hover:text-slate-350 cursor-pointer font-bold transition-all"
                    >
                      {uploadingGallery ? (
                        <>
                          <Loader2 size={16} className="animate-spin text-rose-500" />
                          <span>Enviando...</span>
                        </>
                      ) : (
                        <>
                          <UploadIcon size={16} />
                          <span>Adicionar Foto</span>
                        </>
                      )}
                    </label>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Exibição Ordem</label>
                  <input
                    type="number"
                    value={formOrder}
                    onChange={(e) => setFormOrder(parseInt(e.target.value) || 0)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none font-bold"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Ativo</label>
                  <div className="flex items-center h-full pt-1">
                    <button
                      type="button"
                      onClick={() => setFormIsActive(!formIsActive)}
                      className="text-slate-450 hover:text-slate-250 font-bold text-xs flex items-center gap-1.5 cursor-pointer"
                    >
                      {formIsActive ? (
                        <ToggleRight size={32} className="text-rose-500" />
                      ) : (
                        <ToggleLeft size={32} className="text-slate-700" />
                      )}
                    </button>
                  </div>
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Destacar</label>
                  <div className="flex items-center h-full pt-1">
                    <button
                      type="button"
                      onClick={() => setFormIsFeatured(!formIsFeatured)}
                      className="text-slate-455 hover:text-slate-255 font-bold text-xs flex items-center gap-1.5 cursor-pointer"
                    >
                      {formIsFeatured ? (
                        <ToggleRight size={32} className="text-rose-500" />
                      ) : (
                        <ToggleLeft size={32} className="text-slate-700" />
                      )}
                    </button>
                  </div>
                </div>
              </div>

              <div className="flex gap-4 border-t border-slate-800/60 pt-6 mt-4">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 py-3 border border-slate-800 rounded-xl font-bold text-slate-300 hover:bg-slate-800/40 text-sm cursor-pointer"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={formSubmitting}
                  className="flex-1 py-3 bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black rounded-xl hover:shadow-xl hover:shadow-rose-500/10 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  {formSubmitting ? (
                    <>
                      <Loader2 size={16} className="animate-spin" />
                      Salvando...
                    </>
                  ) : (
                    "Salvar Alterações"
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
