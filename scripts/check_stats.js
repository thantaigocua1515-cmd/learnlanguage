import pkg from 'pg';
const { Client } = pkg;
const client = new Client({
  connectionString: 'postgresql://postgres:Khanggia123$$@db.guonovxcmbwrazvgrkmu.supabase.co:5432/postgres',
  ssl: { rejectUnauthorized: false }
});
await client.connect();
const r1 = await client.query('SELECT level, count(*) FROM public.words GROUP BY level ORDER BY level;');
console.log('Words per level:', r1.rows);
const r2 = await client.query('SELECT count(*) FROM public.word_examples;');
console.log('Total examples in DB:', r2.rows[0].count);
await client.end();

