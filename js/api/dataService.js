/**
 * LingoLearning - Central Data Service
 * Interacts with Supabase PostgreSQL or falls back to local seed data
 */

import { CONFIG } from '../config.js';
import { supabaseManager } from '../supabaseClient.js';

const SEED_VOCABULARY = [
  // A1 Level
  {
    id: 'v-a1-01',
    word: 'Apfel',
    gender: 'der',
    plural_form: 'die Äpfel',
    ipa: '/ˈapfl̩/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Quả táo',
    meaning_en: 'Apple',
    example_de: 'Der Apfel ist rot und schmeckt süß.',
    example_vi: 'Quả táo màu đỏ và có vị ngọt.',
    audio_url: null
  },
  {
    id: 'v-a1-02',
    word: 'Katze',
    gender: 'die',
    plural_form: 'die Katzen',
    ipa: '/ˈkat͡sə/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Con mèo',
    meaning_en: 'Cat',
    example_de: 'Die Katze schläft auf dem Sofa.',
    example_vi: 'Con mèo đang ngủ trên ghế sô-pha.',
    audio_url: null
  },
  {
    id: 'v-a1-03',
    word: 'Buch',
    gender: 'das',
    plural_form: 'die Bücher',
    ipa: '/buːx/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Quyển sách',
    meaning_en: 'Book',
    example_de: 'Das Buch ist sehr interessant.',
    example_vi: 'Cuốn sách này rất thú vị.',
    audio_url: null
  },
  {
    id: 'v-a1-04',
    word: 'Hund',
    gender: 'der',
    plural_form: 'die Hunde',
    ipa: '/hʊnt/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Con chó',
    meaning_en: 'Dog',
    example_de: 'Der Hund spielt im Garten.',
    example_vi: 'Chú chó đang chơi trong vườn.',
    audio_url: null
  },
  {
    id: 'v-a1-05',
    word: 'Sonne',
    gender: 'die',
    plural_form: 'die Sonnen',
    ipa: '/ˈzɔnə/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Mặt trời',
    meaning_en: 'Sun',
    example_de: 'Die Sonne scheint heute sehr warm.',
    example_vi: 'Mặt trời hôm nay chiếu sáng rất ấm áp.',
    audio_url: null
  },
  {
    id: 'v-a1-06',
    word: 'Wasser',
    gender: 'das',
    plural_form: 'die Wässer',
    ipa: '/ˈvasɐ/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Nước',
    meaning_en: 'Water',
    example_de: 'Ich trinke gerne kaltes Wasser.',
    example_vi: 'Tôi thích uống nước lạnh.',
    audio_url: null
  },
  {
    id: 'v-a1-07',
    word: 'Tisch',
    gender: 'der',
    plural_form: 'die Tische',
    ipa: '/tɪʃ/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Cái bàn',
    meaning_en: 'Table',
    example_de: 'Der Tisch ist aus braunem Holz.',
    example_vi: 'Chiếc bàn được làm bằng gỗ nâu.',
    audio_url: null
  },
  {
    id: 'v-a1-08',
    word: 'Blume',
    gender: 'die',
    plural_form: 'die Blumen',
    ipa: '/ˈbluːmə/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Bông hoa',
    meaning_en: 'Flower',
    example_de: 'Die Blume duftet wunderbar.',
    example_vi: 'Bông hoa tỏa hương thơm ngát.',
    audio_url: null
  },
  {
    id: 'v-a1-09',
    word: 'Haus',
    gender: 'das',
    plural_form: 'die Häuser',
    ipa: '/haʊ̯s/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Ngôi nhà',
    meaning_en: 'House',
    example_de: 'Das Haus hat einen schönen Garten.',
    example_vi: 'Ngôi nhà có một khu vườn xinh đẹp.',
    audio_url: null
  },
  {
    id: 'v-a1-10',
    word: 'Kaffee',
    gender: 'der',
    plural_form: 'die Kaffees',
    ipa: '/ˈkafe/',
    pos: 'Noun',
    cefr_level: 'A1',
    meaning_vi: 'Cà phê',
    meaning_en: 'Coffee',
    example_de: 'Der Kaffee schmeckt hervorragend.',
    example_vi: 'Cà phê có hương vị tuyệt hảo.',
    audio_url: null
  },

  // A2 Level
  {
    id: 'v-a2-01',
    word: 'Bahnhof',
    gender: 'der',
    plural_form: 'die Bahnhöfe',
    ipa: '/ˈbaːnˌhoːf/',
    pos: 'Noun',
    cefr_level: 'A2',
    meaning_vi: 'Nhà ga tàu hỏa',
    meaning_en: 'Train station',
    example_de: 'Wir treffen uns am Bahnhof.',
    example_vi: 'Chúng ta sẽ gặp nhau ở nhà ga tàu.',
    audio_url: null
  },
  {
    id: 'v-a2-02',
    word: 'Zeitung',
    gender: 'die',
    plural_form: 'die Zeitungen',
    ipa: '/ˈt͡saɪ̯tʊŋ/',
    pos: 'Noun',
    cefr_level: 'A2',
    meaning_vi: 'Tờ báo',
    meaning_en: 'Newspaper',
    example_de: 'Er liest jeden Morgen die Zeitung.',
    example_vi: 'Anh ấy đọc báo mỗi buổi sáng.',
    audio_url: null
  },
  {
    id: 'v-a2-03',
    word: 'Flugzeug',
    gender: 'das',
    plural_form: 'die Flugzeuge',
    ipa: '/ˈfluːkˌt͡sɔɪ̯k/',
    pos: 'Noun',
    cefr_level: 'A2',
    meaning_vi: 'Máy bay',
    meaning_en: 'Airplane',
    example_de: 'Das Flugzeug landet in Berlin.',
    example_vi: 'Chiếc máy bay hạ cánh ở Berlin.',
    audio_url: null
  },

  // B1 Level
  {
    id: 'v-b1-01',
    word: 'Unterschied',
    gender: 'der',
    plural_form: 'die Unterschiede',
    ipa: '/ˈʊntɐˌʃiːt/',
    pos: 'Noun',
    cefr_level: 'B1',
    meaning_vi: 'Sự khác biệt',
    meaning_en: 'Difference',
    example_de: 'Es gibt einen großen Unterschied.',
    example_vi: 'Có một sự khác biệt rất lớn.',
    audio_url: null
  },
  {
    id: 'v-b1-02',
    word: 'Erfahrung',
    gender: 'die',
    plural_form: 'die Erfahrungen',
    ipa: '/ɛɐ̯ˈfaːʁʊŋ/',
    pos: 'Noun',
    cefr_level: 'B1',
    meaning_vi: 'Kinh nghiệm, trải nghiệm',
    meaning_en: 'Experience',
    example_de: 'Das war eine wertvolle Erfahrung.',
    example_vi: 'Đó là một trải nghiệm quý báu.',
    audio_url: null
  },
  {
    id: 'v-b1-03',
    word: 'Ergebnis',
    gender: 'das',
    plural_form: 'die Ergebnisse',
    ipa: '/ɛɐ̯ˈɡeːpnɪs/',
    pos: 'Noun',
    cefr_level: 'B1',
    meaning_vi: 'Kết quả',
    meaning_en: 'Result',
    example_de: 'Das Ergebnis der Prüfung war positiv.',
    example_vi: 'Kết quả bài kiểm tra rất khả quan.',
    audio_url: null
  },

  // B2 Level
  {
    id: 'v-b2-01',
    word: 'Zusammenhang',
    gender: 'der',
    plural_form: 'die Zusammenhänge',
    ipa: '/t͡suˈzamənˌhaŋ/',
    pos: 'Noun',
    cefr_level: 'B2',
    meaning_vi: 'Mối liên hệ, ngữ cảnh',
    meaning_en: 'Context / Correlation',
    example_de: 'In diesem Zusammenhang müssen wir handeln.',
    example_vi: 'Trong mối tương quan này, chúng ta cần hành động.',
    audio_url: null
  },
  {
    id: 'v-b2-02',
    word: 'Verantwortung',
    gender: 'die',
    plural_form: 'die Verantwortungen',
    ipa: '/fɛɐ̯ˈʔantvɔʁtʊŋ/',
    pos: 'Noun',
    cefr_level: 'B2',
    meaning_vi: 'Trách nhiệm',
    meaning_en: 'Responsibility',
    example_de: 'Wir tragen die Verantwortung für die Natur.',
    example_vi: 'Chúng ta gánh vác trách nhiệm đối với thiên nhiên.',
    audio_url: null
  },

  // C1 Level
  {
    id: 'v-c1-01',
    word: 'Widerspruch',
    gender: 'der',
    plural_form: 'die Widersprüche',
    ipa: '/ˈviːdɐˌʃpʁʊx/',
    pos: 'Noun',
    cefr_level: 'C1',
    meaning_vi: 'Sự mâu thuẫn, phản bác',
    meaning_en: 'Contradiction',
    example_de: 'Seine Aussage steht im Widerspruch zu den Fakten.',
    example_vi: 'Phát biểu của anh ấy mâu thuẫn với sự thật.',
    audio_url: null
  },

  // C2 Level
  {
    id: 'v-c2-01',
    word: 'Weltanschauung',
    gender: 'die',
    plural_form: 'die Weltanschauungen',
    ipa: '/ˈvɛltʔanˌʃaʊ̯ʊŋ/',
    pos: 'Noun',
    cefr_level: 'C2',
    meaning_vi: 'Thế giới quan',
    meaning_en: 'Worldview / Philosophy',
    example_de: 'Seine Weltanschauung prägte sein Lebenswerk.',
    example_vi: 'Thế giới quan của ông đã định hình sự nghiệp đời mình.',
    audio_url: null
  }
];

class DataService {
  constructor() {
    this.storageKey = 'lingo_vocabulary_v1';
    this.sentencesKey = 'lingo_sentences_v1';
    this.initStorage();
  }

  initStorage() {
    if (!localStorage.getItem(this.storageKey)) {
      localStorage.setItem(this.storageKey, JSON.stringify(SEED_VOCABULARY));
    }
    if (!localStorage.getItem(this.sentencesKey)) {
      localStorage.setItem(this.sentencesKey, JSON.stringify([]));
    }
  }

  /**
   * Get all vocabulary with optional filters
   */
  async getVocabulary({ level = null, gender = null, search = '' } = {}) {
    // If Supabase is connected, query database
    if (supabaseManager.isConnected && supabaseManager.client) {
      try {
        let query = supabaseManager.client.from('vocabulary').select('*');
        if (level && level !== 'ALL') query = query.eq('cefr_level', level);
        if (gender && gender !== 'ALL') query = query.eq('gender', gender);
        if (search) query = query.ilike('word', `%${search}%`);
        const { data, error } = await query;
        if (!error && data && data.length > 0) return data;
      } catch (e) {
        console.warn('Fallback to local DB store', e);
      }
    }

    // Fallback Local Storage
    let list = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    if (level && level !== 'ALL') {
      list = list.filter(v => v.cefr_level === level);
    }
    if (gender && gender !== 'ALL') {
      list = list.filter(v => v.gender === gender);
    }
    if (search) {
      const q = search.toLowerCase();
      list = list.filter(v => v.word.toLowerCase().includes(q) || v.meaning_vi.toLowerCase().includes(q));
    }
    return list;
  }

  /**
   * Add or update vocabulary
   */
  async saveVocabulary(item) {
    if (!item.id) {
      item.id = 'v-' + Date.now();
    }

    // Try Supabase first
    if (supabaseManager.isConnected && supabaseManager.client) {
      try {
        await supabaseManager.client.from('vocabulary').upsert(item);
      } catch (err) {
        console.warn('Failed saving to Supabase', err);
      }
    }

    // Save to local storage
    const list = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    const existingIndex = list.findIndex(v => v.id === item.id);
    if (existingIndex >= 0) {
      list[existingIndex] = { ...list[existingIndex], ...item };
    } else {
      list.unshift(item);
    }
    localStorage.setItem(this.storageKey, JSON.stringify(list));
    return item;
  }

  /**
   * Delete vocabulary
   */
  async deleteVocabulary(id) {
    if (supabaseManager.isConnected && supabaseManager.client) {
      try {
        await supabaseManager.client.from('vocabulary').delete().eq('id', id);
      } catch (err) {
        console.warn('Supabase delete error', err);
      }
    }

    let list = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    list = list.filter(v => v.id !== id);
    localStorage.setItem(this.storageKey, JSON.stringify(list));
  }

  /**
   * Save imported Tatoeba sentences
   */
  async saveTatoebaSentences(sentences, cefrLevel = 'A1') {
    const stored = JSON.parse(localStorage.getItem(this.sentencesKey) || '[]');
    let addedCount = 0;

    for (const s of sentences) {
      const exists = stored.some(item => item.tatoebaId === s.tatoebaId);
      if (!exists) {
        stored.unshift({ ...s, cefrLevel, importedAt: new Date().toISOString() });
        addedCount++;
      }
    }

    localStorage.setItem(this.sentencesKey, JSON.stringify(stored));
    return addedCount;
  }

  /**
   * Get all imported sentences
   */
  async getSentences() {
    return JSON.parse(localStorage.getItem(this.sentencesKey) || '[]');
  }

  /**
   * Aggregate stats for SaaS AdminCP
   */
  async getAdminStats() {
    const vocab = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    const sentences = JSON.parse(localStorage.getItem(this.sentencesKey) || '[]');

    const byLevel = { A1: 0, A2: 0, B1: 0, B2: 0, C1: 0, C2: 0 };
    const byGender = { der: 0, die: 0, das: 0 };

    vocab.forEach(v => {
      if (byLevel[v.cefr_level] !== undefined) byLevel[v.cefr_level]++;
      if (byGender[v.gender] !== undefined) byGender[v.gender]++;
    });

    return {
      totalWords: vocab.length,
      totalSentences: sentences.length,
      byLevel,
      byGender
    };
  }
}

export const dataService = new DataService();

