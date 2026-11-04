/**
 * LingoLearning - Global Configuration
 */

export const CONFIG = {
  APP_NAME: 'LingoLearning',
  VERSION: '1.0.0',
  DEFAULT_LANG: 'de',
  
  // Supabase Configuration (Change or configure via UI / LocalStorage)
  SUPABASE: {
    URL: localStorage.getItem('lingo_supabase_url') || 'https://xyzcompany.supabase.co',
    ANON_KEY: localStorage.getItem('lingo_supabase_key') || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
  },

  // Tatoeba API Configuration
  // Route overview: https://api.tatoeba.org/openapi#?route=overview
  TATOEBA: {
    BASE_URL: 'https://api.tatoeba.org/unstable',
    LANG_MAPPING: {
      de: 'deu',
      en: 'eng',
      vi: 'vie',
      ja: 'jpn',
      zh: 'cmn'
    }
  },

  // CEFR Levels
  CEFR_LEVELS: [
    { code: 'A1', name: 'Khởi đầu (Beginner)', color: '#10b981', desc: 'Từ vựng sinh hoạt, giới thiệu, số đếm, gia đình' },
    { code: 'A2', name: 'Cơ bản (Elementary)', color: '#06b6d4', desc: 'Mua sắm, công việc, miêu tả thói quen, đi lại' },
    { code: 'B1', name: 'Trung cấp (Intermediate)', color: '#3b82f6', desc: 'Xử lý tình huống du lịch, công việc, quan điểm' },
    { code: 'B2', name: 'Trung cao cấp (Upper-Int)', color: '#8b5cf6', desc: 'Tranh luận, bài viết chi tiết, ngữ pháp nâng cao' },
    { code: 'C1', name: 'Cao cấp (Advanced)', color: '#ec4899', desc: 'Học thuật, công việc chuyên môn, sắc thái ngôn ngữ' },
    { code: 'C2', name: 'Thành thạo (Mastery)', color: '#f59e0b', desc: 'Bản xứ, văn học, thuật ngữ phức tạp' }
  ],

  // German Genders (Color Convention)
  GENDERS: {
    der: { label: 'der (Maskulin)', article: 'der', color: 'var(--gender-der)', code: 'der' },
    die: { label: 'die (Feminin)', article: 'die', color: 'var(--gender-die)', code: 'die' },
    das: { label: 'das (Neutral)', article: 'das', color: 'var(--gender-das)', code: 'das' }
  }
};

