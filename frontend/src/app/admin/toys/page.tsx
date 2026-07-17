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
  Tag,
  Star,
} from "lucide-react";

import api from "../../../services/api";
import { Toy } from "../../../types";

export default function ToysAdminPage() {
  const [toys, setToys] = useState<Toy[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form Modal States
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingToy, setEditingToy] = useState<Toy | null>(null);
  const [formName, setFormName] = useState("");
  const [formCategory, setFormCategory] = useState("Infláveis");
  const [formMinAge, setFormMinAge] = useState<number>(0);
  const [formMaxAge, setFormMaxAge] = useState<number>(12);
  const [formDescription, setFormDescription] = useState("");
  const [formOrder, setFormOrder] = useState(0);
  const [formIsActive, setFormIsActive] = useState(true);
  const [formIsFeatured, setFormIsFeatured] = useState(false);
  const [formGalleryIds, setFormGalleryIds] = useState<string[]>([]);
  const [formGalleryUrls, setFormGalleryUrls] = useState<string[]>([]);
  const [selectedGalleryIds, setSelectedGalleryIds] = useState<string[]>([]);
  const [deletingImages, setDeletingImages] = useState(false);

  const [uploadingFile, setUploadingFile] = useState(false);
  const [formSubmitting, setFormSubmitting] = useState(false);

  const searchParams = useSearchParams();

  // Load Toys
  const loadToys = async () => {
    setLoading(true);
    try {
      const res = await api.toys.listAdmin();
      if (res?.data?.items) {
        setToys(res.data.items);
      }
    } catch (err: any) {
      setError(err.message || "Erro ao carregar brinquedos.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadToys();
  }, []);

  // Handle action parameter from dashboard (e.g. ?action=new)
  useEffect(() => {
    if (searchParams.get("action") === "new" && !loading) {
      handleOpenCreateModal();
    }
  }, [searchParams, loading]);

  const handleOpenCreateModal = () => {
    setEditingToy(null);
    setFormName("");
    setFormCategory("Infláveis");
    setFormMinAge(0);
    setFormMaxAge(12);
    setFormDescription("");
    setFormOrder(0);
    setFormIsActive(true);
    setFormIsFeatured(false);
    setFormGalleryIds([]);
    setFormGalleryUrls([]);
    setSelectedGalleryIds([]);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (toy: Toy) => {
    setEditingToy(toy);
    setFormName(toy.name);
    setFormCategory(toy.category);
    setFormMinAge(toy.min_age || 0);
    setFormMaxAge(toy.max_age || 0);
    setFormDescription(toy.description || "");
    setFormOrder(toy.display_order);
    setFormIsActive(toy.is_active);
    setFormIsFeatured(toy.is_featured);
    setFormGalleryIds(toy.gallery_image_ids || []);
    setFormGalleryUrls(toy.gallery_urls || []);
    setSelectedGalleryIds([]);
    setIsModalOpen(true);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setUploadingFile(true);
    try {
      const res = await api.upload.files(Array.from(files));
      if (res?.data) {
        const newIds = res.data.map((item) => item.id);
        const newUrls = res.data.map((item) => item.public_url);

        const updatedIds = [...formGalleryIds, ...newIds];
        const updatedUrls = [...formGalleryUrls, ...newUrls];

        setFormGalleryIds(updatedIds);
        setFormGalleryUrls(updatedUrls);

        if (editingToy) {
          await api.toys.update(editingToy.id, {
            gallery_image_ids: updatedIds,
          });
          loadToys();
        }
      }
    } catch (err: any) {
      alert(err.message || "Erro ao fazer upload dos arquivos.");
    } finally {
      setUploadingFile(false);
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

  const slugify = (text: string) => {
    return text
      .toString()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/\s+/g, "-")
      .replace(/[^\w\-]+/g, "")
      .replace(/\-\-+/g, "-")
      .replace(/^-+/, "")
      .replace(/-+$/, "");
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName) return;

    if (formMaxAge < formMinAge) {
      alert("A idade máxima deve ser maior ou igual à idade mínima.");
      return;
    }

    setFormSubmitting(true);
    try {
      const generatedSlug = slugify(formName);
      const payload = {
        name: formName,
        slug: generatedSlug,
        category: formCategory,
        min_age: formMinAge,
        max_age: formMaxAge,
        description: formDescription || null,
        display_order: formOrder,
        is_active: formIsActive,
        is_featured: formIsFeatured,
        gallery_image_ids: formGalleryIds,
      };

      if (editingToy) {
        // Edit Mode
        await api.toys.update(editingToy.id, payload);
      } else {
        // Create Mode
        await api.toys.create(payload);
      }
      setIsModalOpen(false);
      loadToys();
    } catch (err: any) {
      alert(err.message || "Erro ao salvar brinquedo. Certifique-se que o nome é único.");
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Tem certeza que deseja remover permanentemente este brinquedo do catálogo?")) return;

    try {
      await api.toys.delete(id);
      loadToys();
    } catch (err: any) {
      alert(err.message || "Erro ao deletar brinquedo.");
    }
  };

  const handleToggleActive = async (toy: Toy) => {
    try {
      await api.toys.toggleStatus(toy.id);
      setToys(
        toys.map((t) => (t.id === toy.id ? { ...t, is_active: !t.is_active } : t))
      );
    } catch (err: any) {
      alert(err.message || "Erro ao alterar status.");
    }
  };

  const handleToggleFeatured = async (toy: Toy) => {
    try {
      await api.toys.toggleFeatured(toy.id);
      setToys(
        toys.map((t) => (t.id === toy.id ? { ...t, is_featured: !t.is_featured } : t))
      );
    } catch (err: any) {
      alert(err.message || "Erro ao alterar destaque.");
    }
  };

  if (loading && toys.length === 0) {
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
          <h2 className="text-2xl font-black text-slate-100">Catálogo de Brinquedos</h2>
          <p className="text-sm text-slate-400">
            Gerencie o portfólio de brinquedos disponíveis para locação.
          </p>
        </div>
        <button
          onClick={handleOpenCreateModal}
          className="px-5 py-3 rounded-xl bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black text-sm flex items-center justify-center gap-2 cursor-pointer transition-all hover:scale-[1.02]"
        >
          <Plus size={18} />
          Novo Brinquedo
        </button>
      </div>

      {/* Error alert */}
      {error && (
        <div className="p-4 bg-rose-950/20 border border-rose-950/30 rounded-2xl text-rose-400 text-sm flex items-center gap-2">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Catalog items table */}
      {toys.length === 0 ? (
        <div className="p-16 border border-dashed border-slate-800 rounded-3xl text-center text-slate-500">
          Nenhum brinquedo cadastrado. Clique em "Novo Brinquedo" para começar.
        </div>
      ) : (
        <div className="bg-slate-900 border border-slate-800/80 rounded-3xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-widest bg-slate-900/50">
                  <th className="px-6 py-4">Brinquedo</th>
                  <th className="px-6 py-4">Categoria</th>
                  <th className="px-6 py-4">Idade Recomendada</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40 text-sm">
                {toys.map((toy) => (
                  <tr key={toy.id} className="hover:bg-slate-800/20 transition-colors">
                    <td className="px-6 py-4 font-bold text-slate-200">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-slate-950 border border-slate-850 flex items-center justify-center font-bold text-slate-400 text-xs overflow-hidden shrink-0">
                          {toy.gallery_urls && toy.gallery_urls.length > 0 ? (
                            <img
                              src={toy.gallery_urls[0]}
                              alt={toy.name}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <span>🎠</span>
                          )}
                        </div>
                        <div className="flex flex-col min-w-0">
                          <span className="truncate">{toy.name}</span>
                          <span className="text-[10px] font-semibold text-slate-500 font-mono truncate">
                            {toy.slug}
                          </span>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-slate-400 font-semibold">{toy.category}</td>
                    <td className="px-6 py-4 text-slate-400">{toy.min_age} a {toy.max_age} anos</td>
                    <td className="px-6 py-4">
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleToggleActive(toy)}
                          className={`px-3 py-1 rounded-full text-xs font-bold transition-all cursor-pointer ${
                            toy.is_active
                              ? "bg-emerald-500/10 text-emerald-400"
                              : "bg-slate-800 text-slate-500"
                          }`}
                        >
                          {toy.is_active ? "Ativo" : "Inativo"}
                        </button>
                        <button
                          onClick={() => handleToggleFeatured(toy)}
                          className={`p-1.5 rounded-full transition-all cursor-pointer ${
                            toy.is_featured
                              ? "bg-amber-500/10 text-amber-400"
                              : "bg-slate-800 text-slate-500"
                          }`}
                          title="Destaque"
                        >
                          <Star size={12} fill={toy.is_featured ? "currentColor" : "none"} />
                        </button>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-3">
                        <button
                          onClick={() => handleOpenEditModal(toy)}
                          className="p-2 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-xl"
                          title="Editar"
                        >
                          <Edit2 size={16} />
                        </button>
                        <button
                          onClick={() => handleDelete(toy.id)}
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
                {editingToy ? "Editar Brinquedo" : "Novo Brinquedo"}
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="p-2 text-slate-400 hover:text-slate-100 rounded-xl"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleFormSubmit} className="p-8 flex flex-col gap-6 overflow-y-auto flex-1">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Nome do Brinquedo</label>
                  <input
                    type="text"
                    required
                    value={formName}
                    onChange={(e) => setFormName(e.target.value)}
                    placeholder="Ex: Mega Tobogã Inflável"
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Categoria</label>
                  <select
                    value={formCategory}
                    onChange={(e) => setFormCategory(e.target.value)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none font-bold"
                  >
                    <option value="Infláveis">Infláveis</option>
                    <option value="Clássicos">Clássicos</option>
                    <option value="Infantil">Infantil</option>
                    <option value="Esportivos">Esportivos</option>
                    <option value="Outros">Outros</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Idade Mínima</label>
                  <input
                    type="number"
                    required
                    min={0}
                    value={formMinAge}
                    onChange={(e) => setFormMinAge(parseInt(e.target.value) || 0)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none font-bold"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs text-slate-400 font-bold uppercase">Idade Máxima</label>
                  <input
                    type="number"
                    required
                    min={0}
                    value={formMaxAge}
                    onChange={(e) => setFormMaxAge(parseInt(e.target.value) || 0)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none font-bold"
                  />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Descrição / Ficha Técnica</label>
                <textarea
                  rows={4}
                  value={formDescription}
                  onChange={(e) => setFormDescription(e.target.value)}
                  placeholder="Escreva detalhes como medidas de instalação, necessidade elétrica, etc..."
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none resize-none"
                />
              </div>

              {/* Photo Gallery uploads */}
              <div className="flex flex-col gap-3">
                <div className="flex justify-between items-center h-8">
                  <label className="text-xs text-slate-400 font-bold uppercase">Galeria de Fotos</label>
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
                      id="toy-gallery-upload-input"
                      className="hidden"
                      onChange={handleFileUpload}
                    />
                    <label
                      htmlFor="toy-gallery-upload-input"
                      className="w-full h-full border border-dashed border-slate-800 hover:border-slate-700 bg-slate-950 hover:bg-slate-900 rounded-xl flex flex-col items-center justify-center gap-1.5 text-[10px] text-slate-500 hover:text-slate-350 cursor-pointer font-bold transition-all"
                    >
                      {uploadingFile ? (
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
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
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
