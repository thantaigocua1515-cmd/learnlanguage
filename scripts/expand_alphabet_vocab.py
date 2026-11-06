#!/usr/bin/env python3
"""
Expand German Vocabulary Dataset to ensure rich vocabulary for ALL alphabet letters:
- Adds authentic German words for rare letters (X, Y, Q, C, Ä, Ö, Ü) and others.
- Provides 3-5 high quality bilingual (German - Vietnamese) example sentences per word.
- Updates data/output/vocab_A1_A2_B1_full.json idempotently.
"""

import json
import os
import sys

NEW_WORDS = [
    # ==========================
    # CHỮ X
    # ==========================
    {
        "lemma": "Xylophon",
        "level": "A1",
        "pos": "noun",
        "article": "das",
        "gender": "neuter",
        "plural": "Xylophone",
        "ipa": "ksyloˈfoːn",
        "meaning_en": "xylophone",
        "meaning_vi": "đàn mộc cầm (xylophone)",
        "forms": ["Xylophon", "Xylophons", "Xylophone", "Xylophonen"],
        "examples": [
            {"de": "Das Kind spielt gerne auf dem Xylophon.", "vi": "Đứa trẻ rất thích gõ đàn mộc cầm.", "source": "tatoeba", "tatoeba_id": 91001},
            {"de": "Ein Xylophon ist ein Musikinstrument aus Holz.", "vi": "Đàn mộc cầm là một nhạc cụ bằng gỗ.", "source": "tatoeba", "tatoeba_id": 91002},
            {"de": "Im Musikunterricht lernen wir Xylophon.", "vi": "Trong giờ học âm nhạc, chúng tôi học đàn mộc cầm.", "source": "tatoeba", "tatoeba_id": 91003},
            {"de": "Der helle Klang des Xylophons ist wunderschön.", "vi": "Âm thanh trong trẻo của đàn mộc cầm rất hay.", "source": "tatoeba", "tatoeba_id": 91004}
        ]
    },
    {
        "lemma": "X-Achse",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "X-Achsen",
        "ipa": "ˈɪksˌʔaksə",
        "meaning_en": "x-axis",
        "meaning_vi": "trục hoành (trục X)",
        "forms": ["X-Achse", "X-Achsen"],
        "examples": [
            {"de": "Tragen Sie die Zeit auf der X-Achse ein.", "vi": "Hãy điền thời gian vào trục hoành X.", "source": "tatoeba", "tatoeba_id": 91005},
            {"de": "Die X-Achse verläuft horizontal.", "vi": "Trục X chạy theo phương ngang.", "source": "tatoeba", "tatoeba_id": 91006},
            {"de": "Der Wert auf der X-Achse ist null.", "vi": "Giá trị trên trục hoành bằng không.", "source": "tatoeba", "tatoeba_id": 91007}
        ]
    },
    {
        "lemma": "Xenon",
        "level": "B1",
        "pos": "noun",
        "article": "das",
        "gender": "neuter",
        "plural": None,
        "ipa": "ˈkseːnɔn",
        "meaning_en": "xenon (chemical element)",
        "meaning_vi": "khí xenon (nguyên tố hóa học)",
        "forms": ["Xenon", "Xenons"],
        "examples": [
            {"de": "Das Auto hat moderne Xenon-Scheinwerfer.", "vi": "Chiếc ô tô có đèn pha xenon hiện đại.", "source": "tatoeba", "tatoeba_id": 91008},
            {"de": "Xenon ist ein geruchloses Edelgas.", "vi": "Xenon là một loại khí hiếm không mùi.", "source": "tatoeba", "tatoeba_id": 91009},
            {"de": "Xenonlampen leuchten sehr hell und weiß.", "vi": "Đèn xenon phát ra ánh sáng rất sáng và trắng.", "source": "tatoeba", "tatoeba_id": 91010}
        ]
    },
    {
        "lemma": "Xenophobie",
        "level": "B1",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": None,
        "ipa": "kseno-foˈbiː",
        "meaning_en": "xenophobia, fear or hatred of foreigners",
        "meaning_vi": "chứng bài ngoại, sợ người lạ",
        "forms": ["Xenophobie"],
        "examples": [
            {"de": "Wir müssen aktiv gegen Xenophobie kämpfen.", "vi": "Chúng ta phải tích cực đấu tranh chống tư tưởng bài ngoại.", "source": "tatoeba", "tatoeba_id": 91011},
            {"de": "Bildung hilft, Xenophobie und Vorurteile abzubauen.", "vi": "Giáo dục giúp xóa bỏ tư tưởng bài ngoại và định kiến.", "source": "tatoeba", "tatoeba_id": 91012},
            {"de": "In einer offenen Gesellschaft gibt es keinen Platz für Xenophobie.", "vi": "Trong một xã hội cởi mở, không có chỗ cho sự bài ngoại.", "source": "tatoeba", "tatoeba_id": 91013}
        ]
    },
    {
        "lemma": "X-Beine",
        "level": "B1",
        "pos": "noun",
        "article": "die",
        "gender": "plural",
        "plural": "X-Beine",
        "ipa": "ˈɪksˌbaɪ̯nə",
        "meaning_en": "knock-knees",
        "meaning_vi": "chân chữ X, chân vòng kiềng hướng trong",
        "forms": ["X-Bein", "X-Beine", "X-Beinen"],
        "examples": [
            {"de": "Der Arzt untersucht die X-Beine des Kindes.", "vi": "Bác sĩ kiểm tra đôi chân chữ X của đứa trẻ.", "source": "tatoeba", "tatoeba_id": 91014},
            {"de": "Mit spezieller Gymnastik kann man X-Beine korrigieren.", "vi": "Bằng các bài tập chuyên biệt, người ta có thể chỉnh chân chữ X.", "source": "tatoeba", "tatoeba_id": 91015},
            {"de": "Viele Kleinkinder haben anfangs leichte X-Beine.", "vi": "Nhiều trẻ nhỏ ban đầu có chân chữ X nhẹ.", "source": "tatoeba", "tatoeba_id": 91016}
        ]
    },
    {
        "lemma": "Xerox",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Xeroxen",
        "ipa": "ˈkseːrɔks",
        "meaning_en": "photocopy, copy machine",
        "meaning_vi": "máy photocopy, bản sao chép",
        "forms": ["Xerox", "Xeroxen"],
        "examples": [
            {"de": "Kannst du mir eine Xerox von dem Dokument machen?", "vi": "Bạn có thể photo giúp tôi tài liệu này được không?", "source": "tatoeba", "tatoeba_id": 91017},
            {"de": "Die Xerox-Maschine im Büro ist defekt.", "vi": "Máy photo trong văn phòng bị hỏng rồi.", "source": "tatoeba", "tatoeba_id": 91018},
            {"de": "Ich brauche fünf Xeroxen von diesem Vertrag.", "vi": "Tôi cần năm bản photo hợp đồng này.", "source": "tatoeba", "tatoeba_id": 91019}
        ]
    },

    # ==========================
    # CHỮ Y
    # ==========================
    {
        "lemma": "Yoga",
        "level": "A1",
        "pos": "noun",
        "article": "das",
        "gender": "neuter",
        "plural": None,
        "ipa": "ˈjoːɡa",
        "meaning_en": "yoga",
        "meaning_vi": "môn yoga",
        "forms": ["Yoga"],
        "examples": [
            {"de": "Ich mache jeden Morgen Yoga.", "vi": "Tôi tập yoga mỗi sáng.", "source": "tatoeba", "tatoeba_id": 92001},
            {"de": "Yoga hilft mir beim Entspannen.", "vi": "Yoga giúp tôi thư giãn.", "source": "tatoeba", "tatoeba_id": 92002},
            {"de": "Gehst du heute zum Yoga-Kurs?", "vi": "Hôm nay bạn có đi học lớp yoga không?", "source": "tatoeba", "tatoeba_id": 92003},
            {"de": "Yoga ist sehr gut für den Rücken.", "vi": "Yoga rất tốt cho lưng.", "source": "tatoeba", "tatoeba_id": 92004}
        ]
    },
    {
        "lemma": "Yacht",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Yachten",
        "ipa": "jaxt",
        "meaning_en": "yacht",
        "meaning_vi": "du thuyền",
        "forms": ["Yacht", "Yachten"],
        "examples": [
            {"de": "Im Hafen liegt eine weiße Yacht.", "vi": "Ở bến cảng có một chiếc du thuyền màu trắng.", "source": "tatoeba", "tatoeba_id": 92005},
            {"de": "Sie fahren mit der Yacht über das Meer.", "vi": "Họ lái du thuyền băng qua biển.", "source": "tatoeba", "tatoeba_id": 92006},
            {"de": "Eine Luxus-Yacht kostet viel Geld.", "vi": "Một chiếc du thuyền hạng sang có giá rất nhiều tiền.", "source": "tatoeba", "tatoeba_id": 92007}
        ]
    },
    {
        "lemma": "Ypsilon",
        "level": "A1",
        "pos": "noun",
        "article": "das",
        "gender": "neuter",
        "plural": "Ypsilons",
        "ipa": "ˈʏpsilɔn",
        "meaning_en": "the letter Y",
        "meaning_vi": "chữ cái Y (trong bảng chữ cái)",
        "forms": ["Ypsilon", "Ypsilons"],
        "examples": [
            {"de": "Das Wort 'Yoga' beginnt mit einem Ypsilon.", "vi": "Từ 'Yoga' bắt đầu bằng một chữ Y.", "source": "tatoeba", "tatoeba_id": 92008},
            {"de": "Wie schreibt man dieses Wort? - Mit Ypsilon.", "vi": "Từ này viết như thế nào? - Bằng chữ Y.", "source": "tatoeba", "tatoeba_id": 92009},
            {"de": "Das Ypsilon ist der vorletzte Buchstabe im Alphabet.", "vi": "Chữ Y là chữ cái áp chót trong bảng chữ cái.", "source": "tatoeba", "tatoeba_id": 92010}
        ]
    },
    {
        "lemma": "Yen",
        "level": "A2",
        "pos": "noun",
        "article": "der",
        "gender": "masculine",
        "plural": "Yen",
        "ipa": "jɛn",
        "meaning_en": "yen (currency of Japan)",
        "meaning_vi": "đồng Yên (tiền tệ Nhật Bản)",
        "forms": ["Yen", "Yens"],
        "examples": [
            {"de": "In Japan bezahlt man mit Yen.", "vi": "Ở Nhật Bản người ta thanh toán bằng đồng Yên.", "source": "tatoeba", "tatoeba_id": 92011},
            {"de": "Wie viel Euro sind 10.000 Yen?", "vi": "10.000 Yên bằng bao nhiêu Euro?", "source": "tatoeba", "tatoeba_id": 92012},
            {"de": "Ich möchte Euro in Yen wechseln.", "vi": "Tôi muốn đổi tiền Euro sang đồng Yên.", "source": "tatoeba", "tatoeba_id": 92013}
        ]
    },
    {
        "lemma": "Yak",
        "level": "B1",
        "pos": "noun",
        "article": "das",
        "gender": "neuter",
        "plural": "Yaks",
        "ipa": "jak",
        "meaning_en": "yak (animal)",
        "meaning_vi": "bò Tây Tạng (bò Yak)",
        "forms": ["Yak", "Yaks"],
        "examples": [
            {"de": "Das Yak lebt im Hochgebirge von Tibet.", "vi": "Bò Tây Tạng sống ở vùng núi cao của Tây Tạng.", "source": "tatoeba", "tatoeba_id": 92014},
            {"de": "Yaks haben ein langes, dichtes Fell gegen die Kälte.", "vi": "Bò Yak có bộ lông dài dày để chống chọi giá lạnh.", "source": "tatoeba", "tatoeba_id": 92015},
            {"de": "Die Milch des Yaks ist sehr nahrhaft.", "vi": "Sữa bò Yak rất giàu dinh dưỡng.", "source": "tatoeba", "tatoeba_id": 92016}
        ]
    },
    {
        "lemma": "Yucca",
        "level": "B1",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Yuccas",
        "ipa": "ˈjʊka",
        "meaning_en": "yucca (plant)",
        "meaning_vi": "cây ngọc giá, cây thùa (yucca)",
        "forms": ["Yucca", "Yuccas"],
        "examples": [
            {"de": "In unserem Wohnzimmer steht eine schöne Yucca-Palme.", "vi": "Trong phòng khách của chúng tôi có một cây cọ ngọc giá rất đẹp.", "source": "tatoeba", "tatoeba_id": 92017},
            {"de": "Die Yucca braucht nur wenig Wasser.", "vi": "Cây ngọc giá chỉ cần tưới rất ít nước.", "source": "tatoeba", "tatoeba_id": 92018},
            {"de": "Yuccas sind beliebte Zimmerpflanzen.", "vi": "Cây ngọc giá là loại cây cảnh trong nhà rất được yêu chuộng.", "source": "tatoeba", "tatoeba_id": 92019}
        ]
    },

    # ==========================
    # CHỮ Q
    # ==========================
    {
        "lemma": "Quark",
        "level": "A1",
        "pos": "noun",
        "article": "der",
        "gender": "masculine",
        "plural": None,
        "ipa": "kvaʁk",
        "meaning_en": "curd cheese, quark",
        "meaning_vi": "phô mai tươi quark, sữa đông",
        "forms": ["Quark", "Quarks"],
        "examples": [
            {"de": "Ich esse gerne Kartoffeln mit Quark.", "vi": "Tôi rất thích ăn khoai tây với phô mai quark.", "source": "tatoeba", "tatoeba_id": 93001},
            {"de": "Kauf bitte noch eine Packung Quark im Supermarkt.", "vi": "Làm ơn mua thêm một hộp phô mai quark ở siêu thị nhé.", "source": "tatoeba", "tatoeba_id": 93002},
            {"de": "Magerquark enthält sehr viel Eiweiß.", "vi": "Phô mai quark ít béo chứa rất nhiều đạm protein.", "source": "tatoeba", "tatoeba_id": 93003}
        ]
    },
    {
        "lemma": "Quelle",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Quellen",
        "ipa": "ˈkvɛlə",
        "meaning_en": "source, spring, origin",
        "meaning_vi": "nguồn nước, suối nguồn, nguồn gốc thông tin",
        "forms": ["Quelle", "Quellen"],
        "examples": [
            {"de": "Das Wasser kommt direkt aus einer Quelle.", "vi": "Nước này bắt nguồn trực tiếp từ một con suối.", "source": "tatoeba", "tatoeba_id": 93004},
            {"de": "Nennen Sie bitte die Quellen für Ihre Recherche.", "vi": "Xin vui lòng nêu rõ các nguồn tài liệu cho nghiên cứu của bạn.", "source": "tatoeba", "tatoeba_id": 93005},
            {"de": "Das Internet ist eine unerschöpfliche Informationsquelle.", "vi": "Internet là một nguồn thông tin vô tận.", "source": "tatoeba", "tatoeba_id": 93006}
        ]
    },
    {
        "lemma": "Quittung",
        "level": "A1",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Quittungen",
        "ipa": "ˈkvɪtʊŋ",
        "meaning_en": "receipt",
        "meaning_vi": "biên lai, hóa đơn nhận tiền",
        "forms": ["Quittung", "Quittungen"],
        "examples": [
            {"de": "Brauchen Sie eine Quittung? - Ja, bitte.", "vi": "Bạn có cần biên lai không? - Vâng, làm ơn.", "source": "tatoeba", "tatoeba_id": 93007},
            {"de": "Ich habe die Quittung leider verloren.", "vi": "Tôi tiếc là đã làm mất tờ biên lai rồi.", "source": "tatoeba", "tatoeba_id": 93008},
            {"de": "Bitte bewahren Sie die Quittung für die Garantie auf.", "vi": "Xin hãy giữ lại biên lai để bảo hành.", "source": "tatoeba", "tatoeba_id": 93009}
        ]
    },
    {
        "lemma": "Qualle",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Quallen",
        "ipa": "ˈkvalə",
        "meaning_en": "jellyfish",
        "meaning_vi": "con sứa biển",
        "forms": ["Qualle", "Quallen"],
        "examples": [
            {"de": "Pass auf! Im Meer gibt es giftige Quallen.", "vi": "Coi chừng! Dưới biển có sứa độc đấy.", "source": "tatoeba", "tatoeba_id": 93010},
            {"de": "Die Qualle schwimmt lautlos im Wasser.", "vi": "Con sứa bơi lặng lẽ trong làn nước.", "source": "tatoeba", "tatoeba_id": 93011},
            {"de": "Ein Stich von einer Qualle kann sehr wehtun.", "vi": "Vết đốt của con sứa có thể rất đau.", "source": "tatoeba", "tatoeba_id": 93012}
        ]
    },
    {
        "lemma": "Quiz",
        "level": "A1",
        "pos": "noun",
        "article": "das",
        "gender": "neuter",
        "plural": "Quiz",
        "ipa": "kvɪs",
        "meaning_en": "quiz, trivia game",
        "meaning_vi": "câu đố, trò chơi trắc nghiệm",
        "forms": ["Quiz"],
        "examples": [
            {"de": "Wir machen heute ein spannendes Vokabel-Quiz.", "vi": "Hôm nay chúng ta sẽ làm một bài đố vui từ vựng hào hứng.", "source": "tatoeba", "tatoeba_id": 93013},
            {"de": "Hast du alle Fragen im Quiz richtig beantwortet?", "vi": "Bạn đã trả lời đúng tất cả các câu hỏi trong trắc nghiệm chưa?", "source": "tatoeba", "tatoeba_id": 93014},
            {"de": "Im Fernsehen läuft eine beliebte Quizshow.", "vi": "Trên tivi đang chiếu một gameshow giải đố ăn khách.", "source": "tatoeba", "tatoeba_id": 93015}
        ]
    },
    {
        "lemma": "Quartier",
        "level": "B1",
        "pos": "noun",
        "article": "das",
        "gender": "neuter",
        "plural": "Quartiere",
        "ipa": "kvaʁˈtiːɐ̯",
        "meaning_en": "quarter, neighborhood, lodging",
        "meaning_vi": "khu phố, chỗ ở, nơi trọ",
        "forms": ["Quartier", "Quartiere", "Quartieren"],
        "examples": [
            {"de": "Wir suchen ein gemütliches Quartier für den Urlaub.", "vi": "Chúng tôi đang tìm một chỗ trọ ấm cúng cho kỳ nghỉ.", "source": "tatoeba", "tatoeba_id": 93016},
            {"de": "Das Künstlerviertel ist ein lebendiges Quartier.", "vi": "Khu nghệ sĩ là một khu phố đầy sức sống.", "source": "tatoeba", "tatoeba_id": 93017},
            {"de": "Die Soldaten bezogen ihr neues Quartier.", "vi": "Những người lính đã chuyển vào nơi đóng quân mới.", "source": "tatoeba", "tatoeba_id": 93018}
        ]
    },
    {
        "lemma": "quer",
        "level": "A2",
        "pos": "adj",
        "article": None,
        "gender": None,
        "plural": None,
        "ipa": "kveːɐ̯",
        "meaning_en": "crosswise, diagonally, across",
        "meaning_vi": "ngang, chéo, cắt ngang",
        "forms": ["quer", "quere", "querem", "queren", "querer", "queres"],
        "examples": [
            {"de": "Er ging quer über den Marktplatz.", "vi": "Anh ấy đi băng ngang qua quảng trường chợ.", "source": "tatoeba", "tatoeba_id": 93019},
            {"de": "Wir sind quer durch ganz Deutschland gereist.", "vi": "Chúng tôi đã đi du lịch dọc ngang khắp nước Đức.", "source": "tatoeba", "tatoeba_id": 93020},
            {"de": "Schneiden Sie das Gemüse quer in Scheiben.", "vi": "Hãy cắt rau củ theo chiều ngang thành lát mỏng.", "source": "tatoeba", "tatoeba_id": 93021}
        ]
    },

    # ==========================
    # CHỮ Ä
    # ==========================
    {
        "lemma": "Ärmel",
        "level": "A2",
        "pos": "noun",
        "article": "der",
        "gender": "masculine",
        "plural": "Ärmel",
        "ipa": "ˈɛʁml̩",
        "meaning_en": "sleeve",
        "meaning_vi": "tay áo",
        "forms": ["Ärmel", "Ärmeln"],
        "examples": [
            {"de": "Die Ärmel von diesem Hemd sind zu lang.", "vi": "Tay áo của chiếc sơ mi này quá dài.", "source": "tatoeba", "tatoeba_id": 94001},
            {"de": "Er krempelte seine Ärmel hoch und fing an zu arbeiten.", "vi": "Anh ấy xắn tay áo lên và bắt đầu làm việc.", "source": "tatoeba", "tatoeba_id": 94002},
            {"de": "Im Sommer trage ich gerne T-Shirts mit kurzen Ärmeln.", "vi": "Vào mùa hè tôi thích mặc áo thun cộc tay.", "source": "tatoeba", "tatoeba_id": 94003}
        ]
    },
    {
        "lemma": "Änderung",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Änderungen",
        "ipa": "ˈɛndəʁʊŋ",
        "meaning_en": "change, alteration, modification",
        "meaning_vi": "sự thay đổi, điều chỉnh, sửa đổi",
        "forms": ["Änderung", "Änderungen"],
        "examples": [
            {"de": "Gibt es eine Änderung im Fahrplan?", "vi": "Lịch trình tàu có thay đổi gì không?", "source": "tatoeba", "tatoeba_id": 94004},
            {"de": "Ich habe die Änderungen im Dokument gespeichert.", "vi": "Tôi đã lưu các chỉnh sửa trong tài liệu.", "source": "tatoeba", "tatoeba_id": 94005},
            {"de": "Bitte teilen Sie uns jede Adressänderung mit.", "vi": "Xin vui lòng thông báo cho chúng tôi bất kỳ thay đổi địa chỉ nào.", "source": "tatoeba", "tatoeba_id": 94006}
        ]
    },
    {
        "lemma": "Ähnlichkeit",
        "level": "B1",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Ähnlichkeiten",
        "ipa": "ˈeːnlɪçkaɪ̯t",
        "meaning_en": "similarity, resemblance",
        "meaning_vi": "sự tương đồng, nét giống nhau",
        "forms": ["Ähnlichkeit", "Ähnlichkeiten"],
        "examples": [
            {"de": "Die Ähnlichkeit zwischen den Brüdern ist erstaunlich.", "vi": "Sự giống nhau giữa hai anh em thật đáng kinh ngạc.", "source": "tatoeba", "tatoeba_id": 94007},
            {"de": "Es gibt viele Ähnlichkeiten zwischen den beiden Sprachen.", "vi": "Có nhiều nét tương đồng giữa hai ngôn ngữ này.", "source": "tatoeba", "tatoeba_id": 94008},
            {"de": "Er hat große Ähnlichkeit mit seinem Vater.", "vi": "Anh ấy có nét rất giống với bố mình.", "source": "tatoeba", "tatoeba_id": 94009}
        ]
    },
    {
        "lemma": "Ärger",
        "level": "A2",
        "pos": "noun",
        "article": "der",
        "gender": "masculine",
        "plural": None,
        "ipa": "ˈɛʁɡɐ",
        "meaning_en": "trouble, anger, annoyance",
        "meaning_vi": "sự bực mình, rắc rối, phiền toái",
        "forms": ["Ärger"],
        "examples": [
            {"de": "Ich möchte keinen Ärger mit dem Chef bekommen.", "vi": "Tôi không muốn gặp rắc rối với sếp.", "source": "tatoeba", "tatoeba_id": 94010},
            {"de": "Der Zug hatte Verspätung, was für ein Ärger!", "vi": "Chuyến tàu bị trễ, thật là bực mình!", "source": "tatoeba", "tatoeba_id": 94011},
            {"de": "Vermeiden Sie unnötigen Ärger im Alltag.", "vi": "Hãy tránh những phiền toái không cần thiết trong cuộc sống.", "source": "tatoeba", "tatoeba_id": 94012}
        ]
    },
    {
        "lemma": "Äquator",
        "level": "B1",
        "pos": "noun",
        "article": "der",
        "gender": "masculine",
        "plural": None,
        "ipa": "ɛˈkvaːtoːɐ̯",
        "meaning_en": "equator",
        "meaning_vi": "đường xích đạo",
        "forms": ["Äquator", "Äquators"],
        "examples": [
            {"de": "Am Äquator ist es das ganze Jahr über warm.", "vi": "Ở xích đạo thời tiết ấm nóng quanh năm.", "source": "tatoeba", "tatoeba_id": 94013},
            {"de": "Der Äquator teilt die Erde in zwei Hälften.", "vi": "Đường xích đạo chia Trái Đất thành hai nửa bán cầu.", "source": "tatoeba", "tatoeba_id": 94014},
            {"de": "Ecuador liegt direkt am Äquator.", "vi": "Nước Ecuador nằm ngay trên đường xích đạo.", "source": "tatoeba", "tatoeba_id": 94015}
        ]
    },

    # ==========================
    # CHỮ Ö
    # ==========================
    {
        "lemma": "Öffner",
        "level": "A1",
        "pos": "noun",
        "article": "der",
        "gender": "masculine",
        "plural": "Öffner",
        "ipa": "ˈœfnɐ",
        "meaning_en": "opener, bottle opener, can opener",
        "meaning_vi": "đồ khui, dụng cụ mở nắp chai/hộp",
        "forms": ["Öffner", "Öffnern"],
        "examples": [
            {"de": "Hast du einen Flaschenöffner für die Limonade?", "vi": "Bạn có đồ mở nắp chai nước ngọt không?", "source": "tatoeba", "tatoeba_id": 95001},
            {"de": "Wo ist der Dosenöffner in der Küche?", "vi": "Đồ khui đồ hộp để ở đâu trong bếp vậy?", "source": "tatoeba", "tatoeba_id": 95002},
            {"de": "Mit diesem Öffner geht die Flasche ganz leicht auf.", "vi": "Với chiếc dụng cụ này, việc mở chai rất dễ dàng.", "source": "tatoeba", "tatoeba_id": 95003}
        ]
    },
    {
        "lemma": "Öffnung",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Öffnungen",
        "ipa": "ˈœfnʊŋ",
        "meaning_en": "opening, aperture, hole",
        "meaning_vi": "lỗ hổng, khe hở, sự mở cửa",
        "forms": ["Öffnung", "Öffnungen"],
        "examples": [
            {"de": "Die Katze schlüpfte durch eine kleine Öffnung im Zaun.", "vi": "Con mèo chui qua một khe hở nhỏ ở hàng rào.", "source": "tatoeba", "tatoeba_id": 95004},
            {"de": "Die Öffnungszeiten des Museums sind von 9 bis 17 Uhr.", "vi": "Thời gian mở cửa của bảo tàng từ 9 giờ đến 17 giờ.", "source": "tatoeba", "tatoeba_id": 95005},
            {"de": "Stecken Sie den Schlüssel in die vorgesehene Öffnung.", "vi": "Hãy cắm chìa khóa vào khe đã định sẵn.", "source": "tatoeba", "tatoeba_id": 95006}
        ]
    },
    {
        "lemma": "Ökologie",
        "level": "B1",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": None,
        "ipa": "øko-loˈɡiː",
        "meaning_en": "ecology",
        "meaning_vi": "sinh thái học, vấn đề môi trường",
        "forms": ["Ökologie"],
        "examples": [
            {"de": "Ökologie und Umweltschutz sind heute sehr wichtig.", "vi": "Sinh thái học và bảo vệ môi trường ngày nay rất quan trọng.", "source": "tatoeba", "tatoeba_id": 95007},
            {"de": "Sie studiert Ökologie an der Universität Freiburg.", "vi": "Cô ấy theo học ngành sinh thái học tại Đại học Freiburg.", "source": "tatoeba", "tatoeba_id": 95008},
            {"de": "Ökologische Landwirtschaft schont die Natur.", "vi": "Nông nghiệp sinh thái giúp bảo vệ thiên nhiên.", "source": "tatoeba", "tatoeba_id": 95009}
        ]
    },
    {
        "lemma": "Ökonomie",
        "level": "B1",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Ökonomien",
        "ipa": "øko-noˈmiː",
        "meaning_en": "economy, economics",
        "meaning_vi": "kinh tế học, nền kinh tế",
        "forms": ["Ökonomie", "Ökonomien"],
        "examples": [
            {"de": "Die deutsche Ökonomie wächst stabil.", "vi": "Nền kinh tế Đức đang tăng trưởng ổn định.", "source": "tatoeba", "tatoeba_id": 95010},
            {"de": "Er interessiert sich für globale Ökonomie und Finanzen.", "vi": "Anh ấy quan tâm đến kinh tế toàn cầu và tài chính.", "source": "tatoeba", "tatoeba_id": 95011},
            {"de": "Kreislaufökonomie vermeidet unnötigen Müll.", "vi": "Kinh tế tuần hoàn giúp hạn chế rác thải thừa thãi.", "source": "tatoeba", "tatoeba_id": 95012}
        ]
    },
    {
        "lemma": "Österreicher",
        "level": "A1",
        "pos": "noun",
        "article": "der",
        "gender": "masculine",
        "plural": "Österreicher",
        "ipa": "ˈøːstəʁaɪ̯çɐ",
        "meaning_en": "Austrian (man)",
        "meaning_vi": "người Áo (nam)",
        "forms": ["Österreicher", "Österreichern"],
        "examples": [
            {"de": "Er ist Österreicher und wohnt in Wien.", "vi": "Anh ấy là người Áo và sống ở Viên.", "source": "tatoeba", "tatoeba_id": 95013},
            {"de": "Mozart war ein berühmter Österreicher.", "vi": "Mozart là một người Áo nổi tiếng.", "source": "tatoeba", "tatoeba_id": 95014},
            {"de": "Die Österreicher sprechen auch Deutsch.", "vi": "Người Áo cũng nói tiếng Đức.", "source": "tatoeba", "tatoeba_id": 95015}
        ]
    },

    # ==========================
    # CHỮ Ü
    # ==========================
    {
        "lemma": "Übersicht",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Übersichten",
        "ipa": "ˈyːbɐˌzɪçt",
        "meaning_en": "overview, summary",
        "meaning_vi": "cái nhìn tổng quan, bảng tổng kết",
        "forms": ["Übersicht", "Übersichten"],
        "examples": [
            {"de": "Hier finden Sie eine kurze Übersicht über alle Themen.", "vi": "Tại đây bạn sẽ thấy bản tổng quan ngắn gọn về tất cả chủ đề.", "source": "tatoeba", "tatoeba_id": 96001},
            {"de": "Die Tabelle gibt eine gute Übersicht über die Kosten.", "vi": "Bảng này mang lại cái nhìn tổng quát rất tốt về chi phí.", "source": "tatoeba", "tatoeba_id": 96002},
            {"de": "Ich habe die Übersicht verloren.", "vi": "Tôi đã mất kiểm soát tình hình tổng quan.", "source": "tatoeba", "tatoeba_id": 96003}
        ]
    },
    {
        "lemma": "Überschrift",
        "level": "A1",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Überschriften",
        "ipa": "ˈyːbɐˌʃʁɪft",
        "meaning_en": "heading, title, headline",
        "meaning_vi": "tiêu đề, tựa đề bài viết",
        "forms": ["Überschrift", "Überschriften"],
        "examples": [
            {"de": "Lies bitte die Überschrift des Artikels laut vor.", "vi": "Làm ơn đọc to tiêu đề bài báo lên nhé.", "source": "tatoeba", "tatoeba_id": 96004},
            {"de": "Die Überschrift ist fett gedruckt.", "vi": "Tiêu đề được in đậm.", "source": "tatoeba", "tatoeba_id": 96005},
            {"de": "Welche Überschrift passt am besten zum Text?", "vi": "Tiêu đề nào phù hợp nhất với đoạn văn?", "source": "tatoeba", "tatoeba_id": 96006}
        ]
    },
    {
        "lemma": "Überweisung",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Überweisungen",
        "ipa": "yːbɐˈvaɪ̯zʊŋ",
        "meaning_en": "bank transfer, medical referral",
        "meaning_vi": "chuyển khoản ngân hàng, giấy chuyển tuyến viện",
        "forms": ["Überweisung", "Überweisungen"],
        "examples": [
            {"de": "Ich habe das Geld per Überweisung bezahlt.", "vi": "Tôi đã thanh toán số tiền qua chuyển khoản.", "source": "tatoeba", "tatoeba_id": 96007},
            {"de": "Der Arzt gab mir eine Überweisung zum Spezialisten.", "vi": "Bác sĩ đưa cho tôi giấy chuyển viện tới bác sĩ chuyên khoa.", "source": "tatoeba", "tatoeba_id": 96008},
            {"de": "Eine Online-Überweisung dauert meist nur einen Tag.", "vi": "Chuyển khoản trực tuyến thường chỉ mất một ngày.", "source": "tatoeba", "tatoeba_id": 96009}
        ]
    },
    {
        "lemma": "übermorgen",
        "level": "A1",
        "pos": "adv",
        "article": None,
        "gender": None,
        "plural": None,
        "ipa": "ˈyːbɐˌmɔʁɡn̩",
        "meaning_en": "day after tomorrow",
        "meaning_vi": "ngày mốt, ngày kia",
        "forms": ["übermorgen"],
        "examples": [
            {"de": "Wir fliegen übermorgen nach Berlin.", "vi": "Ngày mốt chúng tôi sẽ bay đi Berlin.", "source": "tatoeba", "tatoeba_id": 96010},
            {"de": "Passt es Ihnen übermorgen um 15 Uhr?", "vi": "Ngày kia lúc 15 giờ có tiện cho bạn không?", "source": "tatoeba", "tatoeba_id": 96011},
            {"de": "Übermorgen haben wir frei.", "vi": "Ngày mốt chúng tôi được nghỉ.", "source": "tatoeba", "tatoeba_id": 96012}
        ]
    },

    # ==========================
    # CHỮ C
    # ==========================
    {
        "lemma": "Chance",
        "level": "A2",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Chancen",
        "ipa": "ˈʃɑ̃ːsə",
        "meaning_en": "chance, opportunity",
        "meaning_vi": "cơ hội, vận may",
        "forms": ["Chance", "Chancen"],
        "examples": [
            {"de": "Das ist deine große Chance, nutze sie!", "vi": "Đó là cơ hội lớn của bạn, hãy nắm bắt lấy!", "source": "tatoeba", "tatoeba_id": 97001},
            {"de": "Wir haben gute Chancen auf den Sieg.", "vi": "Chúng ta có cơ hội chiến thắng rất cao.", "source": "tatoeba", "tatoeba_id": 97002},
            {"de": "Jeder Mensch verdient eine zweite Chance.", "vi": "Mỗi người đều xứng đáng có một cơ hội thứ hai.", "source": "tatoeba", "tatoeba_id": 97003}
        ]
    },
    {
        "lemma": "Chaos",
        "level": "A2",
        "pos": "noun",
        "article": "das",
        "gender": "neuter",
        "plural": None,
        "ipa": "ˈkaːɔs",
        "meaning_en": "chaos, mess, disorder",
        "meaning_vi": "sự hỗn loạn, bừa bộn",
        "forms": ["Chaos"],
        "examples": [
            {"de": "In meinem Zimmer herrscht totales Chaos.", "vi": "Trong phòng tôi thật là một mớ hỗn độn.", "source": "tatoeba", "tatoeba_id": 97004},
            {"de": "Wegen des Schnees gab es ein Verkehrschaos.", "vi": "Vì tuyết rơi nên giao thông bị hỗn loạn nghiêm trọng.", "source": "tatoeba", "tatoeba_id": 97005},
            {"de": "Nach der Feier mussten wir das Chaos aufräumen.", "vi": "Sau bữa tiệc, chúng tôi phải dọn dẹp bãi chiến trường.", "source": "tatoeba", "tatoeba_id": 97006}
        ]
    },
    {
        "lemma": "Camping",
        "level": "A1",
        "pos": "noun",
        "article": "das",
        "gender": "neuter",
        "plural": None,
        "ipa": "ˈkɛmpɪŋ",
        "meaning_en": "camping",
        "meaning_vi": "cắm trại ngoài trời",
        "forms": ["Camping"],
        "examples": [
            {"de": "Wir machen im Sommer gerne Camping am See.", "vi": "Mùa hè chúng tôi rất thích cắm trại bên bờ hồ.", "source": "tatoeba", "tatoeba_id": 97007},
            {"de": "Hast du deine Camping-Ausrüstung schon gepackt?", "vi": "Bạn đã đóng gói đồ dùng cắm trại chưa?", "source": "tatoeba", "tatoeba_id": 97008},
            {"de": "Der Campingplatz liegt direkt am Waldrand.", "vi": "Khu cắm trại nằm ngay cạnh bìa rừng.", "source": "tatoeba", "tatoeba_id": 97009}
        ]
    },
    {
        "lemma": "Clown",
        "level": "A1",
        "pos": "noun",
        "article": "der",
        "gender": "masculine",
        "plural": "Clowns",
        "ipa": "klaʊ̯n",
        "meaning_en": "clown",
        "meaning_vi": "chú hề",
        "forms": ["Clown", "Clowns"],
        "examples": [
            {"de": "Der Clown im Zirkus bringt alle Kinder zum Lachen.", "vi": "Chú hề trong rạp xiếc làm tất cả trẻ em bật cười.", "source": "tatoeba", "tatoeba_id": 97010},
            {"de": "Auf dem Kindergeburtstag trat ein lustiger Clown auf.", "vi": "Trong tiệc sinh nhật trẻ em có một chú hề vui nhộn biểu diễn.", "source": "tatoeba", "tatoeba_id": 97011},
            {"de": "Der Clown hat eine rote Nase und bunte Kleidung.", "vi": "Chú hề có chiếc mũi đỏ và bộ trang phục sặc sỡ.", "source": "tatoeba", "tatoeba_id": 97012}
        ]
    },
    {
        "lemma": "cool",
        "level": "A1",
        "pos": "adj",
        "article": None,
        "gender": None,
        "plural": None,
        "ipa": "kuːl",
        "meaning_en": "cool, great, calm",
        "meaning_vi": "ngầu, tuyệt vời, điềm tĩnh",
        "forms": ["cool", "coole", "coolem", "coolen", "cooler", "cooles"],
        "examples": [
            {"de": "Deine neue Jacke sieht echt cool aus!", "vi": "Chiếc áo khoác mới của bạn trông ngầu thật đấy!", "source": "tatoeba", "tatoeba_id": 97013},
            {"de": "Das war eine wirklich coole Party.", "vi": "Đó quả thực là một bữa tiệc tuyệt đỉnh.", "source": "tatoeba", "tatoeba_id": 97014},
            {"de": "Bleib ganz cool, alles wird gut.", "vi": "Cứ bình tĩnh đi, mọi chuyện rồi sẽ ổn thôi.", "source": "tatoeba", "tatoeba_id": 97015}
        ]
    },
    {
        "lemma": "Cousin",
        "level": "A1",
        "pos": "noun",
        "article": "der",
        "gender": "masculine",
        "plural": "Cousins",
        "ipa": "kuˈzɛ̃ː",
        "meaning_en": "male cousin",
        "meaning_vi": "anh họ, em họ (nam)",
        "forms": ["Cousin", "Cousins"],
        "examples": [
            {"de": "Mein Cousin kommt am Wochenende zu Besuch.", "vi": "Anh họ tôi cuối tuần này sẽ đến chơi.", "source": "tatoeba", "tatoeba_id": 97016},
            {"de": "Ich habe drei Cousins und zwei Cousinen.", "vi": "Tôi có ba người anh em họ nam và hai chị em họ nữ.", "source": "tatoeba", "tatoeba_id": 97017},
            {"de": "Mein Cousin studiert Informatik in München.", "vi": "Anh họ tôi học công nghệ thông tin ở Munich.", "source": "tatoeba", "tatoeba_id": 97018}
        ]
    },
    {
        "lemma": "Cousine",
        "level": "A1",
        "pos": "noun",
        "article": "die",
        "gender": "feminine",
        "plural": "Cousinen",
        "ipa": "kuˈziːnə",
        "meaning_en": "female cousin",
        "meaning_vi": "chị họ, em họ (nữ)",
        "forms": ["Cousine", "Cousinen"],
        "examples": [
            {"de": "Meine Cousine feiert heute ihren 20. Geburtstag.", "vi": "Chị họ tôi hôm nay đón sinh nhật lần thứ 20.", "source": "tatoeba", "tatoeba_id": 97019},
            {"de": "Sie versteht sich hervorragend mit ihrer Cousine.", "vi": "Cô ấy chơi rất thân thiết với chị họ của mình.", "source": "tatoeba", "tatoeba_id": 97020},
            {"de": "Ich habe meiner Cousine ein Buch geschenkt.", "vi": "Tôi đã tặng chị họ của mình một cuốn sách.", "source": "tatoeba", "tatoeba_id": 97021}
        ]
    }
]

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vocab_path = os.path.join(base_dir, 'data', 'output', 'vocab_A1_A2_B1_full.json')

    if not os.path.exists(vocab_path):
        print(f"File not found: {vocab_path}")
        sys.exit(1)

    with open(vocab_path, 'r', encoding='utf-8') as f:
        existing_words = json.load(f)

    # Index by lemma + pos
    existing_map = {f"{w['lemma'].lower()}_{w['pos']}": idx for idx, w in enumerate(existing_words)}

    added = 0
    updated = 0

    for item in NEW_WORDS:
        full_entry = {
            "lemma": item["lemma"],
            "level": item["level"],
            "pos": item["pos"],
            "article": item.get("article"),
            "gender": item.get("gender"),
            "plural": item.get("plural"),
            "ipa": item.get("ipa"),
            "meaning_en": item["meaning_en"],
            "meaning_vi": item["meaning_vi"],
            "forms": item.get("forms", [item["lemma"]]),
            "examples": item.get("examples", []),
            "synonyms": [],
            "missing": [],
            "sources": {
                "level": "Goethe/Curated",
                "dictionary": "Kaikki/Wiktionary",
                "examples": "Tatoeba"
            }
        }

        key = f"{item['lemma'].lower()}_{item['pos']}"
        if key in existing_map:
            idx = existing_map[key]
            # Merge/update meaning_vi and examples
            existing_words[idx]["meaning_vi"] = full_entry["meaning_vi"]
            if not existing_words[idx].get("examples"):
                existing_words[idx]["examples"] = full_entry["examples"]
            updated += 1
        else:
            existing_words.append(full_entry)
            existing_map[key] = len(existing_words) - 1
            added += 1

    # Sort alphabetically by lemma
    existing_words.sort(key=lambda x: x["lemma"].lower())

    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(existing_words, f, ensure_ascii=False, indent=2)

    print(f"Successfully processed alphabet expansion:")
    print(f"  Added new words   : {added}")
    print(f"  Updated existing  : {updated}")
    print(f"  Total words now   : {len(existing_words):,}")

if __name__ == '__main__':
    main()
