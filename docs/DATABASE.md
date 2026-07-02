Table users {
  id integer [pk, increment]
  name varchar
  email varchar [unique]
  password varchar

  created_at timestamp
  updated_at timestamp
}

Table toys {
  id integer [pk, increment]

  name varchar
  slug varchar [unique]

  short_description text
  description text

  cover_image varchar
  images json

  dimensions varchar
  recommended_age varchar
  capacity varchar

  is_featured boolean
  is_active boolean

  display_order integer

  created_at timestamp
  updated_at timestamp
}

Table events {
  id integer [pk, increment]

  title varchar
  city varchar
  client varchar

  event_date date

  description text

  cover_image varchar
  images json

  is_featured boolean
  is_active boolean

  display_order integer

  created_at timestamp
  updated_at timestamp
}

Table testimonials {
  id integer [pk, increment]

  name varchar
  city varchar
  company varchar

  photo varchar

  testimonial text

  rating integer

  is_active boolean
  display_order integer

  created_at timestamp
  updated_at timestamp
}

Table contents {
  id integer [pk, increment]

  key varchar [unique]

  title varchar
  subtitle varchar

  content text

  image varchar

  button_text varchar
  button_link varchar

  is_visible boolean

  display_order integer

  created_at timestamp
  updated_at timestamp
}

Table contact_messages {
  id integer [pk, increment]

  name varchar
  email varchar
  phone varchar
  subject varchar

  message text

  is_read boolean

  created_at timestamp
}

Table settings {
  id integer [pk, increment]

  company_name varchar

  phone varchar
  whatsapp varchar
  email varchar

  address varchar

  instagram varchar
  facebook varchar
  youtube varchar

  logo varchar
  favicon varchar

  primary_color varchar
  secondary_color varchar

  created_at timestamp
  updated_at timestamp
}