/**
 * LingoLearning - Game 4: Flashcards 3D with Spaced Repetition (SRS)
 * Supports 3D Flip, Audio Pronunciation, and SM-2 Algorithm Rating
 */

import { sound } from '../services/soundService.js';
import { authService } from '../services/authService.js';
import { progressService } from '../services/progressService.js';

export class FlashcardsGame {
  constructor(containerEl, vocabList, onFinish) {
    this.container = containerEl;
    this.vocabList = vocabList;
    this.onFinish = onFinish;
    this.currentIndex = 0;
    this.isFlipped = false;
    this.total = this.vocabList.length;
  }

  start() {
    if (this.vocabList.length === 0) {
      this.onFinish();
      return;
    }
    this.currentIndex = 0;
    this.isFlipped = false;
    this.render();
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
        <!-- Topbar -->
        <div class="game-header">
          <button class="btn btn-link text-muted p-0 fs-4" id="btn-exit-flashcard" title="Thoát trò chơi">
            <i class="bi bi-x-circle-fill"></i>
          </button>
          <div class="game-progress-bar-wrap">
            <div class="game-progress-bar-fill" style="width: ${progressPercent}%;"></div>
          </div>
          <div class="text-muted fw-bold">
            ${this.currentIndex + 1} / ${this.total}
          </div>
        </div>

        <!-- 3D Flippable Flashcard -->
        <div class="flashcard-scene" id="flashcard-scene">
          <div class="flashcard ${this.isFlipped ? 'is-flipped' : ''}" id="flashcard-card">
            <!-- Front Face -->
            <div class="flashcard-face flashcard-front">
              <div class="d-flex justify-content-between w-100 align-items-center mb-auto">
                <span class="badge badge-level badge-level-${current.cefr_level || 'A1'}">${current.cefr_level || 'A1'}</span>
                ${current.gender ? `<span class="badge badge-gender badge-${current.gender}">${current.gender}</span>` : ''}
                <button class="btn-speaker" id="btn-speak-front" title="Phát âm">
                  <i class="bi bi-volume-up-fill fs-5"></i>
                </button>
              </div>

              <div class="my-auto text-center">
                <div class="display-3 fw-bold mb-2">${current.word}</div>
                <div class="fs-4 text-muted font-monospace">${current.ipa || ''}</div>
              </div>

              <div class="mt-auto text-muted small">
                <i class="bi bi-arrow-repeat me-1"></i> Nhấn để lật xem nghĩa & ví dụ
              </div>
            </div>

            <!-- Back Face -->
            <div class="flashcard-face flashcard-back">
              <div class="d-flex justify-content-between w-100 align-items-center mb-auto">
                <span class="badge bg-secondary">Giải nghĩa & Ngữ cảnh</span>
                <button class="btn-speaker" id="btn-speak-back" title="Phát âm câu">
                  <i class="bi bi-volume-up-fill fs-5"></i>
                </button>
              </div>

              <div class="my-auto text-center">
                <h2 class="fw-bold text-primary mb-2">${current.meaning_vi}</h2>
                <div class="text-secondary mb-3">${current.meaning_en || ''}</div>

                ${current.plural_form ? `
                  <div class="mb-3">
                    <span class="badge bg-light text-dark border px-3 py-2 fs-6">
                      Dạng số nhiều: <strong>${current.plural_form}</strong>
                    </span>
                  </div>
                ` : ''}

                ${current.example_de ? `
                  <div class="p-3 bg-body-tertiary rounded-3 text-start small border">
                    <div class="fw-bold">${current.example_de}</div>
                    <div class="text-muted mt-1">${current.example_vi || ''}</div>
                  </div>
                ` : ''}
              </div>

              <div class="mt-auto text-muted small">
                <i class="bi bi-arrow-repeat me-1"></i> Nhấn để lật lại mặt trước
              </div>
            </div>
          </div>
        </div>

        <!-- SRS Rating Controls (Active only after flipping or reviewing) -->
        <div class="srs-rating-grid mt-4">
          <button class="btn btn-3d btn-3d-outline text-danger border-danger" data-srs-rating="1">
            <i class="bi bi-x-lg"></i> Quên (1)
          </button>
          <button class="btn btn-3d btn-3d-outline text-primary border-primary" data-srs-rating="3">
            <i class="bi bi-hand-thumbs-up"></i> Nhớ (3)
          </button>
          <button class="btn btn-3d btn-3d-primary" data-srs-rating="5">
            <i class="bi bi-lightning-charge"></i> Rất dễ (5)
          </button>
        </div>
      </div>
    `;

    // Event Bindings
    this.container.querySelector('#btn-exit-flashcard').addEventListener('click', () => this.onFinish());

    // Card Flip Click
    const cardEl = this.container.querySelector('#flashcard-card');
    cardEl.addEventListener('click', (e) => {
      // Don't flip if clicking speaker button
      if (e.target.closest('.btn-speaker')) return;
      sound.playFlip();
      this.isFlipped = !this.isFlipped;
      cardEl.classList.toggle('is-flipped', this.isFlipped);
    });

    // Pronunciation buttons
    this.container.querySelector('#btn-speak-front').addEventListener('click', (e) => {
      e.stopPropagation();
      sound.speak(current.word, current.audio_url, 'de-DE');
    });

    this.container.querySelector('#btn-speak-back')?.addEventListener('click', (e) => {
      e.stopPropagation();
      sound.speak(current.example_de || current.word, current.audio_url, 'de-DE');
    });

    // SRS Rating buttons
    this.container.querySelectorAll('[data-srs-rating]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const rating = parseInt(e.currentTarget.getAttribute('data-srs-rating'), 10);
        this.submitRating(rating);
      });
    });

    sound.speak(current.word, current.audio_url, 'de-DE');
  }

  submitRating(rating) {
    const current = this.vocabList[this.currentIndex];
    progressService.recordReview(current.id, rating);

    if (rating >= 3) {
      sound.playSuccess();
      authService.addXp(10);
    } else {
      sound.playError();
      authService.addXp(2);
    }

    this.isFlipped = false;
    this.currentIndex += 1;
    this.render();
  }

  renderGameOver() {
    this.container.innerHTML = `
      <div class="game-container text-center py-4">
        <div class="gamify-card p-5">
          <div class="display-1 text-primary mb-3">
            <i class="bi bi-check-circle-fill"></i>
          </div>
          <h2 class="fw-bold mb-2">Đã ôn tập xong thẻ ghi nhớ!</h2>
          <p class="text-secondary mb-4">Hệ thống Spaced Repetition (SM-2) đã lên lịch ôn tập tối ưu cho bạn.</p>

          <div class="d-flex justify-content-center gap-3">
            <button class="btn btn-3d btn-3d-primary" id="btn-replay">
              <i class="bi bi-arrow-repeat"></i> Ôn lại
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

