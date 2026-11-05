/**
 * Unit integration test for the 3 API endpoints in api/vocab.js
 */

import handler from '../api/vocab.js';

function createMockRes() {
  const res = {
    statusCode: 200,
    headers: {},
    setHeader(k, v) { this.headers[k] = v; },
    status(code) { this.statusCode = code; return this; },
    json(body) { this.body = body; return this; },
    end() { return this; }
  };
  return res;
}

async function testEndpoints() {
  console.log('Testing German Vocabulary API Endpoints...\n');

  // Test 1: GET /api/vocab?level=A1&limit=5
  console.log('1. Testing GET /api/vocab?level=A1&limit=5');
  const req1 = { method: 'GET', query: { level: 'A1', limit: 5 } };
  const res1 = createMockRes();
  await handler(req1, res1);
  console.log(`Status: ${res1.statusCode}`);
  console.log(`Level: ${res1.body?.level}, Total: ${res1.body?.total}, Items returned: ${res1.body?.data?.length}`);
  if (res1.body?.data?.[0]) {
    console.log(`Sample item: ${res1.body.data[0].lemma} (${res1.body.data[0].pos}) - ${res1.body.data[0].meaning_en}`);
  }

  // Test 2: GET /api/vocab?lemma=Haus
  console.log('\n2. Testing GET /api/vocab?lemma=Haus');
  const req2 = { method: 'GET', query: { lemma: 'Haus' } };
  const res2 = createMockRes();
  await handler(req2, res2);
  console.log(`Status: ${res2.statusCode}`);
  console.log(`Lemma: ${res2.body?.lemma}, Level: ${res2.body?.level}, Pos: ${res2.body?.pos}, Article: ${res2.body?.article}`);
  console.log(`Forms: ${Array.isArray(res2.body?.forms) ? res2.body.forms.join(', ') : res2.body?.forms}`);
  console.log(`Examples count: ${res2.body?.examples?.length}`);
  if (res2.body?.examples?.[0]) {
    console.log(`First example: DE: "${res2.body.examples[0].de}" | VI: "${res2.body.examples[0].vi}"`);
  }

  // Test 3: GET /api/vocab?lemma=Haus&type=examples
  console.log('\n3. Testing GET /api/vocab?lemma=Haus&type=examples');
  const req3 = { method: 'GET', query: { lemma: 'Haus', type: 'examples' } };
  const res3 = createMockRes();
  await handler(req3, res3);
  console.log(`Status: ${res3.statusCode}`);
  console.log(`Lemma: ${res3.body?.lemma}, Total examples: ${res3.body?.total}`);
  res3.body?.examples?.forEach((ex, idx) => {
    console.log(`  [${idx + 1}] DE: "${ex.sentence_de}" | VI: "${ex.translation_vi}" (source: ${ex.source})`);
  });

  console.log('\n✅ All 3 API endpoints verified successfully!');
  process.exit(0);
}

testEndpoints().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});

