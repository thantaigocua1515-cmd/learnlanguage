/**
 * LingoLearning - Central Application Controller
 * Modern Menu-based Navigation Architecture (Home, Vocab, Phrases, Games, Exams, Progress, Admin)
 * Strictly Vanilla JS (ES6 Modules) + Bootstrap 5.3 + CSS Variables
 */

import { CONFIG } from './config.js';
import { sound } from './services/soundService.js';
import { authService } from './services/authService.js';
import { progressService } from './services/progressService.js';
import { dataService } from './api/dataService.js';
import { phraseService, PHRASE_CATEGORIES } from './services/phraseService.js';
import { examService } from './services/examService.js';
import { ArticleGame } from './games/articleGame.js';
import { WordScrambleGame } from './games/wordScramble.js';
import { ClozeGame } from './games/clozeGame.js';
import { FlashcardsGame } from './games/flashcards.js';

class App {
  constructor() {
    this.currentTab = 'home';
    this.currentLevel = 'A1';
    this.currentGender = 'ALL';
    this.currentLetter = 'ALL';
    this.searchQuery = '';
    this.activeGameInstance = null;
    this.activeExamState = null;
    this.examTimerInterval = null;

    this.container = document.getElementById('main-app-content');

    this.initTheme();
    this.initAuthUI();
    this.bindNavigationEvents();
    this.bindAuthModalEvents();

    // Render initial view
    this.renderCurrentTab();
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
     AUTHENTICATION & USER PROFILE UI
     ============================================================================== */
  initAuthUI() {
    this.updateUserStatsDisplay();
    this.renderNavAuth();

    // Reactively update Navbar and view whenever user logs in, registers, or logs out
    authService.onAuthChange(() => {
      this.updateUserStatsDisplay();
      this.renderNavAuth();
      this.renderCurrentTab();
    });
  }

  updateUserStatsDisplay() {
    const user = authService.getUser();
    const streakEl = document.getElementById('nav-streak-count');
    const xpEl = document.getElementById('nav-xp-count');
    const heartsEl = document.getElementById('nav-hearts-count');

    if (streakEl) streakEl.textContent = user.streak || 0;
    if (xpEl) xpEl.textContent = user.xp || 0;
    if (heartsEl) heartsEl.textContent = `${user.hearts || 5}/5`;
  }

  renderNavAuth() {
    const authContainer = document.getElementById('nav-auth-container');
    const adminNavTab = document.getElementById('nav-admin-tab');
    if (!authContainer) return;

    const isLoggedIn = authService.isLoggedIn();
    const isAdmin = authService.isAdmin();
    const user = authService.getUser();

    // 1. Control AdminCP visibility: STRICTLY visible only when role is 'admin'
    if (adminNavTab) {
      if (isAdmin) {
        adminNavTab.classList.remove('d-none');
      } else {
        adminNavTab.classList.add('d-none');
      }
    }

    // 2. Render Auth Actions
    if (isLoggedIn) {
      authContainer.innerHTML = `
        <div class="dropdown">
          <button class="btn btn-sm btn-outline-primary dropdown-toggle rounded-pill d-flex align-items-center gap-2 px-3" type="button" data-bs-toggle="dropdown">
            <span class="rounded-circle bg-primary text-white d-inline-flex align-items-center justify-content-center fw-bold" style="width: 24px; height: 24px; font-size: 0.75rem;">
              ${(user.fullName || 'U').charAt(0).toUpperCase()}
            </span>
            <span class="fw-bold d-none d-md-inline" style="max-width: 130px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
              ${user.fullName}
            </span>
            ${isAdmin ? '<span class="badge bg-warning text-dark small">Admin</span>' : '<span class="badge bg-primary-subtle text-primary small">Học viên</span>'}
          </button>
          <ul class="dropdown-menu dropdown-menu-end shadow border-0 mt-2">
            <li class="px-3 py-2 border-bottom">
              <div class="fw-bold text-dark">${user.fullName}</div>
              <div class="small text-muted">${user.email}</div>
            </li>
            <li>
              <a class="dropdown-item py-2" href="#" id="menu-btn-my-progress">
                <i class="bi bi-graph-up-arrow me-2 text-primary"></i> Quá trình học của tôi
              </a>
            </li>
            ${isAdmin ? `
              <li>
                <a class="dropdown-item py-2 text-warning fw-bold" href="admin.html">
                  <i class="bi bi-shield-lock-fill me-2"></i> Bảng quản trị AdminCP
                </a>
              </li>
            ` : ''}
            <li><hr class="dropdown-divider"></li>
            <li>
              <a class="dropdown-item py-2 text-danger" href="#" id="menu-btn-signout">
                <i class="bi bi-box-arrow-right me-2"></i> Đăng xuất
              </a>
            </li>
          </ul>
        </div>
      `;

      document.getElementById('menu-btn-my-progress')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.switchTab('progress');
      });

      document.getElementById('menu-btn-signout')?.addEventListener('click', (e) => {
        e.preventDefault();
        authService.signOut();
      });

    } else {
      // Guest state
      authContainer.innerHTML = `
        <div class="d-flex align-items-center gap-2">
          <button class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-bold" id="nav-btn-login">
            <i class="bi bi-box-arrow-in-right me-1"></i> Đăng nhập
          </button>
          <button class="btn btn-sm btn-3d btn-3d-der rounded-pill px-3 d-none d-sm-inline-flex" id="nav-btn-register">
            Đăng ký
          </button>
        </div>
      `;

      document.getElementById('nav-btn-login')?.addEventListener('click', () => this.openAuthModal('login'));
      document.getElementById('nav-btn-register')?.addEventListener('click', () => this.openAuthModal('register'));
    }
  }

  openAuthModal(defaultTab = 'login') {
    const modalEl = document.getElementById('authModal');
    if (!modalEl) return;

    if (defaultTab === 'register') {
      const regBtn = document.getElementById('tab-register-btn');
      if (regBtn && window.bootstrap) {
        new bootstrap.Tab(regBtn).show();
      }
    } else {
      const loginBtn = document.getElementById('tab-login-btn');
      if (loginBtn && window.bootstrap) {
        new bootstrap.Tab(loginBtn).show();
      }
    }

    if (window.bootstrap) {
      const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
      modal.show();
    }
  }

  bindAuthModalEvents() {
    // 1. Submit Login Form
    document.getElementById('form-login')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const pass = document.getElementById('login-password').value;
      try {
        await authService.signIn(email, pass);
        const modalEl = document.getElementById('authModal');
        if (modalEl && window.bootstrap) {
          bootstrap.Modal.getInstance(modalEl)?.hide();
        }
      } catch (err) {
        alert('Đăng nhập thất bại: ' + (err.message || 'Sai thông tin'));
      }
    });

    // 2. Submit Register Form
    document.getElementById('form-register')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('register-name').value;
      const email = document.getElementById('register-email').value;
      const pass = document.getElementById('register-password').value;
      try {
        await authService.signUp(email, pass, name);
        const modalEl = document.getElementById('authModal');
        if (modalEl && window.bootstrap) {
          bootstrap.Modal.getInstance(modalEl)?.hide();
        }
      } catch (err) {
        alert('Đăng ký thất bại: ' + (err.message || 'Lỗi'));
      }
    });

    // 3. Quick Onboarding Student
    document.getElementById('btn-quick-student')?.addEventListener('click', () => {
      authService.quickLogin('student');
      const modalEl = document.getElementById('authModal');
      if (modalEl && window.bootstrap) {
        bootstrap.Modal.getInstance(modalEl)?.hide();
      }
    });

    // 4. Quick Onboarding Admin
    document.getElementById('btn-quick-admin')?.addEventListener('click', () => {
      authService.quickLogin('admin');
      const modalEl = document.getElementById('authModal');
      if (modalEl && window.bootstrap) {
        bootstrap.Modal.getInstance(modalEl)?.hide();
      }
    });
  }

  /* ==============================================================================
     NAVIGATION MENU EVENTS & TAB SWITCHING
     ============================================================================== */
  bindNavigationEvents() {
    // Brand click -> Home
    document.getElementById('nav-brand')?.addEventListener('click', (e) => {
      e.preventDefault();
      this.switchTab('home');
    });

    // Desktop Nav Menu Tabs
    document.querySelectorAll('#desktop-nav-menu .app-nav-btn[data-tab]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = btn.getAttribute('data-tab');
        this.switchTab(tab);
      });
    });

    // Mobile Bottom Navigation Tabs
    document.querySelectorAll('.mobile-bottom-nav .mobile-nav-item[data-tab]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = btn.getAttribute('data-tab');
        this.switchTab(tab);
      });
    });
  }

  switchTab(tabName) {
    this.destroyActiveGame();
    this.clearIntervalTimer();
    this.currentTab = tabName;

    // Update active class on desktop tabs
    document.querySelectorAll('#desktop-nav-menu .app-nav-btn').forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-tab') === tabName);
    });

    // Update active class on mobile items
    document.querySelectorAll('.mobile-bottom-nav .mobile-nav-item').forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-tab') === tabName);
    });

    // Render active tab content
    this.renderCurrentTab();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  renderCurrentTab() {
    switch (this.currentTab) {
      case 'home':
        this.renderHomeView();
        break;
      case 'vocab':
        this.renderVocabView();
        break;
      case 'phrases':
        this.renderPhrasesView();
        break;
      case 'games':
        this.renderGamesView();
        break;
      case 'exams':
        this.renderExamsView();
        break;
      case 'progress':
        this.renderProgressView();
        break;
      default:
        this.renderHomeView();
    }
  }

  destroyActiveGame() {
    if (this.activeGameInstance && typeof this.activeGameInstance.destroy === 'function') {
      this.activeGameInstance.destroy();
    }
    this.activeGameInstance = null;
  }

  clearIntervalTimer() {
    if (this.examTimerInterval) {
      clearInterval(this.examTimerInterval);
      this.examTimerInterval = null;
    }
  }

  /* ==============================================================================
     VIEW 1: TRANG CHỦ (HOME DASHBOARD & QUICK ACTION HUB)
     ============================================================================== */
  renderHomeView() {
    const user = authService.getUser();
    const isGuest = authService.isGuest();

    this.container.innerHTML = `
      <!-- Welcome Hero Section -->
      <div class="gamify-card p-4 p-md-5 mb-4 position-relative overflow-hidden border-0 text-white" style="background: linear-gradient(135deg, #1e40af, #3b82f6);">
        <div class="row align-items-center position-relative" style="z-index: 2;">
          <div class="col-lg-8">
            <span class="badge bg-white bg-opacity-25 rounded-pill px-3 py-1 mb-2 text-uppercase fw-bold" style="font-size: 0.75rem;">
              🇩🇪 Nền tảng học Tiếng Đức A1–B1
            </span>
            <h1 class="display-6 fw-extrabold mb-2 text-white">
              ${isGuest ? 'Chào mừng bạn đến với LingoLearning!' : `Guten Tag, ${user.fullName}!`}
            </h1>
            <p class="text-white-50 fs-6 mb-4" style="max-width: 600px;">
              Hệ thống 3.315 từ vựng chuẩn CEFR (DWDS & Goethe) tích hợp 7.934 câu ví dụ ngữ cảnh thực tế từ Tatoeba và 4 mini-game tương tác.
            </p>
            <div class="d-flex flex-wrap gap-2">
              <button class="btn btn-light rounded-pill px-4 fw-bold shadow-sm" id="home-btn-start-vocab">
                <i class="bi bi-book-half text-primary me-2"></i> Học từ vựng ngay
              </button>
              <button class="btn btn-outline-light rounded-pill px-4 fw-bold" id="home-btn-play-game">
                <i class="bi bi-joystick me-2"></i> Chơi Minigames
              </button>
            </div>
          </div>
          <div class="col-lg-4 text-center d-none d-lg-block">
            <div class="p-3 bg-white bg-opacity-10 rounded-4 backdrop-blur border border-white border-opacity-25">
              <i class="bi bi-award-fill display-3 text-warning mb-2"></i>
              <div class="fw-bold fs-5 text-white">Chuỗi học tập</div>
              <div class="display-5 fw-extrabold text-warning">${user.streak || 0} Ngày 🔥</div>
              <div class="small text-white-50 mt-1">${user.xp || 0} XP Tích lũy</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Title -->
      <div class="d-flex align-items-center justify-content-between mb-3">
        <h4 class="fw-bold mb-0"><i class="bi bi-grid-fill text-primary me-2"></i>Tính Năng Chính</h4>
        <span class="text-muted small">Khám phá theo danh mục</span>
      </div>

      <!-- 4 Quick-Access Feature Cards -->
      <div class="row g-3 mb-4">
        <!-- Feature 1: Vocabulary Learning -->
        <div class="col-md-6 col-lg-3">
          <div class="gamify-card p-4 h-100 d-flex flex-column justify-content-between border-top border-4 border-primary">
            <div>
              <div class="d-inline-flex align-items-center justify-content-center rounded-3 bg-primary-subtle text-primary mb-3" style="width: 48px; height: 48px;">
                <i class="bi bi-book-half fs-4"></i>
              </div>
              <h5 class="fw-bold mb-1">Học Từ Vựng</h5>
              <p class="text-secondary small mb-3">Lọc theo chữ cái A–Z, giống từ (der/die/das). Nhấn vào từ để xem 3–5 câu ví dụ minh họa.</p>
            </div>
            <button class="btn btn-3d btn-3d-der w-100" id="card-nav-vocab">
              <i class="bi bi-arrow-right-circle me-1"></i> Khám phá từ vựng
            </button>
          </div>
        </div>

        <!-- Feature 2: Common Phrases -->
        <div class="col-md-6 col-lg-3">
          <div class="gamify-card p-4 h-100 d-flex flex-column justify-content-between border-top border-4 border-success">
            <div>
              <div class="d-inline-flex align-items-center justify-content-center rounded-3 bg-success-subtle text-success mb-3" style="width: 48px; height: 48px;">
                <i class="bi bi-chat-quote-fill fs-4"></i>
              </div>
              <h5 class="fw-bold mb-1">Câu Thông Dụng</h5>
              <p class="text-secondary small mb-3">Các mẫu câu đàm thoại đời sống: Chào hỏi, Mua sắm, Du lịch, Khách sạn kèm phát âm native.</p>
            </div>
            <button class="btn btn-3d btn-3d-das w-100" id="card-nav-phrases">
              <i class="bi bi-arrow-right-circle me-1"></i> Xem câu mẫu
            </button>
          </div>
        </div>

        <!-- Feature 3: Minigames Hub -->
        <div class="col-md-6 col-lg-3">
          <div class="gamify-card p-4 h-100 d-flex flex-column justify-content-between border-top border-4 border-danger">
            <div>
              <div class="d-inline-flex align-items-center justify-content-center rounded-3 bg-danger-subtle text-danger mb-3" style="width: 48px; height: 48px;">
                <i class="bi bi-joystick fs-4"></i>
              </div>
              <h5 class="fw-bold mb-1">Minigames Luyện Tập</h5>
              <p class="text-secondary small mb-3">4 trò chơi: Phản xạ Der/Die/Das, Xếp chữ Scramble, Điền khuyết Cloze, và Thẻ ghi nhớ 3D SRS.</p>
            </div>
            <button class="btn btn-3d btn-3d-die w-100" id="card-nav-games">
              <i class="bi bi-play-circle me-1"></i> Vào phòng game
            </button>
          </div>
        </div>

        <!-- Feature 4: Mock Tests & Exams -->
        <div class="col-md-6 col-lg-3">
          <div class="gamify-card p-4 h-100 d-flex flex-column justify-content-between border-top border-4 border-warning">
            <div>
              <div class="d-inline-flex align-items-center justify-content-center rounded-3 bg-warning-subtle text-warning mb-3" style="width: 48px; height: 48px;">
                <i class="bi bi-patch-question-fill fs-4"></i>
              </div>
              <h5 class="fw-bold mb-1">Thi Thử Theo Level</h5>
              <p class="text-secondary small mb-3">Đề thi trắc nghiệm chuẩn CEFR A1, A2, B1 có đồng hồ bấm giờ, chấm điểm tự động và đề thi AI.</p>
            </div>
            <button class="btn btn-3d btn-3d-warning w-100" id="card-nav-exams">
              <i class="bi bi-pencil-square me-1"></i> Làm bài thi thử
            </button>
          </div>
        </div>
      </div>

      <!-- Quick Learning Stats & CEFR Breakdown -->
      <div class="row g-3">
        <div class="col-lg-8">
          <div class="gamify-card p-4 h-100">
            <h5 class="fw-bold mb-3"><i class="bi bi-bar-chart-fill text-primary me-2"></i>Lộ Trình Cấp Độ Khung Chuẩn CEFR</h5>
            <div class="row g-3">
              <div class="col-md-4">
                <div class="p-3 rounded bg-body-tertiary border text-center">
                  <span class="badge badge-level badge-level-A1 fs-6 mb-2">A1</span>
                  <div class="fw-bold">847 Từ Vựng</div>
                  <div class="small text-muted">Khởi đầu & Đời sống</div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="p-3 rounded bg-body-tertiary border text-center">
                  <span class="badge badge-level badge-level-A2 fs-6 mb-2">A2</span>
                  <div class="fw-bold">616 Từ Vựng</div>
                  <div class="small text-muted">Giao tiếp & Du lịch</div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="p-3 rounded bg-body-tertiary border text-center">
                  <span class="badge badge-level badge-level-B1 fs-6 mb-2">B1</span>
                  <div class="fw-bold">1.852 Từ Vựng</div>
                  <div class="small text-muted">Trung cấp & Công việc</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="gamify-card p-4 h-100 text-center d-flex flex-column justify-content-between">
            <div>
              <h5 class="fw-bold mb-2">Quy Ước Giống Từ</h5>
              <p class="text-secondary small mb-3">Học nhớ màu sắc trực quan</p>
              <div class="d-flex flex-column gap-2 text-start">
                <div class="p-2 rounded bg-primary-subtle text-primary border border-primary-subtle d-flex justify-content-between align-items-center">
                  <span class="fw-bold">der (Maskulin)</span>
                  <span class="badge bg-primary">Xanh dương</span>
                </div>
                <div class="p-2 rounded bg-danger-subtle text-danger border border-danger-subtle d-flex justify-content-between align-items-center">
                  <span class="fw-bold">die (Feminin)</span>
                  <span class="badge bg-danger">Đỏ san hô</span>
                </div>
                <div class="p-2 rounded bg-success-subtle text-success border border-success-subtle d-flex justify-content-between align-items-center">
                  <span class="fw-bold">das (Neutral)</span>
                  <span class="badge bg-success">Xanh lục</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    // Bind Home View Events
    document.getElementById('home-btn-start-vocab')?.addEventListener('click', () => this.switchTab('vocab'));
    document.getElementById('home-btn-play-game')?.addEventListener('click', () => this.switchTab('games'));
    document.getElementById('card-nav-vocab')?.addEventListener('click', () => this.switchTab('vocab'));
    document.getElementById('card-nav-phrases')?.addEventListener('click', () => this.switchTab('phrases'));
    document.getElementById('card-nav-games')?.addEventListener('click', () => this.switchTab('games'));
    document.getElementById('card-nav-exams')?.addEventListener('click', () => this.switchTab('exams'));
  }

  /* ==============================================================================
     VIEW 2: HỌC TỪ VỰNG (CHỌN CHỮ CÁI A-Z + MODAL 3-5 CÂU VÍ DỤ MINH HỌA)
     ============================================================================== */
  async renderVocabView() {
    this.container.innerHTML = `
      <div class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <div class="mt-2 text-muted">Đang tải kho từ vựng tiếng Đức...</div>
      </div>
    `;

    // Fetch words based on level
    let words = await dataService.getWords({ level: this.currentLevel, limit: 120 });
    if (!words || words.length === 0) {
      words = await dataService.getVocabulary({ level: this.currentLevel });
    }

    // Apply Letter Filter if selected
    if (this.currentLetter && this.currentLetter !== 'ALL') {
      words = words.filter(w => {
        const firstChar = (w.word || w.lemma || '').charAt(0).toUpperCase();
        return firstChar === this.currentLetter;
      });
    }

    // Apply Gender Filter
    if (this.currentGender && this.currentGender !== 'ALL') {
      words = words.filter(w => w.gender === this.currentGender);
    }

    // Apply Search Filter
    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      words = words.filter(w => 
        w.word.toLowerCase().includes(q) || 
        (w.meaning_vi && w.meaning_vi.toLowerCase().includes(q)) ||
        (w.meaning_en && w.meaning_en.toLowerCase().includes(q))
      );
    }

    const alphabetList = ['ALL', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ä', 'Ö', 'Ü'];

    this.container.innerHTML = `
      <!-- Header Toolbar: Levels & Search -->
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-3">
        <div>
          <h2 class="fw-bold mb-1"><i class="bi bi-book-half text-primary me-2"></i>Học Từ Vựng Tiếng Đức</h2>
          <p class="text-secondary small mb-0">Chọn chữ cái đầu để lọc nhanh. <strong>Nhấn vào từ</strong> để xem chi tiết và 3–5 câu ví dụ minh họa.</p>
        </div>

        <!-- CEFR Level Switcher Pills -->
        <div class="d-inline-flex align-items-center gap-1 p-1 bg-body-tertiary rounded-pill border">
          ${CONFIG.CEFR_LEVELS.slice(0, 3).map(lvl => `
            <button class="btn btn-sm rounded-pill px-3 fw-bold vocab-level-btn ${this.currentLevel === lvl.code ? 'btn-primary' : 'btn-light'}" data-level="${lvl.code}">
              ${lvl.code}
            </button>
          `).join('')}
        </div>
      </div>

      <!-- Alphabet Filter Bar (A-Z) -->
      <div class="gamify-card p-2 mb-3">
        <div class="d-flex align-items-center justify-content-between px-2 mb-1">
          <span class="small fw-bold text-muted"><i class="bi bi-sort-alpha-down me-1"></i>Lọc theo chữ cái đầu:</span>
          <span class="badge bg-primary-subtle text-primary">${this.currentLetter === 'ALL' ? 'Tất cả chữ cái' : `Chữ cái: ${this.currentLetter}`}</span>
        </div>
        <div class="alphabet-bar-container">
          ${alphabetList.map(char => `
            <button class="btn-alpha ${this.currentLetter === char ? 'active' : ''}" data-letter="${char}">
              ${char}
            </button>
          `).join('')}
        </div>
      </div>

      <!-- Secondary Filter Row: Gender & Search -->
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-4">
        <!-- Gender Pills -->
        <div class="btn-group" role="group">
          <button class="btn btn-sm ${this.currentGender === 'ALL' ? 'btn-dark' : 'btn-outline-secondary'} vocab-gender-btn" data-gender="ALL">Tất cả giống</button>
          <button class="btn btn-sm ${this.currentGender === 'der' ? 'btn-3d-der' : 'btn-outline-primary'} vocab-gender-btn" data-gender="der">der (đực)</button>
          <button class="btn btn-sm ${this.currentGender === 'die' ? 'btn-3d-die' : 'btn-outline-danger'} vocab-gender-btn" data-gender="die">die (cái)</button>
          <button class="btn btn-sm ${this.currentGender === 'das' ? 'btn-3d-das' : 'btn-outline-success'} vocab-gender-btn" data-gender="das">das (trung)</button>
        </div>

        <!-- Search Input -->
        <div class="input-group" style="width: 260px;">
          <span class="input-group-text bg-body-tertiary border-end-0"><i class="bi bi-search"></i></span>
          <input type="text" class="form-control form-control-gamify border-start-0" id="vocab-search-field" placeholder="Tìm kiếm từ vựng..." value="${this.searchQuery}">
        </div>
      </div>

      <!-- Vocabulary Card Grid -->
      <div class="row g-3" id="vocab-word-grid">
        ${words.length === 0 ? `
          <div class="col-12 text-center py-5">
            <i class="bi bi-inbox display-3 text-muted"></i>
            <h5 class="mt-3 text-secondary">Không tìm thấy từ vựng nào khớp với bộ lọc "${this.currentLetter}"</h5>
            <button class="btn btn-sm btn-outline-primary rounded-pill mt-2" id="btn-reset-filters">Đặt lại bộ lọc</button>
          </div>
        ` : words.map(item => `
          <div class="col-md-6 col-lg-4">
            <div class="gamify-card p-3 h-100 card-${item.gender || 'neutral'}-accent word-clickable-card" data-lemma="${item.word}" style="cursor: pointer;">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <div class="d-flex align-items-center gap-1">
                  ${item.gender ? `<span class="badge badge-gender badge-${item.gender}">${item.gender}</span>` : ''}
                  <span class="badge badge-level badge-level-${item.cefr_level || 'A1'}">${item.cefr_level || 'A1'}</span>
                  <span class="badge bg-secondary-subtle text-secondary small" style="font-size: 0.72rem;">${item.pos || 'noun'}</span>
                </div>
                <button class="btn-speaker vocab-speaker-btn" data-speak="${item.word}" title="Nghe phát âm">
                  <i class="bi bi-volume-up-fill"></i>
                </button>
              </div>

              <div class="d-flex align-items-baseline gap-2 mb-1">
                <h4 class="fw-bold mb-0 text-primary">${item.word}</h4>
                <span class="text-muted small font-monospace">${item.ipa || ''}</span>
              </div>

              <div class="fw-medium small text-dark-emphasis mb-2">${item.meaning_vi || item.meaning_en || 'Đang cập nhật'}</div>

              ${item.plural_form ? `
                <div class="small text-muted mb-2">
                  <i class="bi bi-layers me-1"></i> Số nhiều: <strong>${item.plural_form}</strong>
                </div>
              ` : ''}

              <!-- Click hint badge -->
              <div class="mt-auto pt-2 border-top d-flex align-items-center justify-content-between text-muted small">
                <span><i class="bi bi-chat-left-text me-1 text-primary"></i>${item.examples?.length || (item.example_de ? 1 : '3-5')} câu ví dụ</span>
                <span class="text-primary fw-bold">Chi tiết <i class="bi bi-chevron-right"></i></span>
              </div>
            </div>
          </div>
        `).join('')}
      </div>
    `;

    this.bindVocabViewEvents();
  }

  bindVocabViewEvents() {
    // 1. Level Switcher
    this.container.querySelectorAll('.vocab-level-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.currentLevel = btn.getAttribute('data-level');
        this.renderVocabView();
      });
    });

    // 2. Alphabet Filter (A-Z)
    this.container.querySelectorAll('.btn-alpha').forEach(btn => {
      btn.addEventListener('click', () => {
        this.currentLetter = btn.getAttribute('data-letter');
        this.renderVocabView();
      });
    });

    // 3. Gender Filter
    this.container.querySelectorAll('.vocab-gender-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.currentGender = btn.getAttribute('data-gender');
        this.renderVocabView();
      });
    });

    // 4. Search Filter
    const searchField = document.getElementById('vocab-search-field');
    if (searchField) {
      searchField.addEventListener('input', (e) => {
        this.searchQuery = e.target.value.trim();
        // debounce simple re-render
        clearTimeout(this._searchTimer);
        this._searchTimer = setTimeout(() => this.renderVocabView(), 300);
      });
    }

    // 5. Reset Filters
    document.getElementById('btn-reset-filters')?.addEventListener('click', () => {
      this.currentLetter = 'ALL';
      this.currentGender = 'ALL';
      this.searchQuery = '';
      this.renderVocabView();
    });

    // 6. Click on Card -> Open Word Detail Modal with 3-5 examples
    this.container.querySelectorAll('.word-clickable-card').forEach(card => {
      card.addEventListener('click', (e) => {
        if (e.target.closest('.vocab-speaker-btn')) return; // Ignore speaker click
        const lemma = card.getAttribute('data-lemma');
        this.openWordDetailModal(lemma);
      });
    });

    // 7. Speaker button
    this.container.querySelectorAll('.vocab-speaker-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const text = btn.getAttribute('data-speak');
        sound.speak(text);
      });
    });
  }

  /**
   * Word Detail Modal: Displays word info + 3-5 example sentences.
   * GUEST GATEWAY: If user is Guest -> blur examples & show Login/Register requirement.
   */
  async openWordDetailModal(lemma) {
    const modalEl = document.getElementById('wordDetailModal');
    const modalBody = document.getElementById('word-detail-modal-body');
    if (!modalEl || !modalBody) return;

    modalBody.innerHTML = `
      <div class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-primary"></div>
        <div class="small text-muted mt-2">Đang tải câu ví dụ minh họa...</div>
      </div>
    `;

    if (window.bootstrap) {
      bootstrap.Modal.getOrCreateInstance(modalEl).show();
    }

    // Query word and examples
    const word = await dataService.getWordByLemma(lemma);
    let examples = await dataService.getWordExamples(lemma);

    // If no examples returned from direct query, fallback to word object examples
    if (!examples || examples.length === 0) {
      examples = word?.examples || [];
    }

    // Format examples
    const formattedExamples = examples.slice(0, 5).map(ex => ({
      de: ex.sentence_de || ex.de,
      vi: ex.translation_vi || ex.vi || 'Bản dịch đang được cập nhật',
      source: ex.source || 'tatoeba',
      tatoebaId: ex.tatoeba_id || null
    }));

    // Header badges
    document.getElementById('modal-word-badge-gender').className = `badge badge-gender badge-${word?.gender || 'der'}`;
    document.getElementById('modal-word-badge-gender').textContent = word?.gender || 'der';
    document.getElementById('modal-word-badge-level').textContent = word?.cefr_level || this.currentLevel;
    document.getElementById('modal-word-pos').textContent = word?.pos || 'noun';

    const isGuest = authService.isGuest();

    modalBody.innerHTML = `
      <!-- Word Main Info Header -->
      <div class="word-detail-header d-flex justify-content-between align-items-center">
        <div>
          <div class="d-flex align-items-baseline gap-2">
            <h2 class="display-6 fw-bold mb-0 text-primary">${word?.word || lemma}</h2>
            <span class="text-muted fs-6 font-monospace">${word?.ipa || ''}</span>
          </div>
          <div class="fs-5 fw-bold text-dark-emphasis mt-1">${word?.meaning_vi || word?.meaning_en || 'Đang cập nhật'}</div>
          ${word?.plural_form ? `<div class="small text-muted mt-1"><i class="bi bi-layers me-1"></i> Số nhiều: <strong>${word.plural_form}</strong></div>` : ''}
        </div>
        <button class="btn btn-3d btn-3d-primary rounded-circle" id="modal-speaker-main-btn" title="Nghe phát âm từ này" style="width: 48px; height: 48px;">
          <i class="bi bi-volume-up-fill fs-5"></i>
        </button>
      </div>

      <!-- Forms / Conjugation preview if present -->
      ${word?.forms && word.forms.length > 0 ? `
        <div class="mb-3">
          <span class="small fw-bold text-muted">Các dạng biến hình (Forms):</span>
          <div class="d-flex flex-wrap gap-1 mt-1">
            ${word.forms.slice(0, 8).map(f => `<span class="badge bg-body-tertiary text-secondary border">${f}</span>`).join('')}
          </div>
        </div>
      ` : ''}

      <!-- 3-5 Example Sentences Section -->
      <div class="mb-2">
        <div class="d-flex align-items-center justify-content-between mb-2">
          <h5 class="fw-bold mb-0">
            <i class="bi bi-chat-square-quote-fill text-primary me-2"></i>Câu Ví Dụ Minh Họa (${formattedExamples.length} câu)
          </h5>
          <span class="badge bg-primary-subtle text-primary">Nguồn: Tatoeba</span>
        </div>

        ${isGuest ? `
          <!-- GUEST GATEWAY LOCK OVERLAY -->
          <div class="guest-lock-container">
            <!-- Blurred Mockup content -->
            <div class="guest-lock-blur">
              <div class="p-3 mb-2 bg-body-tertiary rounded border">
                <div class="fw-bold">Das ist ein wunderschönes deutsches Beispiel.</div>
                <div class="text-muted small">Đây là một câu ví dụ tiếng Đức rất tuyệt vời.</div>
              </div>
              <div class="p-3 bg-body-tertiary rounded border">
                <div class="fw-bold">Ich lerne jeden Tag neue Wörter mit Beispielen.</div>
                <div class="text-muted small">Tôi học từ mới mỗi ngày kèm theo các câu ví dụ.</div>
              </div>
            </div>

            <!-- Lock CTA Overlay -->
            <div class="guest-lock-overlay">
              <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-primary text-white mb-2" style="width: 44px; height: 44px;">
                <i class="bi bi-lock-fill fs-5"></i>
              </div>
              <h5 class="fw-bold mb-1 text-dark">Mở Khóa Câu Ví Dụ Minh Họa</h5>
              <p class="text-secondary small mb-3" style="max-width: 420px;">
                Câu ví dụ ngữ cảnh thực tế kèm bản dịch tiếng Việt và phát âm audio native chỉ dành cho thành viên đã đăng nhập.
              </p>
              <div class="d-flex gap-2">
                <button class="btn btn-sm btn-3d btn-3d-primary px-3" id="modal-guest-login-btn">
                  <i class="bi bi-box-arrow-in-right me-1"></i> Đăng nhập ngay
                </button>
                <button class="btn btn-sm btn-outline-secondary rounded-pill px-3" id="modal-guest-register-btn">
                  Đăng ký miễn phí
                </button>
              </div>
            </div>
          </div>
        ` : `
          <!-- LOGGED IN: FULL 3-5 EXAMPLES -->
          <div class="d-flex flex-column gap-2">
            ${formattedExamples.length === 0 ? `
              <div class="p-3 bg-body-tertiary rounded text-muted small text-center">
                Chưa có câu ví dụ Tatoeba cho từ này trong kho dữ liệu.
              </div>
            ` : formattedExamples.map((ex, idx) => `
              <div class="p-3 bg-body-tertiary rounded border d-flex justify-content-between align-items-start gap-2">
                <div>
                  <div class="fw-bold text-dark fs-6">${ex.de}</div>
                  <div class="text-secondary small mt-1">${ex.vi}</div>
                  ${ex.tatoebaId ? `<span class="badge bg-light text-muted border mt-2" style="font-size: 0.68rem;">Tatoeba ID: #${ex.tatoebaId}</span>` : ''}
                </div>
                <button class="btn-speaker modal-ex-speaker-btn flex-shrink-0" data-speak="${ex.de}" title="Nghe phát âm câu này">
                  <i class="bi bi-volume-up-fill"></i>
                </button>
              </div>
            `).join('')}
          </div>
        `}
      </div>
    `;

    // Bind Speaker in Modal
    document.getElementById('modal-speaker-main-btn')?.addEventListener('click', () => {
      sound.speak(word?.word || lemma);
    });

    modalBody.querySelectorAll('.modal-ex-speaker-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const text = btn.getAttribute('data-speak');
        sound.speak(text);
      });
    });

    // Guest Auth CTA buttons
    document.getElementById('modal-guest-login-btn')?.addEventListener('click', () => {
      if (window.bootstrap) bootstrap.Modal.getInstance(modalEl)?.hide();
      this.openAuthModal('login');
    });

    document.getElementById('modal-guest-register-btn')?.addEventListener('click', () => {
      if (window.bootstrap) bootstrap.Modal.getInstance(modalEl)?.hide();
      this.openAuthModal('register');
    });
  }

  /* ==============================================================================
     VIEW 3: CÂU THÔNG DỤNG (PHRASEBOOK THEO CHỦ ĐỀ & LEVEL)
     ============================================================================== */
  renderPhrasesView() {
    const categories = PHRASE_CATEGORIES;
    if (!this.currentPhraseCategory) this.currentPhraseCategory = 'all';

    const phrases = phraseService.getPhrases({
      category: this.currentPhraseCategory,
      level: this.currentLevel
    });

    this.container.innerHTML = `
      <!-- Header -->
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
        <div>
          <h2 class="fw-bold mb-1"><i class="bi bi-chat-quote-fill text-success me-2"></i>Các Câu Tiếng Đức Thông Dụng</h2>
          <p class="text-secondary small mb-0">Tuyển tập các mẫu câu giao tiếp đời sống thực tế kèm bản dịch tiếng Việt và phát âm native.</p>
        </div>

        <!-- Level Selector -->
        <div class="d-inline-flex align-items-center gap-1 p-1 bg-body-tertiary rounded-pill border">
          <button class="btn btn-sm rounded-pill px-3 fw-bold phrase-level-btn ${this.currentLevel === 'ALL' ? 'btn-dark' : 'btn-light'}" data-level="ALL">Tất cả</button>
          <button class="btn btn-sm rounded-pill px-3 fw-bold phrase-level-btn ${this.currentLevel === 'A1' ? 'btn-primary' : 'btn-light'}" data-level="A1">A1</button>
          <button class="btn btn-sm rounded-pill px-3 fw-bold phrase-level-btn ${this.currentLevel === 'A2' ? 'btn-primary' : 'btn-light'}" data-level="A2">A2</button>
          <button class="btn btn-sm rounded-pill px-3 fw-bold phrase-level-btn ${this.currentLevel === 'B1' ? 'btn-primary' : 'btn-light'}" data-level="B1">B1</button>
        </div>
      </div>

      <!-- Categories Pills -->
      <div class="d-flex flex-wrap gap-2 mb-4">
        ${categories.map(cat => `
          <button class="btn btn-sm rounded-pill px-3 phrase-cat-btn ${this.currentPhraseCategory === cat.id ? 'btn-success fw-bold text-white' : 'btn-outline-secondary'}" data-cat="${cat.id}">
            <i class="bi ${cat.icon} me-1"></i> ${cat.name}
          </button>
        `).join('')}
      </div>

      <!-- Phrases List -->
      <div class="row g-3">
        ${phrases.length === 0 ? `
          <div class="col-12 text-center py-5">
            <i class="bi bi-chat-dots display-3 text-muted"></i>
            <h5 class="mt-3 text-secondary">Không có câu mẫu nào trong danh mục này</h5>
          </div>
        ` : phrases.map(p => `
          <div class="col-md-6">
            <div class="gamify-card p-3 h-100 d-flex justify-content-between align-items-start gap-3">
              <div>
                <div class="d-flex align-items-center gap-2 mb-2">
                  <span class="badge badge-level badge-level-${p.level}">${p.level}</span>
                  <span class="badge bg-secondary-subtle text-secondary small">${p.context || 'Đàm thoại'}</span>
                </div>
                <h5 class="fw-bold text-primary mb-1">${p.de}</h5>
                <p class="text-secondary mb-0">${p.vi}</p>
              </div>

              <button class="btn-speaker phrase-speaker-btn flex-shrink-0" data-speak="${p.de}" title="Nghe phát âm">
                <i class="bi bi-volume-up-fill"></i>
              </button>
            </div>
          </div>
        `).join('')}
      </div>
    `;

    // Category click
    this.container.querySelectorAll('.phrase-cat-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.currentPhraseCategory = btn.getAttribute('data-cat');
        this.renderPhrasesView();
      });
    });

    // Level click
    this.container.querySelectorAll('.phrase-level-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.currentLevel = btn.getAttribute('data-level');
        this.renderPhrasesView();
      });
    });

    // Speaker buttons
    this.container.querySelectorAll('.phrase-speaker-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const text = btn.getAttribute('data-speak');
        sound.speak(text);
      });
    });
  }

  /* ==============================================================================
     VIEW 4: MINIGAMES ARCADE HUB
     ============================================================================== */
  renderGamesView() {
    this.container.innerHTML = `
      <!-- Header -->
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
        <div>
          <h2 class="fw-bold mb-1"><i class="bi bi-joystick text-danger me-2"></i>Khu Trò Chơi Luyện Tập (Minigames)</h2>
          <p class="text-secondary small mb-0">Học từ vựng thông qua trò chơi giải đố, phản xạ màu sắc và thẻ lật Spaced Repetition SM-2.</p>
        </div>

        <span class="badge bg-danger-subtle text-danger border border-danger-subtle px-3 py-2 fw-bold">
          Cấp độ hiện tại: ${this.currentLevel}
        </span>
      </div>

      <!-- Games Grid -->
      <div class="row g-4 mb-4">
        <!-- Game 1: Der Die Das Sorter -->
        <div class="col-md-6 col-lg-3">
          <div class="gamify-card p-4 h-100 d-flex flex-column justify-content-between border-top border-4 border-primary">
            <div>
              <div class="d-flex justify-content-between align-items-center mb-3">
                <span class="badge bg-primary-subtle text-primary"><i class="bi bi-lightning-fill"></i> Phản xạ</span>
                <span class="text-warning fw-bold small">+10 XP</span>
              </div>
              <h4 class="fw-bold mb-2">Der / Die / Das</h4>
              <p class="text-secondary small mb-4">Luyện phản xạ ghi nhớ giống danh từ qua thao tác vuốt thẻ hoặc phím bấm 1, 2, 3.</p>
            </div>
            <button class="btn btn-3d btn-3d-der w-100" id="btn-launch-article">
              <i class="bi bi-play-fill fs-5"></i> Bắt đầu chơi
            </button>
          </div>
        </div>

        <!-- Game 2: Word Scramble -->
        <div class="col-md-6 col-lg-3">
          <div class="gamify-card p-4 h-100 d-flex flex-column justify-content-between border-top border-4 border-success">
            <div>
              <div class="d-flex justify-content-between align-items-center mb-3">
                <span class="badge bg-success-subtle text-success"><i class="bi bi-puzzle-fill"></i> Giải đố</span>
                <span class="text-warning fw-bold small">+15 XP</span>
              </div>
              <h4 class="fw-bold mb-2">Xếp Chữ Đoán Từ</h4>
              <p class="text-secondary small mb-4">Ghép nối các ký tự bị xáo trộn dựa trên gợi ý ngữ cảnh câu ví dụ Tatoeba.</p>
            </div>
            <button class="btn btn-3d btn-3d-das w-100" id="btn-launch-scramble">
              <i class="bi bi-play-fill fs-5"></i> Bắt đầu chơi
            </button>
          </div>
        </div>

        <!-- Game 3: Cloze Test -->
        <div class="col-md-6 col-lg-3">
          <div class="gamify-card p-4 h-100 d-flex flex-column justify-content-between border-top border-4 border-danger">
            <div>
              <div class="d-flex justify-content-between align-items-center mb-3">
                <span class="badge bg-danger-subtle text-danger"><i class="bi bi-pencil-fill"></i> Điền từ</span>
                <span class="text-warning fw-bold small">+20 XP</span>
              </div>
              <h4 class="fw-bold mb-2">Điền Khuyết Tatoeba</h4>
              <p class="text-secondary small mb-4">Thử thách điền từ vựng còn thiếu vào câu tiếng Đức thực tế có audio native.</p>
            </div>
            <button class="btn btn-3d btn-3d-die w-100" id="btn-launch-cloze">
              <i class="bi bi-play-fill fs-5"></i> Bắt đầu chơi
            </button>
          </div>
        </div>

        <!-- Game 4: SRS Flashcards -->
        <div class="col-md-6 col-lg-3">
          <div class="gamify-card p-4 h-100 d-flex flex-column justify-content-between border-top border-4 border-warning">
            <div>
              <div class="d-flex justify-content-between align-items-center mb-3">
                <span class="badge bg-warning-subtle text-warning"><i class="bi bi-repeat"></i> SM-2 SRS</span>
                <span class="text-warning fw-bold small">+10 XP</span>
              </div>
              <h4 class="fw-bold mb-2">Thẻ Ghi Nhớ 3D</h4>
              <p class="text-secondary small mb-4">Lật thẻ 3D hai mặt kết hợp thuật toán lặp lại ngắt quãng SuperMemo SM-2.</p>
            </div>
            <button class="btn btn-3d btn-3d-warning w-100" id="btn-launch-flashcards">
              <i class="bi bi-play-fill fs-5"></i> Bắt đầu chơi
            </button>
          </div>
        </div>
      </div>
    `;

    document.getElementById('btn-launch-article')?.addEventListener('click', () => this.startArticleGame());
    document.getElementById('btn-launch-scramble')?.addEventListener('click', () => this.startWordScramble());
    document.getElementById('btn-launch-cloze')?.addEventListener('click', () => this.startClozeGame());
    document.getElementById('btn-launch-flashcards')?.addEventListener('click', () => this.startFlashcards());
  }

  async startArticleGame() {
    this.container.innerHTML = `<div id="game-active-container"></div>`;
    const vocab = await dataService.getWords({ level: this.currentLevel, limit: 100 });
    this.activeGameInstance = new ArticleGame(
      document.getElementById('game-active-container'),
      vocab,
      () => this.switchTab('games')
    );
  }

  async startWordScramble() {
    this.container.innerHTML = `<div id="game-active-container"></div>`;
    const vocab = await dataService.getWords({ level: this.currentLevel, limit: 100 });
    this.activeGameInstance = new WordScrambleGame(
      document.getElementById('game-active-container'),
      vocab,
      () => this.switchTab('games')
    );
  }

  async startClozeGame() {
    this.container.innerHTML = `<div id="game-active-container"></div>`;
    const vocab = await dataService.getWords({ level: this.currentLevel, limit: 100 });
    this.activeGameInstance = new ClozeGame(
      document.getElementById('game-active-container'),
      vocab,
      () => this.switchTab('games')
    );
  }

  async startFlashcards() {
    this.container.innerHTML = `<div id="game-active-container"></div>`;
    const vocab = await dataService.getWords({ level: this.currentLevel, limit: 100 });
    this.activeGameInstance = new FlashcardsGame(
      document.getElementById('game-active-container'),
      vocab,
      () => this.switchTab('games')
    );
  }

  /* ==============================================================================
     VIEW 5: THI THỬ THEO LEVEL (MOCK EXAMS & TIMER & RESULTS)
     ============================================================================== */
  renderExamsView() {
    const exams = examService.getExams(this.currentLevel);

    this.container.innerHTML = `
      <!-- Header -->
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
        <div>
          <h2 class="fw-bold mb-1"><i class="bi bi-patch-question-fill text-warning me-2"></i>Thi Thử Chuẩn Khung CEFR</h2>
          <p class="text-secondary small mb-0">Các bộ đề thi trắc nghiệm bấm giờ theo cấp độ A1, A2, B1 để đánh giá năng lực học tập.</p>
        </div>

        <!-- Level Selector -->
        <div class="d-inline-flex align-items-center gap-1 p-1 bg-body-tertiary rounded-pill border">
          <button class="btn btn-sm rounded-pill px-3 fw-bold exam-lvl-btn ${this.currentLevel === 'A1' ? 'btn-primary' : 'btn-light'}" data-level="A1">A1</button>
          <button class="btn btn-sm rounded-pill px-3 fw-bold exam-lvl-btn ${this.currentLevel === 'A2' ? 'btn-primary' : 'btn-light'}" data-level="A2">A2</button>
          <button class="btn btn-sm rounded-pill px-3 fw-bold exam-lvl-btn ${this.currentLevel === 'B1' ? 'btn-primary' : 'btn-light'}" data-level="B1">B1</button>
        </div>
      </div>

      <!-- Exam List -->
      <div class="row g-3">
        ${exams.map(ex => `
          <div class="col-md-6 col-lg-4">
            <div class="gamify-card p-4 h-100 d-flex flex-column justify-content-between">
              <div>
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <span class="badge badge-level badge-level-${ex.level}">${ex.level}</span>
                  <span class="text-muted small"><i class="bi bi-clock me-1"></i>${ex.durationMinutes} phút</span>
                </div>
                <h5 class="fw-bold mb-2">${ex.title}</h5>
                <p class="text-secondary small mb-3">${ex.description}</p>
                <div class="small text-muted mb-4">
                  <i class="bi bi-question-circle me-1"></i> ${ex.questions.length} câu hỏi trắc nghiệm
                </div>
              </div>

              <button class="btn btn-3d btn-3d-primary w-100 btn-start-exam" data-exam-id="${ex.id}">
                <i class="bi bi-pencil-fill me-1"></i> Bắt đầu thi
              </button>
            </div>
          </div>
        `).join('')}
      </div>
    `;

    this.container.querySelectorAll('.exam-lvl-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.currentLevel = btn.getAttribute('data-level');
        this.renderExamsView();
      });
    });

    this.container.querySelectorAll('.btn-start-exam').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-exam-id');
        this.startExamSession(id);
      });
    });
  }

  /**
   * Active Exam Session Room
   */
  startExamSession(examId) {
    const exam = examService.getExamById(examId);
    if (!exam) return;

    this.activeExamState = {
      exam,
      currentQuestionIdx: 0,
      answers: {},
      remainingSeconds: exam.durationMinutes * 60
    };

    this.renderExamQuestion();

    // Start Timer
    this.clearIntervalTimer();
    this.examTimerInterval = setInterval(() => {
      this.activeExamState.remainingSeconds--;
      const timerEl = document.getElementById('exam-countdown-timer');
      if (timerEl) {
        const m = Math.floor(this.activeExamState.remainingSeconds / 60);
        const s = this.activeExamState.remainingSeconds % 60;
        timerEl.textContent = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
      }

      if (this.activeExamState.remainingSeconds <= 0) {
        this.clearIntervalTimer();
        alert('Hết giờ làm bài!');
        this.finishExamSession();
      }
    }, 1000);
  }

  renderExamQuestion() {
    const { exam, currentQuestionIdx, answers, remainingSeconds } = this.activeExamState;
    const q = exam.questions[currentQuestionIdx];
    const totalQ = exam.questions.length;
    const selectedAnswer = answers[q.id];

    const m = Math.floor(remainingSeconds / 60);
    const s = remainingSeconds % 60;
    const timerStr = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;

    this.container.innerHTML = `
      <!-- Exam Room Header -->
      <div class="gamify-card p-3 mb-4 d-flex justify-content-between align-items-center">
        <div>
          <span class="badge badge-level badge-level-${exam.level} me-2">${exam.level}</span>
          <strong class="d-none d-md-inline">${exam.title}</strong>
        </div>
        <div class="d-flex align-items-center gap-3">
          <div class="badge bg-danger-subtle text-danger fs-6 px-3 py-2 border border-danger-subtle">
            <i class="bi bi-stopwatch-fill me-1"></i> <span id="exam-countdown-timer">${timerStr}</span>
          </div>
          <button class="btn btn-sm btn-outline-secondary rounded-pill" id="btn-quit-exam">Thoát</button>
        </div>
      </div>

      <!-- Question Card -->
      <div class="gamify-card p-4 p-md-5 mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <span class="small fw-bold text-muted text-uppercase">Câu hỏi ${currentQuestionIdx + 1} / ${totalQ}</span>
          <div class="progress w-25" style="height: 6px;">
            <div class="progress-bar bg-primary" style="width: ${((currentQuestionIdx + 1) / totalQ) * 100}%"></div>
          </div>
        </div>

        <h4 class="fw-bold mb-4 text-dark">${q.question}</h4>

        <!-- Options -->
        <div class="d-flex flex-column gap-2 mb-4">
          ${q.options.map((opt, i) => {
            const letter = ['A', 'B', 'C', 'D'][i];
            const isSelected = selectedAnswer === opt;
            return `
              <div class="exam-option-btn ${isSelected ? 'selected' : ''}" data-answer="${opt}">
                <div class="exam-option-key">${letter}</div>
                <div>${opt}</div>
              </div>
            `;
          }).join('')}
        </div>

        <!-- Navigation buttons -->
        <div class="d-flex justify-content-between align-items-center pt-3 border-top">
          <button class="btn btn-outline-secondary rounded-pill px-4" id="btn-prev-q" ${currentQuestionIdx === 0 ? 'disabled' : ''}>
            <i class="bi bi-chevron-left me-1"></i> Câu trước
          </button>

          ${currentQuestionIdx === totalQ - 1 ? `
            <button class="btn btn-3d btn-3d-primary px-4" id="btn-finish-exam">
              <i class="bi bi-check-circle-fill me-1"></i> Nộp bài thi
            </button>
          ` : `
            <button class="btn btn-3d btn-3d-primary px-4" id="btn-next-q">
              Câu tiếp <i class="bi bi-chevron-right ms-1"></i>
            </button>
          `}
        </div>
      </div>
    `;

    // Bind Option Selection
    this.container.querySelectorAll('.exam-option-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const ans = btn.getAttribute('data-answer');
        this.activeExamState.answers[q.id] = ans;
        this.renderExamQuestion();
      });
    });

    document.getElementById('btn-prev-q')?.addEventListener('click', () => {
      if (this.activeExamState.currentQuestionIdx > 0) {
        this.activeExamState.currentQuestionIdx--;
        this.renderExamQuestion();
      }
    });

    document.getElementById('btn-next-q')?.addEventListener('click', () => {
      if (this.activeExamState.currentQuestionIdx < totalQ - 1) {
        this.activeExamState.currentQuestionIdx++;
        this.renderExamQuestion();
      }
    });

    document.getElementById('btn-finish-exam')?.addEventListener('click', () => {
      if (confirm('Bạn có chắc chắn muốn nộp bài thi?')) {
        this.finishExamSession();
      }
    });

    document.getElementById('btn-quit-exam')?.addEventListener('click', () => {
      if (confirm('Bạn có chắc chắn muốn thoát khỏi bài thi hiện tại?')) {
        this.clearIntervalTimer();
        this.switchTab('exams');
      }
    });
  }

  finishExamSession() {
    this.clearIntervalTimer();
    const { exam, answers } = this.activeExamState;
    const result = examService.submitExamResult(exam.id, answers);
    this.renderExamResult(result);
  }

  renderExamResult(result) {
    this.container.innerHTML = `
      <div class="gamify-card p-4 p-md-5 text-center mb-4">
        <div class="d-inline-flex align-items-center justify-content-center rounded-circle ${result.passed ? 'bg-success-subtle text-success' : 'bg-danger-subtle text-danger'} mb-3" style="width: 80px; height: 80px;">
          <i class="bi ${result.passed ? 'bi-trophy-fill' : 'bi-x-circle-fill'} display-4"></i>
        </div>

        <h2 class="fw-bold mb-1">${result.passed ? 'Chúc mừng bạn đã vượt qua bài thi!' : 'Chưa đạt! Cần luyện tập thêm.'}</h2>
        <p class="text-secondary mb-4">${result.examTitle} (Trình độ: ${result.level})</p>

        <div class="row g-3 justify-content-center mb-4" style="max-width: 600px; margin: 0 auto;">
          <div class="col-4">
            <div class="p-3 rounded bg-body-tertiary border">
              <div class="display-6 fw-bold text-primary">${result.scorePct}%</div>
              <div class="small text-muted">Điểm số</div>
            </div>
          </div>
          <div class="col-4">
            <div class="p-3 rounded bg-body-tertiary border">
              <div class="display-6 fw-bold text-success">${result.correctCount}/${result.totalQuestions}</div>
              <div class="small text-muted">Số câu đúng</div>
            </div>
          </div>
          <div class="col-4">
            <div class="p-3 rounded bg-body-tertiary border">
              <div class="display-6 fw-bold text-warning">+${result.earnedXp}</div>
              <div class="small text-muted">XP Thưởng</div>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-center gap-2 mb-4">
          <button class="btn btn-3d btn-3d-primary px-4" id="btn-retake-exam">
            <i class="bi bi-arrow-clockwise me-1"></i> Thi lại đề này
          </button>
          <button class="btn btn-outline-secondary rounded-pill px-4" id="btn-back-to-exams">
            Về danh sách đề thi
          </button>
        </div>

        <!-- Detailed Explanations -->
        <div class="text-start border-top pt-4">
          <h5 class="fw-bold mb-3">Chi tiết đáp án & Giải thích:</h5>
          <div class="d-flex flex-column gap-3">
            ${result.details.map((d, i) => `
              <div class="p-3 rounded border ${d.isCorrect ? 'border-success bg-success-subtle bg-opacity-25' : 'border-danger bg-danger-subtle bg-opacity-25'}">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <strong>Câu ${i + 1}: ${d.question}</strong>
                  <span class="badge ${d.isCorrect ? 'bg-success' : 'bg-danger'}">${d.isCorrect ? 'Chính xác' : 'Chưa đúng'}</span>
                </div>
                <div class="small mb-1">
                  Câu trả lời của bạn: <strong class="${d.isCorrect ? 'text-success' : 'text-danger'}">${d.userAnswer}</strong>
                </div>
                ${!d.isCorrect ? `<div class="small text-success mb-1">Đáp án đúng: <strong>${d.correctAnswer}</strong></div>` : ''}
                <div class="small text-muted fst-italic">Giải thích: ${d.explanation}</div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;

    document.getElementById('btn-retake-exam')?.addEventListener('click', () => this.startExamSession(result.examId));
    document.getElementById('btn-back-to-exams')?.addEventListener('click', () => this.switchTab('exams'));
  }

  /* ==============================================================================
     VIEW 6: QUÁ TRÌNH HỌC (LEARNING PROGRESS & ANALYTICS)
     ============================================================================== */
  renderProgressView() {
    const user = authService.getUser();
    const history = examService.getExamHistory();

    this.container.innerHTML = `
      <!-- Header -->
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
        <div>
          <h2 class="fw-bold mb-1"><i class="bi bi-graph-up-arrow text-primary me-2"></i>Quá Trình Học & Phân Tích</h2>
          <p class="text-secondary small mb-0">Theo dõi tiến độ tích lũy từ vựng, chuỗi ngày học liên tục và kết quả các kỳ thi thử.</p>
        </div>
      </div>

      <!-- Top KPI Metric Cards -->
      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="gamify-card p-4 text-center">
            <i class="bi bi-star-fill display-4 text-warning mb-2"></i>
            <div class="display-6 fw-bold text-dark">${user.xp || 0} XP</div>
            <div class="small text-muted">Điểm kinh nghiệm tích lũy</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="gamify-card p-4 text-center">
            <i class="bi bi-fire display-4 text-danger mb-2"></i>
            <div class="display-6 fw-bold text-dark">${user.streak || 0} Ngày</div>
            <div class="small text-muted">Chuỗi ngày học liên tục (Streak)</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="gamify-card p-4 text-center">
            <i class="bi bi-check-all display-4 text-success mb-2"></i>
            <div class="display-6 fw-bold text-dark">${history.length} Lần</div>
            <div class="small text-muted">Bài thi thử đã hoàn thành</div>
          </div>
        </div>
      </div>

      <!-- Level Mastery Progress Bars -->
      <div class="gamify-card p-4 mb-4">
        <h5 class="fw-bold mb-3"><i class="bi bi-layers-fill text-primary me-2"></i>Tiến Độ Hoàn Thành Từ Vựng Theo Level</h5>
        
        <div class="mb-3">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <strong>Cấp độ A1 (Cơ bản)</strong>
            <span class="text-muted small">847 Từ vựng</span>
          </div>
          <div class="progress" style="height: 10px;">
            <div class="progress-bar bg-success" style="width: 45%;">45%</div>
          </div>
        </div>

        <div class="mb-3">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <strong>Cấp độ A2 (Sơ trung cấp)</strong>
            <span class="text-muted small">616 Từ vựng</span>
          </div>
          <div class="progress" style="height: 10px;">
            <div class="progress-bar bg-info" style="width: 25%;">25%</div>
          </div>
        </div>

        <div class="mb-2">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <strong>Cấp độ B1 (Trung cấp)</strong>
            <span class="text-muted small">1.852 Từ vựng</span>
          </div>
          <div class="progress" style="height: 10px;">
            <div class="progress-bar bg-primary" style="width: 15%;">15%</div>
          </div>
        </div>
      </div>

      <!-- Exam History Table -->
      <div class="gamify-card p-4">
        <h5 class="fw-bold mb-3"><i class="bi bi-clock-history text-primary me-2"></i>Lịch Sử Thi Thử</h5>
        ${history.length === 0 ? `
          <div class="text-center py-4 text-muted small">
            Bạn chưa làm bài thi thử nào. Hãy vào mục "Thi thử" để bắt đầu đánh giá năng lực!
          </div>
        ` : `
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>Đề thi</th>
                  <th>Level</th>
                  <th>Điểm số</th>
                  <th>Kết quả</th>
                  <th>XP Thưởng</th>
                  <th>Thời gian</th>
                </tr>
              </thead>
              <tbody>
                ${history.map(h => `
                  <tr>
                    <td class="fw-bold">${h.examTitle}</td>
                    <td><span class="badge badge-level badge-level-${h.level}">${h.level}</span></td>
                    <td class="fw-bold">${h.scorePct}% (${h.correctCount}/${h.totalQuestions})</td>
                    <td><span class="badge ${h.passed ? 'bg-success' : 'bg-danger'}">${h.passed ? 'Đạt' : 'Chưa đạt'}</span></td>
                    <td class="text-warning fw-bold">+${h.earnedXp} XP</td>
                    <td class="small text-muted">${new Date(h.completedAt).toLocaleDateString('vi-VN')}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `}
      </div>
    `;
  }
}

// Instantiate App
document.addEventListener('DOMContentLoaded', () => {
  window.lingoApp = new App();
});
