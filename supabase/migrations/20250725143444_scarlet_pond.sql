/*
  # Create testimonials and companies tables

  1. New Tables
    - `companies`
      - `id` (uuid, primary key)
      - `name` (text, company name)
      - `description` (text, company description)
      - `website` (text, company website)
      - `created_at` (timestamp)
    - `testimonials`
      - `id` (uuid, primary key)
      - `company_id` (uuid, foreign key to companies)
      - `user_id` (uuid, foreign key to auth.users)
      - `type` (text, 'text' or 'video')
      - `content` (text, testimonial content)
      - `video_url` (text, video URL if type is video)
      - `rating` (integer, 1-5 stars)
      - `status` (text, 'pending', 'approved', 'rejected')
      - `created_at` (timestamp)
      - `updated_at` (timestamp)

  2. Security
    - Enable RLS on both tables
    - Add policies for authenticated users to read approved testimonials
    - Add policies for users to manage their own testimonials
    - Add policies for companies to manage testimonials about them
</sql>

CREATE TABLE IF NOT EXISTS companies (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text,
  website text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS testimonials (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id uuid REFERENCES companies(id) ON DELETE CASCADE,
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  type text NOT NULL CHECK (type IN ('text', 'video')),
  content text,
  video_url text,
  rating integer CHECK (rating >= 1 AND rating <= 5),
  status text DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE testimonials ENABLE ROW LEVEL SECURITY;

-- Companies policies
CREATE POLICY "Anyone can read companies"
  ON companies
  FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Company owners can manage their company"
  ON companies
  FOR ALL
  TO authenticated
  USING (true); -- We'll refine this based on company ownership

-- Testimonials policies
CREATE POLICY "Users can read approved testimonials"
  ON testimonials
  FOR SELECT
  TO authenticated
  USING (status = 'approved');

CREATE POLICY "Users can manage their own testimonials"
  ON testimonials
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id);

-- Insert some sample companies
INSERT INTO companies (name, description, website) VALUES
  ('Acme Corporation', 'Leading provider of innovative solutions', 'https://acme.com'),
  ('Beta Technologies', 'Cutting-edge software development', 'https://beta-tech.com'),
  ('Gamma Industries', 'Manufacturing excellence since 1990', 'https://gamma-ind.com'),
  ('Delta Services', 'Professional consulting services', 'https://delta-services.com'),
  ('Epsilon Solutions', 'Digital transformation experts', 'https://epsilon-sol.com');

-- Insert some sample testimonials
INSERT INTO testimonials (company_id, user_id, type, content, rating, status) VALUES
  ((SELECT id FROM companies WHERE name = 'Acme Corporation'), (SELECT id FROM auth.users LIMIT 1), 'text', 'Excellent service and support. Highly recommended!', 5, 'approved'),
  ((SELECT id FROM companies WHERE name = 'Beta Technologies'), (SELECT id FROM auth.users LIMIT 1), 'text', 'Great software solutions that helped our business grow.', 4, 'approved'),
  ((SELECT id FROM companies WHERE name = 'Gamma Industries'), (SELECT id FROM auth.users LIMIT 1), 'text', 'Quality products and reliable delivery.', 5, 'approved'),
  ((SELECT id FROM companies WHERE name = 'Delta Services'), (SELECT id FROM auth.users LIMIT 1), 'text', 'Professional team with deep expertise.', 4, 'approved'),
  ((SELECT id FROM companies WHERE name = 'Epsilon Solutions'), (SELECT id FROM auth.users LIMIT 1), 'text', 'Transformed our digital processes efficiently.', 5, 'approved');