"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Loader2, Lock, Mail, Sparkles } from "lucide-react";

import api, { setToken } from "../../../services/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // If already authenticated, redirect to dashboard
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      router.push("/admin/dashboard");
    }
  }, [router]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError("Por favor, preencha todos os campos.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await api.auth.login({ email, password });

      if (res?.data?.access_token) {
        setToken(res.data.access_token);
        
        // Fetch current user details
        try {
          const userRes = await api.auth.me();
          if (userRes?.data) {
            localStorage.setItem("user", JSON.stringify(userRes.data));
          }
        } catch (err) {
          console.error("Failed to fetch user details", err);
        }
        
        router.push("/admin/dashboard");
      } else {
        setError("Ocorreu um erro ao realizar o login. Token não recebido.");
      }
    } catch (err: any) {
      setError(err.message || "E-mail ou senha incorretos.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 px-6 font-sans relative overflow-hidden">
      {/* Background radial effects */}
      <div className="absolute inset-0 z-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-rose-950/15 via-slate-950 to-slate-950" />
      <div className="absolute top-1/3 left-1/3 w-80 h-80 bg-rose-600/5 rounded-full blur-3xl" />
      <div className="absolute bottom-1/3 right-1/3 w-80 h-80 bg-amber-500/5 rounded-full blur-3xl" />

      {/* Main card */}
      <div className="relative z-10 w-full max-w-md bg-slate-900/60 backdrop-blur-md border border-slate-900 rounded-3xl p-8 sm:p-10 shadow-2xl">
        <div className="text-center mb-8 flex flex-col items-center">
          <div className="p-3 bg-gradient-to-tr from-rose-500 to-amber-400 text-slate-950 rounded-2xl font-bold flex items-center justify-center shadow-lg shadow-rose-500/10 mb-4">
            🎪
          </div>
          <h1 className="text-2xl font-black tracking-tight text-slate-100 flex items-center gap-1.5">
            FANTASY CMS
          </h1>
          <p className="text-xs text-slate-400 font-medium tracking-wide uppercase mt-1">
            Painel de Controle
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-rose-950/30 border border-rose-900 rounded-2xl text-xs font-semibold text-rose-400">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <label htmlFor="email" className="text-xs text-slate-400 font-bold uppercase tracking-wider">
              E-mail Administrativo
            </label>
            <div className="relative">
              <Mail className="absolute left-4 top-3.5 text-slate-500" size={16} />
              <input
                type="email"
                id="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="nome@exemplo.com"
                className="w-full pl-11 pr-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none transition-colors"
              />
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <label htmlFor="password" className="text-xs text-slate-400 font-bold uppercase tracking-wider">
              Senha de Acesso
            </label>
            <div className="relative">
              <Lock className="absolute left-4 top-3.5 text-slate-500" size={16} />
              <input
                type="password"
                id="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-11 pr-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:border-rose-500 focus:outline-none transition-colors"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black rounded-xl hover:shadow-xl hover:shadow-rose-500/10 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                Autenticando...
              </>
            ) : (
              "Entrar no Painel"
            )}
          </button>
        </form>

        <div className="mt-8 text-center">
          <a
            href="/"
            className="text-xs font-bold text-slate-500 hover:text-rose-400 transition-colors"
          >
            &larr; Voltar para a Landing Page
          </a>
        </div>
      </div>
    </div>
  );
}
