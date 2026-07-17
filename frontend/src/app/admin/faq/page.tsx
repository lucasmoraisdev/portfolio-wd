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
  HelpCircle,
} from "lucide-react";

import api from "../../../services/api";
import { FAQ } from "../../../types";

export default function FAQAdminPage() {
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form Modal States
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingFaq, setEditingFaq] = useState<FAQ | null>(null);
  const [formQuestion, setFormQuestion] = useState("");
  const [formAnswer, setFormAnswer] = useState("");
  const [formOrder, setFormOrder] = useState(0);
  const [formIsActive, setFormIsActive] = useState(true);
  const [formSubmitting, setFormSubmitting] = useState(false);

  const searchParams = useSearchParams();

  // Load FAQs
  const loadFaqs = async () => {
    setLoading(true);
    try {
      const res = await api.faq.listAdmin();
      if (res?.data?.items) {
        setFaqs(res.data.items);
      }
    } catch (err: any) {
      setError(err.message || "Erro ao carregar FAQs.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFaqs();
  }, []);

  // Handle action parameter from dashboard (e.g. ?action=new)
  useEffect(() => {
    if (searchParams.get("action") === "new" && !loading) {
      handleOpenCreateModal();
    }
  }, [searchParams, loading]);

  const handleOpenCreateModal = () => {
    setEditingFaq(null);
    setFormQuestion("");
    setFormAnswer("");
    setFormOrder(0);
    setFormIsActive(true);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (faq: FAQ) => {
    setEditingFaq(faq);
    setFormQuestion(faq.question);
    setFormAnswer(faq.answer);
    setFormOrder(faq.display_order);
    setFormIsActive(faq.is_active);
    setIsModalOpen(true);
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formQuestion || !formAnswer) return;

    setFormSubmitting(true);
    try {
      if (editingFaq) {
        // Edit Mode
        await api.faq.update(editingFaq.id, {
          question: formQuestion,
          answer: formAnswer,
          display_order: formOrder,
          is_active: formIsActive,
        });
      } else {
        // Create Mode
        await api.faq.create({
          question: formQuestion,
          answer: formAnswer,
          display_order: formOrder,
          is_active: formIsActive,
        });
      }
      setIsModalOpen(false);
      loadFaqs();
    } catch (err: any) {
      alert(err.message || "Erro ao salvar FAQ.");
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Tem certeza que deseja remover permanentemente este FAQ?")) return;

    try {
      await api.faq.delete(id);
      loadFaqs();
    } catch (err: any) {
      alert(err.message || "Erro ao deletar FAQ.");
    }
  };

  const handleToggleActive = async (faq: FAQ) => {
    try {
      await api.faq.toggleStatus(faq.id);
      // Toggle locally for speed
      setFaqs(
        faqs.map((f) => (f.id === faq.id ? { ...f, is_active: !f.is_active } : f))
      );
    } catch (err: any) {
      alert(err.message || "Erro ao alterar status.");
    }
  };

  if (loading && faqs.length === 0) {
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
          <h2 className="text-2xl font-black text-slate-100">Perguntas Frequentes (FAQ)</h2>
          <p className="text-sm text-slate-400">
            Gerencie as perguntas exibidas na seção de FAQ da página principal.
          </p>
        </div>
        <button
          onClick={handleOpenCreateModal}
          className="px-5 py-3 rounded-xl bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black text-sm flex items-center justify-center gap-2 cursor-pointer transition-all hover:scale-[1.02]"
        >
          <Plus size={18} />
          Nova Pergunta
        </button>
      </div>

      {/* Error alert */}
      {error && (
        <div className="p-4 bg-rose-950/20 border border-rose-950/30 rounded-2xl text-rose-400 text-sm flex items-center gap-2">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Data Table */}
      {faqs.length === 0 ? (
        <div className="p-16 border border-dashed border-slate-800 rounded-3xl text-center text-slate-500">
          Nenhuma pergunta cadastrada. Clique em "Nova Pergunta" para começar.
        </div>
      ) : (
        <div className="bg-slate-900 border border-slate-800/80 rounded-3xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-widest bg-slate-900/50">
                  <th className="px-6 py-4">Pergunta</th>
                  <th className="px-6 py-4">Ordem</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40 text-sm">
                {faqs.map((faq) => (
                  <tr key={faq.id} className="hover:bg-slate-800/20 transition-colors">
                    <td className="px-6 py-4 font-bold text-slate-200">
                      <div className="flex flex-col gap-1 max-w-lg">
                        <span>{faq.question}</span>
                        <span className="text-xs font-normal text-slate-500 line-clamp-1">
                          {faq.answer}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-slate-400 font-bold">{faq.display_order}</td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => handleToggleActive(faq)}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold transition-all cursor-pointer ${
                          faq.is_active
                            ? "bg-emerald-500/10 text-emerald-400"
                            : "bg-slate-800 text-slate-500"
                        }`}
                      >
                        {faq.is_active ? "Ativo" : "Inativo"}
                      </button>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-3">
                        <button
                          onClick={() => handleOpenEditModal(faq)}
                          className="p-2 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-xl transition-colors"
                          title="Editar"
                        >
                          <Edit2 size={16} />
                        </button>
                        <button
                          onClick={() => handleDelete(faq.id)}
                          className="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-xl transition-colors"
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

      {/* Create / Edit Modal Dialog */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full max-h-[90vh] flex flex-col overflow-hidden shadow-2xl relative">
            <div className="flex justify-between items-center px-8 py-6 border-b border-slate-800/80 shrink-0">
              <h3 className="font-extrabold text-slate-100">
                {editingFaq ? "Editar Pergunta" : "Nova Pergunta"}
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="p-2 text-slate-400 hover:text-slate-100 rounded-xl"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleFormSubmit} className="p-8 flex flex-col gap-6 overflow-y-auto flex-1">
              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Pergunta</label>
                <input
                  type="text"
                  required
                  value={formQuestion}
                  onChange={(e) => setFormQuestion(e.target.value)}
                  placeholder="Ex: Como funciona o processo de entrega?"
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Resposta</label>
                <textarea
                  required
                  rows={4}
                  value={formAnswer}
                  onChange={(e) => setFormAnswer(e.target.value)}
                  placeholder="Descreva a resposta completa do FAQ..."
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
                  <div className="flex items-center h-full">
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
