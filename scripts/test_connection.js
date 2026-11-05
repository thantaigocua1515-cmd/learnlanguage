import pg from 'pg';

const connectionString = 'postgresql://postgres:Khanggia123$$@db.guonovxcmbwrazvgrkmu.supabase.co:5432/postgres';

const client = new pg.Client({
  connectionString,
  ssl: { rejectUnauthorized: false }
});

async function test() {
  try {
    await client.connect();
    console.log('✅ Connected to Supabase PostgreSQL successfully!');
    const res = await client.query('SELECT table_name FROM information_schema.tables WHERE table_schema = $1', ['public']);
    console.log('Existing tables in public schema:', res.rows.map(r => r.table_name));
    await client.end();
  } catch (err) {
    console.error('❌ Connection error:', err.message);
    process.exit(1);
  }
}

test();

