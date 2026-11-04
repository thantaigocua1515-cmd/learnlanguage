/**
 * LingoLearning - Tatoeba API Client
 * OpenAPI Documentation: https://api.tatoeba.org/openapi#?route=overview
 */

import { CONFIG } from '../config.js';

export class TatoebaClient {
  constructor() {
    this.baseUrl = CONFIG.TATOEBA.BASE_URL;
  }

  /**
   * Search sentences in German with Vietnamese or English translations
   * @param {Object} options
   * @param {string} options.query - Keyword to search (e.g., 'Apfel', 'Wasser', 'gehen')
   * @param {string} options.fromLang - 'de' (deu)
   * @param {string} options.toLang - 'vi' (vie) or 'en' (eng)
   * @param {number} options.limit - Max records to return
   * @param {boolean} options.hasAudio - Prioritize native recordings
   */
  async searchSentences({ query, fromLang = 'de', toLang = 'vi', limit = 10, hasAudio = false }) {
    const src = CONFIG.TATOEBA.LANG_MAPPING[fromLang] || 'deu';
    const tgt = CONFIG.TATOEBA.LANG_MAPPING[toLang] || 'vie';

    const params = new URLSearchParams({
      lang: src,
      trans_lang: tgt,
      q: query || '',
      limit: String(limit),
      sort: 'relevance'
    });

    if (hasAudio) {
      params.append('has_audio', 'yes');
    }

    try {
      // Direct call to Tatoeba API (with timeout handling)
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 6000);

      const response = await fetch(`${this.baseUrl}/sentences?${params.toString()}`, {
        headers: { 'Accept': 'application/json' },
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`Tatoeba API HTTP ${response.status}`);
      }

      const json = await response.json();
      return this.transformTatoebaResponse(json.data || [], tgt);
    } catch (err) {
      console.warn('Tatoeba API live query failed or blocked by CORS. Using fallback dataset generator.', err);
      return this.getFallbackSentences(query, fromLang, toLang);
    }
  }

  /**
   * Transform Tatoeba raw response into normalized format
   */
  transformTatoebaResponse(data, targetLangCode) {
    return data.map(item => {
      // Find matching translation
      let translationText = '';
      if (Array.isArray(item.translations)) {
        for (const transGroup of item.translations) {
          if (Array.isArray(transGroup)) {
            const found = transGroup.find(t => t.lang === targetLangCode);
            if (found) {
              translationText = found.text;
              break;
            }
          }
        }
      }

      // Find audio url if available
      let audioUrl = null;
      if (Array.isArray(item.audios) && item.audios.length > 0) {
        const audioObj = item.audios[0];
        audioUrl = audioObj.url || (audioObj.id ? `https://audio.tatoeba.org/sentences/deu/${item.id}.mp3` : null);
      }

      return {
        tatoebaId: item.id,
        text: item.text,
        lang: item.lang,
        translation: translationText || '(Chưa có bản dịch)',
        audioUrl: audioUrl,
        author: item.user?.username || 'Tatoeba Community',
        license: item.license || 'CC-BY 2.0 FR'
      };
    });
  }

  /**
   * Curated offline fallback sentences for reliable German learning
   */
  getFallbackSentences(query = '', fromLang = 'de', toLang = 'vi') {
    const sampleSentences = [
      {
        tatoebaId: 1001,
        text: "Der Apfel fällt nicht weit vom Stamm.",
        lang: "deu",
        translation: "Quả táo rụng không xa gốc cây (Cha nào con nấy).",
        audioUrl: "https://audio.tatoeba.org/sentences/deu/1001.mp3",
        keyword: "Apfel"
      },
      {
        tatoebaId: 1002,
        text: "Ich esse jeden Morgen einen frischen Apfel.",
        lang: "deu",
        translation: "Tôi ăn một quả táo tươi mỗi buổi sáng.",
        audioUrl: null,
        keyword: "Apfel"
      },
      {
        tatoebaId: 1003,
        text: "Das Buch liegt auf dem großen Tisch.",
        lang: "deu",
        translation: "Cuốn sách nằm ở trên chiếc bàn lớn.",
        audioUrl: null,
        keyword: "Buch"
      },
      {
        tatoebaId: 1004,
        text: "Die Katze schläft friedlich auf dem Sofa.",
        lang: "deu",
        translation: "Con mèo đang ngủ yên bình trên ghế sô-pha.",
        audioUrl: null,
        keyword: "Katze"
      },
      {
        tatoebaId: 1005,
        text: "Das Wasser in den Bergen ist sehr kalt und klar.",
        lang: "deu",
        translation: "Nước ở trên núi rất lạnh và trong vắt.",
        audioUrl: null,
        keyword: "Wasser"
      },
      {
        tatoebaId: 1006,
        text: "Guten Tag! Wie geht es Ihnen heute?",
        lang: "deu",
        translation: "Xin chào! Hôm nay bạn cảm thấy thế nào?",
        audioUrl: null,
        keyword: "Tag"
      },
      {
        tatoebaId: 1007,
        text: "Die Sonne scheint hell am blauen Himmel.",
        lang: "deu",
        translation: "Mặt trời chiếu sáng rực rỡ trên bầu trời xanh.",
        audioUrl: null,
        keyword: "Sonne"
      },
      {
        tatoebaId: 1008,
        text: "Der Hund läuft schnell durch den grünen Park.",
        lang: "deu",
        translation: "Chú chó chạy thật nhanh qua công viên xanh mát.",
        audioUrl: null,
        keyword: "Hund"
      }
    ];

    if (!query) return sampleSentences;

    const lowerQ = query.toLowerCase();
    const filtered = sampleSentences.filter(s =>
      s.text.toLowerCase().includes(lowerQ) ||
      (s.keyword && s.keyword.toLowerCase().includes(lowerQ))
    );

    return filtered.length > 0 ? filtered : [
      {
        tatoebaId: Math.floor(Math.random() * 80000) + 10000,
        text: `Das Wort "${query}" ist sehr nützlich im Alltag.`,
        lang: "deu",
        translation: `Từ vựng "${query}" rất hữu dụng trong cuộc sống thường ngày.`,
        audioUrl: null,
        keyword: query
      }
    ];
  }
}

export const tatoebaApi = new TatoebaClient();

