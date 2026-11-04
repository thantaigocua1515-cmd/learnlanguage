/**
 * LingoLearning - Progress & Spaced Repetition (SRS) Engine
 * Implements SuperMemo SM-2 algorithm for long-term vocabulary retention
 */

class ProgressService {
  constructor() {
    this.progressKey = 'lingo_srs_progress_v1';
  }

  getProgressMap() {
    return JSON.parse(localStorage.getItem(this.progressKey) || '{}');
  }

  saveProgressMap(map) {
    localStorage.setItem(this.progressKey, JSON.stringify(map));
  }

  /**
   * SuperMemo SM-2 Algorithm
   * @param {string} vocabId - Unique vocabulary ID
   * @param {number} quality - Rating from 0 (forgot completely) to 5 (perfect recall)
   */
  recordReview(vocabId, quality) {
    const map = this.getProgressMap();
    const item = map[vocabId] || {
      repetitions: 0,
      interval: 1,
      easeFactor: 2.5,
      nextReviewDate: new Date().toISOString()
    };

    let { repetitions, interval, easeFactor } = item;

    if (quality < 3) {
      // Failed recall: reset intervals
      repetitions = 0;
      interval = 1;
    } else {
      // Successful recall
      if (repetitions === 0) {
        interval = 1;
      } else if (repetitions === 1) {
        interval = 6;
      } else {
        interval = Math.round(interval * easeFactor);
      }
      repetitions += 1;
    }

    // Update ease factor (min 1.30)
    easeFactor = easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
    if (easeFactor < 1.3) easeFactor = 1.3;

    // Calculate next review date
    const nextDate = new Date();
    nextDate.setDate(nextDate.getDate() + interval);

    map[vocabId] = {
      repetitions,
      interval,
      easeFactor: Number(easeFactor.toFixed(2)),
      lastQuality: quality,
      nextReviewDate: nextDate.toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.saveProgressMap(map);
    return map[vocabId];
  }

  getDueWords(vocabList) {
    const map = this.getProgressMap();
    const now = new Date();

    return vocabList.filter(v => {
      const p = map[v.id];
      if (!p) return true; // Brand new word
      return new Date(p.nextReviewDate) <= now;
    });
  }
}

export const progressService = new ProgressService();

