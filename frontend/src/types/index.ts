export interface User {
  id: string;
  name: string;
  email: string;
  is_active: boolean;
  role: string;
  created_at: string;
  updated_at: string;
}

export interface Toy {
  id: string;
  name: string;
  slug: string;
  category: string;
  min_age: number;
  max_age: number;
  description: string | null;
  is_featured: boolean;
  is_active: boolean;
  display_order: number;
  cover_image_id?: string | null;
  cover_image_url?: string | null;
  gallery_image_ids: string[];
  gallery_urls?: string[]; // Resolved at runtime
  created_at: string;
  updated_at: string;
}

export interface Event {
  id: string;
  title: string;
  city: string;
  client: string;
  event_date: string;
  description: string | null;
  is_featured: boolean;
  is_active: boolean;
  display_order: number;
  cover_image_id: string | null;
  cover_image_url?: string | null; // Resolved at runtime
  gallery_image_ids: string[];
  gallery_urls?: string[]; // Resolved at runtime
  created_at: string;
  updated_at: string;
}

export interface Testimonial {
  id: string;
  name: string;
  city: string | null;
  company: string | null;
  testimonial: string;
  rating: number;
  is_active: boolean;
  display_order: number;
  photo_id: string | null;
  photo_url?: string | null; // Resolved at runtime
  created_at: string;
  updated_at: string;
}

export interface FAQ {
  id: string;
  question: string;
  answer: string;
  is_active: boolean;
  display_order: number;
  created_at: string;
  updated_at: string;
}

export interface ContactMessage {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  subject: string | null;
  message: string;
  is_read: boolean;
  created_at: string;
}

export interface HeroConfig {
  tag: string | null;
  title: string | null;
  subtitle: string | null;
  text: string | null;
  primary_button: string | null;
  primary_link: string | null;
  secondary_button: string | null;
  secondary_link: string | null;
  background_image: string | null;
  background_video: string | null;
  carousel_images: string[];
  carousel_transition: number;
  safety_cards: Array<{
    id: string;
    title: string;
    description: string;
    icon: string;
  }>;
  bg_color: string | null;
}

export interface DashboardStats {
  total_toys: number;
  active_toys: number;
  total_events: number;
  active_events: number;
  total_testimonials: number;
  active_testimonials: number;
  total_faqs: number;
  active_faqs: number;
  total_contacts: number;
  unread_contacts: number;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    name: string;
    email: string;
  };
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
}

export interface ApiPaginatedResponse<T> {
  success: boolean;
  data: {
    items: T[];
    total: number;
    page: number;
    per_page: number;
    pages: number;
  };
  message: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface UploadResponse {
  id: string;
  public_url: string;
  original_filename: string;
  stored_filename: string;
  file_path: string;
  file_size: number;
  mime_type: string;
  extension: string;
}

