"use client";

import React, { useEffect, useState } from "react";
import {
  Trash2,
  Mail,
  MailOpen,
  Loader2,
  AlertCircle,
  Clock,
  Phone,
  User,
  X,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

import api from "../../../services/api";
import { ContactMessage } from "../../../types";

export default function ContactsAdminPage() {
  const [messages, setMessages] = useState<ContactMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [filterRead, setFilterRead] = useState<string>("all"); // "all", "unread", "read"
  const [selectedMessage, setSelectedMessage] = useState<ContactMessage | null>(null);

  const loadMessages = async () => {
    setLoading(true);
    try {
      const params: Record<string, any> = {};
      if (filterRead === "unread") params.is_read = false;
      if (filterRead === "read") params.is_read = true;

      const res = await api.contacts.listAdmin(params);
      if (res?.data?.items) {
        setMessages(res.data.items);
      }
    } catch (err: any) {
      setError(err.message || "Erro ao carregar mensagens.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMessages();
  }, [filterRead]);

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Avoid opening detail card
    if (!confirm("Tem certeza que deseja excluir esta mensagem?")) return;

    try {
      await api.contacts.delete(id);
      if (selectedMessage?.id === id) {
        setSelectedMessage(null);
      }
      loadMessages();
    } catch (err: any) {
      alert(err.message || "Erro ao excluir mensagem.");
    }
  };

  const handleOpenMessage = async (msg: ContactMessage) => {
    setSelectedMessage(msg);
    if (!msg.is_read) {
      try {
        await api.contacts.markRead(msg.id);
        // Update local list
        setMessages(
          messages.map((m) => (m.id === msg.id ? { ...m, is_read: true } : m))
        );
      } catch (err: any) {
        console.error("Erro ao marcar mensagem como lida:", err);
      }
    }
  };

  if (loading && messages.length === 0) {
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
          <h2 className="text-2xl font-black text-slate-100">Mensagens Recebidas</h2>
          <p className="text-sm text-slate-400">
            Gerencie os contatos e solicitações de orçamento enviados pelo site.
          </p>
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-2 bg-slate-900 border border-slate-800 p-1.5 rounded-2xl text-xs font-bold">
          <button
            onClick={() => setFilterRead("all")}
            className={`px-4 py-2 rounded-xl transition-all cursor-pointer ${
              filterRead === "all"
                ? "bg-slate-800 text-slate-100"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Todas
          </button>
          <button
            onClick={() => setFilterRead("unread")}
            className={`px-4 py-2 rounded-xl transition-all cursor-pointer ${
              filterRead === "unread"
                ? "bg-slate-800 text-slate-100"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Não Lidas
          </button>
          <button
            onClick={() => setFilterRead("read")}
            className={`px-4 py-2 rounded-xl transition-all cursor-pointer ${
              filterRead === "read"
                ? "bg-slate-800 text-slate-100"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Lidas
          </button>
        </div>
      </div>

      {/* Error alert */}
      {error && (
        <div className="p-4 bg-rose-950/20 border border-rose-950/30 rounded-2xl text-rose-400 text-sm flex items-center gap-2">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Main layout split list/detail */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* List Box */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          {messages.length === 0 ? (
            <div className="p-16 border border-dashed border-slate-800 rounded-3xl text-center text-slate-500">
              Nenhuma mensagem encontrada nesta categoria.
            </div>
          ) : (
            <div className="flex flex-col gap-3">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  onClick={() => handleOpenMessage(msg)}
                  className={`p-5 rounded-2xl border transition-all cursor-pointer flex items-start justify-between gap-4 ${
                    selectedMessage?.id === msg.id
                      ? "bg-slate-900 border-rose-500/20 shadow-md"
                      : "bg-slate-900/40 border-slate-900 hover:border-slate-850 hover:bg-slate-900/60"
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div
                      className={`p-2.5 rounded-xl shrink-0 mt-0.5 ${
                        msg.is_read
                          ? "bg-slate-950 text-slate-500 border border-slate-850"
                          : "bg-amber-500/10 text-amber-400 border border-amber-500/10"
                      }`}
                    >
                      {msg.is_read ? <MailOpen size={16} /> : <Mail size={16} />}
                    </div>

                    <div className="flex flex-col min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-bold text-slate-200 text-sm truncate">
                          {msg.name}
                        </span>
                        {!msg.is_read && (
                          <span className="px-2 py-0.5 rounded-md bg-amber-500/10 text-[9px] font-black text-amber-400 uppercase border border-amber-500/10 tracking-widest">
                            Novo
                          </span>
                        )}
                      </div>
                      <span className="text-xs text-slate-400 font-bold truncate mt-0.5">
                        {msg.subject || "(Sem assunto)"}
                      </span>
                      <span className="text-[10px] text-slate-500 flex items-center gap-1 mt-2">
                        <Clock size={10} /> {new Date(msg.created_at).toLocaleString()}
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={(e) => handleDelete(msg.id, e)}
                    className="p-2 text-slate-500 hover:text-rose-400 hover:bg-slate-850 rounded-xl transition-colors shrink-0"
                    title="Excluir mensagem"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Detail Box */}
        <div className="lg:col-span-1">
          {selectedMessage ? (
            <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-6 sm:p-8 flex flex-col gap-6 sticky top-24 shadow-lg shadow-slate-950/20">
              <div className="flex justify-between items-start border-b border-slate-800/60 pb-5">
                <div>
                  <h3 className="text-lg font-black text-slate-200">Detalhes do Contato</h3>
                  <span className="text-[10px] text-slate-500 flex items-center gap-1 mt-1">
                    <Clock size={10} /> {new Date(selectedMessage.created_at).toLocaleString()}
                  </span>
                </div>
                <button
                  onClick={() => setSelectedMessage(null)}
                  className="p-1 text-slate-400 hover:text-slate-200 rounded"
                >
                  <X size={16} />
                </button>
              </div>

              {/* Sender Details */}
              <div className="flex flex-col gap-4 text-xs font-semibold text-slate-300">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-slate-950 rounded-lg text-rose-500">
                    <User size={14} />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[9px] text-slate-500 uppercase tracking-widest font-bold">Remetente</span>
                    <span className="text-slate-200 font-bold">{selectedMessage.name}</span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="p-2 bg-slate-950 rounded-lg text-rose-500">
                    <Mail size={14} />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[9px] text-slate-500 uppercase tracking-widest font-bold">E-mail</span>
                    <a
                      href={`mailto:${selectedMessage.email}`}
                      className="text-rose-400 font-bold hover:underline"
                    >
                      {selectedMessage.email}
                    </a>
                  </div>
                </div>

                {selectedMessage.phone && (
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-slate-950 rounded-lg text-rose-500">
                      <Phone size={14} />
                    </div>
                    <div className="flex flex-col">
                      <span className="text-[9px] text-slate-500 uppercase tracking-widest font-bold">Telefone</span>
                      <span className="text-slate-200 font-bold">{selectedMessage.phone}</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Message Content */}
              <div className="flex flex-col gap-2 pt-4 border-t border-slate-800/60">
                <span className="text-[9px] text-slate-500 uppercase tracking-widest font-bold">Assunto</span>
                <span className="text-sm font-extrabold text-slate-350">{selectedMessage.subject || "(Sem assunto)"}</span>
              </div>

              <div className="flex flex-col gap-2.5 p-4 bg-slate-950 border border-slate-850 rounded-2xl">
                <span className="text-[9px] text-slate-500 uppercase tracking-widest font-bold">Mensagem</span>
                <p className="text-xs text-slate-400 leading-relaxed whitespace-pre-wrap">
                  {selectedMessage.message}
                </p>
              </div>

              <button
                onClick={(e) => handleDelete(selectedMessage.id, e)}
                className="w-full py-3 bg-rose-950/20 hover:bg-rose-950/40 border border-rose-900 text-rose-400 font-bold text-xs rounded-xl flex items-center justify-center gap-2 cursor-pointer transition-colors"
              >
                <Trash2 size={14} />
                Excluir Mensagem Definitivamente
              </button>
            </div>
          ) : (
            <div className="hidden lg:flex border border-dashed border-slate-800 rounded-3xl h-64 items-center justify-center text-slate-500 p-8 text-center text-xs">
              Selecione uma mensagem na lista para visualizar seus detalhes e conteúdo completo.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
