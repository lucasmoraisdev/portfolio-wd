"use client";

import React, { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import {
  LayoutDashboard,
  Settings,
  ToyBrick,
  Calendar,
  MessageSquare,
  HelpCircle,
  Mail,
  LogOut,
  User as UserIcon,
  Loader2,
  Sparkles,
} from "lucide-react";

import { setToken } from "../../services/api";

interface SidebarItem {
  name: string;
  href: string;
  icon: React.ComponentType<any>;
}

const SIDEBAR_ITEMS: SidebarItem[] = [
  { name: "Visão Geral", href: "/admin/dashboard", icon: LayoutDashboard },
  { name: "Hero & Ajustes", href: "/admin/settings", icon: Settings },
  { name: "Brinquedos", href: "/admin/toys", icon: ToyBrick },
  { name: "Eventos & Shows", href: "/admin/events", icon: Calendar },
  { name: "Depoimentos", href: "/admin/testimonials", icon: MessageSquare },
  { name: "FAQ / Perguntas", href: "/admin/faq", icon: HelpCircle },
  { name: "Fale Conosco", href: "/admin/contacts", icon: Mail },
];

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);
  const router = useRouter();
  const pathname = usePathname();

  // Auth check
  useEffect(() => {
    // Skip checking on login page
    if (pathname === "/admin/login") {
      setLoading(false);
      return;
    }

    const token = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");

    if (!token) {
      router.push("/admin/login");
    } else {
      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch (e) {
          console.error("Failed to parse stored user:", e);
          localStorage.removeItem("user");
        }
      }
      setLoading(false);
    }
  }, [router, pathname]);

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("user");
    router.push("/admin/login");
  };

  // If path is login, don't show the layout frame
  if (pathname === "/admin/login") {
    return <>{children}</>;
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 font-sans text-slate-100">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="animate-spin text-rose-500" size={36} />
          <span className="text-sm font-semibold text-slate-400">Verificando credenciais...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-slate-950 font-sans text-slate-200">
      {/* SIDEBAR */}
      <aside className="hidden md:flex flex-col w-64 bg-slate-900 border-r border-slate-800/80 shrink-0">
        {/* Logo banner */}
        <div className="px-6 py-6 border-b border-slate-800/80 flex items-center gap-2">
          <span className="p-1.5 rounded-lg bg-gradient-to-tr from-rose-500 to-amber-400 text-slate-950 font-black text-sm">
            🎪
          </span>
          <div className="flex flex-col">
            <span className="text-sm font-black tracking-wider text-slate-100 uppercase">
              Fantasy Admin
            </span>
            <span className="text-[10px] text-slate-500 font-bold tracking-widest uppercase -mt-0.5">
              Gestor de Conteúdo
            </span>
          </div>
        </div>

        {/* Sidebar Nav */}
        <nav className="flex-1 px-4 py-6 flex flex-col gap-1.5 overflow-y-auto">
          {SIDEBAR_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3.5 px-4 py-3 rounded-xl text-sm font-bold tracking-wide transition-all ${
                  isActive
                    ? "bg-rose-500/10 text-rose-400 border border-rose-500/10"
                    : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/40 border border-transparent"
                }`}
              >
                <Icon size={18} className={isActive ? "text-rose-400" : "text-slate-400"} />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Logout bottom */}
        <div className="p-4 border-t border-slate-800/80">
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 py-3 rounded-xl border border-slate-800/80 hover:border-rose-500/20 hover:bg-rose-950/20 text-slate-400 hover:text-rose-400 font-bold text-sm cursor-pointer transition-colors"
          >
            <LogOut size={16} />
            Efetuar Logout
          </button>
        </div>
      </aside>

      {/* MAIN CONTAINER */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Navbar */}
        <header className="h-16 bg-slate-900 border-b border-slate-800/80 flex items-center justify-between px-6 z-10 shrink-0">
          {/* Page title placeholder */}
          <div className="font-extrabold text-slate-200">
            {SIDEBAR_ITEMS.find((item) => pathname === item.href)?.name || "CMS Painel"}
          </div>

          {/* User profile dropdown info */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex flex-col text-right">
              <span className="text-xs font-black text-slate-300">{user?.name || "Administrador"}</span>
              <span className="text-[10px] text-slate-500 font-semibold">{user?.email || "admin@fantasy.com"}</span>
            </div>
            <div className="w-9 h-9 rounded-full bg-slate-800 border border-slate-700/80 flex items-center justify-center text-slate-400 font-bold text-sm">
              <UserIcon size={16} />
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-6 md:p-10 bg-slate-950">
          <div className="max-w-6xl mx-auto w-full animate-fade-in">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
