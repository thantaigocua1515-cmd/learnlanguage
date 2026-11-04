/**
 * LingoLearning - SaaS AdminCP Controller
 * Complete Management: KPIs, Tatoeba Ingestion, Vocab CRUD, Supabase Settings
 */

import { CONFIG } from './config.js';
import { sound } from './services/soundService.js';
import { dataService } from './api/dataService.js';
import { tatoebaApi } from './api/tatoeba.js';
import { supabaseManager } from './supabaseClient.js';

class AdminApp {
  constructor() {
    this.currentTab = 'dashboard';
    this.container = document.getElementById('admin-view-container');
    this.tatoebaSearchResults = [];

    this.initTheme();
    this.bindSidebar();
    this.renderCurrentTab();
  }

  initTheme() {
    const savedTheme = localStorage.getItem('lingo_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const icon = document.getElementById('admin-theme-icon');
    if (icon) {
      icon.className = savedTheme === 'dark' ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-fill';
    }

    document.getElementById('admin-theme-toggle')?.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const next = current === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('lingo_theme', next);
      if (icon) {
        icon.className = next === 'dark' ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-fill';
      }
    });
  }

  bindSidebar() {
    document.querySelectorAll('.admin-nav-item[data-tab]').forEach(item => {
      item.addEventListener('click', (e) => {
        document.querySelectorAll('.admin-nav-item[data-tab]').forEach(el => el.classList.remove('active'));
        item.classList.add('active');
        this.currentTab = item.getAttribute('data-tab');
        this.renderCurrentTab();
      });
    });
  }

  renderCurrentTab() {
    if (this.currentTab === 'dashboard') this.renderDashboard();
    else if (this.currentTab === 'tatoeba') this.renderTatoebaImporter();
    else if (this.currentTab === 'vocabulary') this.renderVocabulary();
    else if (this.currentTab === 'sentences') this.renderSentences();
    else if (this.currentTab === 'supabase') this.renderSupabaseSettings();
  }

  /* ==============================================================================
     1. SAAS DASHBOARD & METRICS
     ============================================================================== */
  async renderDashboard() {
    const stats = await dataService.getAdminStats();

    this.container.innerHTML = `
      <div class="admin-topbar">
        <div>
          <h2 class="fw-bold mb-1">SaaS Overview & Analytics</h2>
          <p class="text-secondary mb-0">Thống kê toàn diện hệ thống học đa ngôn ngữ LingoLearning.</p>
        </div>
        <div class="d-flex gap-2">
          <button class="btn btn-3d btn-3d-primary btn-3d-sm" id="btn-quick-import-tatoeba">
            <i class="bi bi-cloud-arrow-down-fill"></i> Import Tatoeba
          </button>
          <button class="btn btn-3d btn-3d-outline btn-3d-sm" id="btn-quick-add-vocab">
            <i class="bi bi-plus-lg"></i> Thêm từ mới
          </button>
        </div>
      </div>

      <!-- KPI Metrics Grid -->
      <div class="row g-3 mb-4">
        <div class="col-sm-6 col-xl-3">
          <div class="kpi-card border-top border-4 border-primary">
            <div class="kpi-title">Tổng số từ vựng (DE)</div>
            <div class="kpi-value">${stats.totalWords}</div>
            <div class="kpi-trend positive"><i class="bi bi-arrow-up-right"></i> Đang mở rộng A1-C2</div>
          </div>
        </div>

        <div class="col-sm-6 col-xl-3">
          <div class="kpi-card border-top border-4 border-info">
            <div class="kpi-title">Câu mẫu Tatoeba</div>
            <div class="kpi-value">${stats.totalSentences}</div>
            <div class="kpi-trend positive"><i class="bi bi-check2-all"></i> Đã đồng bộ & gắn thẻ</div>
          </div>
        </div>

        <div class="col-sm-6 col-xl-3">
          <div class="kpi-card border-top border-4 border-success">
            <div class="kpi-title">Học viên hoạt động</div>
            <div class="kpi-value">1,482</div>
            <div class="kpi-trend positive"><i class="bi bi-arrow-up-right"></i> +12% tuần này</div>
          </div>
        </div>

        <div class="col-sm-6 col-xl-3">
          <div class="kpi-card border-top border-4 border-warning">
            <div class="kpi-title">Lượt chơi Mini-games</div>
            <div class="kpi-value">8,920</div>
            <div class="kpi-trend positive"><i class="bi bi-star-fill text-warning"></i> Retention 84%</div>
          </div>
        </div>
      </div>

      <!-- German Genders & CEFR Breakdown -->
      <div class="row g-3 mb-4">
        <!-- Gender Distribution Card -->
        <div class="col-lg-6">
          <div class="gamify-card p-4 h-100">
            <h5 class="fw-bold mb-3"><i class="bi bi-pie-chart-fill text-primary me-2"></i>Phân bố giống từ Tiếng Đức</h5>
            <div class="d-flex align-items-center gap-3 mb-4">
              <div class="p-3 rounded-3 flex-fill text-center" style="background-color: var(--gender-der-bg); border: 1px solid var(--gender-der-border);">
                <div class="fw-bold fs-4" style="color: var(--gender-der);">${stats.byGender.der}</div>
                <div class="badge badge-gender badge-der">der (Maskulin)</div>
              </div>
              <div class="p-3 rounded-3 flex-fill text-center" style="background-color: var(--gender-die-bg); border: 1px solid var(--gender-die-border);">
                <div class="fw-bold fs-4" style="color: var(--gender-die);">${stats.byGender.die}</div>
                <div class="badge badge-gender badge-die">die (Feminin)</div>
              </div>
              <div class="p-3 rounded-3 flex-fill text-center" style="background-color: var(--gender-das-bg); border: 1px solid var(--gender-das-border);">
                <div class="fw-bold fs-4" style="color: var(--gender-das);">${stats.byGender.das}</div>
                <div class="badge badge-gender badge-das">das (Neutral)</div>
              </div>
            </div>
            <div class="text-secondary small">
              <i class="bi bi-info-circle"></i> Tỷ lệ mạo từ danh từ được chuẩn hóa để phục vụ trò chơi luyện phản xạ Der/Die/Das.
            </div>
          </div>
        </div>

        <!-- CEFR Levels Distribution -->
        <div class="col-lg-6">
          <div class="gamify-card p-4 h-100">
            <h5 class="fw-bold mb-3"><i class="bi bi-bar-chart-fill text-success me-2"></i>Từ vựng theo Cấp độ CEFR</h5>
            <div class="row g-2">
              ${CONFIG.CEFR_LEVELS.map(lvl => `
                <div class="col-4">
                  <div class="p-2 border rounded-3 bg-body-tertiary text-center">
                    <span class="badge badge-level badge-level-${lvl.code}">${lvl.code}</span>
                    <div class="fs-5 fw-bold mt-1">${stats.byLevel[lvl.code] || 0} từ</div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      </div>
    `;

    this.container.querySelector('#btn-quick-import-tatoeba')?.addEventListener('click', () => {
      document.querySelector('.admin-nav-item[data-tab="tatoeba"]')?.click();
    });
    this.container.querySelector('#btn-quick-add-vocab')?.addEventListener('click', () => {
      this.openVocabModal();
    });
  }

  /* ==============================================================================
     2. TATOEBA LIVE INGESTION TOOL
     ============================================================================== */
  renderTatoebaImporter() {
    this.container.innerHTML = `
      <div class="tatoeba-hero-banner">
        <div class="row align-items-center">
          <div class="col-lg-8">
            <div class="badge bg-white text-primary mb-2 fw-bold">OpenAPI Data Pipeline</div>
            <h2 class="fw-bold mb-1">Tatoeba API Sentence Ingestion Engine</h2>
            <p class="mb-0 text-white-50">Tìm kiếm, nghe phát âm và import trực tiếp hàng triệu câu mẫu Tiếng Đức từ Tatoeba.org vào Supabase.</p>
          </div>
          <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
            <span class="badge bg-success-subtle text-success p-2 fs-6">
              <i class="bi bi-shield-check"></i> Connected: api.tatoeba.org
            </span>
          </div>
        </div>
      </div>

      <!-- Ingestion Search Controls -->
      <div class="gamify-card p-4 mb-4">
        <form id="tatoeba-search-form" class="row g-3 align-items-end">
          <div class="col-md-4">
            <label class="form-label fw-bold small">Từ khóa tiếng Đức (Keyword) *</label>
            <input type="text" class="form-control form-control-gamify" id="tatoeba-query" placeholder="ví dụ: Apfel, Buch, Kaffee, Liebe..." required value="Apfel">
          </div>
          <div class="col-md-3">
            <label class="form-label fw-bold small">Gán Cấp độ CEFR</label>
            <select class="form-select form-select-gamify" id="tatoeba-cefr-assign">
              <option value="A1">A1 - Khởi đầu</option>
              <option value="A2">A2 - Cơ bản</option>
              <option value="B1">B1 - Trung cấp</option>
              <option value="B2">B2 - Trung cao cấp</option>
              <option value="C1">C1 - Cao cấp</option>
              <option value="C2">C2 - Thành thạo</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label fw-bold small">Ngôn ngữ dịch</label>
            <select class="form-select form-select-gamify" id="tatoeba-target-lang">
              <option value="vi">Tiếng Việt (vie)</option>
              <option value="en">Tiếng Anh (eng)</option>
            </select>
          </div>
          <div class="col-md-2">
            <button type="submit" class="btn btn-3d btn-3d-primary w-100" id="btn-tatoeba-fetch">
              <i class="bi bi-search"></i> Quét API
            </button>
          </div>
        </form>
      </div>

      <!-- Search Results Area -->
      <div id="tatoeba-results-wrapper">
        <div class="text-center py-5 text-muted">
          <i class="bi bi-cloud-arrow-down display-4"></i>
          <p class="mt-2">Nhập từ khóa và bấm "Quét API" để nạp dữ liệu từ Tatoeba.</p>
        </div>
      </div>
    `;

    const form = this.container.querySelector('#tatoeba-search-form');
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.executeTatoebaSearch();
    });
  }

  async executeTatoebaSearch() {
    const query = this.container.querySelector('#tatoeba-query').value.trim();
    const cefr = this.container.querySelector('#tatoeba-cefr-assign').value;
    const toLang = this.container.querySelector('#tatoeba-target-lang').value;
    const wrapper = this.container.querySelector('#tatoeba-results-wrapper');

    wrapper.innerHTML = `
      <div class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-2 text-secondary">Đang kết nối và trích xuất câu mẫu từ Tatoeba API...</p>
      </div>
    `;

    try {
      const results = await tatoebaApi.searchSentences({
        query,
        fromLang: 'de',
        toLang,
        limit: 8
      });

      this.tatoebaSearchResults = results;
      this.renderTatoebaResults(results, cefr);
    } catch (err) {
      wrapper.innerHTML = `
        <div class="alert alert-danger" role="alert">
          <i class="bi bi-exclamation-triangle-fill me-2"></i> Lỗi kết nối Tatoeba API: ${err.message}
        </div>
      `;
    }
  }

  renderTatoebaResults(results, cefrLevel) {
    const wrapper = this.container.querySelector('#tatoeba-results-wrapper');

    if (results.length === 0) {
      wrapper.innerHTML = `
        <div class="text-center py-5">
          <i class="bi bi-inbox display-4 text-muted"></i>
          <p class="mt-2 text-secondary">Không tìm thấy câu mẫu phù hợp trên Tatoeba.</p>
        </div>
      `;
      return;
    }

    wrapper.innerHTML = `
      <div class="d-flex align-items-center justify-content-between mb-3">
        <h5 class="fw-bold mb-0">Tìm thấy ${results.length} câu mẫu từ Tatoeba</h5>
        <button class="btn btn-3d btn-3d-das btn-3d-sm" id="btn-import-all-tatoeba">
          <i class="bi bi-cloud-check-fill"></i> Import tất cả (${results.length}) vào DB
        </button>
      </div>

      <div class="row g-2" id="tatoeba-list">
        ${results.map((item, idx) => `
          <div class="col-12">
            <div class="tatoeba-result-item">
              <div class="d-flex align-items-center gap-3">
                <button class="btn-speaker preview-speaker-btn" data-text="${item.text}" data-audio="${item.audioUrl || ''}" title="Nghe phát âm">
                  <i class="bi bi-volume-up-fill"></i>
                </button>
                <div>
                  <div class="fw-bold text-dark fs-6">${item.text}</div>
                  <div class="text-secondary small"><i class="bi bi-translate text-muted"></i> ${item.translation}</div>
                  <div class="text-muted" style="font-size: 0.75rem;">
                    <span>Tatoeba #${item.tatoebaId}</span> • <span>Tác giả: ${item.author}</span> • <span>${item.license}</span>
                  </div>
                </div>
              </div>
              <button class="btn btn-3d btn-3d-outline btn-3d-sm single-import-btn" data-index="${idx}">
                <i class="bi bi-plus-circle"></i> Import
              </button>
            </div>
          </div>
        `).join('')}
      </div>
    `;

    // Audio preview
    wrapper.querySelectorAll('.preview-speaker-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const text = e.currentTarget.getAttribute('data-text');
        const audio = e.currentTarget.getAttribute('data-audio');
        sound.speak(text, audio, 'de-DE');
      });
    });

    // Single item import
    wrapper.querySelectorAll('.single-import-btn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const idx = parseInt(e.currentTarget.getAttribute('data-index'), 10);
        const item = this.tatoebaSearchResults[idx];
        await dataService.saveTatoebaSentences([item], cefrLevel);
        sound.playSuccess();
        e.currentTarget.disabled = true;
        e.currentTarget.innerHTML = `<i class="bi bi-check-lg text-success"></i> Đã lưu`;
      });
    });

    // Bulk import
    wrapper.querySelector('#btn-import-all-tatoeba')?.addEventListener('click', async () => {
      await dataService.saveTatoebaSentences(this.tatoebaSearchResults, cefrLevel);
      sound.playSuccess();
      alert(`✅ Đã import thành công ${this.tatoebaSearchResults.length} câu vào cơ sở dữ liệu!`);
      this.currentTab = 'sentences';
      this.renderCurrentTab();
    });
  }

  /* ==============================================================================
     3. VOCABULARY MASTER CRUD
     ============================================================================== */
  async renderVocabulary() {
    const vocabList = await dataService.getVocabulary();

    this.container.innerHTML = `
      <div class="admin-topbar">
        <div>
          <h2 class="fw-bold mb-1">Quản lý Từ vựng Tiếng Đức</h2>
          <p class="text-secondary mb-0">Toàn bộ kho từ vựng theo chuẩn CEFR, giống từ, phiên âm IPA.</p>
        </div>
        <button class="btn btn-3d btn-3d-primary btn-3d-sm" id="btn-add-vocab-modal">
          <i class="bi bi-plus-lg"></i> Thêm từ mới
        </button>
      </div>

      <div class="saas-table-card">
        <div class="table-responsive">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Từ vựng (DE)</th>
                <th>Giống</th>
                <th>Số nhiều</th>
                <th>Cấp độ</th>
                <th>Nghĩa Tiếng Việt</th>
                <th>Phát âm</th>
                <th class="text-end">Hành động</th>
              </tr>
            </thead>
            <tbody>
              ${vocabList.map(item => `
                <tr>
                  <td>
                    <div class="fw-bold text-primary">${item.word}</div>
                    <small class="text-muted font-monospace">${item.ipa || ''}</small>
                  </td>
                  <td>
                    ${item.gender ? `<span class="badge badge-gender badge-${item.gender}">${item.gender}</span>` : '<span class="text-muted">-</span>'}
                  </td>
                  <td>${item.plural_form || '<span class="text-muted">-</span>'}</td>
                  <td><span class="badge badge-level badge-level-${item.cefr_level || 'A1'}">${item.cefr_level || 'A1'}</span></td>
                  <td>${item.meaning_vi}</td>
                  <td>
                    <button class="btn-speaker btn-speaker-table" data-word="${item.word}">
                      <i class="bi bi-volume-up-fill"></i>
                    </button>
                  </td>
                  <td class="text-end">
                    <button class="btn btn-sm btn-outline-danger delete-vocab-btn" data-id="${item.id}" title="Xóa">
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    this.container.querySelector('#btn-add-vocab-modal')?.addEventListener('click', () => {
      this.openVocabModal();
    });

    this.container.querySelectorAll('.btn-speaker-table').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const word = e.currentTarget.getAttribute('data-word');
        sound.speak(word, null, 'de-DE');
      });
    });

    this.container.querySelectorAll('.delete-vocab-btn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        if (confirm('Bạn có chắc chắn muốn xóa từ vựng này?')) {
          await dataService.deleteVocabulary(id);
          this.renderVocabulary();
        }
      });
    });
  }

  openVocabModal() {
    const modalEl = document.getElementById('vocabModal');
    const modal = new bootstrap.Modal(modalEl);
    document.getElementById('vocabForm').reset();
    document.getElementById('form-vocab-id').value = '';

    const saveBtn = document.getElementById('btn-save-vocab');
    saveBtn.onclick = async () => {
      const item = {
        id: document.getElementById('form-vocab-id').value || null,
        word: document.getElementById('form-word').value.trim(),
        gender: document.getElementById('form-gender').value || null,
        plural_form: document.getElementById('form-plural').value.trim() || null,
        ipa: document.getElementById('form-ipa').value.trim() || null,
        cefr_level: document.getElementById('form-level').value,
        pos: document.getElementById('form-pos').value.trim(),
        meaning_vi: document.getElementById('form-meaning-vi').value.trim(),
        example_de: document.getElementById('form-example-de').value.trim(),
        example_vi: document.getElementById('form-example-vi').value.trim()
      };

      if (!item.word || !item.meaning_vi) {
        alert('Vui lòng nhập Từ vựng và Nghĩa tiếng Việt!');
        return;
      }

      await dataService.saveVocabulary(item);
      sound.playSuccess();
      modal.hide();
      this.renderVocabulary();
    };

    modal.show();
  }

  /* ==============================================================================
     4. SENTENCES REPOSITORY
     ============================================================================== */
  async renderSentences() {
    const sentences = await dataService.getSentences();

    this.container.innerHTML = `
      <div class="admin-topbar">
        <div>
          <h2 class="fw-bold mb-1">Kho Câu Mẫu Đã Lưu (${sentences.length} câu)</h2>
          <p class="text-secondary mb-0">Các câu mẫu đồng bộ từ Tatoeba phục vụ cho trò chơi Điền Khuyết (Cloze Test).</p>
        </div>
        <button class="btn btn-3d btn-3d-primary btn-3d-sm" id="btn-goto-tatoeba">
          <i class="bi bi-cloud-arrow-down"></i> Tìm thêm câu trên Tatoeba
        </button>
      </div>

      <div class="saas-table-card">
        <div class="table-responsive">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Tatoeba ID</th>
                <th>Câu Tiếng Đức</th>
                <th>Bản dịch Tiếng Việt</th>
                <th>Cấp độ</th>
                <th>Phát âm</th>
              </tr>
            </thead>
            <tbody>
              ${sentences.length === 0 ? `
                <tr><td colspan="5" class="text-center py-4 text-muted">Chưa có câu nào được import. Hãy sang tab Tatoeba Importer để nạp câu.</td></tr>
              ` : sentences.map(s => `
                <tr>
                  <td><span class="badge bg-secondary">#${s.tatoebaId}</span></td>
                  <td class="fw-bold text-dark">${s.text}</td>
                  <td>${s.translation}</td>
                  <td><span class="badge badge-level badge-level-${s.cefrLevel || 'A1'}">${s.cefrLevel || 'A1'}</span></td>
                  <td>
                    <button class="btn-speaker preview-speaker-btn" data-text="${s.text}" data-audio="${s.audioUrl || ''}">
                      <i class="bi bi-volume-up-fill"></i>
                    </button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    this.container.querySelector('#btn-goto-tatoeba')?.addEventListener('click', () => {
      document.querySelector('.admin-nav-item[data-tab="tatoeba"]')?.click();
    });

    this.container.querySelectorAll('.preview-speaker-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const text = e.currentTarget.getAttribute('data-text');
        const audio = e.currentTarget.getAttribute('data-audio');
        sound.speak(text, audio, 'de-DE');
      });
    });
  }

  /* ==============================================================================
     5. SUPABASE SETTINGS & CONNECTION STATUS
     ============================================================================== */
  renderSupabaseSettings() {
    const isConn = supabaseManager.isConnected;

    this.container.innerHTML = `
      <div class="admin-topbar">
        <div>
          <h2 class="fw-bold mb-1">Cấu hình Supabase Backend</h2>
          <p class="text-secondary mb-0">Quản lý kết nối PostgreSQL Database, Row-Level Security (RLS) và Auth.</p>
        </div>
        <span class="badge ${isConn ? 'bg-success' : 'bg-warning text-dark'} p-2 fs-6">
          <i class="bi ${isConn ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'}"></i>
          ${isConn ? 'Đã kết nối Supabase Cloud' : 'Chế độ Local Mock Store'}
        </span>
      </div>

      <div class="row g-4">
        <div class="col-lg-7">
          <div class="gamify-card p-4">
            <h5 class="fw-bold mb-3"><i class="bi bi-key-fill text-primary me-2"></i>Thông tin kết nối Supabase</h5>
            <form id="supabase-config-form">
              <div class="mb-3">
                <label class="form-label fw-bold small">Supabase Project URL</label>
                <input type="url" class="form-control form-control-gamify" id="input-supabase-url" value="${CONFIG.SUPABASE.URL}" placeholder="https://your-project.supabase.co" required>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold small">Supabase Anon Key</label>
                <input type="text" class="form-control form-control-gamify" id="input-supabase-key" value="${CONFIG.SUPABASE.ANON_KEY}" placeholder="eyJhbGciOiJIUzI1NiIsIn..." required>
              </div>
              <button type="submit" class="btn btn-3d btn-3d-primary">
                <i class="bi bi-arrow-repeat"></i> Lưu & Kiểm tra kết nối
              </button>
            </form>
          </div>
        </div>

        <div class="col-lg-5">
          <div class="gamify-card p-4">
            <h5 class="fw-bold mb-2"><i class="bi bi-file-earmark-code-fill text-success me-2"></i>Database Schema</h5>
            <p class="text-secondary small mb-3">File SQL migration hoàn chỉnh với RLS và phân quyền đã được tạo sẵn tại:</p>
            <div class="p-2 bg-body-tertiary rounded font-monospace small mb-3 border">
              sql/schema.sql
            </div>
            <p class="text-secondary small mb-0">
              Chỉ cần copy nội dung file này dán vào <strong>Supabase SQL Editor</strong> để khởi tạo toàn bộ các bảng, RLS và dữ liệu mẫu.
            </p>
          </div>
        </div>
      </div>
    `;

    this.container.querySelector('#supabase-config-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const url = this.container.querySelector('#input-supabase-url').value.trim();
      const key = this.container.querySelector('#input-supabase-key').value.trim();
      supabaseManager.updateCredentials(url, key);
      sound.playSuccess();
      alert('Đã cập nhật thông tin Supabase!');
      this.renderSupabaseSettings();
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new AdminApp();
});

