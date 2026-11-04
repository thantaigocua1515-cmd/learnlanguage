import fs from 'fs';
import pg from 'pg';

const connectionString = 'postgresql://postgres:Khanggia123$$@db.guonovxcmbwrazvgrkmu.supabase.co:5432/postgres';

const client = new pg.Client({
  connectionString,
  ssl: { rejectUnauthorized: false }
});

async function main() {
  console.log('🔄 Đang kết nối tới Supabase PostgreSQL...');
  await client.connect();
  console.log('✅ Kết nối thành công!');

  // 1. Seed Languages
  console.log('📦 Kiểm tra và nạp danh sách Ngôn ngữ (languages)...');
  const langQuery = `
    INSERT INTO public.languages (code, name, native_name, flag_emoji, is_active)
    VALUES
        ('de', 'German', 'Deutsch', '🇩🇪', true),
        ('en', 'English', 'English', '🇬🇧', true),
        ('ja', 'Japanese', '日本語', '🇯🇵', true),
        ('zh', 'Chinese', '中文', '🇨🇳', true)
    ON CONFLICT (code) DO UPDATE SET is_active = EXCLUDED.is_active
    RETURNING id, code;
  `;
  const langRes = await client.query(langQuery);
  console.log(`✅ Đã nạp ${langRes.rows.length} ngôn ngữ.`);

  // Get German Language ID
  const getDeLang = await client.query("SELECT id FROM public.languages WHERE code = 'de' LIMIT 1");
  const deLangId = getDeLang.rows[0].id;
  console.log(`📌 German Language ID: ${deLangId}`);

  // 2. Seed CEFR Levels
  console.log('📦 Kiểm tra và nạp danh sách Cấp độ CEFR (cefr_levels)...');
  const levelQuery = `
    INSERT INTO public.cefr_levels (code, name, description, order_index, badge_color)
    VALUES
        ('A1', 'Khởi đầu (Beginner)', 'Giao tiếp cơ bản, chào hỏi, từ vựng đời sống thường nhật', 1, '#10b981'),
        ('A2', 'Cơ bản (Elementary)', 'Miêu tả bản thân, thói quen, mua sắm, môi trường xung quanh', 2, '#06b6d4'),
        ('B1', 'Trung cấp (Intermediate)', 'Tự tin xử lý tình huống du lịch, diễn đạt suy nghĩ, dự định', 3, '#3b82f6'),
        ('B2', 'Trung cao cấp (Upper-Int)', 'Hiểu văn bản phức tạp, tranh luận và trình bày quan điểm trôi chảy', 4, '#8b5cf6'),
        ('C1', 'Cao cấp (Advanced)', 'Sử dụng linh hoạt trong học thuật, công việc chuyên môn sâu', 5, '#ec4899'),
        ('C2', 'Thành thạo (Mastery)', 'Gần như người bản xứ, thấu hiểu ngữ cảnh văn hóa tinh tế', 6, '#f59e0b')
    ON CONFLICT (code) DO UPDATE SET order_index = EXCLUDED.order_index
    RETURNING id, code;
  `;
  await client.query(levelQuery);
  const levelsRes = await client.query("SELECT id, code FROM public.cefr_levels");
  const levelMap = {};
  levelsRes.rows.forEach(r => {
    levelMap[r.code] = r.id;
  });
  console.log('📌 CEFR Level IDs:', levelMap);

  // 3. Read 1000 items from JSON
  const rawData = fs.readFileSync('/home/jikay/Desktop/LingoLearning/scripts/vocab_1000_final.json', 'utf-8');
  const vocabList = JSON.parse(rawData);
  console.log(`📖 Đã đọc ${vocabList.length} từ vựng từ tệp dataset.`);

  // 4. Batch Insert Vocabulary
  console.log('🚀 Bắt đầu thêm 1000 từ vựng vào bảng vocabulary...');
  const BATCH_SIZE = 100;
  let insertedTotal = 0;

  for (let i = 0; i < vocabList.length; i += BATCH_SIZE) {
    const batch = vocabList.slice(i, i + BATCH_SIZE);
    const values = [];
    const params = [];
    let paramIndex = 1;

    for (const item of batch) {
      const levelId = levelMap[item.cefr_level] || levelMap['A1'];
      const gender = (item.gender && ['der', 'die', 'das'].includes(item.gender.toLowerCase()))
        ? item.gender.toLowerCase()
        : null;

      params.push(
        deLangId,                           // language_id
        levelId,                            // cefr_level_id
        item.word,                          // word
        item.ipa || null,                   // ipa
        item.pos || 'Noun',                 // pos
        gender,                             // gender
        item.plural_form || null,           // plural_form
        item.meaning_vi,                    // meaning_vi
        item.meaning_en || null,            // meaning_en
        item.example_de || null,            // example_de
        item.example_vi || null             // example_vi
      );

      values.push(
        `($${paramIndex++}, $${paramIndex++}, $${paramIndex++}, $${paramIndex++}, $${paramIndex++}, $${paramIndex++}, $${paramIndex++}, $${paramIndex++}, $${paramIndex++}, $${paramIndex++}, $${paramIndex++})`
      );
    }

    const insertSql = `
      INSERT INTO public.vocabulary (
        language_id, cefr_level_id, word, ipa, pos, gender, plural_form, meaning_vi, meaning_en, example_de, example_vi
      )
      VALUES ${values.join(', ')}
    `;

    await client.query(insertSql, params);
    insertedTotal += batch.length;
    console.log(`   ➔ Đã nạp ${insertedTotal} / ${vocabList.length} từ vựng...`);
  }

  console.log(`🎉 HOÀN THÀNH! Đã thêm thành công ${insertedTotal} từ vựng vào Supabase!`);

  // 5. Statistics Check
  const countRes = await client.query("SELECT COUNT(*) FROM public.vocabulary");
  console.log(`\n📊 Tổng số bản ghi trong bảng vocabulary hiện tại: ${countRes.rows[0].count}`);

  const levelStats = await client.query(`
    SELECT cl.code AS level, COUNT(v.id) AS count
    FROM public.vocabulary v
    JOIN public.cefr_levels cl ON v.cefr_level_id = cl.id
    GROUP BY cl.code, cl.order_index
    ORDER BY cl.order_index
  `);
  console.log('📈 Thống kê theo cấp độ CEFR:');
  console.table(levelStats.rows);

  const genderStats = await client.query(`
    SELECT COALESCE(gender::text, 'Không có giống (Động từ/Tính từ)') AS gender, COUNT(*) AS count
    FROM public.vocabulary
    GROUP BY gender
    ORDER BY count DESC
  `);
  console.log('🔵🔴🟢 Thống kê theo giống từ:');
  console.table(genderStats.rows);

  await client.end();
  console.log('🔒 Đã đóng kết nối cơ sở dữ liệu an toàn.');
}

main().catch(err => {
  console.error('❌ Lỗi khi thực thi:', err);
  process.exit(1);
});
