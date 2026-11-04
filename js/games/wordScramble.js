/**
 * LingoLearning - Game 2: Word Scramble / Anagram
 * Guess and assemble scrambled German letters with Tatoeba sentence context
 */

import { sound } from '../services/soundService.js';
import { authService } from '../services/authService.js';

export class WordScrambleGame {
  constructor(containerEl, vocabList, onFinish) {
    this.container = containerEl;
    this.vocabList = vocabList;
    this.onFinish = onFinish;
    this.currentIndex = 0;
    this.score = 0;
    this.total = Math.min(this.vocabList.length, 8);
    this.userLetters = [];
    this.shuffledLetters = [];
  }

  start() {
    if (this.vocabList.length === 0) {
      this.onFinish();
      return;
    }

    this.vocabList = [...this.vocabList].sort(() => Math.random() - 0.5).slice(0, this.total);
    this.currentIndex = 0;
    this.score = 0;
    this.loadQuestion();
  }

  loadQuestion() {
    if (this.currentIndex >= this.total) {
      this.renderGameOver();
      return;
    }

    const current = this.vocabList[this.currentIndex];
    const targetWord = current.word.toUpperCase();
    this.targetWord = targetWord;
    this.userLetters = [];

    // Create scrambled letters
    const letters = targetWord.split('').map((char, index) => ({
      id: `${char}-${index}`,
      char,
      used: false
    }));

    // Shuffle letters ensuring it is not already solved
    let shuffled = [...letters].sort(() => Math.random() - 0.5);
    if (shuffled.map(l => l.char).join('') === targetWord && targetWord.length > 2) {
      shuffled.reverse();
    }
    this.shuffledLetters = shuffled;

    this.render();
  }

  render() {
    const current = this.vocabList[this.currentIndex];
    const progressPercent = Math.round((this.currentIndex / this.total) * 100);

    this.container.innerHTML = `
      <div class="game-container">
        <!-- Game Topbar -->
        <div class="game-header">
          <button class="btn btn-link text-muted p-0 fs-4" id="btn-exit-scramble" title="Thoát trò chơi">
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

        <!-- Clue Card with Context Sentence -->
        <div class="scramble-clue-box">
          <div class="d-flex justify-content-center align-items-center gap-2 mb-2">
            ${current.gender ? `<span class="badge badge-gender badge-${current.gender}">${current.gender}</span>` : ''}
            <span class="badge badge-level badge-level-${current.cefr_level || 'A1'}">${current.cefr_level || 'A1'}</span>
            <button class="btn-speaker" id="btn-listen-clue" title="Nghe câu ví dụ">
              <i class="bi bi-volume-up-fill fs-5"></i>
            </button>
          </div>

          <h3 class="fw-bold mb-1">${current.meaning_vi}</h3>
          <p class="text-secondary mb-0 fst-italic">"${current.example_de ? current.example_de.replace(new RegExp(current.word, 'gi'), '_____') : 'Gợi ý từ vựng'}"</p>
        </div>

        <!-- Answer Slots -->
        <div class="scramble-slots" id="answer-slots">
          ${Array.from({ length: this.targetWord.length }).map((_, i) => {
            const letterObj = this.userLetters[i];
            return `
              <div class="scramble-slot ${letterObj ? 'filled' : ''}" data-slot-index="${i}">
                ${letterObj ? letterObj.char : ''}
              </div>
            `;
          }).join('')}
        </div>

        <!-- Letter Pool -->
        <div class="letter-pool" id="letter-pool">
          ${this.shuffledLetters.map((l) => `
            <div class="letter-tile ${l.used ? 'used' : ''}" data-letter-id="${l.id}">
              ${l.char}
            </div>
          `).join('')}
        </div>

        <!-- Game Action Buttons -->
        <div class="d-flex justify-content-center gap-2 mt-4">
          <button class="btn btn-3d btn-3d-outline btn-3d-sm" id="btn-backspace">
            <i class="bi bi-backspace"></i> Xóa
          </button>
          <button class="btn btn-3d btn-3d-outline btn-3d-sm" id="btn-clear-all">
            <i class="bi bi-arrow-counterclockwise"></i> Đặt lại
          </button>
          <button class="btn btn-3d btn-3d-primary" id="btn-check-scramble">
            <i class="bi bi-check2-circle"></i> Kiểm tra
          </button>
        </div>
      </div>
    `;

    // Bind event handlers
    this.container.querySelector('#btn-exit-scramble').addEventListener('click', () => this.onFinish());
    
    this.container.querySelector('#btn-listen-clue').addEventListener('click', () => {
      sound.speak(current.example_de || current.word, current.audio_url, 'de-DE');
    });

    // Tile Click (from pool to slot)
    this.container.querySelectorAll('.letter-tile').forEach(tile => {
      tile.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-letter-id');
        this.selectLetter(id);
      });
    });

    // Slot Click (from slot back to pool)
    this.container.querySelectorAll('.scramble-slot').forEach(slot => {
      slot.addEventListener('click', (e) => {
        const idx = parseInt(e.currentTarget.getAttribute('data-slot-index'), 10);
        this.deselectSlot(idx);
      });
    });

    this.container.querySelector('#btn-backspace').addEventListener('click', () => this.backspace());
    this.container.querySelector('#btn-clear-all').addEventListener('click', () => this.clearAll());
    this.container.querySelector('#btn-check-scramble').addEventListener('click', () => this.checkAnswer());
  }

  selectLetter(id) {
    if (this.userLetters.length >= this.targetWord.length) return;
    const letterObj = this.shuffledLetters.find(l => l.id === id);
    if (!letterObj || letterObj.used) return;

    sound.playClick();
    letterObj.used = true;
    this.userLetters.push(letterObj);
    this.render();

    // Auto check if all slots filled
    if (this.userLetters.length === this.targetWord.length) {
      setTimeout(() => this.checkAnswer(), 200);
    }
  }

  deselectSlot(idx) {
    if (!this.userLetters[idx]) return;
    sound.playClick();
    const removed = this.userLetters.splice(idx, 1)[0];
    removed.used = false;
    this.render();
  }

  backspace() {
    if (this.userLetters.length === 0) return;
    sound.playClick();
    const removed = this.userLetters.pop();
    removed.used = false;
    this.render();
  }

  clearAll() {
    sound.playClick();
    this.userLetters = [];
    this.shuffledLetters.forEach(l => l.used = false);
    this.render();
  }

  checkAnswer() {
    const currentWord = this.userLetters.map(l => l.char).join('');
    if (currentWord.length < this.targetWord.length) {
      sound.playError();
      return;
    }

    const current = this.vocabList[this.currentIndex];
    const isCorrect = currentWord === this.targetWord;

    if (isCorrect) {
      sound.playSuccess();
      sound.speak(current.word, current.audio_url, 'de-DE');
      this.score += 15;
      authService.addXp(15);

      const slotsEl = this.container.querySelector('#answer-slots');
      if (slotsEl) {
        slotsEl.style.borderColor = '#10b981';
        slotsEl.style.backgroundColor = '#ecfdf5';
      }

      setTimeout(() => {
        this.currentIndex += 1;
        this.loadQuestion();
      }, 900);
    } else {
      sound.playError();
      authService.loseHeart();
      const slotsEl = this.container.querySelector('#answer-slots');
      if (slotsEl) {
        slotsEl.classList.add('wrong-anim');
        setTimeout(() => slotsEl.classList.remove('wrong-anim'), 500);
      }
    }
  }

  renderGameOver() {
    this.container.innerHTML = `
      <div class="game-container text-center py-4">
        <div class="gamify-card p-5">
          <div class="display-1 text-warning mb-3">
            <i class="bi bi-patch-check-fill"></i>
          </div>
          <h2 class="fw-bold mb-2">Tuyệt đỉnh giải đố!</h2>
          <p class="text-secondary mb-4">Bạn đã xếp đúng tất cả các từ vựng tiếng Đức trong bài học!</p>

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

