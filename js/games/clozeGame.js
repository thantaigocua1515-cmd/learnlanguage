/**
 * LingoLearning - Game 3: Tatoeba Sentence Cloze Test
 * Real-world context sentences with fill-in-the-blank challenge
 */

import { sound } from '../services/soundService.js';
import { authService } from '../services/authService.js';

export class ClozeGame {
  constructor(containerEl, vocabList, onFinish) {
    this.container = containerEl;
    this.vocabList = vocabList;
    this.onFinish = onFinish;
    this.currentIndex = 0;
    this.score = 0;
    this.total = Math.min(this.vocabList.length, 6);
  }

  start() {
    if (this.vocabList.length === 0) {
      this.onFinish();
      return;
    }

    this.vocabList = [...this.vocabList].sort(() => Math.random() - 0.5).slice(0, this.total);
    this.currentIndex = 0;
    this.score = 0;
    this.render();
  }

  render() {
    if (this.currentIndex >= this.total) {
      this.renderGameOver();
      return;
    }

    const current = this.vocabList[this.currentIndex];
    const sentenceDe = current.example_de || `Ich sehe ${current.gender ? current.gender + ' ' : ''}${current.word}.`;
    const sentenceVi = current.example_vi || `Tôi nhìn thấy ${current.meaning_vi}.`;
    
    // Mask target word
    const regex = new RegExp(`\\b${current.word}\\b`, 'gi');
    const maskedSentence = sentenceDe.replace(regex, '<span class="text-primary fw-bold text-decoration-underline px-2">[ _______ ]</span>');

    // Create 4 multiple choice options
    const distractors = this.vocabList
      .filter(v => v.id !== current.id)
      .sort(() => Math.random() - 0.5)
      .slice(0, 3)
      .map(v => v.word);

    const options = [current.word, ...distractors].sort(() => Math.random() - 0.5);
    const progressPercent = Math.round((this.currentIndex / this.total) * 100);

    this.container.innerHTML = `
      <div class="game-container">
        <!-- Game Topbar -->
        <div class="game-header">
          <button class="btn btn-link text-muted p-0 fs-4" id="btn-exit-cloze" title="Thoát trò chơi">
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

        <!-- Sentence Card -->
        <div class="sorter-card mb-4" id="cloze-card">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <span class="badge badge-level badge-level-${current.cefr_level || 'A1'}">${current.cefr_level || 'A1'} - Tatoeba Context</span>
            <button class="btn-speaker" id="btn-speak-sentence" title="Nghe câu tiếng Đức">
              <i class="bi bi-volume-up-fill fs-5"></i>
            </button>
          </div>

          <div class="fs-3 fw-bold mb-3 text-start lh-base">
            ${maskedSentence}
          </div>
          <div class="text-secondary text-start fs-5 border-top pt-2">
            <i class="bi bi-translate text-muted me-1"></i> ${sentenceVi}
          </div>
        </div>

        <!-- Multiple Choice 3D Buttons -->
        <div class="row g-3">
          ${options.map(opt => `
            <div class="col-6">
              <button class="btn btn-3d btn-3d-outline w-100 py-3 fs-5 option-btn" data-word="${opt}">
                ${opt}
              </button>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    // Bind event handlers
    this.container.querySelector('#btn-exit-cloze').addEventListener('click', () => this.onFinish());
    
    this.container.querySelector('#btn-speak-sentence').addEventListener('click', () => {
      sound.speak(sentenceDe, current.audio_url, 'de-DE');
    });

    this.container.querySelectorAll('.option-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const selected = e.currentTarget.getAttribute('data-word');
        this.submitAnswer(selected, e.currentTarget);
      });
    });

    sound.speak(sentenceDe, current.audio_url, 'de-DE');
  }

  submitAnswer(selectedWord, buttonEl) {
    const current = this.vocabList[this.currentIndex];
    const isCorrect = selectedWord.toLowerCase() === current.word.toLowerCase();
    const cardEl = this.container.querySelector('#cloze-card');

    this.container.querySelectorAll('.option-btn').forEach(b => b.disabled = true);

    if (isCorrect) {
      sound.playSuccess();
      this.score += 20;
      authService.addXp(20);
      buttonEl.classList.remove('btn-3d-outline');
      buttonEl.classList.add('btn-3d-primary');
      cardEl.classList.add('correct-anim');
    } else {
      sound.playError();
      authService.loseHeart();
      buttonEl.style.backgroundColor = '#ef4444';
      buttonEl.style.color = '#ffffff';
      cardEl.classList.add('wrong-anim');

      // Highlight the correct answer
      this.container.querySelectorAll('.option-btn').forEach(b => {
        if (b.getAttribute('data-word').toLowerCase() === current.word.toLowerCase()) {
          b.classList.remove('btn-3d-outline');
          b.classList.add('btn-3d-primary');
        }
      });
    }

    setTimeout(() => {
      this.currentIndex += 1;
      this.render();
    }, 1000);
  }

  renderGameOver() {
    this.container.innerHTML = `
      <div class="game-container text-center py-4">
        <div class="gamify-card p-5">
          <div class="display-1 text-success mb-3">
            <i class="bi bi-award-fill"></i>
          </div>
          <h2 class="fw-bold mb-2">Hoàn thành ngữ cảnh Tatoeba!</h2>
          <p class="text-secondary mb-4">Bạn đã vận dụng rất tốt từ vựng vào ngữ cảnh câu thực tế.</p>

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
                <div class="fs-5 fw-bold">+${this.score} XP</div>
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

