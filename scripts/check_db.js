import pg from 'pg';

const connectionString = 'postgresql://postgres:Khanggia123$$@db.guonovxcmbwrazvgrkmu.supabase.co:5432/postgres';

const client = new pg.Client({
  connectionString,
  ssl: { rejectUnauthorized: false }
});

async function run() {
  await client.connect();
  const langs = await client.query('SELECT id, code, name FROM languages');
  console.log('Languages:', langs.rows);
  const levels = await client.query('SELECT id, code, name FROM cefr_levels ORDER BY order_index');
  console.log('CEFR Levels:', levels.rows);
  const count = await client.query('SELECT count(*) FROM vocabulary');
  console.log('Current vocabulary count:', count.rows[0].count);
  await client.end();
}

run();
