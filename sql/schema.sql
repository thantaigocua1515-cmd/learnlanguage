-- ==============================================================================
-- LINGOLEN - Multi-Language Learning Platform (Database Schema for Supabase)
-- Target: German ('de') with full CEFR A1-C2, expandable to 'en', 'ja', 'zh'
-- ==============================================================================

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. ENUM TYPES
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('student', 'teacher', 'admin', 'superadmin');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE german_gender AS ENUM ('der', 'die', 'das');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. LANGUAGES TABLE
CREATE TABLE IF NOT EXISTS public.languages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(10) UNIQUE NOT NULL, -- 'de', 'en', 'ja', 'zh'
    name VARCHAR(50) NOT NULL,
    native_name VARCHAR(50) NOT NULL,
    flag_emoji VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. CEFR LEVELS TABLE (A1 -> C2)
CREATE TABLE IF NOT EXISTS public.cefr_levels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(5) UNIQUE NOT NULL, -- 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'
    name VARCHAR(50) NOT NULL,
    description TEXT,
    order_index INT NOT NULL,
    badge_color VARCHAR(20) DEFAULT '#2563eb'
);

-- 5. TOPICS / LESSONS TABLE
CREATE TABLE IF NOT EXISTS public.topics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_id UUID REFERENCES public.languages(id) ON DELETE CASCADE,
    cefr_level_id UUID REFERENCES public.cefr_levels(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    icon_name VARCHAR(50) DEFAULT 'bi-bookmark-star',
    order_index INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. VOCABULARY TABLE (Optimized for German: Gender, Plural, IPA, Sound)
CREATE TABLE IF NOT EXISTS public.vocabulary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language_id UUID REFERENCES public.languages(id) ON DELETE CASCADE,
    cefr_level_id UUID REFERENCES public.cefr_levels(id) ON DELETE SET NULL,
    topic_id UUID REFERENCES public.topics(id) ON DELETE SET NULL,
    word VARCHAR(150) NOT NULL,
    ipa VARCHAR(100),
    pos VARCHAR(50), -- Noun, Verb, Adjective, Adverb, Preposition, etc.
    gender german_gender, -- 'der', 'die', 'das' (null if not noun or non-German)
    plural_form VARCHAR(150), -- e.g. "die Äpfel", "die Tische"
    meaning_vi TEXT NOT NULL,
    meaning_en TEXT,
    audio_url TEXT,
    example_de TEXT,
    example_vi TEXT,
    metadata JSONB DEFAULT '{}'::jsonb, -- Dành cho Kanji, Pinyin sau này
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. SENTENCES TABLE (Integrated with Tatoeba API schema)
CREATE TABLE IF NOT EXISTS public.sentences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tatoeba_id INT UNIQUE, -- ID từ tatoeba.org
    language_id UUID REFERENCES public.languages(id) ON DELETE CASCADE,
    cefr_level_id UUID REFERENCES public.cefr_levels(id) ON DELETE SET NULL,
    text TEXT NOT NULL,
    translation_vi TEXT,
    translation_en TEXT,
    audio_url TEXT,
    author VARCHAR(100),
    license VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. JUNCTION TABLE: VOCABULARY <-> SENTENCES
CREATE TABLE IF NOT EXISTS public.vocab_sentences (
    vocab_id UUID REFERENCES public.vocabulary(id) ON DELETE CASCADE,
    sentence_id UUID REFERENCES public.sentences(id) ON DELETE CASCADE,
    PRIMARY KEY (vocab_id, sentence_id)
);

-- 9. USER PROFILES TABLE (Linked with Supabase Auth)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    avatar_url TEXT,
    role user_role DEFAULT 'student',
    current_language_code VARCHAR(10) DEFAULT 'de',
    xp_points INT DEFAULT 0,
    current_streak INT DEFAULT 0,
    longest_streak INT DEFAULT 0,
    hearts INT DEFAULT 5,
    last_active_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. SPACED REPETITION (SRS) & LEARNING PROGRESS
CREATE TABLE IF NOT EXISTS public.user_word_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    vocab_id UUID REFERENCES public.vocabulary(id) ON DELETE CASCADE,
    repetition_count INT DEFAULT 0,
    interval_days INT DEFAULT 0,
    ease_factor NUMERIC(4,2) DEFAULT 2.50, -- SM-2 algorithm
    next_review_at TIMESTAMPTZ DEFAULT NOW(),
    last_quality_score INT DEFAULT 0, -- 0-5
    is_mastered BOOLEAN DEFAULT false,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, vocab_id)
);

-- 11. GAME SESSIONS & ANALYTICS
CREATE TABLE IF NOT EXISTS public.game_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    game_type VARCHAR(50) NOT NULL, -- 'article_sorter', 'word_scramble', 'cloze_sentence', 'flashcards'
    score INT NOT NULL DEFAULT 0,
    xp_earned INT NOT NULL DEFAULT 0,
    accuracy NUMERIC(5,2) DEFAULT 100.0,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ==============================================================================
ALTER TABLE public.languages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cefr_levels ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vocabulary ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sentences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vocab_sentences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_word_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;

-- Read policies: Content is publicly readable
CREATE POLICY "Public read languages" ON public.languages FOR SELECT USING (true);
CREATE POLICY "Public read cefr_levels" ON public.cefr_levels FOR SELECT USING (true);
CREATE POLICY "Public read topics" ON public.topics FOR SELECT USING (true);
CREATE POLICY "Public read vocabulary" ON public.vocabulary FOR SELECT USING (true);
CREATE POLICY "Public read sentences" ON public.sentences FOR SELECT USING (true);
CREATE POLICY "Public read vocab_sentences" ON public.vocab_sentences FOR SELECT USING (true);

-- User Profiles policies
CREATE POLICY "Users view own profile or public profile" ON public.profiles FOR SELECT USING (true);
CREATE POLICY "Users update own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id);

-- User Progress policies
CREATE POLICY "Users can manage own progress" ON public.user_word_progress FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can manage own game sessions" ON public.game_sessions FOR ALL USING (auth.uid() = user_id);

-- Admin policies (Admins have full write access to content)
CREATE POLICY "Admin write languages" ON public.languages FOR ALL USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'superadmin'))
);
CREATE POLICY "Admin write cefr_levels" ON public.cefr_levels FOR ALL USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'superadmin'))
);
CREATE POLICY "Admin write topics" ON public.topics FOR ALL USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'superadmin'))
);
CREATE POLICY "Admin write vocabulary" ON public.vocabulary FOR ALL USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'superadmin'))
);
CREATE POLICY "Admin write sentences" ON public.sentences FOR ALL USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'superadmin'))
);

-- ==============================================================================
-- SEED INITIAL DATA (German A1-C2, Topics, Core Vocabulary)
-- ==============================================================================
INSERT INTO public.languages (code, name, native_name, flag_emoji, is_active)
VALUES
    ('de', 'German', 'Deutsch', '🇩🇪', true),
    ('en', 'English', 'English', '🇬🇧', true),
    ('ja', 'Japanese', '日本語', '🇯🇵', true),
    ('zh', 'Chinese', '中文', '🇨🇳', true)
ON CONFLICT (code) DO NOTHING;

INSERT INTO public.cefr_levels (code, name, description, order_index, badge_color)
VALUES
    ('A1', 'Khởi đầu (Beginner)', 'Giao tiếp cơ bản, chào hỏi, từ vựng đời sống thường nhật', 1, '#10b981'),
    ('A2', 'Cơ bản (Elementary)', 'Miêu tả bản thân, thói quen, mua sắm, môi trường xung quanh', 2, '#06b6d4'),
    ('B1', 'Trung cấp (Intermediate)', 'Tự tin xử lý tình huống du lịch, diễn đạt suy nghĩ, dự định', 3, '#3b82f6'),
    ('B2', 'Trung cao cấp (Upper-Int)', 'Hiểu văn bản phức tạp, tranh luận và trình bày quan điểm trôi chảy', 4, '#8b5cf6'),
    ('C1', 'Cao cấp (Advanced)', 'Sử dụng linh hoạt trong học thuật, công việc chuyên môn sâu', 5, '#ec4899'),
    ('C2', 'Thành thạo (Mastery)', 'Gần như người bản xứ, thấu hiểu ngữ cảnh văn hóa tinh tế', 6, '#f59e0b')
ON CONFLICT (code) DO NOTHING;

-- Trigger automatically create profile when new auth user signs up
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, avatar_url, role)
    VALUES (
        new.id,
        new.email,
        COALESCE(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1)),
        COALESCE(new.raw_user_meta_data->>'avatar_url', ''),
        'student'
    );
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

