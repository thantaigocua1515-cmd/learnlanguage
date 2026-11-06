/**
 * Vercel Serverless Function & REST API Endpoint Handler for German Vocabulary:
 * 1. GET /api/vocab?level=A1&limit=50&offset=0
 * 2. GET /api/vocab?lemma=Haus (or /api/vocab/:lemma)
 * 3. GET /api/vocab?lemma=Haus&type=examples (or /api/vocab/:lemma/examples)
 * 
 * Backed by Supabase PostgreSQL (via pg pool) with fallback to local JSON.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pkg from 'pg';
const { Pool } = pkg;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONNECTION_STRING = process.env.DATABASE_URL || 'postgresql://postgres:Khanggia123$$@db.guonovxcmbwrazvgrkmu.supabase.co:5432/postgres';

let pool = null;
function getPool() {
  if (!pool) {
    pool = new Pool({
      connectionString: CONNECTION_STRING,
      ssl: { rejectUnauthorized: false },
      max: 5,
      idleTimeoutMillis: 30000
    });
  }
  return pool;
}

// Fallback JSON loader
let localCache = null;
function getLocalCache() {
  if (!localCache) {
    const fullPath = path.resolve(__dirname, '../data/output/vocab_A1_A2_B1_full.json');
    const samplePath = path.resolve(__dirname, '../data/output/vocab_A1_100.json');
    const targetPath = fs.existsSync(fullPath) ? fullPath : samplePath;
    if (fs.existsSync(targetPath)) {
      localCache = JSON.parse(fs.readFileSync(targetPath, 'utf8'));
    } else {
      localCache = [];
    }
  }
  return localCache;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { level, letter, gender, search, lemma, type, limit = 60, offset = 0 } = req.query;

  try {
    const db = getPool();

    // 1. GET /api/vocab/{lemma}/examples
    if (lemma && type === 'examples') {
      try {
        const query = `
          SELECT e.id, e.sentence_de, e.translation_vi, e.sentence_de AS de, e.translation_vi AS vi, e.source, e.tatoeba_id
          FROM public.word_examples e
          JOIN public.words w ON e.word_id = w.id
          WHERE LOWER(w.lemma) = LOWER($1);
        `;
        const result = await db.query(query, [lemma.trim()]);
        return res.status(200).json({
          lemma,
          total: result.rows.length,
          examples: result.rows
        });
      } catch (dbErr) {
        console.warn('DB query failed, fallback to local cache:', dbErr.message);
        const allWords = getLocalCache();
        const found = allWords.find(w => w.lemma.toLowerCase() === lemma.trim().toLowerCase());
        if (!found) {
          return res.status(404).json({ error: `Lemma '${lemma}' not found` });
        }
        return res.status(200).json({
          lemma: found.lemma,
          total: (found.examples || []).length,
          examples: (found.examples || []).map(ex => ({
            sentence_de: ex.sentence_de || ex.de,
            translation_vi: ex.translation_vi || ex.vi,
            de: ex.de || ex.sentence_de,
            vi: ex.vi || ex.translation_vi,
            source: ex.source || 'tatoeba',
            tatoeba_id: ex.tatoeba_id || null
          }))
        });
      }
    }

    // 2. GET /api/vocab/{lemma}
    if (lemma) {
      try {
        const query = `
          SELECT 
            w.id, w.lemma, w.level, w.pos, w.article, w.gender, w.plural, w.ipa,
            w.meaning_en, w.meaning_vi, w.forms, w.synonyms, w.missing, w.sources,
            COALESCE(
              json_agg(
                json_build_object(
                  'id', e.id,
                  'de', e.sentence_de,
                  'vi', e.translation_vi,
                  'source', e.source,
                  'tatoeba_id', e.tatoeba_id
                )
              ) FILTER (WHERE e.id IS NOT NULL),
              '[]'
            ) AS examples
          FROM public.words w
          LEFT JOIN public.word_examples e ON w.id = e.word_id
          WHERE LOWER(w.lemma) = LOWER($1)
          GROUP BY w.id
          LIMIT 1;
        `;
        const result = await db.query(query, [lemma.trim()]);
        if (result.rows.length === 0) {
          return res.status(404).json({ error: `Lemma '${lemma}' not found` });
        }
        return res.status(200).json(result.rows[0]);
      } catch (dbErr) {
        console.warn('DB query failed, fallback to local cache:', dbErr.message);
        const allWords = getLocalCache();
        const found = allWords.find(w => w.lemma.toLowerCase() === lemma.trim().toLowerCase());
        if (!found) {
          return res.status(404).json({ error: `Lemma '${lemma}' not found` });
        }
        return res.status(200).json(found);
      }
    }

    // 3. GET /api/vocab with filters (level, letter, gender, search)
    if (level || letter || gender || search || req.query.all !== undefined || req.query.list !== undefined) {
      const lim = Math.min(Math.max(parseInt(limit, 10) || 60, 1), 500);
      const off = Math.max(parseInt(offset, 10) || 0, 0);

      try {
        const conditions = [];
        const params = [];
        let pIdx = 1;

        if (level && level.toUpperCase() !== 'ALL') {
          conditions.push(`w.level = $${pIdx++}`);
          params.push(level.toUpperCase());
        }

        if (letter && letter.toUpperCase() !== 'ALL') {
          const char = letter.trim().toUpperCase();
          conditions.push(`(UPPER(LEFT(w.lemma, 1)) = $${pIdx++} OR LEFT(w.lemma, 1) ILIKE $${pIdx - 1})`);
          params.push(char);
        }

        if (gender && gender.toUpperCase() !== 'ALL') {
          conditions.push(`(w.article = $${pIdx} OR w.gender = $${pIdx})`);
          pIdx++;
          params.push(gender.toLowerCase());
        }

        if (search && search.trim()) {
          conditions.push(`(w.lemma ILIKE $${pIdx} OR w.meaning_vi ILIKE $${pIdx} OR w.meaning_en ILIKE $${pIdx})`);
          pIdx++;
          params.push(`%${search.trim()}%`);
        }

        const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

        const countRes = await db.query(`SELECT COUNT(*) FROM public.words w ${whereClause}`, params);
        const total = parseInt(countRes.rows[0].count, 10);

        const query = `
          SELECT id, lemma, level, pos, article, gender, plural, ipa,
                 meaning_en, meaning_vi, forms, synonyms, missing, sources
          FROM public.words w
          ${whereClause}
          ORDER BY w.lemma ASC
          LIMIT $${pIdx++} OFFSET $${pIdx++};
        `;
        const result = await db.query(query, [...params, lim, off]);

        return res.status(200).json({
          level: level || 'ALL',
          letter: letter || 'ALL',
          gender: gender || 'ALL',
          total,
          limit: lim,
          offset: off,
          data: result.rows
        });
      } catch (dbErr) {
        console.warn('DB query failed, fallback to local cache:', dbErr.message);
        let allWords = getLocalCache();

        if (level && level.toUpperCase() !== 'ALL') {
          allWords = allWords.filter(w => (w.level || '').toUpperCase() === level.toUpperCase());
        }

        if (letter && letter.toUpperCase() !== 'ALL') {
          const char = letter.trim().toUpperCase();
          allWords = allWords.filter(w => (w.lemma || w.word || '').toUpperCase().startsWith(char));
        }

        if (gender && gender.toUpperCase() !== 'ALL') {
          allWords = allWords.filter(w => w.article === gender.toLowerCase() || w.gender === gender.toLowerCase());
        }

        if (search && search.trim()) {
          const q = search.trim().toLowerCase();
          allWords = allWords.filter(w =>
            (w.lemma || '').toLowerCase().includes(q) ||
            (w.meaning_vi || '').toLowerCase().includes(q) ||
            (w.meaning_en || '').toLowerCase().includes(q)
          );
        }

        return res.status(200).json({
          level: level || 'ALL',
          letter: letter || 'ALL',
          gender: gender || 'ALL',
          total: allWords.length,
          limit: lim,
          offset: off,
          data: allWords.slice(off, off + lim)
        });
      }
    }

    // Default: Root info & level counts
    try {
      const statsRes = await db.query(`
        SELECT level, COUNT(*) as count 
        FROM public.words 
        GROUP BY level 
        ORDER BY level ASC;
      `);
      return res.status(200).json({
        message: 'LingoLearning German Vocabulary API (DWDS + Kaikki + Tatoeba)',
        levels: statsRes.rows,
        routes: {
          by_level: '/api/vocab?level=A1&limit=50',
          by_lemma: '/api/vocab?lemma=Haus',
          examples: '/api/vocab?lemma=Haus&type=examples'
        }
      });
    } catch {
      return res.status(200).json({
        message: 'LingoLearning German Vocabulary API',
        routes: {
          by_level: '/api/vocab?level=A1&limit=50',
          by_lemma: '/api/vocab?lemma=Haus',
          examples: '/api/vocab?lemma=Haus&type=examples'
        }
      });
    }

  } catch (err) {
    console.error('Unhandled API Error:', err);
    return res.status(500).json({ error: err.message || 'Internal server error' });
  }
}
