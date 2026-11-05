/**
 * Applies sql/schema_words.sql to the user's Supabase PostgreSQL database.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pkg from 'pg';
const { Client } = pkg;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONNECTION_STRING = process.env.DATABASE_URL || 'postgresql://postgres:Khanggia123$$@db.guonovxcmbwrazvgrkmu.supabase.co:5432/postgres';

async function main() {
  const schemaPath = path.resolve(__dirname, '../sql/schema_words.sql');
  const sql = fs.readFileSync(schemaPath, 'utf8');

  console.log('Connecting to Supabase PostgreSQL...');
  const client = new Client({
    connectionString: CONNECTION_STRING,
    ssl: { rejectUnauthorized: false }
  });

  try {
    await client.connect();
    console.log('Connected successfully. Applying schema_words.sql...');
    await client.query(sql);
    console.log('✅ Schema migration applied successfully: table words & word_examples ready!');
  } catch (err) {
    console.error('❌ Migration failed:', err);
    process.exit(1);
  } finally {
    await client.end();
  }
}

main();

