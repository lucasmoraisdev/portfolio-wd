"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  ToyBrick,
  Calendar,
  MessageSquare,
  HelpCircle,
  Mail,
  Loader2,
  AlertCircle,
  Plus,
  ArrowRight,
  TrendingUp,
} from "lucide-react";

import api from "../../../services/api";
import { DashboardStats } from "../../../types";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.dashboard
      .stats()
      .then((res) => {
        if (res?.data) {
          setStats(res.data);
        }
      })
      .catch((err) => {
        console.error("Erro ao carregar estatísticas do dashboard:", err);
        setError("Não foi possível carregar as estatísticas. Verifique a conexão com o servidor.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="animate-spin text-rose-500" size={32} />
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-3xl text-center max-w-lg mx-auto flex flex-col items-center gap-4">
        <AlertCircle size={40} className="text-rose-500" />
        <h3 className="text-lg font-bold">Falha de Conexão</h3>
        <p className="text-sm text-slate-400 leading-relaxed">
          {error || "Erro ao consultar as estatísticas no banco de dados remotos."}
        </p>
      </div>
    );
  }

  // Quick Card Configurations
  const cardItems = [
    {
      title: "Catálogo de Brinquedos",
      count: stats.total_toys,
      active: stats.active_toys,
      activeLabel: "Ativos na vitrine",
      icon: ToyBrick,
      color: "from-rose-500 to-pink-500",
      href: "/admin/toys",
    },
    {
      title: "Eventos & Shows",
      count: stats.total_events,
      active: stats.active_events,
      activeLabel: "Exibidos no portfólio",
      icon: Calendar,
      color: "from-violet-500 to-indigo-500",
      href: "/admin/events",
    },
    {
      title: "Depoimentos de Clientes",
      count: stats.total_testimonials,
      active: stats.active_testimonials,
      activeLabel: "Habilitados publicamente",
      icon: MessageSquare,
      color: "from-sky-500 to-blue-500",
      href: "/admin/testimonials",
    },
    {
      title: "Perguntas FAQ",
      count: stats.total_faqs,
      active: stats.active_faqs,
      activeLabel: "Disponíveis no suporte",
      icon: HelpCircle,
      color: "from-emerald-500 to-teal-500",
      href: "/admin/faq",
    },
  ];

  return (
    <div className="flex flex-col gap-10">
      {/* Overview header */}
      <div className="flex flex-col gap-2">
        <h2 className="text-2xl font-black text-slate-100">Visão Geral</h2>
        <p className="text-sm text-slate-400 leading-relaxed">
          Estatísticas consolidadas e atalhos rápidos de gerenciamento.
        </p>
      </div>

      {/* Unread message banner alerts */}
      {stats.unread_contacts > 0 && (
        <Link
          href="/admin/contacts"
          className="flex items-center justify-between gap-4 p-4 sm:p-5 bg-amber-500/10 border border-amber-500/20 hover:border-amber-500/30 rounded-2xl text-amber-400 transition-colors animate-pulse"
        >
          <div className="flex items-center gap-3">
            <Mail size={20} />
            <div className="text-xs sm:text-sm font-semibold">
              Você possui <strong className="font-extrabold text-amber-300">{stats.unread_contacts}</strong> novas mensagens de orçamento pendentes de leitura.
            </div>
          </div>
          <div className="flex items-center gap-1 text-xs font-black uppercase tracking-wider text-amber-300">
            Ver mensagens <ArrowRight size={14} />
          </div>
        </Link>
      )}

      {/* Grid count cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {cardItems.map((item, i) => {
          const Icon = item.icon;
          return (
            <div
              key={i}
              className="bg-slate-900 border border-slate-800/80 rounded-3xl p-6 flex flex-col justify-between hover:border-slate-700/80 transition-all relative overflow-hidden group"
            >
              {/* Highlight background light */}
              <div className="absolute -top-12 -right-12 w-28 h-28 bg-slate-800 rounded-full blur-2xl group-hover:scale-125 transition-transform duration-300" />

              <div className="flex justify-between items-start mb-6 relative z-10">
                <span className="text-sm font-bold text-slate-400 tracking-wide uppercase">
                  {item.title}
                </span>
                <div className={`p-2.5 rounded-xl bg-gradient-to-tr ${item.color} text-slate-950 shadow-md shadow-slate-950/20`}>
                  <Icon size={18} />
                </div>
              </div>

              <div className="relative z-10 flex items-baseline gap-2 mb-2">
                <span className="text-4xl font-black text-slate-100 tracking-tight">
                  {item.count}
                </span>
                <span className="text-xs font-semibold text-slate-500">total</span>
              </div>

              <div className="relative z-10 flex items-center gap-1.5 text-xs font-semibold text-slate-400 mb-6">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span>
                  {item.active} {item.activeLabel}
                </span>
              </div>

              <Link
                href={item.href}
                className="relative z-10 flex items-center justify-between text-xs font-bold text-slate-300 hover:text-rose-400 pt-3 border-t border-slate-800/60 transition-colors"
              >
                <span>Acessar Módulo</span>
                <ArrowRight size={14} />
              </Link>
            </div>
          );
        })}
      </div>

      {/* Secondary layout sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Quick actions box */}
        <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-8 flex flex-col gap-6">
          <div className="flex items-center gap-2">
            <TrendingUp className="text-rose-400" size={20} />
            <h3 className="font-extrabold text-slate-200">Ações Rápidas</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Link
              href="/admin/toys?action=new"
              className="flex items-center justify-between p-4 bg-slate-950 border border-slate-800 hover:border-rose-500/20 rounded-2xl text-slate-300 hover:text-slate-100 transition-all font-bold text-sm"
            >
              <span>Novo Brinquedo</span>
              <Plus size={16} className="text-rose-400" />
            </Link>

            <Link
              href="/admin/events?action=new"
              className="flex items-center justify-between p-4 bg-slate-950 border border-slate-800 hover:border-rose-500/20 rounded-2xl text-slate-300 hover:text-slate-100 transition-all font-bold text-sm"
            >
              <span>Novo Evento</span>
              <Plus size={16} className="text-rose-400" />
            </Link>

            <Link
              href="/admin/testimonials?action=new"
              className="flex items-center justify-between p-4 bg-slate-950 border border-slate-800 hover:border-rose-500/20 rounded-2xl text-slate-300 hover:text-slate-100 transition-all font-bold text-sm"
            >
              <span>Novo Depoimento</span>
              <Plus size={16} className="text-rose-400" />
            </Link>

            <Link
              href="/admin/faq?action=new"
              className="flex items-center justify-between p-4 bg-slate-950 border border-slate-800 hover:border-rose-500/20 rounded-2xl text-slate-300 hover:text-slate-100 transition-all font-bold text-sm"
            >
              <span>Nova Pergunta FAQ</span>
              <Plus size={16} className="text-rose-400" />
            </Link>
          </div>
        </div>

        {/* Support contacts box */}
        <div className="bg-slate-900 border border-slate-800/80 rounded-3xl p-8 flex flex-col gap-6">
          <div className="flex items-center gap-2">
            <Mail className="text-rose-400" size={20} />
            <h3 className="font-extrabold text-slate-200">Mensagens de Contato</h3>
          </div>
          <div className="flex flex-col gap-4">
            <div className="text-sm text-slate-400 leading-relaxed">
              Você possui <strong className="text-slate-200">{stats.unread_contacts}</strong> mensagens não lidas e um total de <strong className="text-slate-200">{stats.total_contacts}</strong> registros de contato.
            </div>
            <Link
              href="/admin/contacts"
              className="py-3 px-6 rounded-xl bg-slate-950 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 font-bold text-sm text-slate-300 flex items-center justify-center gap-2 transition-all"
            >
              Ver Todas as Mensagens
              <ArrowRight size={16} />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
