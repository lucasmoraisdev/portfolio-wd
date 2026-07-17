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
  Star,
  Upload as UploadIcon,
} from "lucide-react";

import api from "../../../services/api";
import { Testimonial } from "../../../types";

export default function TestimonialsAdminPage() {
  const [testimonials, setTestimonials] = useState<Testimonial[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form Modal States
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTestimonial, setEditingTestimonial] = useState<Testimonial | null>(null);
  const [formName, setFormName] = useState("");
  const [formCity, setFormCity] = useState("");
  const [formCompany, setFormCompany] = useState("");
  const [formText, setFormText] = useState("");
  const [formRating, setFormRating] = useState(5);
  const [formOrder, setFormOrder] = useState(0);
  const [formIsActive, setFormIsActive] = useState(true);
  const [formPhotoId, setFormPhotoId] = useState<string | null>(null);
  const [formPhotoUrl, setFormPhotoUrl] = useState<string | null>(null);

  const [uploadingFile, setUploadingFile] = useState(false);
  const [formSubmitting, setFormSubmitting] = useState(false);

  const searchParams = useSearchParams();

  // Load Testimonials
  const loadTestimonials = async () => {
    setLoading(true);
    try {
      const res = await api.testimonials.listAdmin();
      if (res?.data?.items) {
        setTestimonials(res.data.items);
      }
    } catch (err: any) {
      setError(err.message || "Erro ao carregar depoimentos.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTestimonials();
  }, []);

  // Handle action parameter from dashboard (e.g. ?action=new)
  useEffect(() => {
    if (searchParams.get("action") === "new" && !loading) {
      handleOpenCreateModal();
    }
  }, [searchParams, loading]);

  const handleOpenCreateModal = () => {
    setEditingTestimonial(null);
    setFormName("");
    setFormCity("");
    setFormCompany("");
    setFormText("");
    setFormRating(5);
    setFormOrder(0);
    setFormIsActive(true);
    setFormPhotoId(null);
    setFormPhotoUrl(null);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (testimonial: Testimonial) => {
    setEditingTestimonial(testimonial);
    setFormName(testimonial.name);
    setFormCity(testimonial.city || "");
    setFormCompany(testimonial.company || "");
    setFormText(testimonial.testimonial);
    setFormRating(testimonial.rating);
    setFormOrder(testimonial.display_order);
    setFormIsActive(testimonial.is_active);
    setFormPhotoId(testimonial.photo_id);
    setFormPhotoUrl(testimonial.photo_url || null);
    setIsModalOpen(true);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadingFile(true);
    try {
      const res = await api.upload.file(file);
      if (res?.data?.id) {
        setFormPhotoId(res.data.id);
        setFormPhotoUrl(res.data.public_url);
      }
    } catch (err: any) {
      alert(err.message || "Erro ao fazer upload da imagem.");
    } finally {
      setUploadingFile(false);
    }
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName || !formText) return;

    setFormSubmitting(true);
    try {
      const payload = {
        name: formName,
        city: formCity || null,
        company: formCompany || null,
        testimonial: formText,
        rating: formRating,
        display_order: formOrder,
        is_active: formIsActive,
        photo_id: formPhotoId,
      };

      if (editingTestimonial) {
        // Edit Mode
        await api.testimonials.update(editingTestimonial.id, payload);
      } else {
        // Create Mode
        await api.testimonials.create(payload);
      }
      setIsModalOpen(false);
      loadTestimonials();
    } catch (err: any) {
      alert(err.message || "Erro ao salvar depoimento.");
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Tem certeza que deseja remover permanentemente este depoimento?")) return;

    try {
      await api.testimonials.delete(id);
      loadTestimonials();
    } catch (err: any) {
      alert(err.message || "Erro ao deletar depoimento.");
    }
  };

  const handleToggleActive = async (testimonial: Testimonial) => {
    try {
      await api.testimonials.toggleStatus(testimonial.id);
      setTestimonials(
        testimonials.map((t) =>
          t.id === testimonial.id ? { ...t, is_active: !t.is_active } : t
        )
      );
    } catch (err: any) {
      alert(err.message || "Erro ao alterar status.");
    }
  };

  if (loading && testimonials.length === 0) {
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
          <h2 className="text-2xl font-black text-slate-100">Depoimentos de Clientes</h2>
          <p className="text-sm text-slate-400">
            Gerencie as avaliações e depoimentos que aparecem no site público.
          </p>
        </div>
        <button
          onClick={handleOpenCreateModal}
          className="px-5 py-3 rounded-xl bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black text-sm flex items-center justify-center gap-2 cursor-pointer transition-all hover:scale-[1.02]"
        >
          <Plus size={18} />
          Novo Depoimento
        </button>
      </div>

      {/* Error alert */}
      {error && (
        <div className="p-4 bg-rose-950/20 border border-rose-950/30 rounded-2xl text-rose-400 text-sm flex items-center gap-2">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Testimonials grid list */}
      {testimonials.length === 0 ? (
        <div className="p-16 border border-dashed border-slate-800 rounded-3xl text-center text-slate-500">
          Nenhum depoimento cadastrado. Clique em "Novo Depoimento" para começar.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {testimonials.map((test) => (
            <div
              key={test.id}
              className="bg-slate-900 border border-slate-800/80 rounded-3xl p-6 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-4 mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center font-bold text-slate-400 text-sm overflow-hidden border border-slate-700">
                      {test.photo_url ? (
                        <img
                          src={test.photo_url}
                          alt={test.name}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        test.name.charAt(0)
                      )}
                    </div>
                    <div className="flex flex-col">
                      <span className="font-bold text-slate-200 text-sm">{test.name}</span>
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">
                        {test.company} {test.city ? `(${test.city})` : ""}
                      </span>
                    </div>
                  </div>
                  <div className="flex gap-0.5 text-amber-400">
                    {Array.from({ length: test.rating }).map((_, i) => (
                      <Star key={i} size={14} fill="currentColor" />
                    ))}
                  </div>
                </div>
                <p className="text-slate-400 text-xs sm:text-sm leading-relaxed italic mb-6">
                  "{test.testimonial}"
                </p>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-slate-800/60 text-xs mt-2">
                <button
                  onClick={() => handleToggleActive(test)}
                  className={`px-3 py-1 rounded-full font-bold transition-all ${
                    test.is_active
                      ? "bg-emerald-500/10 text-emerald-400"
                      : "bg-slate-800 text-slate-500"
                  }`}
                >
                  {test.is_active ? "Ativo" : "Inativo"}
                </button>

                <div className="flex gap-2">
                  <button
                    onClick={() => handleOpenEditModal(test)}
                    className="p-2 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-xl"
                  >
                    <Edit2 size={14} />
                  </button>
                  <button
                    onClick={() => handleDelete(test.id)}
                    className="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-xl"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Form Modal Dialog */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-xl w-full max-h-[90vh] flex flex-col overflow-hidden shadow-2xl relative">
            <div className="flex justify-between items-center px-8 py-6 border-b border-slate-800/80 shrink-0">
              <h3 className="font-extrabold text-slate-100">
                {editingTestimonial ? "Editar Depoimento" : "Novo Depoimento"}
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="p-2 text-slate-400 hover:text-slate-100 rounded-xl"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleFormSubmit} className="p-8 flex flex-col gap-6 overflow-y-auto flex-1">
              {/* Photo Upload Row */}
              <div className="flex items-center gap-6 p-4 bg-slate-950 border border-slate-800 rounded-2xl">
                <div className="w-16 h-16 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center font-black text-slate-500 overflow-hidden shrink-0">
                  {formPhotoUrl ? (
                    <img src={formPhotoUrl} alt="Avatar Preview" className="w-full h-full object-cover" />
                  ) : (
                    "FOTO"
                  )}
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Foto do Autor</label>
                  <div className="relative">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileUpload}
                      className="hidden"
                      id="photo-upload-input"
                    />
                    <label
                      htmlFor="photo-upload-input"
                      className="px-4 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 font-bold text-xs rounded-xl flex items-center gap-2 cursor-pointer transition-colors"
                    >
                      {uploadingFile ? (
                        <>
                          <Loader2 size={14} className="animate-spin" /> Enviando...
                        </>
                      ) : (
                        <>
                          <UploadIcon size={14} /> Selecionar Imagem
                        </>
                      )}
                    </label>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Nome do Cliente</label>
                  <input
                    type="text"
                    required
                    value={formName}
                    onChange={(e) => setFormName(e.target.value)}
                    placeholder="Ex: Mariana Silva"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Empresa / Relação</label>
                  <input
                    type="text"
                    value={formCompany}
                    onChange={(e) => setFormCompany(e.target.value)}
                    placeholder="Ex: Mãe do Lucas"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Cidade</label>
                  <input
                    type="text"
                    value={formCity}
                    onChange={(e) => setFormCity(e.target.value)}
                    placeholder="Ex: Santo André"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Avaliação (1 a 5 estrelas)</label>
                  <div className="flex gap-2 items-center h-full pt-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        type="button"
                        key={star}
                        onClick={() => setFormRating(star)}
                        className="text-amber-400 hover:scale-110 transition-transform"
                      >
                        <Star
                          size={24}
                          fill={star <= formRating ? "currentColor" : "none"}
                        />
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Depoimento</label>
                <textarea
                  required
                  rows={4}
                  value={formText}
                  onChange={(e) => setFormText(e.target.value)}
                  placeholder="Escreva a avaliação completa enviada pelo cliente..."
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none resize-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Ordem de Exibição</label>
                  <input
                    type="number"
                    value={formOrder}
                    onChange={(e) => setFormOrder(parseInt(e.target.value) || 0)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Status Inicial</label>
                  <div className="flex items-center h-full pt-1">
                    <button
                      type="button"
                      onClick={() => setFormIsActive(!formIsActive)}
                      className="text-slate-400 hover:text-slate-200 transition-colors flex items-center gap-2 font-bold text-sm cursor-pointer"
                    >
                      {formIsActive ? (
                        <>
                          <ToggleRight size={36} className="text-rose-500" />
                          <span>Ativo</span>
                        </>
                      ) : (
                        <>
                          <ToggleLeft size={36} className="text-slate-600" />
                          <span>Inativo</span>
                        </>
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
                    "Salvar Depoimento"
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
