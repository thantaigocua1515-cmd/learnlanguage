/**
 * LingoLearning - Common Phrases Service (Các câu thông dụng)
 * Curated practical phrases by real-life topics + Tatoeba examples integration
 */

export const PHRASE_CATEGORIES = [
  { id: 'all', name: 'Tất cả chủ đề', icon: 'bi-grid-fill' },
  { id: 'greeting', name: 'Chào hỏi & Giao tiếp', icon: 'bi-chat-dots-fill' },
  { id: 'shopping', name: 'Mua sắm & Giá cả', icon: 'bi-cart-fill' },
  { id: 'restaurant', name: 'Nhà hàng & Ăn uống', icon: 'bi-cup-hot-fill' },
  { id: 'travel', name: 'Du lịch & Hỏi đường', icon: 'bi-compass-fill' },
  { id: 'hotel', name: 'Khách sạn & Lưu trú', icon: 'bi-building-fill' },
  { id: 'health', name: 'Sức khỏe & Khẩn cấp', icon: 'bi-heart-pulse-fill' },
  { id: 'work', name: 'Công việc & Lớp học', icon: 'bi-briefcase-fill' }
];

const CURATED_PHRASES = [
  // 1. Chào hỏi & Giao tiếp (Greeting)
  {
    id: 'ph-01',
    category: 'greeting',
    level: 'A1',
    de: 'Guten Tag! Wie geht es Ihnen?',
    vi: 'Xin chào! Ngài có khỏe không?',
    context: 'Chào hỏi lịch sự trang trọng',
    audio: null
  },
  {
    id: 'ph-02',
    category: 'greeting',
    level: 'A1',
    de: 'Hallo! Wie geht\'s dir?',
    vi: 'Chào bạn! Bạn thế nào rồi?',
    context: 'Chào hỏi thân mật với bạn bè',
    audio: null
  },
  {
    id: 'ph-03',
    category: 'greeting',
    level: 'A1',
    de: 'Ich heiße Nam und komme aus Vietnam.',
    vi: 'Tôi tên là Nam và tôi đến từ Việt Nam.',
    context: 'Giới thiệu bản thân và quê quán',
    audio: null
  },
  {
    id: 'ph-04',
    category: 'greeting',
    level: 'A1',
    de: 'Freut mich, Sie kennenzulernen!',
    vi: 'Rất vui được làm quen với ngài!',
    context: 'Khi gặp mặt lần đầu',
    audio: null
  },
  {
    id: 'ph-05',
    category: 'greeting',
    level: 'A1',
    de: 'Auf Wiedersehen! Einen schönen Tag noch!',
    vi: 'Tạm biệt! Chúc bạn một ngày tốt lành!',
    context: 'Chào tạm biệt',
    audio: null
  },
  {
    id: 'ph-06',
    category: 'greeting',
    level: 'A2',
    de: 'Könnten Sie das bitte wiederholen? Ich habe es nicht verstanden.',
    vi: 'Bạn có thể vui lòng nhắc lại được không? Tôi chưa hiểu rõ.',
    context: 'Khi cần người khác nhắc lại',
    audio: null
  },

  // 2. Mua sắm & Giá cả (Shopping)
  {
    id: 'ph-07',
    category: 'shopping',
    level: 'A1',
    de: 'Wie viel kostet das, bitte?',
    vi: 'Cái này giá bao nhiêu vậy ạ?',
    context: 'Hỏi giá tiền món hàng',
    audio: null
  },
  {
    id: 'ph-08',
    category: 'shopping',
    level: 'A1',
    de: 'Kann ich mit Karte bezahlen?',
    vi: 'Tôi có thể thanh toán bằng thẻ được không?',
    context: 'Phương thức thanh toán',
    audio: null
  },
  {
    id: 'ph-09',
    category: 'shopping',
    level: 'A2',
    de: 'Haben Sie das auch in einer anderen Größe oder Farbe?',
    vi: 'Bạn có món này ở kích cỡ hoặc màu sắc khác không?',
    context: 'Hỏi kích cỡ/màu trong cửa hàng',
    audio: null
  },
  {
    id: 'ph-10',
    category: 'shopping',
    level: 'A2',
    de: 'Ich möchte das gerne umtauschen, hier ist der Kassenbon.',
    vi: 'Tôi muốn đổi món đồ này, đây là hóa đơn thanh toán.',
    context: 'Đổi trả hàng hóa',
    audio: null
  },

  // 3. Nhà hàng & Ăn uống (Restaurant)
  {
    id: 'ph-11',
    category: 'restaurant',
    level: 'A1',
    de: 'Einen Tisch für zwei Personen, bitte.',
    vi: 'Làm ơn cho một bàn dành cho hai người.',
    context: 'Đặt bàn khi vào nhà hàng',
    audio: null
  },
  {
    id: 'ph-12',
    category: 'restaurant',
    level: 'A1',
    de: 'Die Speisekarte, bitte. Was können Sie empfehlen?',
    vi: 'Làm ơn cho tôi xem thực đơn. Bạn có gợi ý món nào ngon không?',
    context: 'Xem thực đơn và xin gợi ý',
    audio: null
  },
  {
    id: 'ph-13',
    category: 'restaurant',
    level: 'A1',
    de: 'Ich möchte ein Glas Wasser und eine Tasse Kaffee bestellen.',
    vi: 'Tôi muốn gọi một ly nước lọc và một tách cà phê.',
    context: 'Gọi đồ uống',
    audio: null
  },
  {
    id: 'ph-14',
    category: 'restaurant',
    level: 'A2',
    de: 'Wir möchten bitte zahlen. Zusammen oder getrennt?',
    vi: 'Chúng tôi muốn thanh toán. Tính gộp hay tính riêng?',
    context: 'Thanh toán tiền ăn tại Đức',
    audio: null
  },
  {
    id: 'ph-15',
    category: 'restaurant',
    level: 'A1',
    de: 'Das Essen war wirklich sehr lecker, danke!',
    vi: 'Món ăn thật sự rất ngon, cảm ơn bạn!',
    context: 'Khen ngợi món ăn',
    audio: null
  },

  // 4. Du lịch & Hỏi đường (Travel)
  {
    id: 'ph-16',
    category: 'travel',
    level: 'A1',
    de: 'Entschuldigung, wo ist der Bahnhof?',
    vi: 'Xin lỗi, nhà ga xe lửa ở đâu vậy?',
    context: 'Hỏi đường đến ga tàu',
    audio: null
  },
  {
    id: 'ph-17',
    category: 'travel',
    level: 'A2',
    de: 'Wie komme ich am besten zum Flughafen?',
    vi: 'Làm thế nào để tôi đến sân bay thuận tiện nhất?',
    context: 'Hỏi phương tiện đi sân bay',
    audio: null
  },
  {
    id: 'ph-18',
    category: 'travel',
    level: 'A1',
    de: 'Fährt dieser Zug nach Berlin Hauptbahnhof?',
    vi: 'Chuyến tàu này có đi đến ga trung tâm Berlin không?',
    context: 'Xác nhận tuyến tàu',
    audio: null
  },
  {
    id: 'ph-19',
    category: 'travel',
    level: 'B1',
    de: 'Wann fährt der nächste Bus ab und von welchem Bahnsteig?',
    vi: 'Khi nào chuyến xe buýt tiếp theo khởi hành và từ bến nào?',
    context: 'Hỏi lịch trình và ke ga',
    audio: null
  },

  // 5. Khách sạn & Lưu trú (Hotel)
  {
    id: 'ph-20',
    category: 'hotel',
    level: 'A1',
    de: 'Ich habe eine Reservierung auf den Namen Nguyen.',
    vi: 'Tôi có đặt phòng trước dưới tên Nguyen.',
    context: 'Làm thủ tục nhận phòng (Check-in)',
    audio: null
  },
  {
    id: 'ph-21',
    category: 'hotel',
    level: 'A1',
    de: 'Wie lautet das Passwort für das WLAN?',
    vi: 'Mật khẩu Wi-Fi là gì vậy ạ?',
    context: 'Hỏi mật khẩu mạng',
    audio: null
  },
  {
    id: 'ph-22',
    category: 'hotel',
    level: 'A2',
    de: 'Bis wann müssen wir morgen auschecken?',
    vi: 'Ngày mai chúng tôi phải trả phòng trước mấy giờ?',
    context: 'Hỏi giờ trả phòng (Check-out)',
    audio: null
  },

  // 6. Sức khỏe & Y tế (Health)
  {
    id: 'ph-23',
    category: 'health',
    level: 'A1',
    de: 'Ich fühle mich nicht wohl. Ich habe Kopfschmerzen und Fieber.',
    vi: 'Tôi cảm thấy không khỏe. Tôi bị đau đầu và sốt.',
    context: 'Mô tả triệu chứng bệnh',
    audio: null
  },
  {
    id: 'ph-24',
    category: 'health',
    level: 'A2',
    de: 'Wo befindet sich die nächste Apotheke?',
    vi: 'Hiệu thuốc gần nhất nằm ở đâu?',
    context: 'Tìm hiệu thuốc',
    audio: null
  },
  {
    id: 'ph-25',
    category: 'health',
    level: 'B1',
    de: 'Ich brauche dringend einen Arzt. Bitte rufen Sie einen Krankenwagen!',
    vi: 'Tôi đang cần bác sĩ gấp. Xin hãy gọi xe cứu thương giúp tôi!',
    context: 'Trường hợp khẩn cấp cấp cứu (112)',
    audio: null
  },

  // 7. Công việc & Học tập (Work)
  {
    id: 'ph-26',
    category: 'work',
    level: 'B1',
    de: 'Ich arbeite als Softwareentwickler in einer internationalen Firma.',
    vi: 'Tôi làm việc với tư cách là kỹ sư phần mềm tại một công ty quốc tế.',
    context: 'Nói về nghề nghiệp chuyên môn',
    audio: null
  },
  {
    id: 'ph-27',
    category: 'work',
    level: 'B1',
    de: 'Können wir das Meeting auf morgen Vormittag verschieben?',
    vi: 'Chúng ta có thể dời cuộc họp sang sáng mai được không?',
    context: 'Sắp xếp lại lịch hẹn công việc',
    audio: null
  },
  {
    id: 'ph-28',
    category: 'work',
    level: 'B1',
    de: 'Vielen Dank für Ihre Unterstützung und die gute Zusammenarbeit!',
    vi: 'Cảm ơn ngài rất nhiều vì sự hỗ trợ và tinh thần hợp tác tốt đẹp!',
    context: 'Cảm ơn đồng nghiệp/đối tác',
    audio: null
  }
];

class PhraseService {
  constructor() {
    this.storageKey = 'lingo_common_phrases_v1';
    this.initStorage();
  }

  initStorage() {
    if (!localStorage.getItem(this.storageKey)) {
      localStorage.setItem(this.storageKey, JSON.stringify(CURATED_PHRASES));
    }
  }

  getPhrases({ category = 'all', level = 'ALL', search = '' } = {}) {
    let list = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    if (category && category !== 'all') {
      list = list.filter(p => p.category === category);
    }
    if (level && level !== 'ALL') {
      list = list.filter(p => p.level === level);
    }
    if (search) {
      const q = search.toLowerCase();
      list = list.filter(p => p.de.toLowerCase().includes(q) || p.vi.toLowerCase().includes(q) || (p.context && p.context.toLowerCase().includes(q)));
    }
    return list;
  }

  addPhrase(item) {
    const list = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    item.id = 'ph-' + Date.now();
    list.unshift(item);
    localStorage.setItem(this.storageKey, JSON.stringify(list));
    return item;
  }
}

export const phraseService = new PhraseService();

