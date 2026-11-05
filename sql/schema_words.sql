-- ==============================================================================
-- Schema for DWDS + Kaikki + Tatoeba Integrated German Vocabulary
-- Matches Project Supabase Database (PostgreSQL 15)
-- ==============================================================================

-- 1. Words Table (Idempotent upsert by lemma + pos)
CREATE TABLE IF NOT EXISTS public.words (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lemma VARCHAR(150) NOT NULL,
    level VARCHAR(5) NOT NULL, -- 'A1', 'A2', 'B1'
    pos VARCHAR(50) NOT NULL,  -- 'noun', 'verb', 'adj', etc.
    article VARCHAR(10),       -- 'der', 'die', 'das'
    gender VARCHAR(20),        -- 'masculine', 'feminine', 'neuter'
    plural VARCHAR(150),
    ipa VARCHAR(100),
    meaning_en TEXT,
    meaning_vi TEXT,
    forms JSONB DEFAULT '[]'::jsonb,
    synonyms JSONB DEFAULT '[]'::jsonb,
    missing JSONB DEFAULT '[]'::jsonb,
    sources JSONB DEFAULT '{"level": "DWDS/Goethe", "dictionary": "Kaikki/Wiktionary", "examples": "Tatoeba"}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_words_lemma_pos UNIQUE (lemma, pos)
);

-- 2. Performance Indexes
CREATE INDEX IF NOT EXISTS idx_words_lemma ON public.words(lemma);
CREATE INDEX IF NOT EXISTS idx_words_level ON public.words(level);
CREATE INDEX IF NOT EXISTS idx_words_pos ON public.words(pos);
CREATE INDEX IF NOT EXISTS idx_words_lemma_lower ON public.words(LOWER(lemma));

-- 3. Word Examples Table (Tatoeba integration)
CREATE TABLE IF NOT EXISTS public.word_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    word_id UUID REFERENCES public.words(id) ON DELETE CASCADE,
    sentence_de TEXT NOT NULL,
    translation_vi TEXT,
    source VARCHAR(50) DEFAULT 'tatoeba',
    tatoeba_id INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_word_examples_word_id ON public.word_examples(word_id);
CREATE INDEX IF NOT EXISTS idx_word_examples_tatoeba_id ON public.word_examples(tatoeba_id);

-- 4. Row Level Security (RLS)
ALTER TABLE public.words ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.word_examples ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'words' AND policyname = 'Public read words') THEN
        CREATE POLICY "Public read words" ON public.words FOR SELECT USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'word_examples' AND policyname = 'Public read word_examples') THEN
        CREATE POLICY "Public read word_examples" ON public.word_examples FOR SELECT USING (true);
    END IF;
END $$;

