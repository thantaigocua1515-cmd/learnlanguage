/**
 * LingoLearning - Game 1: Der / Die / Das Speed Sorter
 * Rapid-fire noun gender classification game with tactile feedback & keyboard shortcuts
 */

import { sound } from '../services/soundService.js';
import { authService } from '../services/authService.js';

export class ArticleGame {
  constructor(containerEl, vocabList, onFinish) {
    this.container = containerEl;
    this.vocabList = vocabList.filter(v => v.gender && ['der', 'die', 'das'].includes(v.gender));
    this.onFinish = onFinish;
    this.currentIndex = 0;
    this.score = 0;
    this.streak = 0;
    this.total = Math.min(this.vocabList.length, 10);
    this.boundKeyHandler = this.handleKeydown.bind(this);
  }

  start() {
    if (this.vocabList.length === 0) {
      this.container.innerHTML = `
        <div class="text-center py-5">
          <i class="bi bi-emoji-neutral display-3 text-muted"></i>
          <h4 class="mt-3">Chưa có danh từ nào cho cấp độ này</h4>
          <button class="btn btn-3d btn-3d-primary mt-3" id="btn-back">Quay lại</button>
        </div>
      `;
      this.container.querySelector('#btn-back')?.addEventListener('click', () => this.onFinish());
      return;
    }

    // Shuffle vocabulary
    this.vocabList = [...this.vocabList].sort(() => Math.random() - 0.5).slice(0, this.total);
    this.currentIndex = 0;
    this.score = 0;
    this.streak = 0;

    window.addEventListener('keydown', this.boundKeyHandler);
    this.render();
  }

  destroy() {
    window.removeEventListener('keydown', this.boundKeyHandler);
  }

  handleKeydown(e) {
    const key = e.key.toLowerCase();
    if (key === '1' || key === 'a' || key === 'arrowleft') {
      this.submitAnswer('der');
    } else if (key === '2' || key === 's' || key === 'arrowdown') {
      this.submitAnswer('die');
    } else if (key === '3' || key === 'd' || key === 'arrowright') {
      this.submitAnswer('das');
    }
  }

  render() {
    if (this.currentIndex >= this.total) {
      this.renderGameOver();
      return;
    }

    const current = this.vocabList[this.currentIndex];
    const progressPercent = Math.round((this.currentIndex / this.total) * 100);

    this.container.innerHTML = `
      <div class="game-container">
        <!-- Game Topbar -->
        <div class="game-header">
          <button class="btn btn-link text-muted p-0 fs-4" id="btn-exit-game" title="Thoát trò chơi">
            <i class="bi bi-x-circle-fill"></i>
          </button>
          <div class="game-progress-bar-wrap">
            <div class="game-progress-bar-fill" style="width: ${progressPercent}%;"></div>
          </div>
          <div class="game-score-box">
            <i class="bi bi-star-fill text-warning"></i>
            <span>${this.score}</span>
          </div>
        </div>

        <!-- Central Noun Card -->
        <div class="sorter-card" id="sorter-card">
          <div class="d-flex justify-content-center align-items-center gap-2 mb-2">
            <span class="badge badge-level badge-level-${current.cefr_level || 'A1'}">${current.cefr_level || 'A1'}</span>
            <button class="btn-speaker" id="btn-play-audio" title="Nghe phát âm">
              <i class="bi bi-volume-up-fill fs-5"></i>
            </button>
          </div>

          <div class="sorter-word">${current.word}</div>
          <div class="sorter-ipa">${current.ipa || ''}</div>
          <div class="sorter-meaning">${current.meaning_vi}</div>
          ${current.plural_form ? `<div class="sorter-plural">Số nhiều: <strong>${current.plural_form}</strong></div>` : ''}
        </div>

        <!-- 3D Tactile Action Buttons: DER / DIE / DAS -->
        <div class="article-btn-grid">
          <button class="btn btn-3d btn-3d-der btn-article" data-article="der">
            <span>DER</span>
            <span class="key-hint"><i class="bi bi-arrow-left"></i> [A]</span>
          </button>
          <button class="btn btn-3d btn-3d-die btn-article" data-article="die">
            <span>DIE</span>
            <span class="key-hint"><i class="bi bi-arrow-down"></i> [S]</span>
          </button>
          <button class="btn btn-3d btn-3d-das btn-article" data-article="das">
            <span>DAS</span>
            <span class="key-hint"><i class="bi bi-arrow-right"></i> [D]</span>
          </button>
        </div>

        <div class="text-center mt-4 text-muted small">
          <i class="bi bi-keyboard"></i> Mẹo: Dùng phím <strong>[A]</strong> Der, <strong>[S]</strong> Die, <strong>[D]</strong> Das hoặc phím mũi tên.
        </div>
      </div>
    `;

    // Bind event handlers
    this.container.querySelector('#btn-exit-game').addEventListener('click', () => {
      this.destroy();
      this.onFinish();
    });

    this.container.querySelector('#btn-play-audio').addEventListener('click', () => {
      sound.speak(current.word, current.audio_url, 'de-DE');
    });

    this.container.querySelectorAll('.btn-article').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const article = e.currentTarget.getAttribute('data-article');
        this.submitAnswer(article);
      });
    });

    // Auto-pronounce when card appears
    sound.speak(current.word, current.audio_url, 'de-DE');
  }

  submitAnswer(chosenArticle) {
    const current = this.vocabList[this.currentIndex];
    const isCorrect = chosenArticle === current.gender;
    const cardEl = this.container.querySelector('#sorter-card');

    if (!cardEl) return;

    if (isCorrect) {
      sound.playSuccess();
      this.score += 10;
      this.streak += 1;
      authService.addXp(10);
      cardEl.classList.add('correct-anim');
    } else {
      sound.playError();
      this.streak = 0;
      authService.loseHeart();
      cardEl.classList.add('wrong-anim');
    }

    // Disable buttons temporarily
    this.container.querySelectorAll('.btn-article').forEach(b => b.disabled = true);

    setTimeout(() => {
      this.currentIndex += 1;
      this.render();
    }, 600);
  }

  renderGameOver() {
    this.destroy();
    const earnedXp = this.score;

    this.container.innerHTML = `
      <div class="game-container text-center py-4">
        <div class="gamify-card p-5">
          <div class="display-1 text-warning mb-3">
            <i class="bi bi-trophy-fill"></i>
          </div>
          <h2 class="fw-bold mb-2">Hoàn thành thử thách!</h2>
          <p class="text-secondary mb-4">Bạn đã xuất sắc phân biệt các giống từ tiếng Đức!</p>

          <div class="d-flex justify-content-center gap-4 mb-4">
            <div class="stat-pill">
              <i class="bi bi-star-fill text-warning fs-4"></i>
              <div class="text-start">
                <div class="small text-muted">Điểm số</div>
                <div class="fs-5 fw-bold">${this.score} pts</div>
              </div>
            </div>
            <div class="stat-pill">
              <i class="bi bi-lightning-charge-fill text-primary fs-4"></i>
              <div class="text-start">
                <div class="small text-muted">Kinh nghiệm</div>
                <div class="fs-5 fw-bold">+${earnedXp} XP</div>
              </div>
            </div>
          </div>

          <div class="d-flex justify-content-center gap-3">
            <button class="btn btn-3d btn-3d-primary" id="btn-replay">
              <i class="bi bi-arrow-repeat"></i> Chơi lại
            </button>
            <button class="btn btn-3d btn-3d-outline" id="btn-finish">
              <i class="bi bi-house"></i> Về trang chủ
            </button>
          </div>
        </div>
      </div>
    `;

    this.container.querySelector('#btn-replay').addEventListener('click', () => this.start());
    this.container.querySelector('#btn-finish').addEventListener('click', () => this.onFinish());
  }
}

