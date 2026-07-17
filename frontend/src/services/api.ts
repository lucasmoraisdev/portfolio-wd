import {
  Toy,
  Event,
  Testimonial,
  FAQ,
  ContactMessage,
  HeroConfig,
  DashboardStats,
  LoginResponse,
  LoginRequest,
  UploadResponse,
  ApiResponse,
  ApiPaginatedResponse,
} from "../types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

// Retrieve token on client side
const getToken = (): string | null => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("token");
  }
  return null;
};

// Set token
export const setToken = (token: string | null) => {
  if (typeof window !== "undefined") {
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }
};

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers = new Headers(options.headers || {});

  if (token && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const config: RequestInit = {
    ...options,
    headers,
  };
  console.log(`Config: $${config}`);
  console.log(`Headers: $${headers}`);
  console.log(`Options: $${options}`);
  console.log("URL: ", `${API_BASE_URL}${endpoint}`, config);
  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
  console.log("Response: ", response);
  if (response.status === 401) {
    // Unauthorized: token might be expired. Clean up token.
    setToken(null);
    if (typeof window !== "undefined" && window.location.pathname.startsWith("/admin") && window.location.pathname !== "/admin/login") {
      window.location.href = "/admin/login";
    }
  }

  if (!response.ok) {
    let errorMsg = `HTTP Error ${response.status}`;
    try {
      const errJson = await response.json();
      errorMsg = errJson.message || errJson.detail || errorMsg;
    } catch {
      // Ignored
    }
    throw new Error(errorMsg);
  }

  return response.json() as Promise<T>;
}

export const api = {
  // 1. Auth Module
  auth: {
    login: async (payload: LoginRequest): Promise<ApiResponse<LoginResponse>> => {
      return request<ApiResponse<LoginResponse>>("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    me: async (): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>("/auth/me");
    },
  },

  // 2. Upload Module
  upload: {
    file: async (file: File): Promise<ApiResponse<UploadResponse>> => {
      const formData = new FormData();
      formData.append("file", file);
      return request<ApiResponse<UploadResponse>>("/uploads", {
        method: "POST",
        body: formData,
      });
    },
    files: async (files: File[]): Promise<ApiResponse<UploadResponse[]>> => {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("files", file);
      });
      return request<ApiResponse<UploadResponse[]>>("/uploads", {
        method: "POST",
        body: formData,
      });
    },
    delete: async (id: string): Promise<ApiResponse<UploadResponse>> => {
      return request<ApiResponse<UploadResponse>>(`/uploads/${id}`, {
        method: "DELETE",
      });
    },
  },

  // 3. Settings & Hero Module
  settings: {
    getPublic: async (): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>("/settings/public");
    },
    getAdmin: async (): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>("/settings");
    },
    updateBulk: async (settingsPayload: Record<string, any>): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/settings`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ settings: settingsPayload }),
      });
    },
    uploadLogo: async (file: File): Promise<ApiResponse<any>> => {
      const formData = new FormData();
      formData.append("file", file);
      return request<ApiResponse<any>>("/settings/logo?logo_type=main", {
        method: "POST",
        body: formData,
      });
    },
  },
  hero: {
    getPublic: async (): Promise<ApiResponse<HeroConfig>> => {
      return request<ApiResponse<HeroConfig>>("/hero/public");
    },
    getAdmin: async (): Promise<ApiResponse<HeroConfig>> => {
      return request<ApiResponse<HeroConfig>>("/hero");
    },
    update: async (payload: Partial<HeroConfig>): Promise<ApiResponse<HeroConfig>> => {
      return request<ApiResponse<HeroConfig>>("/hero", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
  },

  // 4. Toys Module
  toys: {
    listPublic: async (params?: Record<string, any>): Promise<ApiPaginatedResponse<Toy>> => {
      const search = params ? new URLSearchParams(params).toString() : "";
      return request<ApiPaginatedResponse<Toy>>(`/toys/public?${search}`);
    },
    listAdmin: async (params?: Record<string, any>): Promise<ApiPaginatedResponse<Toy>> => {
      const search = params ? new URLSearchParams(params).toString() : "";
      return request<ApiPaginatedResponse<Toy>>(`/toys?${search}`);
    },
    getPublicDetail: async (slug: string): Promise<ApiResponse<Toy>> => {
      return request<ApiResponse<Toy>>(`/toys/public/${slug}`);
    },
    getAdminDetail: async (id: string): Promise<ApiResponse<Toy>> => {
      return request<ApiResponse<Toy>>(`/toys/${id}`);
    },
    create: async (payload: Partial<Toy>): Promise<ApiResponse<Toy>> => {
      return request<ApiResponse<Toy>>("/toys", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    update: async (id: string, payload: Partial<Toy>): Promise<ApiResponse<Toy>> => {
      return request<ApiResponse<Toy>>(`/toys/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    delete: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/toys/${id}`, { method: "DELETE" });
    },
    toggleStatus: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/toys/${id}/status`, { method: "PATCH" });
    },
    toggleFeatured: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/toys/${id}/featured`, { method: "PATCH" });
    },
    updatePosition: async (id: string, position: number): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/toys/${id}/position?new_order=${position}`, {
        method: "PATCH",
      });
    },
  },

  // 5. Events Module
  events: {
    listPublic: async (params?: Record<string, any>): Promise<ApiPaginatedResponse<Event>> => {
      const search = params ? new URLSearchParams(params).toString() : "";
      return request<ApiPaginatedResponse<Event>>(`/events/public/events?${search}`);
    },
    listFeatured: async (limit = 10): Promise<ApiResponse<Event[]>> => {
      return request<ApiResponse<Event[]>>(`/events/public/events/featured?limit=${limit}`);
    },
    listAdmin: async (params?: Record<string, any>): Promise<ApiPaginatedResponse<Event>> => {
      const search = params ? new URLSearchParams(params).toString() : "";
      return request<ApiPaginatedResponse<Event>>(`/events?${search}`);
    },
    getPublicDetail: async (id: string): Promise<ApiResponse<Event>> => {
      return request<ApiResponse<Event>>(`/events/public/events/${id}`);
    },
    getAdminDetail: async (id: string): Promise<ApiResponse<Event>> => {
      return request<ApiResponse<Event>>(`/events/${id}`);
    },
    create: async (payload: Partial<Event>): Promise<ApiResponse<Event>> => {
      return request<ApiResponse<Event>>("/events", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    update: async (id: string, payload: Partial<Event>): Promise<ApiResponse<Event>> => {
      return request<ApiResponse<Event>>(`/events/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    delete: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/events/${id}`, { method: "DELETE" });
    },
    toggleStatus: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/events/${id}/status`, { method: "PATCH" });
    },
    toggleFeatured: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/events/${id}/featured`, { method: "PATCH" });
    },
    updatePosition: async (id: string, position: number): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/events/${id}/position?new_order=${position}`, {
        method: "PATCH",
      });
    },
  },

  // 6. Testimonials Module
  testimonials: {
    listPublic: async (params?: Record<string, any>): Promise<ApiPaginatedResponse<Testimonial>> => {
      const search = params ? new URLSearchParams(params).toString() : "";
      return request<ApiPaginatedResponse<Testimonial>>(`/testimonials/public/testimonials?${search}`);
    },
    listAdmin: async (params?: Record<string, any>): Promise<ApiPaginatedResponse<Testimonial>> => {
      const search = params ? new URLSearchParams(params).toString() : "";
      return request<ApiPaginatedResponse<Testimonial>>(`/testimonials?${search}`);
    },
    getAdminDetail: async (id: string): Promise<ApiResponse<Testimonial>> => {
      return request<ApiResponse<Testimonial>>(`/testimonials/${id}`);
    },
    create: async (payload: Partial<Testimonial>): Promise<ApiResponse<Testimonial>> => {
      return request<ApiResponse<Testimonial>>("/testimonials", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    update: async (id: string, payload: Partial<Testimonial>): Promise<ApiResponse<Testimonial>> => {
      return request<ApiResponse<Testimonial>>(`/testimonials/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    delete: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/testimonials/${id}`, { method: "DELETE" });
    },
    toggleStatus: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/testimonials/${id}/status`, { method: "PATCH" });
    },
    updatePosition: async (id: string, position: number): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/testimonials/${id}/position?new_order=${position}`, {
        method: "PATCH",
      });
    },
  },

  // 7. FAQ Module
  faq: {
    listPublic: async (params?: Record<string, any>): Promise<ApiPaginatedResponse<FAQ>> => {
      const search = params ? new URLSearchParams(params).toString() : "";
      return request<ApiPaginatedResponse<FAQ>>(`/faq/public/faqs?${search}`);
    },
    listAdmin: async (params?: Record<string, any>): Promise<ApiPaginatedResponse<FAQ>> => {
      const search = params ? new URLSearchParams(params).toString() : "";
      return request<ApiPaginatedResponse<FAQ>>(`/faq?${search}`);
    },
    getAdminDetail: async (id: string): Promise<ApiResponse<FAQ>> => {
      return request<ApiResponse<FAQ>>(`/faq/${id}`);
    },
    create: async (payload: Partial<FAQ>): Promise<ApiResponse<FAQ>> => {
      return request<ApiResponse<FAQ>>("/faq", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    update: async (id: string, payload: Partial<FAQ>): Promise<ApiResponse<FAQ>> => {
      return request<ApiResponse<FAQ>>(`/faq/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    delete: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/faq/${id}`, { method: "DELETE" });
    },
    toggleStatus: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/faq/${id}/status`, { method: "PATCH" });
    },
    updatePosition: async (id: string, position: number): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/faq/${id}/position?new_order=${position}`, {
        method: "PATCH",
      });
    },
  },

  // 8. Contact Module
  contacts: {
    submit: async (payload: {
      name: string;
      email: string;
      phone?: string;
      subject?: string;
      message: string;
    }): Promise<ApiResponse<ContactMessage>> => {
      return request<ApiResponse<ContactMessage>>("/contacts/public", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    },
    listAdmin: async (params?: Record<string, any>): Promise<ApiPaginatedResponse<ContactMessage>> => {
      const search = params ? new URLSearchParams(params).toString() : "";
      return request<ApiPaginatedResponse<ContactMessage>>(`/contacts?${search}`);
    },
    getAdminDetail: async (id: string): Promise<ApiResponse<ContactMessage>> => {
      return request<ApiResponse<ContactMessage>>(`/contacts/${id}`);
    },
    markRead: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/contacts/${id}/read`, { method: "PATCH" });
    },
    delete: async (id: string): Promise<ApiResponse<any>> => {
      return request<ApiResponse<any>>(`/contacts/${id}`, { method: "DELETE" });
    },
  },

  // 9. Dashboard Module
  dashboard: {
    stats: async (): Promise<ApiResponse<DashboardStats>> => {
      return request<ApiResponse<DashboardStats>>("/dashboard");
    },
  },
};
export default api;
