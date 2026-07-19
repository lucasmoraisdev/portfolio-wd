"use client";

import React, { useState, useEffect } from "react";
import * as Icons from "lucide-react";
import {
  Sparkles,
  Phone,
  Mail,
  MapPin,
  Calendar,
  Star,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ArrowRight,
  Send,
  Loader2,
  Menu,
  X,
  Plus,
  ShieldCheck,
  CheckCircle,
  HelpCircle,
} from "lucide-react";

import api from "../services/api";
import { Toy, Event, Testimonial, FAQ, HeroConfig } from "../types";

// Mock Fallbacks
const DEFAULT_HERO: HeroConfig = {
  tag: "Locação de Brinquedos e Recreação Premium",
  title: "FANTASY EVENTOS",
  subtitle: "Recreação & Locação de Brinquedos",
  text: "Oferecemos os melhores brinquedos infláveis e serviços de recreação premium para tornar a sua festa ou evento corporativo inesquecível.",
  primary_button: "Ver Brinquedos",
  primary_link: "#brinquedos",
  secondary_button: "Fale Conosco",
  secondary_link: "#contato",
  background_image: "",
  background_video: "",
  carousel_images: [],
  carousel_transition: 5,
  safety_cards: [
    {
      id: "1",
      title: "Segurança Máxima",
      description: "Brinquedos inspecionados regularmente, com proteções reforçadas e equipe treinada de montagem e suporte técnico.",
      icon: "ShieldCheck",
    },
    {
      id: "2",
      title: "Higiene Absoluta",
      description: "Lavagem profunda e desinfecção com produtos atóxicos no local do evento, garantindo proteção completa para sua família.",
      icon: "CheckCircle",
    },
    {
      id: "3",
      title: "Monitores Dedicados",
      description: "Monitores de recreação atenciosos e divertidos para acompanhar as crianças e enriquecer a festa com total tranquilidade.",
      icon: "Sparkles",
    },
  ],
  bg_color: null,
};

const DEFAULT_TOYS: Toy[] = [
  {
    id: "1",
    name: "Mega Tobogã Escalada",
    slug: "mega-toboga-escalada",
    category: "Infláveis",
    min_age: 3,
    max_age: 12,
    description: "Tobogã inflável gigante com parede de escalada interna. Confeccionado em lona vinílica super resistente, garantindo 100% de segurança com costuras reforçadas e cores vibrantes.",
    is_featured: true,
    is_active: true,
    display_order: 1,
    gallery_image_ids: [],
    gallery_urls: [],
    created_at: "",
    updated_at: "",
  },
  {
    id: "2",
    name: "Cama Elástica Master",
    slug: "cama-elastica-master",
    category: "Clássicos",
    min_age: 2,
    max_age: 99,
    description: "Cama elástica profissional com rede de proteção reforçada de alta densidade, protetor de molas colorido e estrutura metálica galvanizada de alta estabilidade.",
    is_featured: true,
    is_active: true,
    display_order: 2,
    gallery_image_ids: [],
    gallery_urls: [],
    created_at: "",
    updated_at: "",
  },
  {
    id: "3",
    name: "Piscina de Bolinhas Premium",
    slug: "piscina-de-bolinhas-premium",
    category: "Infantil",
    min_age: 1,
    max_age: 6,
    description: "Piscina de bolinhas inflável decorada, preenchida com 2000 bolinhas coloridas certificadas. Ideal para os pequenininhos gastarem energia com total segurança.",
    is_featured: false,
    is_active: true,
    display_order: 3,
    gallery_image_ids: [],
    gallery_urls: [],
    created_at: "",
    updated_at: "",
  },
  {
    id: "4",
    name: "Castelo Inflável Medieval",
    slug: "castelo-inflavel-medieval",
    category: "Infláveis",
    min_age: 2,
    max_age: 8,
    description: "Castelo pula-pula inflável temático medieval. Compacto, adapta-se a salões e garagens menores. Excelente para fotos de recordação e diversão intensa.",
    is_featured: true,
    is_active: true,
    display_order: 4,
    gallery_image_ids: [],
    gallery_urls: [],
    created_at: "",
    updated_at: "",
  },
];

const DEFAULT_EVENTS: Event[] = [
  {
    id: "1",
    title: "Festival de Férias Shopping Multi",
    city: "São Paulo",
    client: "Multi Shopping S/A",
    event_date: "2026-01-15",
    description: "Montagem completa de arena kids recreativa no hall principal do shopping. Contou com recreadores treinados, oficinas de pintura, shows teatrais e brinquedos de grande porte.",
    is_featured: true,
    is_active: true,
    display_order: 1,
    cover_image_id: null,
    gallery_image_ids: [],
    gallery_urls: [],
    created_at: "",
    updated_at: "",
  },
  {
    id: "2",
    title: "Aniversário Especial do Enzo - Avengers Theme",
    city: "Campinas",
    client: "Família Barbosa",
    event_date: "2026-02-28",
    description: "Festa residencial tematizada com painel de heróis, tobogã inflável gigante e equipe de animadores caracterizados promovendo jogos e gincanas com as crianças.",
    is_featured: true,
    is_active: true,
    display_order: 2,
    cover_image_id: null,
    gallery_image_ids: [],
    gallery_urls: [],
    created_at: "",
    updated_at: "",
  },
];

const DEFAULT_TESTIMONIALS: Testimonial[] = [
  {
    id: "1",
    name: "Carolina Menezes",
    city: "São Paulo",
    company: "Mãe do Gabriel",
    testimonial: "Atendimento impecável! Os brinquedos chegaram super limpos e no horário combinado. A equipe que montou foi de extrema educação e carinho com as crianças. Com certeza alugarei novamente!",
    rating: 5,
    is_active: true,
    display_order: 1,
    photo_id: null,
    created_at: "",
    updated_at: "",
  },
  {
    id: "2",
    name: "Felipe G. Santos",
    city: "Campinas",
    company: "Condomínio Vila Bella",
    testimonial: "Contratamos a recreação completa e os infláveis para o Dia das Crianças do condomínio. Organização impecável, monitores atenciosos e diversão garantida para mais de 100 crianças. Parabéns pelo serviço!",
    rating: 5,
    is_active: true,
    display_order: 2,
    photo_id: null,
    created_at: "",
    updated_at: "",
  },
];

const DEFAULT_FAQS: FAQ[] = [
  {
    id: "1",
    question: "Como funciona a contratação e entrega dos brinquedos?",
    answer: "Você escolhe os brinquedos de sua preferência no catálogo e faz o contato conosco. Nós confirmamos a disponibilidade para o dia e horário solicitados, realizamos a montagem do contrato e entregamos e retiramos tudo de forma autônoma no local do seu evento.",
    is_active: true,
    display_order: 1,
    created_at: "",
    updated_at: "",
  },
  {
    id: "2",
    question: "Os brinquedos são seguros e higienizados?",
    answer: "Sim, 100%! A segurança e higiene são nossas maiores prioridades. Todos os brinquedos passam por uma limpeza profunda e sanitização completa com produtos atóxicos e biodegradáveis antes de serem embalados para entrega e imediatamente após a desmontagem.",
    is_active: true,
    display_order: 2,
    created_at: "",
    updated_at: "",
  },
  {
    id: "3",
    question: "O transporte e montagem já estão inclusos no preço?",
    answer: "A montagem profissional completa está inclusa em todas as locações. O frete é calculado de forma justa com base na distância entre nossa base operacional e o local do seu evento. O cálculo exato é enviado no seu orçamento final.",
    is_active: true,
    display_order: 3,
    created_at: "",
    updated_at: "",
  },
];

export default function LandingPage() {
  const [hero, setHero] = useState<HeroConfig>(DEFAULT_HERO);
  const [settings, setSettings] = useState<any>(null);
  const [toys, setToys] = useState<Toy[]>(DEFAULT_TOYS);
  const [events, setEvents] = useState<Event[]>(DEFAULT_EVENTS);
  const [currentEventIndex, setCurrentEventIndex] = useState(0);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [currentSafetyIndex, setCurrentSafetyIndex] = useState(0);
  const [isMobile, setIsMobile] = useState(true);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 768);
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const nextEvent = () => {
    setCurrentImageIndex(0);
    setCurrentEventIndex((prev) => (prev + 1) % events.length);
  };

  const prevEvent = () => {
    setCurrentImageIndex(0);
    setCurrentEventIndex((prev) => (prev - 1 + events.length) % events.length);
  };

  // Auto-play cycling through event images and transitioning events
  useEffect(() => {
    if (events.length === 0) return;

    const timer = setInterval(() => {
      const currentEvent = events[currentEventIndex];
      if (!currentEvent) return;

      const currentImages = [
        ...(currentEvent.cover_image_url ? [currentEvent.cover_image_url] : []),
        ...((currentEvent as any).gallery_image_urls || currentEvent.gallery_urls || []),
      ];

      if (currentImages.length > 1 && currentImageIndex < currentImages.length - 1) {
        setCurrentImageIndex((prev) => prev + 1);
      } else {
        setCurrentImageIndex(0);
        setCurrentEventIndex((prev) => (prev + 1) % events.length);
      }
    }, 4000);

    return () => clearInterval(timer);
  }, [events, currentEventIndex, currentImageIndex]);
  const [testimonials, setTestimonials] = useState<Testimonial[]>(DEFAULT_TESTIMONIALS);
  const [faqs, setFaqs] = useState<FAQ[]>(DEFAULT_FAQS);

  // States for UX
  const [selectedCategory, setSelectedCategory] = useState<string>("Todos");
  const [selectedToy, setSelectedToy] = useState<Toy | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeFAQIndex, setActiveFAQIndex] = useState<number | null>(null);
  const [isNavbarScrolled, setIsNavbarScrolled] = useState(false);

  // Contact Form State
  const [formName, setFormName] = useState("");
  const [formEmail, setFormEmail] = useState("");
  const [formPhone, setFormPhone] = useState("");
  const [formSubject, setFormSubject] = useState("");
  const [formMessage, setFormMessage] = useState("");
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [formFeedback, setFormFeedback] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  // Load initial cached data from localStorage on mount (client-side only)
  useEffect(() => {
    try {
      const cachedHero = localStorage.getItem("portfolio_cache_hero");
      if (cachedHero) setHero(JSON.parse(cachedHero));

      const cachedSettings = localStorage.getItem("portfolio_cache_settings");
      if (cachedSettings) setSettings(JSON.parse(cachedSettings));

      const cachedToys = localStorage.getItem("portfolio_cache_toys");
      if (cachedToys) setToys(JSON.parse(cachedToys));

      const cachedEvents = localStorage.getItem("portfolio_cache_events");
      if (cachedEvents) setEvents(JSON.parse(cachedEvents));

      const cachedTestimonials = localStorage.getItem("portfolio_cache_testimonials");
      if (cachedTestimonials) setTestimonials(JSON.parse(cachedTestimonials));

      const cachedFaqs = localStorage.getItem("portfolio_cache_faqs");
      if (cachedFaqs) setFaqs(JSON.parse(cachedFaqs));
    } catch (e) {
      console.error("Erro ao ler dados do cache local:", e);
    }
  }, []);

  // Load configuration from API
  useEffect(() => {
    // 0. Fetch Settings
    api.settings
      .getPublic()
      .then((res) => {
        if (res?.data) {
          setSettings(res.data);
          localStorage.setItem("portfolio_cache_settings", JSON.stringify(res.data));
        }
      })
      .catch((err) => console.log("Erro ao buscar Settings:", err));

    // 1. Fetch Hero Config
    api.hero
      .getPublic()
      .then((res) => {
        if (res?.data) {
          setHero(res.data);
          localStorage.setItem("portfolio_cache_hero", JSON.stringify(res.data));
        }
      })
      .catch((err) => console.log("Erro ao buscar Hero:", err));

    // 2. Fetch Toys
    api.toys
      .listPublic()
      .then((res) => {
        if (res?.data?.items && res.data.items.length > 0) {
          setToys(res.data.items);
          localStorage.setItem("portfolio_cache_toys", JSON.stringify(res.data.items));
        }
      })
      .catch((err) => console.log("Erro ao buscar Brinquedos:", err));

    // 3. Fetch Events
    api.events
      .listPublic()
      .then((res) => {
        if (res?.data?.items && res.data.items.length > 0) {
          setEvents(res.data.items);
          localStorage.setItem("portfolio_cache_events", JSON.stringify(res.data.items));
        }
      })
      .catch((err) => console.log("Erro ao buscar Eventos:", err));

    // 4. Fetch Testimonials
    api.testimonials
      .listPublic()
      .then((res) => {
        if (res?.data?.items && res.data.items.length > 0) {
          setTestimonials(res.data.items);
          localStorage.setItem("portfolio_cache_testimonials", JSON.stringify(res.data.items));
        }
      })
      .catch((err) => console.log("Erro ao buscar Depoimentos:", err));

    // 5. Fetch FAQs
    api.faq
      .listPublic()
      .then((res) => {
        if (res?.data?.items && res.data.items.length > 0) {
          setFaqs(res.data.items);
          localStorage.setItem("portfolio_cache_faqs", JSON.stringify(res.data.items));
        }
      })
      .catch((err) => console.log("Erro ao buscar FAQs:", err));

    // Scroll listener for Navbar style
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setIsNavbarScrolled(true);
      } else {
        setIsNavbarScrolled(false);
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Filter toys by category
  const categories = ["Todos", ...Array.from(new Set(toys.map((t) => t.category)))];
  const filteredToys =
    selectedCategory === "Todos"
      ? toys
      : toys.filter((t) => t.category === selectedCategory);

  // Submit Contact Form
  const handleContactSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName || !formEmail || !formMessage) {
      setFormFeedback({
        type: "error",
        text: "Por favor, preencha todos os campos obrigatórios (Nome, E-mail e Mensagem).",
      });
      return;
    }

    setFormSubmitting(true);
    setFormFeedback(null);

    try {
      await api.contacts.submit({
        name: formName,
        email: formEmail,
        phone: formPhone || undefined,
        subject: formSubject || undefined,
        message: formMessage,
      });

      setFormFeedback({
        type: "success",
        text: "Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.",
      });

      // Clear form
      setFormName("");
      setFormEmail("");
      setFormPhone("");
      setFormSubject("");
      setFormMessage("");

      // Redirecionar para o WhatsApp
      const whatsappNumber = settings?.contact?.whatsapp || "5511987654321";
      const cleanNumber = whatsappNumber.replace(/\D/g, "");

      const whatsappText = `Olá, vim pelo site!
          *Nome:* ${formName}
          *E-mail:* ${formEmail}
          *Assunto:* ${formSubject || "Não informado"}
          *Mensagem:* ${formMessage}`;

      const whatsappUrl = `https://wa.me/${cleanNumber}?text=${encodeURIComponent(whatsappText)}`;
      window.open(whatsappUrl, "_blank");
    } catch (err: any) {
      setFormFeedback({
        type: "error",
        text: err.message || "Ocorreu um erro ao enviar sua mensagem. Tente novamente mais tarde.",
      });
    } finally {
      setFormSubmitting(false);
    }
  };

  return (
    <div
      className="flex flex-col min-h-screen text-slate-100 font-sans selection:bg-rose-500 selection:text-white"
      style={{ backgroundColor: hero.bg_color || "#020617" }}
    >
      {/* HEADER / NAVBAR */}
      <header
        className={`fixed top-0 left-0 w-full z-50 transition-all duration-300 ${isNavbarScrolled
          ? "bg-slate-950/80 backdrop-blur-md border-b border-slate-900 py-4 shadow-lg shadow-slate-950/20"
          : "bg-transparent py-6"
          }`}
      >
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          <a href="#" className="flex items-center gap-2 group">
            {settings?.uploads?.logo_main ? (
              <img src={settings.uploads.logo_main} alt="Logo" className="h-10 w-auto object-contain transform group-hover:scale-105 transition-transform" />
            ) : (
              <>
                <span className="p-2 rounded-xl bg-gradient-to-tr from-rose-500 to-amber-400 text-slate-950 font-bold flex items-center justify-center transform group-hover:rotate-12 transition-transform shadow-md shadow-rose-500/20">
                  🎪
                </span>
                <div className="flex flex-col">
                  <span className="text-xl font-black tracking-wider bg-gradient-to-r from-rose-400 to-amber-300 bg-clip-text text-transparent">
                    {settings?.company?.name || "FANTASY"}
                  </span>
                  <span className="text-xs text-slate-400 tracking-widest uppercase font-bold -mt-1">
                    {settings?.company?.slogan || "Eventos & Lazer"}
                  </span>
                </div>
              </>
            )}
          </a>

          {/* Desktop Nav Links */}
          <nav className="hidden md:flex items-center gap-8 text-sm font-semibold tracking-wide">
            <a
              href="#sobre"
              className="text-slate-300 hover:text-rose-400 transition-colors"
            >
              Sobre Nós
            </a>
            <a
              href="#brinquedos"
              className="text-slate-300 hover:text-rose-400 transition-colors"
            >
              Catálogo
            </a>
            <a
              href="#eventos"
              className="text-slate-300 hover:text-rose-400 transition-colors"
            >
              Eventos
            </a>
            <a
              href="#depoimentos"
              className="text-slate-300 hover:text-rose-400 transition-colors"
            >
              Avaliações
            </a>
            <a
              href="#faq"
              className="text-slate-300 hover:text-rose-400 transition-colors"
            >
              FAQ
            </a>
            <a
              href="#contato"
              className="px-5 py-2.5 rounded-full bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-extrabold hover:shadow-lg hover:shadow-rose-500/20 transition-all hover:-translate-y-0.5 active:translate-y-0"
            >
              Orçamento
            </a>
          </nav>

          {/* Mobile Menu Icon */}
          <button
            className="p-2 md:hidden text-slate-300 hover:text-rose-400"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Dropdown Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-slate-950 border-b border-slate-900 absolute top-full left-0 w-full px-6 py-8 flex flex-col gap-6 text-center font-bold text-lg shadow-xl animate-fade-in-down">
            <a
              href="#sobre"
              className="text-slate-300 hover:text-rose-400"
              onClick={() => setMobileMenuOpen(false)}
            >
              Sobre Nós
            </a>
            <a
              href="#brinquedos"
              className="text-slate-300 hover:text-rose-400"
              onClick={() => setMobileMenuOpen(false)}
            >
              Catálogo
            </a>
            <a
              href="#eventos"
              className="text-slate-300 hover:text-rose-400"
              onClick={() => setMobileMenuOpen(false)}
            >
              Eventos
            </a>
            <a
              href="#depoimentos"
              className="text-slate-300 hover:text-rose-400"
              onClick={() => setMobileMenuOpen(false)}
            >
              Avaliações
            </a>
            <a
              href="#faq"
              className="text-slate-300 hover:text-rose-400"
              onClick={() => setMobileMenuOpen(false)}
            >
              FAQ
            </a>
            <a
              href="#contato"
              className="py-3 rounded-full bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950"
              onClick={() => setMobileMenuOpen(false)}
            >
              Solicitar Orçamento
            </a>
          </div>
        )}
      </header>

      {/* HERO SECTION */}
      <section className="relative min-h-screen flex items-center justify-center pt-24 overflow-hidden bg-slate-950">
        {/* 1. Background Gradients (bottom-most layer) */}
        <div className="absolute inset-0 z-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-rose-950/20 via-slate-950 to-slate-950" />
        <div className="absolute top-1/4 left-1/10 w-96 h-96 bg-rose-600/10 rounded-full blur-3xl z-0" />
        <div className="absolute bottom-1/4 right-1/10 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl z-0" />
        {/* 2. Background Media */}

        {hero.background_video ? (
          <video
            src={hero.background_video}
            autoPlay
            loop
            muted
            playsInline
            key={hero.background_video}
            className="absolute inset-0 w-full h-full object-cover opacity-30 pointer-events-none z-10"
          />
        ) : (
          hero.background_image && (
            <img
              src={hero.background_image}
              alt="Hero Background"
              className="absolute inset-0 w-full h-full object-cover opacity-35 pointer-events-none z-10"
            />
          )
        )}

        {/* 3. Dark overlay for readability (layered on top of media) */}
        {(hero.background_video || hero.background_image) && (
          <div className="absolute inset-0 bg-gradient-to-b from-slate-950/60 via-slate-950/40 to-slate-950 pointer-events-none z-20" />
        )}

        {/* Content Wrapper */}
        <div className="relative z-30 max-w-5xl mx-auto px-6 text-center flex flex-col items-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900/60 border border-rose-500/20 text-rose-300 text-xs font-semibold uppercase tracking-wider mb-8 animate-pulse">
            <Sparkles size={14} className="text-rose-400" /> {hero.tag || DEFAULT_HERO.tag}
          </div>

          <h1 className="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight leading-none text-slate-100 max-w-4xl mb-6">
            {hero.title || DEFAULT_HERO.title}
          </h1>

          <h2 className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-rose-400 to-amber-300 bg-clip-text text-transparent mb-6">
            {hero.subtitle || DEFAULT_HERO.subtitle}
          </h2>

          <p className="text-base sm:text-lg text-slate-400 max-w-2xl leading-relaxed mb-12">
            {hero.text || DEFAULT_HERO.text}
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center w-full max-w-md">
            <a
              href={hero.primary_link || DEFAULT_HERO.primary_link || "#brinquedos"}
              className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black rounded-full hover:shadow-xl hover:shadow-rose-500/20 transition-all transform hover:-translate-y-0.5 flex items-center justify-center gap-2"
            >
              {hero.primary_button || DEFAULT_HERO.primary_button || "Ver Catálogo"}
              <ArrowRight size={18} />
            </a>
            <a
              href={hero.secondary_link || DEFAULT_HERO.secondary_link || "#contato"}
              className="w-full sm:w-auto px-8 py-4 bg-slate-900/80 text-slate-200 border border-slate-800 font-bold rounded-full hover:bg-slate-900 hover:text-white transition-all flex items-center justify-center"
            >
              {hero.secondary_button || DEFAULT_HERO.secondary_button || "Fale Conosco"}
            </a>
          </div>
        </div>
      </section>

      {/* SAFETY & STATS SECTION */}
      <section id="sobre" className="py-20 border-t border-slate-900 bg-slate-950/40">
        {(() => {
          const safetyCards = hero.safety_cards && hero.safety_cards.length > 0
            ? hero.safety_cards
            : DEFAULT_HERO.safety_cards;

          // Carousel when > 4 cards, fixed grid when <= 4
          const isCarousel = safetyCards.length > 4;
          const visibleCount = isMobile ? 1 : 3;
          const cardWidthPct = 100 / visibleCount;
          const maxIndex = Math.max(0, safetyCards.length - visibleCount);

          // Grid cols class based on card count (capped at 4)
          const gridCols =
            safetyCards.length === 1 ? "grid-cols-1" :
              safetyCards.length === 2 ? "grid-cols-1 sm:grid-cols-2" :
                safetyCards.length === 3 ? "grid-cols-1 md:grid-cols-3" :
                  "grid-cols-1 sm:grid-cols-2 xl:grid-cols-4";

          const prevSafety = () => setCurrentSafetyIndex((prev) => Math.max(0, prev - 1));
          const nextSafety = () => setCurrentSafetyIndex((prev) => Math.min(maxIndex, prev + 1));

          return (
            <div className="max-w-7xl mx-auto px-6">
              {/* Carousel header with navigation */}
              {isCarousel && (
                <div className="flex items-center justify-between mb-8">
                  <div>
                    <p className="text-xs uppercase tracking-widest font-bold text-rose-500 mb-1">Por que nos escolher</p>
                    <h2 className="text-2xl font-black text-slate-100">Nossos Diferenciais</h2>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={prevSafety}
                      disabled={currentSafetyIndex === 0}
                      className="p-2.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:text-rose-400 disabled:opacity-30 text-slate-400 cursor-pointer transition-colors duration-200"
                    >
                      <ChevronLeft size={20} />
                    </button>
                    <button
                      onClick={nextSafety}
                      disabled={currentSafetyIndex >= maxIndex}
                      className="p-2.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:text-rose-400 disabled:opacity-30 text-slate-400 cursor-pointer transition-colors duration-200"
                    >
                      <ChevronRight size={20} />
                    </button>
                  </div>
                </div>
              )}

              {isCarousel ? (
                // Carousel Mode — slides 3 visible at a time on desktop
                <div className="overflow-hidden">
                  <div
                    className="flex transition-transform duration-500 ease-out"
                    style={{ transform: `translateX(-${currentSafetyIndex * cardWidthPct}%)` }}
                  >
                    {safetyCards.map((card) => {
                      const IconComponent = (Icons as any)[card.icon] || ShieldCheck;
                      return (
                        <div
                          key={card.id}
                          style={{ minWidth: `${cardWidthPct}%` }}
                          className="px-3"
                        >
                          <div className="flex flex-col items-start gap-4 p-8 bg-slate-900/30 rounded-3xl border border-slate-900 h-full hover:border-slate-800 transition-colors">
                            <div className="p-4 bg-rose-500/10 rounded-2xl text-rose-400">
                              <IconComponent size={32} />
                            </div>
                            <h3 className="text-xl font-bold">{card.title}</h3>
                            <p className="text-sm text-slate-400 leading-relaxed">{card.description}</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Dot indicators */}
                  <div className="flex justify-center gap-2 mt-8">
                    {Array.from({ length: maxIndex + 1 }).map((_, i) => (
                      <button
                        key={i}
                        onClick={() => setCurrentSafetyIndex(i)}
                        className={`h-1.5 rounded-full transition-all duration-300 ${i === currentSafetyIndex
                          ? "w-6 bg-rose-500"
                          : "w-1.5 bg-slate-700 hover:bg-slate-600"
                          }`}
                      />
                    ))}
                  </div>
                </div>
              ) : (
                // Fixed Grid Mode — up to 4 cards
                <div className={`grid ${gridCols} gap-8`}>
                  {safetyCards.map((card) => {
                    const IconComponent = (Icons as any)[card.icon] || ShieldCheck;
                    return (
                      <div
                        key={card.id}
                        className="flex flex-col items-center md:items-start text-center md:text-left gap-4 p-6 bg-slate-900/30 rounded-3xl border border-slate-900 hover:border-slate-800 transition-colors"
                      >
                        <div className="p-4 bg-rose-500/10 rounded-2xl text-rose-400">
                          <IconComponent size={32} />
                        </div>
                        <h3 className="text-xl font-bold">{card.title}</h3>
                        <p className="text-sm text-slate-400 leading-relaxed">{card.description}</p>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })()}
      </section>

      {/* TOYS / CATALOG SECTION */}
      <section id="brinquedos" className="py-24 max-w-7xl mx-auto px-6 w-full">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16">
          <div className="max-w-xl">
            <h2 className="text-xs uppercase font-extrabold tracking-widest text-rose-500 mb-3">
              Diversão para todas as idades
            </h2>
            <h3 className="text-3xl sm:text-4xl font-black tracking-tight">
              Catálogo de Brinquedos
            </h3>
          </div>

          {/* Categories filter */}
          <div className="flex flex-wrap gap-2 text-sm">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-full font-bold transition-all border ${selectedCategory === cat
                  ? "bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 border-transparent shadow-lg shadow-rose-500/10"
                  : "bg-slate-900/60 text-slate-400 border-slate-800 hover:text-slate-200"
                  }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Toys Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {filteredToys.map((toy) => (
            <div
              key={toy.id}
              onClick={() => setSelectedToy(toy)}
              className="group bg-slate-900/40 rounded-3xl border border-slate-900 hover:border-rose-500/20 overflow-hidden cursor-pointer transition-all hover:-translate-y-1 hover:shadow-xl hover:shadow-rose-950/10"
            >
              {/* Image box */}
              <div className="relative h-52 w-full bg-slate-900 flex items-center justify-center text-4xl group-hover:scale-105 transition-transform duration-300">
                {(() => {
                  const imageUrl = toy.cover_image_url ||
                    ((toy as any).gallery_image_urls && (toy as any).gallery_image_urls.length > 0 ? (toy as any).gallery_image_urls[0] : null) ||
                    (toy.gallery_urls && toy.gallery_urls.length > 0 ? toy.gallery_urls[0] : null);
                  return imageUrl ? (
                    <img
                      src={imageUrl}
                      alt={toy.name}
                      className="object-cover w-full h-full"
                    />
                  ) : (
                    <span>🎠</span>
                  );
                })()}
                <div className="absolute top-4 right-4 px-3 py-1 rounded-full bg-slate-950/60 backdrop-blur-md text-xs font-bold text-slate-300 border border-slate-800">
                  {toy.category}
                </div>
              </div>

              {/* Text info */}
              <div className="p-6">
                <div className="flex items-center justify-between gap-2 mb-2">
                  <h4 className="text-lg font-bold group-hover:text-rose-400 transition-colors truncate">
                    {toy.name}
                  </h4>
                </div>
                <div className="flex justify-between items-center text-xs text-slate-400 font-semibold mb-4">
                  <span>Idade recomendada: {toy.min_age} a {toy.max_age} anos</span>
                </div>
                <div className="flex items-center gap-1 text-xs text-rose-400 font-bold group-hover:underline">
                  Ver Detalhes e Fotos <ArrowRight size={12} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* PORTFOLIO EVENTS SECTION */}
      <section id="eventos" className="py-24 border-t border-slate-900 bg-slate-950/30">
        <div className="max-w-7xl mx-auto px-6">
          <div className="max-w-xl mb-16 text-center md:text-left">
            <h2 className="text-xs uppercase font-extrabold tracking-widest text-rose-500 mb-3">
              Trabalhos recentes de sucesso
            </h2>
            <h3 className="text-3xl sm:text-4xl font-black tracking-tight">
              Galeria de Eventos & Shows
            </h3>
          </div>

          {events.length > 0 && (
            <div className="relative max-w-4xl mx-auto">
              <div className="overflow-hidden rounded-3xl border border-slate-900 bg-slate-900/30 backdrop-blur-sm shadow-2xl">
                <div
                  className="flex transition-transform duration-1000 cubic-bezier(0.25, 1, 0.5, 1)"
                  style={{ transform: `translateX(-${currentEventIndex * 100}%)` }}
                >
                  {events.map((event) => (
                    <div key={event.id} className="w-full shrink-0 flex flex-col md:flex-row h-auto md:h-[450px]">
                      {/* Photo Column */}
                      <div className="w-full md:w-1/2 h-64 md:h-full bg-slate-950 relative overflow-hidden group">
                        {(() => {
                          const eventImages = [
                            ...(event.cover_image_url ? [event.cover_image_url] : []),
                            ...((event as any).gallery_image_urls || event.gallery_urls || []),
                          ];
                          const isActiveEvent = events[currentEventIndex]?.id === event.id;
                          const activeUrl = isActiveEvent && eventImages.length > 0
                            ? eventImages[currentImageIndex % eventImages.length]
                            : event.cover_image_url;

                          return activeUrl ? (
                            <img
                              key={activeUrl}
                              src={activeUrl}
                              alt={event.title}
                              className="object-cover w-full h-full transition-transform duration-750 group-hover:scale-105 animate-fade-in-slow"
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center text-6xl">
                              🎉
                            </div>
                          );
                        })()}
                        <div className="absolute top-4 left-4 px-3 py-1.5 bg-slate-950/80 backdrop-blur-md rounded-xl text-[10px] text-slate-300 font-extrabold uppercase tracking-wider flex items-center gap-1 border border-slate-800">
                          <MapPin size={10} className="text-rose-500" /> {event.city}
                        </div>
                      </div>

                      {/* Content Column */}
                      <div className="w-full md:w-1/2 p-8 md:p-12 flex flex-col justify-between bg-slate-900/60">
                        <div className="flex flex-col gap-4">
                          <div className="text-[10px] text-rose-500 font-extrabold uppercase tracking-widest">
                            Eventos Realizados
                          </div>
                          <div>
                            <h4 className="text-2xl md:text-3xl font-black text-slate-100 leading-tight">
                              {event.title}
                            </h4>
                            <div className="text-sm text-slate-400 font-bold mt-1">
                              Cliente: <span className="text-rose-500">{event.client}</span>
                            </div>
                          </div>
                          <p className="text-xs text-slate-400 leading-relaxed mt-2 font-medium">
                            {event.description}
                          </p>
                        </div>

                        <div className="flex justify-between items-center border-t border-slate-800/60 pt-6 mt-6 md:mt-0">
                          <div className="text-xs text-slate-500 font-bold uppercase tracking-wider flex items-center gap-1">
                            <Calendar size={12} className="text-rose-500" />
                            <span>Data: {event.event_date}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Navigation Controls */}
              {events.length > 1 && (
                <>
                  <button
                    onClick={prevEvent}
                    className="absolute top-1/2 -left-4 md:-left-16 -translate-y-1/2 w-10 md:w-12 h-10 md:h-12 bg-slate-900/90 hover:bg-slate-800 border border-slate-800 text-slate-350 rounded-full flex items-center justify-center shadow-xl hover:text-slate-100 transition-all hover:scale-105 cursor-pointer"
                  >
                    <ChevronLeft size={20} />
                  </button>
                  <button
                    onClick={nextEvent}
                    className="absolute top-1/2 -right-4 md:-right-16 -translate-y-1/2 w-10 md:w-12 h-10 md:h-12 bg-slate-900/90 hover:bg-slate-800 border border-slate-800 text-slate-355 rounded-full flex items-center justify-center shadow-xl hover:text-slate-100 transition-all hover:scale-105 cursor-pointer"
                  >
                    <ChevronRight size={20} />
                  </button>

                  {/* Dot Indicators */}
                  <div className="flex justify-center gap-2 mt-8">
                    {events.map((_, idx) => (
                      <button
                        key={idx}
                        onClick={() => setCurrentEventIndex(idx)}
                        className={`h-2.5 rounded-full transition-all duration-300 cursor-pointer ${currentEventIndex === idx ? "w-8 bg-rose-500" : "w-2.5 bg-slate-850 hover:bg-slate-750"
                          }`}
                      />
                    ))}
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </section>

      {/* TESTIMONIALS SECTION */}
      <section id="depoimentos" className="py-24 border-t border-slate-900 max-w-7xl mx-auto px-6 w-full">
        <div className="max-w-xl mb-16 text-center md:text-left">
          <h2 className="text-xs uppercase font-extrabold tracking-widest text-rose-500 mb-3">
            O que dizem nossos clientes
          </h2>
          <h3 className="text-3xl sm:text-4xl font-black tracking-tight">
            Depoimentos & Experiências
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {testimonials.map((test) => (
            <div
              key={test.id}
              className="p-8 bg-slate-900/30 rounded-3xl border border-slate-900 flex flex-col justify-between relative"
            >
              <div>
                {/* Rating stars */}
                <div className="flex gap-1 text-amber-400 mb-6">
                  {Array.from({ length: test.rating }).map((_, i) => (
                    <Star key={i} size={16} fill="currentColor" />
                  ))}
                </div>
                <p className="text-sm sm:text-base text-slate-300 italic leading-relaxed mb-6">
                  "{test.testimonial}"
                </p>
              </div>

              <div className="flex items-center gap-4 border-t border-slate-800/60 pt-4 mt-2">
                <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center font-black text-slate-400 text-lg">
                  {test.photo_url ? (
                    <img
                      src={test.photo_url}
                      alt={test.name}
                      className="w-full h-full rounded-full object-cover"
                    />
                  ) : (
                    test.name.charAt(0)
                  )}
                </div>
                <div className="flex flex-col">
                  <span className="font-bold text-slate-100 text-sm">{test.name}</span>
                  <span className="text-xs text-slate-400">
                    {test.company} {test.city ? `(${test.city})` : ""}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* FAQ SECTION */}
      <section id="faq" className="py-24 border-t border-slate-900 bg-slate-950/30">
        <div className="max-w-4xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-xs uppercase font-extrabold tracking-widest text-rose-500 mb-3">
              Dúvidas frequentes
            </h2>
            <h3 className="text-3xl sm:text-4xl font-black tracking-tight">
              Central de Dúvidas (FAQ)
            </h3>
          </div>

          <div className="flex flex-col gap-4">
            {faqs.map((faq, index) => (
              <div
                key={faq.id}
                className="bg-slate-900/40 rounded-2xl border border-slate-900 overflow-hidden transition-colors"
              >
                <button
                  onClick={() =>
                    setActiveFAQIndex(activeFAQIndex === index ? null : index)
                  }
                  className="w-full px-6 py-5 flex items-center justify-between text-left font-bold text-slate-200 hover:text-rose-400"
                >
                  <span className="flex items-center gap-3">
                    <HelpCircle size={18} className="text-rose-500 shrink-0" />
                    {faq.question}
                  </span>
                  <ChevronDown
                    size={18}
                    className={`text-slate-400 transition-transform ${activeFAQIndex === index ? "rotate-180" : ""
                      }`}
                  />
                </button>

                {activeFAQIndex === index && (
                  <div className="px-6 pb-6 pt-2 text-sm text-slate-400 leading-relaxed border-t border-slate-900 animate-fade-in">
                    {faq.answer}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CONTACT / BUDGET FORM SECTION */}
      <section id="contato" className="py-24 border-t border-slate-900 max-w-7xl mx-auto px-6 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
          {/* Info Details */}
          <div>
            <h2 className="text-xs uppercase font-extrabold tracking-widest text-rose-500 mb-3">
              Estamos prontos para atender você
            </h2>
            <h3 className="text-3xl sm:text-4xl font-black tracking-tight mb-6">
              Solicite um Orçamento Sem Compromisso!
            </h3>
            <p className="text-sm sm:text-base text-slate-400 leading-relaxed mb-10">
              Preencha os campos ao lado com as informações da sua festa ou evento e nossa equipe entrará em contato em menos de 24 horas úteis com uma proposta personalizada.
            </p>

            <div className="flex flex-col gap-6">
              <div className="flex items-center gap-4">
                <div className="p-4 bg-slate-900 rounded-2xl text-rose-500">
                  <Phone size={20} />
                </div>
                <div className="flex flex-col">
                  <span className="text-xs text-slate-500 font-bold uppercase">Telefone / WhatsApp</span>
                  <span className="font-semibold text-slate-200">{settings?.contact?.phone_primary || "(11) 98765-4321"}</span>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="p-4 bg-slate-900 rounded-2xl text-rose-500">
                  <Mail size={20} />
                </div>
                <div className="flex flex-col">
                  <span className="text-xs text-slate-500 font-bold uppercase">E-mail Comercial</span>
                  <span className="font-semibold text-slate-200">{settings?.contact?.email_commercial || "contato@fantasybrinquedos.com"}</span>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="p-4 bg-slate-900 rounded-2xl text-rose-500">
                  <MapPin size={20} />
                </div>
                <div className="flex flex-col">
                  <span className="text-xs text-slate-500 font-bold uppercase">Área de Atendimento</span>
                  <span className="font-semibold text-slate-200">{settings?.contact?.business_hours || "São Paulo, ABC Paulista e Grande SP"}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Form Box */}
          <div className="bg-slate-900/30 rounded-3xl border border-slate-900 p-8 sm:p-10">
            <form onSubmit={handleContactSubmit} className="flex flex-col gap-6">
              {formFeedback && (
                <div
                  className={`p-4 rounded-xl text-sm font-semibold border ${formFeedback.type === "success"
                    ? "bg-emerald-950/20 text-emerald-400 border-emerald-900"
                    : "bg-rose-950/20 text-rose-400 border-rose-900"
                    }`}
                >
                  {formFeedback.text}
                </div>
              )}

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label htmlFor="name" className="text-xs text-slate-400 font-bold uppercase">
                    Nome Completo <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="name"
                    value={formName}
                    onChange={(e) => setFormName(e.target.value)}
                    required
                    placeholder="Ex: Maria Oliveira"
                    className="px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-sm focus:border-rose-500 focus:outline-none transition-colors"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label htmlFor="email" className="text-xs text-slate-400 font-bold uppercase">
                    E-mail <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={formEmail}
                    onChange={(e) => setFormEmail(e.target.value)}
                    required
                    placeholder="Ex: maria@exemplo.com"
                    className="px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-sm focus:border-rose-500 focus:outline-none transition-colors"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label htmlFor="phone" className="text-xs text-slate-400 font-bold uppercase">
                    Telefone / Celular
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    value={formPhone}
                    onChange={(e) => setFormPhone(e.target.value)}
                    placeholder="Ex: (11) 99999-9999"
                    className="px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-sm focus:border-rose-500 focus:outline-none transition-colors"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label htmlFor="subject" className="text-xs text-slate-400 font-bold uppercase">
                    Assunto
                  </label>
                  <input
                    type="text"
                    id="subject"
                    value={formSubject}
                    onChange={(e) => setFormSubject(e.target.value)}
                    placeholder="Ex: Orçamento aniversário"
                    className="px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-sm focus:border-rose-500 focus:outline-none transition-colors"
                  />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <label htmlFor="message" className="text-xs text-slate-400 font-bold uppercase">
                  Mensagem <span className="text-rose-500">*</span>
                </label>
                <textarea
                  id="message"
                  rows={4}
                  value={formMessage}
                  onChange={(e) => setFormMessage(e.target.value)}
                  required
                  placeholder="Conte um pouco sobre o brinquedo de interesse, a data desejada e local..."
                  className="px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-sm focus:border-rose-500 focus:outline-none transition-colors resize-none"
                />
              </div>

              <button
                type="submit"
                disabled={formSubmitting}
                className="w-full py-4 rounded-xl bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black hover:shadow-xl hover:shadow-rose-500/10 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {formSubmitting ? (
                  <>
                    <Loader2 size={18} className="animate-spin" />
                    Enviando...
                  </>
                ) : (
                  <>
                    <Send size={18} />
                    Enviar Mensagem
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="mt-auto border-t border-slate-900 bg-slate-950 py-12 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <span className="p-1 rounded bg-gradient-to-tr from-rose-500 to-amber-400 text-slate-950 font-black text-[10px]">
              🎪
            </span>
            <span className="font-bold text-slate-400 tracking-wider">
              {settings?.company?.name?.toUpperCase() || "FANTASY"} EVENTOS &copy; {new Date().getFullYear()}
            </span>
          </div>

          <div className="flex gap-6 text-slate-400">
            <a href="#sobre" className="hover:text-rose-400">Sobre</a>
            <a href="#brinquedos" className="hover:text-rose-400">Brinquedos</a>
            <a href="#eventos" className="hover:text-rose-400">Eventos</a>
            <a href="/admin/login" className="hover:text-rose-400 font-bold uppercase text-[10px] border border-slate-800 rounded px-2.5 py-1">
              CMS Painel
            </a>
          </div>
        </div>
      </footer>

      {/* DETAIL DIALOG / MODAL */}
      {selectedToy && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-2xl w-full overflow-hidden shadow-2xl relative">
            <button
              onClick={() => setSelectedToy(null)}
              className="absolute top-4 right-4 p-2 rounded-full bg-slate-950/60 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition-colors z-10"
            >
              <X size={20} />
            </button>

            {/* Toy dialog image */}
            <div className="relative h-72 w-full bg-slate-950 flex items-center justify-center text-6xl">
              {(() => {
                const imageUrl = selectedToy.cover_image_url ||
                  ((selectedToy as any).gallery_image_urls && (selectedToy as any).gallery_image_urls.length > 0 ? (selectedToy as any).gallery_image_urls[0] : null) ||
                  (selectedToy.gallery_urls && selectedToy.gallery_urls.length > 0 ? selectedToy.gallery_urls[0] : null);
                return imageUrl ? (
                  <img
                    src={imageUrl}
                    alt={selectedToy.name}
                    className="object-cover w-full h-full"
                  />
                ) : (
                  <span>🎠</span>
                );
              })()}
            </div>

            <div className="p-8">
              <span className="inline-block px-3 py-1 rounded-full bg-rose-500/10 text-rose-300 text-xs font-bold uppercase tracking-wider mb-4 border border-rose-500/10">
                {selectedToy.category}
              </span>
              <h3 className="text-2xl font-black text-slate-100 mb-2">
                {selectedToy.name}
              </h3>
              <div className="flex gap-4 text-sm text-slate-400 font-medium mb-6">
                <span>Idade sugerida: <strong className="text-slate-200">{selectedToy.min_age} a {selectedToy.max_age} anos</strong></span>
              </div>

              <p className="text-sm text-slate-400 leading-relaxed mb-8">
                {selectedToy.description}
              </p>

              <div className="flex gap-4">
                <a
                  href={`#contato`}
                  onClick={() => {
                    setFormSubject(`Orçamento: ${selectedToy.name}`);
                    setSelectedToy(null);
                  }}
                  className="flex-1 py-4 bg-gradient-to-r from-rose-500 to-amber-500 text-slate-950 font-black rounded-xl hover:shadow-xl hover:shadow-rose-500/10 transition-all text-center"
                >
                  Solicitar Orçamento Deste Brinquedo
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
