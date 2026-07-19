"use client";

import React, { useEffect, useState } from "react";
import * as Icons from "lucide-react";
import {
  Save,
  Loader2,
  AlertCircle,
  FileImage,
  Upload as UploadIcon,
  Video,
  Sparkles,
  Info,
  ShieldCheck,
  Trash2,
  ArrowUp,
  ArrowDown,
  Plus,
} from "lucide-react";

import api from "../../../services/api";
import { HeroConfig } from "../../../types";

export default function SettingsAdminPage() {
  const [hero, setHero] = useState<HeroConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form Fields
  // Company & Contact
  const [formCompanyName, setFormCompanyName] = useState("");
  const [formCompanySlogan, setFormCompanySlogan] = useState("");
  const [formPhonePrimary, setFormPhonePrimary] = useState("");
  const [formWhatsapp, setFormWhatsapp] = useState("");
  const [formEmailCommercial, setFormEmailCommercial] = useState("");
  const [formBusinessHours, setFormBusinessHours] = useState("");
  const [formLogo, setFormLogo] = useState("");
  const [uploadingLogo, setUploadingLogo] = useState(false);

  // Hero
  const [formTag, setFormTag] = useState("");
  const [formTitle, setFormTitle] = useState("");
  const [formSubtitle, setFormSubtitle] = useState("");
  const [formText, setFormText] = useState("");
  const [safetyCards, setSafetyCards] = useState<Array<{
    id: string;
    title: string;
    description: string;
    icon: string;
  }>>([]);
  const [newCardTitle, setNewCardTitle] = useState("");
  const [newCardDesc, setNewCardDesc] = useState("");
  const [newCardIcon, setNewCardIcon] = useState("ShieldCheck");
  const [formPrimaryButton, setFormPrimaryButton] = useState("");
  const [formPrimaryLink, setFormPrimaryLink] = useState("");
  const [formSecondaryButton, setFormSecondaryButton] = useState("");
  const [formSecondaryLink, setFormSecondaryLink] = useState("");
  const [formBgImage, setFormBgImage] = useState("");
  const [formBgVideo, setFormBgVideo] = useState("");
  const [formBgColor, setFormBgColor] = useState("#020617");
  const [formCarouselTransition, setFormCarouselTransition] = useState(5);

  const [uploadingImage, setUploadingImage] = useState(false);
  const [uploadingVideo, setUploadingVideo] = useState(false);
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [savingCards, setSavingCards] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  // Load Settings
  const loadSettings = async () => {
    setLoading(true);
    try {
      const res = await api.settings.getAdmin();
      if (res?.data) {
        const { hero: h, company, contact, uploads } = res.data;
        
        // Hero
        setHero(h);
        setFormTag(h.tag || "");
        setFormTitle(h.title || "");
        setFormSubtitle(h.subtitle || "");
        setFormText(h.text || "");
        setSafetyCards(h.safety_cards || []);
        setFormPrimaryButton(h.primary_button || "");
        setFormPrimaryLink(h.primary_link || "");
        setFormSecondaryButton(h.secondary_button || "");
        setFormSecondaryLink(h.secondary_link || "");
        setFormBgImage(h.background_image || "");
        setFormBgVideo(h.background_video || "");
        setFormBgColor(h.bg_color || "#020617");
        setFormCarouselTransition(h.carousel_transition || 5);

        // Company
        setFormCompanyName(company?.name || "");
        setFormCompanySlogan(company?.slogan || "");
        
        // Contact
        setFormPhonePrimary(contact?.phone_primary || "");
        setFormWhatsapp(contact?.whatsapp || "");
        setFormEmailCommercial(contact?.email_commercial || "");
        setFormBusinessHours(contact?.business_hours || "");

        // Uploads
        setFormLogo(uploads?.logo_main || "");
      }
    } catch (err: any) {
      setError(err.message || "Erro ao carregar configurações.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSettings();
  }, []);

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadingImage(true);
    try {
      const res = await api.upload.file(file);
      if (res?.data?.public_url) {
        setFormBgImage(res.data.public_url);
      }
    } catch (err: any) {
      alert(err.message || "Erro ao fazer upload da imagem.");
    } finally {
      setUploadingImage(false);
    }
  };

  const handleVideoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadingVideo(true);
    try {
      const res = await api.upload.file(file);
      if (res?.data?.public_url) {
        setFormBgVideo(res.data.public_url);
      }
    } catch (err: any) {
      alert(err.message || "Erro ao fazer upload do vídeo.");
    } finally {
      setUploadingVideo(false);
    }
  };

  const persistCards = async (updatedCards: typeof safetyCards) => {
    setSavingCards(true);
    try {
      await api.hero.update({ safety_cards: updatedCards });
      setSafetyCards(updatedCards);
    } catch (err: any) {
      setFeedbackMsg({ type: "error", text: err.message || "Erro ao salvar os cards." });
    } finally {
      setSavingCards(false);
    }
  };

  const addSafetyCard = async () => {
    if (!newCardTitle.trim() || !newCardDesc.trim()) return;
    const newCard = {
      id: Date.now().toString(),
      title: newCardTitle,
      description: newCardDesc,
      icon: newCardIcon,
    };
    const updated = [...safetyCards, newCard];
    await persistCards(updated);
    setNewCardTitle("");
    setNewCardDesc("");
    setNewCardIcon("ShieldCheck");
  };

  const removeSafetyCard = async (id: string) => {
    const updated = safetyCards.filter((card) => card.id !== id);
    await persistCards(updated);
  };

  const moveSafetyCard = async (index: number, direction: "up" | "down") => {
    const nextIndex = direction === "up" ? index - 1 : index + 1;
    if (nextIndex < 0 || nextIndex >= safetyCards.length) return;
    const newCards = [...safetyCards];
    const temp = newCards[index];
    newCards[index] = newCards[nextIndex];
    newCards[nextIndex] = temp;
    await persistCards(newCards);
  };

  const handleLogoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadingLogo(true);
    try {
      const res = await api.settings.uploadLogo(file);
      if (res?.data?.value) {
        setFormLogo(res.data.value);
      }
    } catch (err: any) {
      alert(err.message || "Erro ao fazer upload do logo.");
    } finally {
      setUploadingLogo(false);
    }
  };

  const getUuidFromUrl = (url: string): string | null => {
    if (!url) return null;
    const match = url.match(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i);
    return match ? match[0] : null;
  };

  const handleRemoveLogo = async () => {
    if (!confirm("Tem certeza que deseja remover e excluir permanentemente o logo principal?")) {
      return;
    }

    try {
      const uuid = getUuidFromUrl(formLogo);
      if (uuid) {
        try {
          await api.upload.delete(uuid);
        } catch (err: any) {
          const errMsg = (err.message || "").toLowerCase();
          const isFileNotFound = 
            errMsg.includes("not found") || 
            errMsg.includes("não encontrado") || 
            errMsg.includes("404") || 
            errMsg.includes("file_not_found");
          if (!isFileNotFound) {
            throw err;
          }
        }
      }
      await api.settings.updateBulk({ upload_logo_main: null });
      setFormLogo("");
      window.location.reload();
    } catch (err: any) {
      alert(err.message || "Erro ao remover o logo principal.");
    }
  };

  const handleRemoveBgImage = async () => {
    if (!confirm("Tem certeza que deseja remover e excluir permanentemente a imagem de fundo?")) {
      return;
    }

    try {
      const uuid = getUuidFromUrl(formBgImage);
      if (uuid) {
        try {
          await api.upload.delete(uuid);
        } catch (err: any) {
          const errMsg = (err.message || "").toLowerCase();
          const isFileNotFound = 
            errMsg.includes("not found") || 
            errMsg.includes("não encontrado") || 
            errMsg.includes("404") || 
            errMsg.includes("file_not_found");
          if (!isFileNotFound) {
            throw err;
          }
        }
      }
      await api.hero.update({ background_image: null });
      setFormBgImage("");
      window.location.reload();
    } catch (err: any) {
      alert(err.message || "Erro ao remover a imagem de fundo.");
    }
  };

  const handleRemoveBgVideo = async () => {
    if (!confirm("Tem certeza que deseja remover e excluir permanentemente o vídeo de fundo?")) {
      return;
    }

    try {
      const uuid = getUuidFromUrl(formBgVideo);
      if (uuid) {
        try {
          await api.upload.delete(uuid);
        } catch (err: any) {
          const errMsg = (err.message || "").toLowerCase();
          const isFileNotFound = 
            errMsg.includes("not found") || 
            errMsg.includes("não encontrado") || 
            errMsg.includes("404") || 
            errMsg.includes("file_not_found");
          if (!isFileNotFound) {
            throw err;
          }
        }
      }
      await api.hero.update({ background_video: null });
      setFormBgVideo("");
      window.location.reload();
    } catch (err: any) {
      alert(err.message || "Erro ao remover o vídeo de fundo.");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormSubmitting(true);
    setFeedbackMsg(null);

    try {
      // Hero Payload
      const heroPayload: Partial<HeroConfig> = {
        tag: formTag || null,
        title: formTitle || null,
        subtitle: formSubtitle || null,
        text: formText || null,
        safety_cards: safetyCards,
        primary_button: formPrimaryButton || null,
        primary_link: formPrimaryLink || null,
        secondary_button: formSecondaryButton || null,
        secondary_link: formSecondaryLink || null,
        background_image: formBgImage || null,
        background_video: formBgVideo || null,
        bg_color: formBgColor || null,
        carousel_transition: formCarouselTransition,
      };

      // Settings Payload (Company & Contact)
      const settingsPayload: Record<string, any> = {
        company_name: formCompanyName || null,
        company_slogan: formCompanySlogan || null,
        contact_phone_primary: formPhonePrimary || null,
        contact_whatsapp: formWhatsapp || null,
        contact_email_commercial: formEmailCommercial || null,
        contact_business_hours: formBusinessHours || null,
      };

      await api.hero.update(heroPayload);
      await api.settings.updateBulk(settingsPayload);

      setFeedbackMsg({
        type: "success",
        text: "Configurações salvas e aplicadas com sucesso!",
      });
      loadSettings();
    } catch (err: any) {
      setFeedbackMsg({
        type: "error",
        text: err.message || "Erro ao salvar configurações.",
      });
    } finally {
      setFormSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="animate-spin text-rose-500" size={32} />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-10">
      {/* Header */}
      <div className="flex flex-col gap-2">
        <h2 className="text-2xl font-black text-slate-100">Hero & Ajustes do Site</h2>
        <p className="text-sm text-slate-400">
          Edite as informações da seção principal de boas-vindas do site público.
        </p>
      </div>

      {error && (
        <div className="p-4 bg-rose-950/20 border border-rose-950/30 rounded-2xl text-rose-400 text-sm flex items-center gap-2">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {feedbackMsg && (
        <div
          className={`p-5 rounded-2xl text-sm font-semibold border ${
            feedbackMsg.type === "success"
              ? "bg-emerald-950/20 text-emerald-400 border-emerald-900"
              : "bg-rose-950/20 text-rose-400 border-rose-900"
          }`}
        >
          {feedbackMsg.text}
        </div>
      )}

      <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Texts Info (Col-Span-2) */}
        <div className="lg:col-span-2 flex flex-col gap-8">
          
          {/* Company & Contact */}
          <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-8 flex flex-col gap-6">
            <div className="flex items-center gap-2 mb-2 pb-3 border-b border-slate-800/60">
              <Sparkles className="text-amber-500" size={18} />
              <h3 className="font-extrabold text-slate-200">Empresa & Contato</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Nome da Empresa (Fantasia)</label>
                <input
                  type="text"
                  value={formCompanyName}
                  onChange={(e) => setFormCompanyName(e.target.value)}
                  placeholder="Ex: Fantasy"
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Slogan / Subtítulo</label>
                <input
                  type="text"
                  value={formCompanySlogan}
                  onChange={(e) => setFormCompanySlogan(e.target.value)}
                  placeholder="Ex: Eventos & Lazer"
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                />
              </div>
              
              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Telefone Principal</label>
                <input
                  type="text"
                  value={formPhonePrimary}
                  onChange={(e) => setFormPhonePrimary(e.target.value)}
                  placeholder="Ex: (11) 99999-9999"
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">WhatsApp (Apenas Números)</label>
                <input
                  type="text"
                  value={formWhatsapp}
                  onChange={(e) => setFormWhatsapp(e.target.value)}
                  placeholder="Ex: 5511999999999"
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Email Comercial</label>
                <input
                  type="email"
                  value={formEmailCommercial}
                  onChange={(e) => setFormEmailCommercial(e.target.value)}
                  placeholder="Ex: contato@fantasy.com.br"
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Horário de Atendimento</label>
                <input
                  type="text"
                  value={formBusinessHours}
                  onChange={(e) => setFormBusinessHours(e.target.value)}
                  placeholder="Ex: Seg a Sex, 09h às 18h"
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                />
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-8 flex flex-col gap-6">
          <div className="flex items-center gap-2 mb-2 pb-3 border-b border-slate-800/60">
            <Sparkles className="text-rose-500" size={18} />
            <h3 className="font-extrabold text-slate-200">Textos do Hero</h3>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs text-slate-400 font-bold uppercase">Badge / Tag Superior</label>
            <input
              type="text"
              value={formTag}
              onChange={(e) => setFormTag(e.target.value)}
              placeholder="Ex: Locação de Brinquedos e Recreação Premium"
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs text-slate-400 font-bold uppercase">Título Principal</label>
            <input
              type="text"
              value={formTitle}
              onChange={(e) => setFormTitle(e.target.value)}
              placeholder="Ex: Transforme Seu Evento em uma Aventura!"
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs text-slate-400 font-bold uppercase">Subtítulo secundário</label>
            <input
              type="text"
              value={formSubtitle}
              onChange={(e) => setFormSubtitle(e.target.value)}
              placeholder="Ex: Brinquedos Premium e Festas Infantis"
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs text-slate-400 font-bold uppercase">Texto Descritivo / Parágrafo</label>
            <textarea
              rows={4}
              value={formText}
              onChange={(e) => setFormText(e.target.value)}
              placeholder="Descreva detalhadamente a proposta de valor..."
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none resize-none"
            />
          </div>

          <div className="flex items-center gap-2 mt-4 mb-2 pb-3 border-b border-slate-800/60">
            <Info className="text-rose-500" size={18} />
            <h3 className="font-extrabold text-slate-200">Botões de Chamada de Ação (CTA)</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-bold uppercase">Texto Botão Primário</label>
              <input
                type="text"
                value={formPrimaryButton}
                onChange={(e) => setFormPrimaryButton(e.target.value)}
                placeholder="Ex: Ver Catálogo"
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-bold uppercase">Link Botão Primário</label>
              <input
                type="text"
                value={formPrimaryLink}
                onChange={(e) => setFormPrimaryLink(e.target.value)}
                placeholder="Ex: #brinquedos"
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-bold uppercase">Texto Botão Secundário</label>
              <input
                type="text"
                value={formSecondaryButton}
                onChange={(e) => setFormSecondaryButton(e.target.value)}
                placeholder="Ex: Fale Conosco"
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-bold uppercase">Link Botão Secundário</label>
              <input
                type="text"
                value={formSecondaryLink}
                onChange={(e) => setFormSecondaryLink(e.target.value)}
                placeholder="Ex: #contato"
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
              />
            </div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-8 flex flex-col gap-6">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800/60">
            <div className="flex items-center gap-2">
              <ShieldCheck className="text-rose-500" size={18} />
              <h3 className="font-extrabold text-slate-200">Diferenciais / Proposition (Seção Sobre)</h3>
            </div>
            <span className="text-xs bg-slate-950 px-2.5 py-1 rounded-full border border-slate-800 text-slate-400 font-bold">
              {safetyCards.length} {safetyCards.length === 1 ? "Card" : "Cards"}
            </span>
          </div>

          {/* Current cards list */}
          {safetyCards.length === 0 ? (
            <div className="py-8 border border-dashed border-slate-800 rounded-xl text-center text-xs text-slate-500">
              Nenhum card cadastrado. Adicione pelo menos 3 cards abaixo.
            </div>
          ) : (
            <div className="flex flex-col gap-4">
              {safetyCards.map((card, index) => {
                const IconComponent = (Icons as any)[card.icon] || ShieldCheck;
                return (
                  <div key={card.id} className="flex items-center justify-between p-4 bg-slate-950/40 border border-slate-800 rounded-2xl gap-4">
                    <div className="flex items-center gap-4 min-w-0">
                      <div className="p-3 bg-rose-500/10 rounded-xl text-rose-400 shrink-0">
                        <IconComponent size={20} />
                      </div>
                      <div className="min-w-0">
                        <h4 className="text-sm font-bold text-slate-200 truncate">{card.title}</h4>
                        <p className="text-xs text-slate-400 truncate max-w-md">{card.description}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-1.5 shrink-0">
                      <button
                        type="button"
                        onClick={() => moveSafetyCard(index, "up")}
                        disabled={index === 0 || savingCards}
                        className="p-1.5 rounded-lg border border-slate-800 bg-slate-950 hover:bg-slate-900 text-slate-400 disabled:opacity-30 transition-colors"
                      >
                        {savingCards ? <Loader2 size={14} className="animate-spin" /> : <ArrowUp size={14} />}
                      </button>
                      <button
                        type="button"
                        onClick={() => moveSafetyCard(index, "down")}
                        disabled={index === safetyCards.length - 1 || savingCards}
                        className="p-1.5 rounded-lg border border-slate-800 bg-slate-950 hover:bg-slate-900 text-slate-400 disabled:opacity-30 transition-colors"
                      >
                        {savingCards ? <Loader2 size={14} className="animate-spin" /> : <ArrowDown size={14} />}
                      </button>
                      <button
                        type="button"
                        onClick={() => removeSafetyCard(card.id)}
                        disabled={savingCards}
                        className="p-1.5 rounded-lg border border-rose-500/20 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 disabled:opacity-30 transition-colors"
                      >
                        {savingCards ? <Loader2 size={14} className="animate-spin" /> : <Trash2 size={14} />}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Add card section */}
          <div className="mt-4 pt-6 border-t border-slate-800/60 flex flex-col gap-4">
            <h4 className="text-xs font-black text-rose-500 uppercase tracking-wider flex items-center gap-1">
              <Plus size={14} /> Adicionar Novo Card
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Título</label>
                <input
                  type="text"
                  value={newCardTitle}
                  onChange={(e) => setNewCardTitle(e.target.value)}
                  placeholder="Ex: Segurança Máxima"
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Ícone</label>
                <select
                  value={newCardIcon}
                  onChange={(e) => setNewCardIcon(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                >
                  <option value="ShieldCheck">🛡️ Segurança (Escudo)</option>
                  <option value="CheckCircle">✅ Higiene / Validação (Check)</option>
                  <option value="Sparkles">✨ Diversão (Brilhos)</option>
                  <option value="Heart">❤️ Carinho (Coração)</option>
                  <option value="Smile">😊 Alegria (Sorriso)</option>
                  <option value="Star">⭐ Qualidade (Estrela)</option>
                  <option value="Info">ℹ️ Suporte (Info)</option>
                  <option value="Users">👥 Monitores (Equipe)</option>
                  <option value="Clock">🕒 Pontualidade (Relógio)</option>
                  <option value="Flame">🔥 Energia (Fogo)</option>
                </select>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xs text-slate-400 font-bold uppercase">Descrição</label>
                <input
                  type="text"
                  value={newCardDesc}
                  onChange={(e) => setNewCardDesc(e.target.value)}
                  placeholder="Brinquedos higienizados..."
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none"
                />
              </div>
            </div>

            <button
              type="button"
              onClick={addSafetyCard}
              disabled={!newCardTitle.trim() || !newCardDesc.trim() || savingCards}
              className="self-start mt-1 px-6 py-3 bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black rounded-xl flex items-center gap-2 transition-all cursor-pointer shadow-lg shadow-rose-500/10 text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:shadow-rose-500/20 hover:scale-[1.02]"
            >
              {savingCards ? (
                <><Loader2 size={16} className="animate-spin" /> Salvando...</>
              ) : (
                <><Plus size={16} /> Adicionar Card</>
              )}
            </button>
          </div>
        </div>
      </div>

        {/* Media Side settings (Col-Span-1) */}
        <div className="flex flex-col gap-6">

          {/* Logo upload */}
          <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-6 flex flex-col gap-4">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-800/60">
              <FileImage className="text-amber-500" size={16} />
              <h3 className="font-extrabold text-sm text-slate-200">Logo Principal</h3>
            </div>

            {formLogo ? (
              <div className="relative h-32 bg-slate-950 rounded-xl border border-slate-800 overflow-hidden flex items-center justify-center p-4">
                <img src={formLogo} alt="Logo Preview" className="object-contain w-full h-full" />
                <button
                  type="button"
                  onClick={handleRemoveLogo}
                  className="absolute top-2 right-2 p-1.5 rounded-full bg-slate-950/80 hover:bg-rose-500/20 text-slate-400 hover:text-rose-450 transition-colors"
                >
                  Remover
                </button>
              </div>
            ) : (
              <div className="py-6 border border-dashed border-slate-800 rounded-xl text-center text-xs text-slate-500">
                Nenhum logo principal selecionado.
              </div>
            )}

            <input
              type="file"
              accept="image/*"
              id="logo-image-file-input"
              className="hidden"
              onChange={handleLogoUpload}
            />
            <label
              htmlFor="logo-image-file-input"
              className="py-3 bg-slate-950 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 font-bold text-xs rounded-xl flex items-center justify-center gap-2 cursor-pointer transition-all"
            >
              {uploadingLogo ? (
                <>
                  <Loader2 size={14} className="animate-spin" /> Enviando...
                </>
              ) : (
                <>
                  <UploadIcon size={14} /> Fazer Upload de Logo
                </>
              )}
            </label>
          </div>
          {/* Background color picker */}
          <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-6 flex flex-col gap-4">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-800/60">
              <Sparkles className="text-rose-500" size={16} />
              <h3 className="font-extrabold text-sm text-slate-200">Cor de Fundo da Página</h3>
            </div>
            
            <div className="flex items-center gap-4">
              <input
                type="color"
                value={formBgColor}
                onChange={(e) => setFormBgColor(e.target.value)}
                className="w-12 h-12 rounded-xl cursor-pointer bg-slate-950 border border-slate-800 p-1"
              />
              <div className="flex flex-col">
                <span className="text-sm font-bold text-slate-200">Cor Principal</span>
                <span className="text-xs text-slate-400 font-mono uppercase">{formBgColor}</span>
              </div>
            </div>
            <p className="text-xs text-slate-500 mt-2">
              Selecione a cor sólida que ficará atrás de todo o conteúdo da landing page.
            </p>
          </div>

          {/* Background image upload */}
          <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-6 flex flex-col gap-4">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-800/60">
              <FileImage className="text-rose-500" size={16} />
              <h3 className="font-extrabold text-sm text-slate-200">Imagem de Fundo</h3>
            </div>

            {formBgImage ? (
              <div className="relative h-36 bg-slate-950 rounded-xl border border-slate-800 overflow-hidden flex items-center justify-center">
                <img src={formBgImage} alt="Hero Background Preview" className="object-cover w-full h-full" />
                <button
                  type="button"
                  onClick={handleRemoveBgImage}
                  className="absolute top-2 right-2 p-1.5 rounded-full bg-slate-950/80 hover:bg-rose-500/20 text-slate-400 hover:text-rose-450 transition-colors"
                >
                  Remover
                </button>
              </div>
            ) : (
              <div className="py-8 border border-dashed border-slate-800 rounded-xl text-center text-xs text-slate-500">
                Nenhuma imagem de fundo selecionada.
              </div>
            )}

            <input
              type="file"
              accept="image/*"
              id="bg-image-file-input"
              className="hidden"
              onChange={handleImageUpload}
            />
            <label
              htmlFor="bg-image-file-input"
              className="py-3 bg-slate-950 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 font-bold text-xs rounded-xl flex items-center justify-center gap-2 cursor-pointer transition-all"
            >
              {uploadingImage ? (
                <>
                  <Loader2 size={14} className="animate-spin" /> Enviando...
                </>
              ) : (
                <>
                  <UploadIcon size={14} /> Fazer Upload de Imagem
                </>
              )}
            </label>
          </div>

          {/* Background video upload */}
          <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-6 flex flex-col gap-4">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-800/60">
              <Video className="text-rose-500" size={16} />
              <h3 className="font-extrabold text-sm text-slate-200">Vídeo de Fundo</h3>
            </div>

            {formBgVideo ? (
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between text-xs text-slate-400">
                <span className="truncate pr-4">{formBgVideo}</span>
                <button
                  type="button"
                  onClick={handleRemoveBgVideo}
                  className="text-rose-500 hover:text-rose-450 font-bold hover:underline shrink-0"
                >
                  Remover
                </button>
              </div>
            ) : (
              <div className="py-8 border border-dashed border-slate-800 rounded-xl text-center text-xs text-slate-500">
                Nenhum vídeo de fundo selecionado.
              </div>
            )}

            <input
              type="file"
              accept="video/*"
              id="bg-video-file-input"
              className="hidden"
              onChange={handleVideoUpload}
            />
            <label
              htmlFor="bg-video-file-input"
              className="py-3 bg-slate-950 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 font-bold text-xs rounded-xl flex items-center justify-center gap-2 cursor-pointer transition-all"
            >
              {uploadingVideo ? (
                <>
                  <Loader2 size={14} className="animate-spin" /> Enviando...
                </>
              ) : (
                <>
                  <UploadIcon size={14} /> Fazer Upload de Vídeo
                </>
              )}
            </label>
          </div>

          {/* Save Action box */}
          <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-6 flex flex-col gap-4">
            <button
              type="submit"
              disabled={formSubmitting}
              className="w-full py-4 bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black rounded-xl hover:shadow-xl hover:shadow-rose-500/10 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
            >
              {formSubmitting ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  Salvando...
                </>
              ) : (
                <>
                  <Save size={16} />
                  Salvar Ajustes
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
