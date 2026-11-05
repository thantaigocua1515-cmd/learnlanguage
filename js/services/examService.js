/**
 * LingoLearning - Mock Exam Engine & AI Test Generator (Thi thử theo Level & Tạo đề AI)
 * Provides standard CEFR mock exams (A1, A2, B1), scoring, and AI question generation
 */

import { authService } from './authService.js';
import { dataService } from '../api/dataService.js';

const SEED_EXAMS = [
  {
    id: 'exam-a1-01',
    title: 'Đề thi thử Chuẩn CEFR A1 - Đề số 1',
    level: 'A1',
    durationMinutes: 10,
    description: 'Kiểm tra tổng hợp 10 câu: Mạo từ (der/die/das), từ vựng cơ bản và điền câu giao tiếp hàng ngày.',
    createdAt: '2026-11-05',
    questions: [
      {
        id: 'q1',
        type: 'article',
        question: 'Mạo từ xác định đúng của từ "Haus" (ngôi nhà) là gì?',
        options: ['der', 'die', 'das', 'den'],
        correctAnswer: 'das',
        explanation: '"Haus" là danh từ giống trung (das Haus, số nhiều: die Häuser).'
      },
      {
        id: 'q2',
        type: 'meaning',
        question: 'Từ "Buch" trong tiếng Đức có nghĩa là gì?',
        options: ['Quyển sách', 'Chiếc bút', 'Cái bàn', 'Ngôi nhà'],
        correctAnswer: 'Quyển sách',
        explanation: 'das Buch = quyển sách (số nhiều: die Bücher).'
      },
      {
        id: 'q3',
        type: 'article',
        question: 'Mạo từ xác định đúng của từ "Apfel" (quả táo) là gì?',
        options: ['der', 'die', 'das', 'dem'],
        correctAnswer: 'der',
        explanation: '"Apfel" là danh từ giống đực (der Apfel, số nhiều: die Äpfel).'
      },
      {
        id: 'q4',
        type: 'cloze',
        question: 'Điền từ còn thiếu: "Guten Tag! Wie ______ es Ihnen?"',
        options: ['geht', 'gehst', 'gehen', 'ging'],
        correctAnswer: 'geht',
        explanation: 'Cấu trúc chào hỏi lịch sự: "Wie geht es Ihnen?" (Ngài có khỏe không?).'
      },
      {
        id: 'q5',
        type: 'article',
        question: 'Mạo từ xác định đúng của từ "Katze" (con mèo) là gì?',
        options: ['der', 'die', 'das', 'des'],
        correctAnswer: 'die',
        explanation: '"Katze" là danh từ giống cái (die Katze, số nhiều: die Katzen).'
      },
      {
        id: 'q6',
        type: 'plural',
        question: 'Dạng số nhiều chính xác của danh từ "Kind" (đứa trẻ) là gì?',
        options: ['die Kinder', 'die Kinde', 'die Kinds', 'die Kindes'],
        correctAnswer: 'die Kinder',
        explanation: 'das Kind -> die Kinder.'
      },
      {
        id: 'q7',
        type: 'cloze',
        question: 'Điền từ còn thiếu: "Ich ______ aus Vietnam und wohne in Berlin."',
        options: ['komme', 'kommst', 'kommt', 'kommen'],
        correctAnswer: 'komme',
        explanation: 'Chủ ngữ "Ich" chia động từ đuôi -e: "Ich komme".'
      },
      {
        id: 'q8',
        type: 'meaning',
        question: 'Từ "Wasser" trong tiếng Đức nghĩa là gì?',
        options: ['Nước', 'Bánh mì', 'Cà phê', 'Sữa'],
        correctAnswer: 'Nước',
        explanation: 'das Wasser = nước uống.'
      },
      {
        id: 'q9',
        type: 'article',
        question: 'Mạo từ xác định đúng của từ "Sonne" (mặt trời) là gì?',
        options: ['die', 'der', 'das', 'ein'],
        correctAnswer: 'die',
        explanation: '"Sonne" là danh từ giống cái (die Sonne).'
      },
      {
        id: 'q10',
        type: 'cloze',
        question: 'Điền từ vào câu: "Wir möchten bitte ______. Zusammen oder getrennt?"',
        options: ['zahlen', 'zahlt', 'bezahlst', 'kauft'],
        correctAnswer: 'zahlen',
        explanation: 'Động từ khuyết thiếu "möchten" đi với động từ nguyên thể ở cuối câu: "zahlen" (thanh toán).'
      }
    ]
  },
  {
    id: 'exam-a2-01',
    title: 'Đề thi thử Chuẩn CEFR A2 - Đề số 1',
    level: 'A2',
    durationMinutes: 12,
    description: 'Kiểm tra 10 câu trình độ A2: Thì quá khứ Perfekt, giới từ chỉ nơi chốn, từ vựng công việc & du lịch.',
    createdAt: '2026-11-05',
    questions: [
      {
        id: 'q1',
        type: 'cloze',
        question: 'Chọn trợ động từ thích hợp: "Gestern ______ ich nach München gefahren."',
        options: ['bin', 'habe', 'war', 'hatte'],
        correctAnswer: 'bin',
        explanation: 'Động từ chuyển động "fahren" tạo thì Perfekt với trợ động từ "sein" (ich bin gefahren).'
      },
      {
        id: 'q2',
        type: 'meaning',
        question: 'Từ "Erfahrung" nghĩa là gì?',
        options: ['Kinh nghiệm, trải nghiệm', 'Kết quả', 'Quyết định', 'Hy vọng'],
        correctAnswer: 'Kinh nghiệm, trải nghiệm',
        explanation: 'die Erfahrung = kinh nghiệm, trải nghiệm.'
      },
      {
        id: 'q3',
        type: 'cloze',
        question: 'Điền giới từ: "Das Buch liegt ______ dem Tisch."',
        options: ['auf', 'in', 'an', 'zu'],
        correctAnswer: 'auf',
        explanation: 'Vị trí nằm trên mặt phẳng dùng giới từ "auf" + Dativ (dem Tisch).'
      },
      {
        id: 'q4',
        type: 'article',
        question: 'Mạo từ xác định của "Ergebnis" (kết quả) là gì?',
        options: ['das', 'der', 'die', 'des'],
        correctAnswer: 'das',
        explanation: 'Các danh từ có hậu tố -nis thường là giống trung: das Ergebnis.'
      },
      {
        id: 'q5',
        type: 'cloze',
        question: 'Điền từ nối: "Ich lerne Deutsch, ______ ich in Deutschland studieren möchte."',
        options: ['weil', 'denn', 'aber', 'oder'],
        correctAnswer: 'weil',
        explanation: '"weil" là liên từ phụ thuộc, đẩy động từ "möchte" về cuối câu.'
      }
    ]
  },
  {
    id: 'exam-b1-01',
    title: 'Đề thi thử Chuẩn CEFR B1 - Đề số 1',
    level: 'B1',
    durationMinutes: 15,
    description: 'Kiểm tra B1: Câu bị động Passiv, mệnh đề quan hệ Relativsatz, cấu trúc liên từ kép.',
    createdAt: '2026-11-05',
    questions: [
      {
        id: 'q1',
        type: 'cloze',
        question: 'Chuyển sang bị động: "Das Haus ______ vor zwei Jahren gebaut."',
        options: ['wurde', 'worden', 'gewesen', 'hatte'],
        correctAnswer: 'wurde',
        explanation: 'Bị động thời quá khứ Präteritum: "wurde + Partizip II (gebaut)".'
      },
      {
        id: 'q2',
        type: 'meaning',
        question: 'Từ "Verantwortung" có nghĩa là gì?',
        options: ['Trách nhiệm', 'Mâu thuẫn', 'Cơ hội', 'Thành công'],
        correctAnswer: 'Trách nhiệm',
        explanation: 'die Verantwortung = trách nhiệm.'
      },
      {
        id: 'q3',
        type: 'cloze',
        question: 'Điền đại từ quan hệ: "Der Mann, ______ dort drüben steht, ist mein Deutschlehrer."',
        options: ['der', 'den', 'dem', 'dessen'],
        correctAnswer: 'der',
        explanation: 'Mệnh đề quan hệ đóng vai trò chủ ngữ giống đực: "der".'
      }
    ]
  }
];

class ExamService {
  constructor() {
    this.storageKey = 'lingo_mock_exams_v1';
    this.historyKey = 'lingo_exam_history_v1';
    this.initStorage();
  }

  initStorage() {
    if (!localStorage.getItem(this.storageKey)) {
      localStorage.setItem(this.storageKey, JSON.stringify(SEED_EXAMS));
    }
  }

  getExams(level = 'ALL') {
    let exams = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    if (level && level !== 'ALL') {
      exams = exams.filter(e => e.level === level.toUpperCase());
    }
    return exams;
  }

  getExamById(id) {
    const exams = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    return exams.find(e => e.id === id) || null;
  }

  saveExam(exam) {
    const exams = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    if (!exam.id) {
      exam.id = 'exam-' + Date.now();
      exam.createdAt = new Date().toISOString().split('T')[0];
      exams.unshift(exam);
    } else {
      const idx = exams.findIndex(e => e.id === exam.id);
      if (idx >= 0) exams[idx] = exam;
      else exams.unshift(exam);
    }
    localStorage.setItem(this.storageKey, JSON.stringify(exams));
    return exam;
  }

  deleteExam(id) {
    let exams = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    exams = exams.filter(e => e.id !== id);
    localStorage.setItem(this.storageKey, JSON.stringify(exams));
  }

  submitExamResult(examId, answers = {}) {
    const exam = this.getExamById(examId);
    if (!exam) return null;

    let correctCount = 0;
    const details = exam.questions.map((q, idx) => {
      const userAns = answers[q.id];
      const isCorrect = userAns === q.correctAnswer;
      if (isCorrect) correctCount++;
      return {
        questionId: q.id,
        question: q.question,
        userAnswer: userAns || 'Chưa trả lời',
        correctAnswer: q.correctAnswer,
        isCorrect,
        explanation: q.explanation
      };
    });

    const scorePct = Math.round((correctCount / exam.questions.length) * 100);
    const passed = scorePct >= 60;
    const earnedXp = correctCount * 10 + (passed ? 50 : 10);

    // Award XP to user profile
    authService.addXp(earnedXp);

    const resultRecord = {
      id: 'res-' + Date.now(),
      examId: exam.id,
      examTitle: exam.title,
      level: exam.level,
      totalQuestions: exam.questions.length,
      correctCount,
      scorePct,
      passed,
      earnedXp,
      details,
      completedAt: new Date().toISOString()
    };

    const history = JSON.parse(localStorage.getItem(this.historyKey) || '[]');
    history.unshift(resultRecord);
    localStorage.setItem(this.historyKey, JSON.stringify(history));

    return resultRecord;
  }

  getExamHistory() {
    return JSON.parse(localStorage.getItem(this.historyKey) || '[]');
  }

  /**
   * AI Exam Generator (Nút tạo đề bằng AI)
   * Uses local AI rule-based synthesizer or external LLM API
   */
  async generateExamWithAI({ level = 'A1', questionCount = 10, focus = 'mixed', customTopic = '' } = {}) {
    console.log(`🤖 AI Engine is synthesizing a new ${level} exam (${questionCount} questions)...`);

    // Fetch pool of words from target level
    let words = await dataService.getWords({ level, limit: 100 });
    if (!words || words.length === 0) {
      words = await dataService.getVocabulary({ level });
    }

    // Filter words that have articles or meanings
    const nounPool = words.filter(w => w.article && ['der', 'die', 'das'].includes(w.article));
    const sentencePool = words.filter(w => w.example_de && w.example_vi);

    const questions = [];
    const count = Math.min(questionCount, 25);

    for (let i = 0; i < count; i++) {
      const qIndex = i + 1;
      const typeChoice = (focus === 'article') ? 'article' :
                         (focus === 'vocab') ? 'meaning' :
                         (focus === 'cloze') ? 'cloze' :
                         ['article', 'meaning', 'cloze', 'plural'][i % 4];

      if (typeChoice === 'article' && nounPool.length > 0) {
        const word = nounPool[Math.floor(Math.random() * nounPool.length)];
        const correct = word.article;
        questions.push({
          id: `ai-q${qIndex}`,
          type: 'article',
          question: `Mạo từ xác định đúng của danh từ "${word.word}" (${word.meaning_vi || word.meaning_en}) là gì?`,
          options: ['der', 'die', 'das', 'den'],
          correctAnswer: correct,
          explanation: `"${word.word}" là danh từ ${correct === 'der' ? 'giống đực (Maskulin)' : correct === 'die' ? 'giống cái (Feminin)' : 'giống trung (Neutral)'} -> ${correct} ${word.word}.`
        });
      } else if (typeChoice === 'cloze' && sentencePool.length > 0) {
        const word = sentencePool[Math.floor(Math.random() * sentencePool.length)];
        const sentence = word.example_de;
        const targetWord = word.word;

        // Replace target word in sentence with blank
        const regex = new RegExp(`\\b${targetWord}\\b`, 'i');
        const clozeSentence = sentence.replace(regex, '______');

        // Distractors
        const distractors = words
          .filter(w => w.word !== targetWord && w.pos === word.pos)
          .slice(0, 3)
          .map(w => w.word);

        while (distractors.length < 3) distractors.push('machen', 'haben', 'sein');

        const options = [targetWord, ...distractors.slice(0, 3)].sort(() => Math.random() - 0.5);

        questions.push({
          id: `ai-q${qIndex}`,
          type: 'cloze',
          question: `Điền từ còn thiếu vào câu: "${clozeSentence}" (Nghĩa: ${word.example_vi})`,
          options,
          correctAnswer: targetWord,
          explanation: `Từ đúng ngữ cảnh là "${targetWord}". Câu hoàn chỉnh: "${sentence}".`
        });
      } else if (typeChoice === 'plural' && nounPool.length > 0) {
        const word = nounPool.find(w => w.plural_form || w.plural) || nounPool[0];
        const plural = word.plural_form || `die ${word.plural}`;
        const fake1 = `die ${word.word}e`;
        const fake2 = `die ${word.word}er`;
        const fake3 = `die ${word.word}s`;
        const options = Array.from(new Set([plural, fake1, fake2, fake3])).slice(0, 4).sort(() => Math.random() - 0.5);

        questions.push({
          id: `ai-q${qIndex}`,
          type: 'plural',
          question: `Dạng số nhiều chính xác của danh từ "${word.article} ${word.word}" là gì?`,
          options,
          correctAnswer: plural,
          explanation: `Số nhiều chuẩn của ${word.word} là: ${plural}.`
        });
      } else {
        // Meaning question
        const word = words[Math.floor(Math.random() * words.length)];
        const correct = word.meaning_vi || word.meaning_en || 'đang cập nhật';
        const otherMeanings = words
          .filter(w => w.word !== word.word && (w.meaning_vi || w.meaning_en))
          .slice(0, 3)
          .map(w => w.meaning_vi || w.meaning_en);

        while (otherMeanings.length < 3) otherMeanings.push('Ngôi nhà', 'Trường học', 'Thành phố');

        const options = [correct, ...otherMeanings.slice(0, 3)].sort(() => Math.random() - 0.5);

        questions.push({
          id: `ai-q${qIndex}`,
          type: 'meaning',
          question: `Từ "${word.word}" (${word.pos}) trong tiếng Đức có nghĩa là gì?`,
          options,
          correctAnswer: correct,
          explanation: `"${word.word}" có nghĩa là: ${correct}.`
        });
      }
    }

    const aiExam = {
      id: `exam-ai-${Date.now()}`,
      title: `Đề thi AI CEFR ${level} - ${customTopic || 'Tổng hợp kiến thức'}`,
      level: level.toUpperCase(),
      durationMinutes: Math.max(Math.round(count * 1.2), 5),
      description: `Đề thi do AI sinh tự động từ ngân hàng 3.315 từ DWDS/Kaikki và câu ví dụ Tatoeba (${count} câu hỏi).`,
      createdAt: new Date().toISOString().split('T')[0],
      isAiGenerated: true,
      questions
    };

    this.saveExam(aiExam);
    return aiExam;
  }
}

export const examService = new ExamService();

