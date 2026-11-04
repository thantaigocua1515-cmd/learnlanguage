/**
 * LingoLearning - Main Student Application Controller
 * Vanilla ES6 Module Architecture
 */

import { CONFIG } from './config.js';
import { sound } from './services/soundService.js';
import { authService } from './services/authService.js';
import { dataService } from './api/dataService.js';
import { ArticleGame } from './games/articleGame.js';
import { WordScrambleGame } from './games/wordScramble.js';
import { ClozeGame } from './games/clozeGame.js';
import { FlashcardsGame } from './games/flashcards.js';

class App {
  constructor() {
    this.currentLevel = 'A1';
    this.currentGender = 'ALL';
    this.searchQuery = '';
    this.activeGameInstance = null;
    this.container = document.getElementById('main-app-content');

    this.initTheme();
    this.bindGlobalEvents();
    this.updateUserStatsDisplay();
    this.renderLearnView();
  }

  /* ==============================================================================
     THEME (LIGHT / DARK) MANAGEMENT
     ============================================================================== */
  initTheme() {
    const savedTheme = localStorage.getItem('lingo_theme') || 'light';
    this.applyTheme(savedTheme);

    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(nextTheme);
      });
    }
  }

  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('lingo_theme', theme);
    const icon = document.getElementById('theme-toggle-icon');
    if (icon) {
      icon.className = theme === 'dark' ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-stars-fill';
    }
  }

  /* ==============================================================================
     GLOBAL EVENTS & STATS
     ============================================================================== */
  bindGlobalEvents() {
    document.getElementById('nav-brand')?.addEventListener('click', (e) => {
      e.preventDefault();
      this.renderLearnView();
    });

    // Mobile nav triggers
    document.querySelectorAll('.mobile-nav-item[data-nav-target]').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelectorAll('.mobile-nav-item').forEach(el => el.classList.remove('active'));
        item.classList.add('active');

        const target = item.getAttribute('data-nav-target');
        if (target === 'learn') this.renderLearnView();
        if (target === 'games') this.startArticleGame();
        if (target === 'flashcards') this.startFlashcards();
      });
    });
  }

  updateUserStatsDisplay() {
    const user = authService.getUser();
    if (!user) return;

    const streakEl = document.getElementById('nav-streak-count');
    const xpEl = document.getElementById('nav-xp-count');
    const heartsEl = document.getElementById('nav-hearts-count');

    if (streakEl) streakEl.textContent = user.streak || 1;
    if (xpEl) xpEl.textContent = user.xp || 0;
    if (heartsEl) heartsEl.textContent = `${user.hearts || 5}/5`;
  }

  /* ==============================================================================
     MAIN VIEW: LEARN & EXPLORE VOCABULARY
     ============================================================================== */
  async renderLearnView() {
    this.destroyActiveGame();
    this.updateUserStatsDisplay();

    const vocabList = await dataService.getVocabulary({
      level: this.currentLevel,
      gender: this.currentGender,
      search: this.searchQuery
    });

    this.container.innerHTML = `
      <!-- Hero Banner & CEFR Levels Selector -->
      <div class="row align-items-center mb-4 g-3">
        <div class="col-lg-7">
          <h1 class="fw-bold mb-1">Học Tiếng Đức theo Chuẩn CEFR 🇩🇪</h1>
          <p class="text-secondary mb-0">Hệ thống từ vựng, giống từ (der/die/das) và ngữ cảnh câu thực tế từ Tatoeba.</p>
        </div>
        <div class="col-lg-5 text-lg-end">
          <div class="d-inline-flex align-items-center gap-2 p-1 bg-body-tertiary rounded-pill border">
            ${CONFIG.CEFR_LEVELS.map(lvl => `
              <button class="btn btn-sm rounded-pill px-3 fw-bold level-select-btn ${this.currentLevel === lvl.code ? 'btn-primary' : 'btn-light'}" data-level="${lvl.code}">
                ${lvl.code}
              </button>
            `).join('')}
          </div>
        </div>
      </div>

      <!-- Gamified Mini-Games Hub (Quick Action Cards) -->
      <div class="mb-4">
        <div class="d-flex align-items-center justify-content-between mb-3">
          <h4 class="fw-bold mb-0"><i class="bi bi-joystick text-primary me-2"></i>Mini-Games Luyện Tập</h4>
          <span class="badge bg-primary-subtle text-primary border border-primary-subtle">Cấp độ: ${this.currentLevel}</span>
        </div>

        <div class="row g-3">
          <!-- Game 1: Der Die Das Sorter -->
          <div class="col-md-6 col-lg-3">
            <div class="gamify-card p-3 h-100 d-flex flex-column justify-content-between border-top border-4 border-primary">
              <div>
                <div class="d-flex align-items-center justify-content-between mb-2">
                  <span class="badge bg-primary-subtle text-primary"><i class="bi bi-lightning-fill"></i> Phản xạ</span>
                  <span class="text-warning small fw-bold">+10 XP/từ</span>
                </div>
                <h5 class="fw-bold mb-1">Der / Die / Das</h5>
                <p class="text-secondary small mb-3">Luyện phản xạ phân biệt 3 giống danh từ Đức qua thao tác vuốt & phím tắt.</p>
              </div>
              <button class="btn btn-3d btn-3d-primary w-100" id="btn-start-derdiedas">
                <i class="bi bi-play-fill fs-5"></i> Bắt đầu chơi
              </button>
            </div>
          </div>

          <!-- Game 2: Word Scramble -->
          <div class="col-md-6 col-lg-3">
            <div class="gamify-card p-3 h-100 d-flex flex-column justify-content-between border-top border-4 border-success">
              <div>
                <div class="d-flex align-items-center justify-content-between mb-2">
                  <span class="badge bg-success-subtle text-success"><i class="bi bi-puzzle-fill"></i> Giải đố</span>
                  <span class="text-warning small fw-bold">+15 XP/từ</span>
                </div>
                <h5 class="fw-bold mb-1">Xếp Chữ Đoán Từ</h5>
                <p class="text-secondary small mb-3">Ghép nối các chữ cái bị xáo trộn dựa trên ngữ cảnh câu ví dụ Tatoeba.</p>
              </div>
              <button class="btn btn-3d btn-3d-das w-100" id="btn-start-scramble">
                <i class="bi bi-play-fill fs-5"></i> Ghép chữ
              </button>
            </div>
          </div>

          <!-- Game 3: Tatoeba Cloze Test -->
          <div class="col-md-6 col-lg-3">
            <div class="gamify-card p-3 h-100 d-flex flex-column justify-content-between border-top border-4 border-danger">
              <div>
                <div class="d-flex align-items-center justify-content-between mb-2">
                  <span class="badge bg-danger-subtle text-danger"><i class="bi bi-pencil-fill"></i> Điền từ</span>
                  <span class="text-warning small fw-bold">+20 XP/câu</span>
                </div>
                <h5 class="fw-bold mb-1">Điền Khuyết Tatoeba</h5>
                <p class="text-secondary small mb-3">Thử thách điền từ vựng còn thiếu vào câu tiếng Đức thực tế có audio native.</p>
              </div>
              <button class="btn btn-3d btn-3d-die w-100" id="btn-start-cloze">
                <i class="bi bi-play-fill fs-5"></i> Làm bài tập
              </button>
            </div>
          </div>

          <!-- Game 4: SRS Flashcards -->
          <div class="col-md-6 col-lg-3">
            <div class="gamify-card p-3 h-100 d-flex flex-column justify-content-between border-top border-4 border-warning">
              <div>
                <div class="d-flex align-items-center justify-content-between mb-2">
                  <span class="badge bg-warning-subtle text-warning"><i class="bi bi-repeat"></i> SM-2 SRS</span>
                  <span class="text-muted small fw-bold">Ghi nhớ sâu</span>
                </div>
                <h5 class="fw-bold mb-1">Thẻ Ghi Nhớ 3D</h5>
                <p class="text-secondary small mb-3">Lật thẻ 3D hai mặt kèm thuật toán lặp lại ngắt quãng SuperMemo SM-2.</p>
              </div>
              <button class="btn btn-3d btn-3d-warning w-100" id="btn-start-flashcard">
                <i class="bi bi-play-fill fs-5"></i> Lật thẻ
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Vocabulary Explorer Toolbar -->
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
        <div>
          <h4 class="fw-bold mb-0">Kho Từ Vựng [${this.currentLevel}] (${vocabList.length} từ)</h4>
          <span class="text-muted small">Quy ước màu: 
            <span class="badge badge-gender badge-der">der</span> xanh dương, 
            <span class="badge badge-gender badge-die">die</span> đỏ, 
            <span class="badge badge-gender badge-das">das</span> xanh lá
          </span>
        </div>

        <div class="d-flex flex-wrap gap-2">
          <!-- Gender Filter Pills -->
          <div class="btn-group" role="group">
            <button class="btn btn-sm ${this.currentGender === 'ALL' ? 'btn-dark' : 'btn-outline-secondary'} filter-gender-btn" data-gender="ALL">Tất cả</button>
            <button class="btn btn-sm ${this.currentGender === 'der' ? 'btn-3d-der' : 'btn-outline-primary'} filter-gender-btn" data-gender="der">der</button>
            <button class="btn btn-sm ${this.currentGender === 'die' ? 'btn-3d-die' : 'btn-outline-danger'} filter-gender-btn" data-gender="die">die</button>
            <button class="btn btn-sm ${this.currentGender === 'das' ? 'btn-3d-das' : 'btn-outline-success'} filter-gender-btn" data-gender="das">das</button>
          </div>

          <!-- Search Input -->
          <div class="input-group" style="width: 240px;">
            <span class="input-group-text bg-body-tertiary border-end-0"><i class="bi bi-search"></i></span>
            <input type="text" class="form-control form-control-gamify border-start-0" id="vocab-search-input" placeholder="Tìm từ hoặc nghĩa..." value="${this.searchQuery}">
          </div>
        </div>
      </div>

      <!-- Vocabulary Card Grid -->
      <div class="row g-3" id="vocab-card-grid">
        ${vocabList.length === 0 ? `
          <div class="col-12 text-center py-5">
            <i class="bi bi-search display-3 text-muted"></i>
            <h5 class="mt-3 text-secondary">Không tìm thấy từ vựng nào khớp với bộ lọc</h5>
          </div>
        ` : vocabList.map(item => `
          <div class="col-md-6 col-lg-4">
            <div class="gamify-card p-3 h-100 card-${item.gender || 'neutral'}-accent">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <div class="d-flex align-items-center gap-2">
                  ${item.gender ? `<span class="badge badge-gender badge-${item.gender}">${item.gender}</span>` : ''}
                  <span class="badge badge-level badge-level-${item.cefr_level || 'A1'}">${item.cefr_level || 'A1'}</span>
                </div>
                <button class="btn-speaker vocab-speaker-btn" data-word="${item.word}" data-audio="${item.audio_url || ''}" title="Nghe phát âm">
                  <i class="bi bi-volume-up-fill"></i>
                </button>
              </div>

              <div class="d-flex align-items-baseline gap-2 mb-1">
                <h4 class="fw-bold mb-0 text-primary">${item.word}</h4>
                <span class="text-muted small font-monospace">${item.ipa || ''}</span>
              </div>

              <div class="fw-bold fs-6 mb-2 text-dark-emphasis">${item.meaning_vi}</div>

              ${item.plural_form ? `
                <div class="small text-muted mb-2">
                  <i class="bi bi-layers me-1"></i> Số nhiều: <strong>${item.plural_form}</strong>
                </div>
              ` : ''}

              ${item.example_de ? `
                <div class="p-2 bg-body-tertiary rounded small text-secondary mt-auto border">
                  <div class="fw-medium">${item.example_de}</div>
                  <div class="text-muted mt-1 fst-italic">${item.example_vi || ''}</div>
                </div>
              ` : ''}
            </div>
          </div>
        `).join('')}
      </div>
    `;

    this.bindLearnViewEvents();
  }

  bindLearnViewEvents() {
    // Level Selection
    this.container.querySelectorAll('.level-select-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        sound.playClick();
        this.currentLevel = e.currentTarget.getAttribute('data-level');
        this.renderLearnView();
      });
    });

    // Gender Filter
    this.container.querySelectorAll('.filter-gender-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        sound.playClick();
        this.currentGender = e.currentTarget.getAttribute('data-gender');
        this.renderLearnView();
      });
    });

    // Search Input with debounce
    const searchInput = this.container.querySelector('#vocab-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.searchQuery = e.target.value.trim();
        this.renderLearnView();
      });
    }

    // Speaker Pronunciation
    this.container.querySelectorAll('.vocab-speaker-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const word = e.currentTarget.getAttribute('data-word');
        const audio = e.currentTarget.getAttribute('data-audio');
        sound.speak(word, audio, 'de-DE');
      });
    });

    // Mini-Game Launches
    this.container.querySelector('#btn-start-derdiedas')?.addEventListener('click', () => this.startArticleGame());
    this.container.querySelector('#btn-start-scramble')?.addEventListener('click', () => this.startWordScramble());
    this.container.querySelector('#btn-start-cloze')?.addEventListener('click', () => this.startClozeGame());
    this.container.querySelector('#btn-start-flashcard')?.addEventListener('click', () => this.startFlashcards());
  }

  destroyActiveGame() {
    if (this.activeGameInstance && typeof this.activeGameInstance.destroy === 'function') {
      this.activeGameInstance.destroy();
    }
    this.activeGameInstance = null;
  }

  /* ==============================================================================
     GAME LAUNCHERS
     ============================================================================== */
  async startArticleGame() {
    const vocabList = await dataService.getVocabulary({ level: this.currentLevel });
    this.destroyActiveGame();
    this.activeGameInstance = new ArticleGame(this.container, vocabList, () => this.renderLearnView());
    this.activeGameInstance.start();
  }

  async startWordScramble() {
    const vocabList = await dataService.getVocabulary({ level: this.currentLevel });
    this.destroyActiveGame();
    this.activeGameInstance = new WordScrambleGame(this.container, vocabList, () => this.renderLearnView());
    this.activeGameInstance.start();
  }

  async startClozeGame() {
    const vocabList = await dataService.getVocabulary({ level: this.currentLevel });
    this.destroyActiveGame();
    this.activeGameInstance = new ClozeGame(this.container, vocabList, () => this.renderLearnView());
    this.activeGameInstance.start();
  }

  async startFlashcards() {
    const vocabList = await dataService.getVocabulary({ level: this.currentLevel });
    this.destroyActiveGame();
    this.activeGameInstance = new FlashcardsGame(this.container, vocabList, () => this.renderLearnView());
    this.activeGameInstance.start();
  }
}

// Instantiate on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  new App();
});

