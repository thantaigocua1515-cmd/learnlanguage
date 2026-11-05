/**
 * Idempotent Fast Batch Database Importer for German Vocabulary.
 * Merges DWDS + Kaikki + Tatoeba into Supabase PostgreSQL:
 * - public.words (ON CONFLICT (lemma, pos) DO UPDATE ...)
 * - public.word_examples
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pkg from 'pg';
const { Client } = pkg;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONNECTION_STRING = process.env.DATABASE_URL || 'postgresql://postgres:Khanggia123$$@db.guonovxcmbwrazvgrkmu.supabase.co:5432/postgres';

function parseArgs() {
  const args = process.argv.slice(2);
  let filePath = path.resolve(__dirname, '../data/output/vocab_A1_A2_B1_full.json');
  if (!fs.existsSync(filePath)) {
    filePath = path.resolve(__dirname, '../data/output/vocab_A1_100.json');
  }

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--file' && args[i + 1]) {
      filePath = path.resolve(process.cwd(), args[i + 1]);
    }
  }
  return { filePath };
}

async function main() {
  const { filePath } = parseArgs();
  if (!fs.existsSync(filePath)) {
    console.error(`❌ Input file not found: ${filePath}`);
    process.exit(1);
  }

  console.log(`📖 Reading vocabulary JSON from: ${filePath}`);
  const rawData = fs.readFileSync(filePath, 'utf8');
  const items = JSON.parse(rawData);
  console.log(`Loaded ${items.length.toLocaleString()} vocabulary items.`);

  console.log('Connecting to Supabase PostgreSQL database...');
  const client = new Client({
    connectionString: CONNECTION_STRING,
    ssl: { rejectUnauthorized: false }
  });

  await client.connect();
  console.log('Connected successfully. Beginning fast bulk idempotent import...\n');

  const BATCH_SIZE = 100;
  let insertedWords = 0;
  let insertedExamples = 0;
  const startTime = Date.now();

  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const chunk = items.slice(i, i + BATCH_SIZE);
    await client.query('BEGIN');
    try {
      // 1. Bulk Upsert Words
      const wordPlaceholders = [];
      const wordParams = [];
      let pIdx = 1;

      for (const item of chunk) {
        wordPlaceholders.push(`($${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, $${pIdx++}, NOW())`);
        wordParams.push(
          item.lemma,
          item.level,
          item.pos,
          item.article || null,
          item.gender || null,
          item.plural || null,
          item.ipa || null,
          item.meaning_en || null,
          item.meaning_vi || null,
          JSON.stringify(item.forms || []),
          JSON.stringify(item.synonyms || []),
          JSON.stringify(item.missing || []),
          JSON.stringify(item.sources || {})
        );
      }

      const wordInsertQuery = `
        INSERT INTO public.words (
          lemma, level, pos, article, gender, plural, ipa,
          meaning_en, meaning_vi, forms, synonyms, missing, sources, updated_at
        )
        VALUES ${wordPlaceholders.join(', ')}
        ON CONFLICT (lemma, pos) DO UPDATE SET
          level = EXCLUDED.level,
          article = EXCLUDED.article,
          gender = EXCLUDED.gender,
          plural = EXCLUDED.plural,
          ipa = EXCLUDED.ipa,
          meaning_en = EXCLUDED.meaning_en,
          meaning_vi = COALESCE(EXCLUDED.meaning_vi, words.meaning_vi),
          forms = EXCLUDED.forms,
          synonyms = EXCLUDED.synonyms,
          missing = EXCLUDED.missing,
          sources = EXCLUDED.sources,
          updated_at = NOW()
        RETURNING id, lemma, pos;
      `;

      const wordRes = await client.query(wordInsertQuery, wordParams);
      insertedWords += wordRes.rows.length;

      // Build map of lemma+pos -> id
      const idMap = new Map();
      const wordIds = [];
      for (const row of wordRes.rows) {
        idMap.set(`${row.lemma}_${row.pos}`, row.id);
        wordIds.push(row.id);
      }

      // 2. Clear old examples for words in this chunk
      if (wordIds.length > 0) {
        await client.query('DELETE FROM public.word_examples WHERE word_id = ANY($1::uuid[])', [wordIds]);
      }

      // 3. Bulk Insert Examples
      const examplePlaceholders = [];
      const exampleParams = [];
      let exIdx = 1;

      for (const item of chunk) {
        const wordId = idMap.get(`${item.lemma}_${item.pos}`);
        if (!wordId || !item.examples || item.examples.length === 0) continue;

        for (const ex of item.examples) {
          examplePlaceholders.push(`($${exIdx++}, $${exIdx++}, $${exIdx++}, $${exIdx++}, $${exIdx++})`);
          exampleParams.push(
            wordId,
            ex.de,
            ex.vi || null,
            ex.source || 'tatoeba',
            ex.tatoeba_id || null
          );
        }
      }

      if (examplePlaceholders.length > 0) {
        const exampleInsertQuery = `
          INSERT INTO public.word_examples (word_id, sentence_de, translation_vi, source, tatoeba_id)
          VALUES ${examplePlaceholders.join(', ')};
        `;
        await client.query(exampleInsertQuery, exampleParams);
        insertedExamples += (exampleParams.length / 5);
      }

      await client.query('COMMIT');
      const progressPct = (((i + chunk.length) / items.length) * 100).toFixed(1);
      console.log(`Progress: ${progressPct}% (${i + chunk.length}/${items.length} words imported)...`);
    } catch (batchErr) {
      await client.query('ROLLBACK');
      console.error(`❌ Error in batch starting at index ${i}:`, batchErr);
      throw batchErr;
    }
  }

  const durationSec = ((Date.now() - startTime) / 1000).toFixed(2);
  console.log('\n======================================================');
  console.log('🎉 FAST BULK IMPORT COMPLETED SUCCESSFULLY!');
  console.log(`Total words processed    : ${insertedWords.toLocaleString()}`);
  console.log(`Total examples imported   : ${insertedExamples.toLocaleString()}`);
  console.log(`Total elapsed time        : ${durationSec}s`);
  console.log('======================================================\n');

  await client.end();
}

main().catch(err => {
  console.error('Fatal error during import:', err);
  process.exit(1);
});
