#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate complete 1000 authentic, distinct German words across CEFR A1-C2 with accurate grammar and translations.
"""

import json

vocab = []
seen = set()

def add(w, g, pl, ipa, pos, lvl, vi, en, ex_de, ex_vi):
    if w in seen:
        return
    seen.add(w)
    vocab.append({
        "word": w,
        "gender": g,
        "plural_form": pl,
        "ipa": ipa,
        "pos": pos,
        "cefr_level": lvl,
        "meaning_vi": vi,
        "meaning_en": en,
        "example_de": ex_de,
        "example_vi": ex_vi
    })

# Load the initial A1 items from vocab_check.json
try:
    with open("/home/jikay/Desktop/LingoLearning/scripts/vocab_check.json", "r", encoding="utf-8") as f:
        a1_initial = json.load(f)
        for item in a1_initial:
            add(item["word"], item["gender"], item["plural_form"], item["ipa"], item["pos"], item["cefr_level"], item["meaning_vi"], item["meaning_en"], item["example_de"], item["example_vi"])
except Exception as e:
    print("Warning loading initial A1:", e)

print(f"Loaded {len(vocab)} words from A1 base.")

# -------------------------------------------------------------
# A2 EXPANSION (Target: 250 words)
# -------------------------------------------------------------
a2_data = [
    # Nouns Travel & Transport
    ("Flughafen", "der", "die Flughäfen", "/ˈfluːkˌhaːfn̩/", "Noun", "A2", "Sân bay", "Airport", "Der Flughafen Frankfurt ist sehr groß.", "Sân bay Frankfurt rất lớn."),
    ("Bahnsteig", "der", "die Bahnsteige", "/ˈbaːnˌʃtaɪ̯k/", "Noun", "A2", "Sân ga đón tàu", "Platform", "Der Zug fährt auf Bahnsteig 4 ein.", "Tàu đang vào sân ga số 4."),
    ("Fahrplan", "der", "die Fahrpläne", "/ˈfaːɐ̯ˌplaːn/", "Noun", "A2", "Lịch trình tàu xe", "Timetable", "Schau bitte im Fahrplan nach.", "Làm ơn tra lịch trình tàu xe."),
    ("Koffer", "der", "die Koffer", "/ˈkɔfɐ/", "Noun", "A2", "Vali du lịch", "Suitcase", "Ich packe meinen Koffer für den Urlaub.", "Tôi đang xếp đồ vào vali đi nghỉ."),
    ("Ausweis", "der", "die Ausweise", "/ˈaʊ̯sˌvaɪ̯s/", "Noun", "A2", "Thẻ căn cước", "ID card", "Zeigen Sie bitte Ihren Ausweis.", "Làm ơn xuất trình thẻ căn cước."),
    ("Reisepass", "der", "die Reisepässe", "/ˈʁaɪ̯zəˌpas/", "Noun", "A2", "Hộ chiếu", "Passport", "Mein Reisepass ist noch fünf Jahre gültig.", "Hộ chiếu của tôi còn hạn năm năm."),
    ("Führerschein", "der", "die Führerscheine", "/ˈfyːʁɐˌʃaɪ̯n/", "Noun", "A2", "Bằng lái xe", "Driving license", "Ich habe den Führerschein gemacht.", "Tôi đã thi lấy bằng lái xe."),
    ("Gepäck", "das", "die Gepäcke", "/ɡəˈpɛk/", "Noun", "A2", "Hành lý", "Luggage", "Geben Sie das Gepäck am Schalter auf.", "Hãy gửi hành lý tại quầy."),
    ("Verspätung", "die", "die Verspätungen", "/fɛɐ̯ˈʃpɛːtʊŋ/", "Noun", "A2", "Sự trễ giờ", "Delay", "Der Zug hat zehn Minuten Verspätung.", "Chuyến tàu bị trễ mười phút."),
    ("Verbindung", "die", "die Verbindungen", "/fɛɐ̯ˈbɪndʊŋ/", "Noun", "A2", "Tuyến nối, kết nối", "Connection", "Es gibt eine direkte Verbindung.", "Có một tuyến chạy thẳng."),
    ("Auskunft", "die", "die Auskünfte", "/ˈaʊ̯sˌkʊnft/", "Noun", "A2", "Thông tin hướng dẫn", "Information", "Fragen Sie am Schalter nach Auskunft.", "Hãy hỏi thông tin ở quầy."),
    ("Reise", "die", "die Reisen", "/ˈʁaɪ̯zə/", "Noun", "A2", "Chuyến đi, chuyến du lịch", "Journey", "Gute Reise und viel Spaß!", "Chúc chuyến đi tốt đẹp và vui vẻ!"),
    ("Gleis", "das", "die Gleise", "/ɡlaɪ̯s/", "Noun", "A2", "Đường ray", "Track", "Der Zug fährt von Gleis 3 ab.", "Tàu khởi hành từ đường ray 3."),
    ("Motorrad", "das", "die Motorräder", "/moˈtoːɐ̯ˌʁaːt/", "Noun", "A2", "Xe mô tô", "Motorcycle", "Er fährt am Wochenende Motorrad.", "Cuối tuần anh ấy lái xe mô tô."),
    ("Boot", "das", "die Boote", "/boːt/", "Noun", "A2", "Thuyền nhỏ", "Boat", "Wir mieten ein Boot am See.", "Chúng tôi thuê thuyền nhỏ trên hồ."),
    ("Fahrkarte", "die", "die Fahrkarten", "/ˈfaːɐ̯ˌkaʁtə/", "Noun", "A2", "Vé tàu xe", "Ticket", "Entwerten Sie bitte die Fahrkarte.", "Làm ơn bấm lỗ vé tàu xe."),
    # Health & Medical
    ("Krankheit", "die", "die Krankheiten", "/ˈkʁaŋkhaɪ̯t/", "Noun", "A2", "Căn bệnh", "Illness", "Die Krankheit ist heilbar.", "Căn bệnh có thể chữa khỏi."),
    ("Gesundheit", "die", "die Gesundheiten", "/ɡəˈzʊnthaɪ̯t/", "Noun", "A2", "Sức khỏe", "Health", "Gesundheit ist das Wichtigste.", "Sức khỏe là điều quan trọng nhất."),
    ("Medizin", "die", "die Medizinen", "/mediˈt͡siːn/", "Noun", "A2", "Thuốc men, y học", "Medicine", "Nehmen Sie die Medizin dreimal täglich.", "Uống thuốc ba lần mỗi ngày."),
    ("Tablette", "die", "die Tabletten", "/taˈblɛtə/", "Noun", "A2", "Viên thuốc", "Pill", "Die Tablette hilft gegen Schmerzen.", "Viên thuốc giúp giảm đau."),
    ("Untersuchung", "die", "die Untersuchungen", "/ʊntɐˈzuːxʊŋ/", "Noun", "A2", "Khám bệnh", "Examination", "Die Untersuchung war schmerzfrei.", "Việc khám bệnh không hề đau đớn."),
    ("Praxis", "die", "die Praxen", "/ˈpʁaksɪs/", "Noun", "A2", "Phòng khám bác sĩ", "Doctor's office", "Die Praxis öffnet um acht Uhr.", "Phòng khám mở cửa lúc tám giờ."),
    ("Rezept", "das", "die Rezepte", "/ʁeˈt͡sɛpt/", "Noun", "A2", "Đơn thuốc", "Prescription", "Der Arzt stellt ein Rezept aus.", "Bác sĩ kê một đơn thuốc."),
    ("Pflaster", "das", "die Pflaster", "/ˈpflastɐ/", "Noun", "A2", "Băng cá nhân", "Plaster", "Kleben Sie ein Pflaster auf die Wunde.", "Dán miếng băng lên vết thương."),
    ("Fieber", "das", "die Fieber", "/ˈfiːbɐ/", "Noun", "A2", "Cơn sốt", "Fever", "Das Kind hat hohes Fieber.", "Đứa bé bị sốt cao."),
    ("Schmerz", "der", "die Schmerzen", "/ʃmɛʁt͡s/", "Noun", "A2", "Cơn đau", "Pain", "Haben Sie starke Schmerzen?", "Bạn có bị đau nhiều không?"),
    ("Bauch", "der", "die Bäuche", "/baʊ̯x/", "Noun", "A2", "Bụng", "Stomach", "Mein Bauch tut weh.", "Bụng tôi bị đau."),
    ("Rücken", "der", "die Rücken", "/ˈʁʏkn̩/", "Noun", "A2", "Lưng", "Back", "Er hat Schmerzen im Rücken.", "Anh ấy bị đau ở lưng."),
    ("Arm", "der", "die Arme", "/aʁm/", "Noun", "A2", "Cánh tay", "Arm", "Der Arm ist eingegipst.", "Cánh tay đang được bó bột."),
    ("Bein", "das", "die Beine", "/baɪ̯n/", "Noun", "A2", "Chân", "Leg", "Mein linkes Bein schmerzt.", "Chân trái của tôi bị đau."),
    ("Knie", "das", "die Knie", "/kniː/", "Noun", "A2", "Đầu gối", "Knee", "Er stürzte auf das Knie.", "Anh ấy ngã đập đầu gối."),
    ("Zahn", "der", "die Zähne", "/t͡saːn/", "Noun", "A2", "Răng", "Tooth", "Der Zahnarzt bohrt den Zahn.", "Nha sĩ đang khoan răng."),
    ("Hals", "der", "die Hälse", "/hals/", "Noun", "A2", "Cổ họng", "Throat", "Ich habe Halsschmerzen.", "Tôi bị đau họng."),
    ("Haar", "das", "die Haare", "/haːɐ̯/", "Noun", "A2", "Mái tóc", "Hair", "Sie hat langes blondes Haar.", "Cô ấy có mái tóc vàng dài."),
    ("Herz", "das", "die Herzen", "/hɛʁt͡s/", "Noun", "A2", "Trái tim", "Heart", "Das Herz schlägt kräftig.", "Trái tim đập mạnh mẽ."),
    # Work & Living
    ("Beruf", "der", "die Berufe", "/bəˈʁuːf/", "Noun", "A2", "Nghề nghiệp", "Profession", "Welchen Beruf üben Sie aus?", "Bạn làm nghề nghiệp gì?"),
    ("Chef", "der", "die Chefs", "/ʃɛf/", "Noun", "A2", "Sếp nam", "Boss", "Mein Chef leitet das Meeting.", "Sếp tôi chủ trì cuộc họp."),
    ("Chefin", "die", "die Chefinnen", "/ˈʃɛfɪn/", "Noun", "A2", "Sếp nữ", "Female boss", "Unsere Chefin ist sehr kompetent.", "Sếp nữ của chúng tôi rất giỏi."),
    ("Kollege", "der", "die Kollegen", "/kɔˈleːɡə/", "Noun", "A2", "Đồng nghiệp nam", "Colleague", "Der Kollege hilft mir gern.", "Người đồng nghiệp vui vẻ giúp tôi."),
    ("Kollegin", "die", "die Kolleginnen", "/kɔˈleːɡɪn/", "Noun", "A2", "Đồng nghiệp nữ", "Female colleague", "Meine Kollegin hat Urlaub.", "Đồng nghiệp nữ của tôi đang nghỉ phép."),
    ("Büro", "das", "die Büros", "/byˈʁoː/", "Noun", "A2", "Văn phòng", "Office", "Das Büro liegt in der Innenstadt.", "Văn phòng nằm ở khu trung tâm."),
    ("Vertrag", "der", "die Verträge", "/fɛɐ̯ˈtʁaːk/", "Noun", "A2", "Bản hợp đồng", "Contract", "Ich habe den Vertrag unterschrieben.", "Tôi đã ký hợp đồng."),
    ("Gehalt", "das", "die Gehälter", "/ɡəˈhalt/", "Noun", "A2", "Tiền lương", "Salary", "Das Gehalt kommt am Monatsende.", "Tiền lương đến vào cuối tháng."),
    ("Miete", "die", "die Mieten", "/ˈmiːtə/", "Noun", "A2", "Tiền thuê nhà", "Rent", "Die Miete ist bezahlbar.", "Tiền thuê nhà trong mức chi trả được."),
    ("Vermieter", "der", "die Vermieter", "/fɛɐ̯ˈmiːtɐ/", "Noun", "A2", "Chủ nhà cho thuê", "Landlord", "Der Vermieter repariert das Dach.", "Chủ nhà đang sửa lại mái nhà."),
    ("Nachbar", "der", "die Nachbarn", "/ˈnaxbaːɐ̯/", "Noun", "A2", "Hàng xóm nam", "Neighbor", "Mein Nachbar ist sehr nett.", "Hàng xóm của tôi rất tốt bụng."),
    ("Garage", "die", "die Garagen", "/ɡaˈʁaːʒə/", "Noun", "A2", "Nhà để xe", "Garage", "Das Auto steht in der Garage.", "Xe ô tô đỗ trong nhà xe."),
    ("Keller", "der", "die Keller", "/ˈkɛlɐ/", "Noun", "A2", "Tầng hầm", "Cellar", "Alte Kisten lagern im Keller.", "Những thùng cũ được cất dưới hầm."),
    ("Treppe", "die", "die Treppen", "/ˈtʁɛpə/", "Noun", "A2", "Cầu thang", "Stairs", "Wir nehmen die Treppe.", "Chúng tôi đi cầu thang bộ."),
    ("Aufzug", "der", "die Aufzüge", "/ˈaʊ̯fˌt͡suːk/", "Noun", "A2", "Thang máy", "Elevator", "Der Aufzug ist außer Betrieb.", "Thang máy đang tạm ngừng hoạt động."),
    # Clothes & Shopping
    ("Kleidung", "die", "die Kleidungen", "/ˈklaɪ̯dʊŋ/", "Noun", "A2", "Quần áo", "Clothes", "Warme Kleidung schützt vor Kälte.", "Quần áo ấm bảo vệ khỏi cái lạnh."),
    ("Hose", "die", "die Hosen", "/ˈhoːzə/", "Noun", "A2", "Chiếc quần", "Pants", "Die schwarze Hose passt perfekt.", "Chiếc quần đen vừa vặn hoàn hảo."),
    ("Rock", "der", "die Röcke", "/ʁɔk/", "Noun", "A2", "Chân váy", "Skirt", "Der Rock ist aus Baumwolle.", "Chân váy làm từ vải cotton."),
    ("Pullover", "der", "die Pullover", "/pʊˈloːvɐ/", "Noun", "A2", "Áo len chui đầu", "Sweater", "Der dicke Pullover wärmt.", "Chiếc áo len dày giữ ấm."),
    ("Jacke", "die", "die Jacken", "/ˈjakə/", "Noun", "A2", "Áo khoác ngắn", "Jacket", "Zieh eine Jacke an.", "Hãy mặc áo khoác vào."),
    ("Mantel", "der", "die Mäntel", "/ˈmantl̩/", "Noun", "A2", "Áo măng tô dài", "Coat", "Der Mantel schützt vor Wind.", "Áo măng tô che chắn gió."),
    ("Schuh", "der", "die Schuhe", "/ʃuː/", "Noun", "A2", "Đôi giày, chiếc giày", "Shoe", "Die Schuhe sind bequem zum Wandern.", "Đôi giày thoải mái khi đi bộ đường dài."),
    ("Stiefel", "der", "die Stiefel", "/ˈʃtiːfl̩/", "Noun", "A2", "Đôi bốt", "Boot", "Im Winter trage ich warme Stiefel.", "Mùa đông tôi đi bốt ấm."),
    ("Mütze", "die", "die Mützen", "/ˈmʏt͡sə/", "Noun", "A2", "Mũ len", "Beanie", "Die Mütze hält den Kopf warm.", "Mũ len giữ ấm đầu."),
    ("Handschuh", "der", "die Handschuhe", "/ˈhantˌʃuː/", "Noun", "A2", "Găng tay", "Glove", "Vergiss deine Handschuhe nicht.", "Đừng quên găng tay của bạn."),
    ("Schal", "der", "die Schals", "/ʃaːl/", "Noun", "A2", "Khăn quàng cổ", "Scarf", "Ein bunter Schal sieht gut aus.", "Một chiếc khăn quàng sặc sỡ trông rất đẹp."),
    ("Gürtel", "der", "die Gürtel", "/ˈɡʏʁtl̩/", "Noun", "A2", "Thắt lưng", "Belt", "Der Gürtel ist aus Leder.", "Chiếc thắt lưng làm bằng da."),
    ("Krawatte", "die", "die Krawatten", "/kʁaˈvatə/", "Noun", "A2", "Cà vạt", "Tie", "Er bindet seine Krawatte.", "Anh ấy đang thắt cà vạt."),
    ("Brille", "die", "die Brillen", "/ˈbʁɪlə/", "Noun", "A2", "Kính mắt", "Glasses", "Ohne Brille sehe ich unscharf.", "Không có kính tôi nhìn bị mờ."),
    ("Regenschirm", "der", "die Regenschirme", "/ˈʁeːɡn̩ˌʃɪʁm/", "Noun", "A2", "Chiếc ô đi mưa", "Umbrella", "Nimm einen Regenschirm mit.", "Hãy mang theo một chiếc ô."),
    ("Größe", "die", "die Größen", "/ˈɡʁøːsə/", "Noun", "A2", "Kích cỡ", "Size", "Welche Größe tragen Sie?", "Bạn mặc cỡ số mấy?"),
    # Nature & Weather
    ("Wetterbericht", "der", "die Wetterberichte", "/ˈvɛtɐbəˌʁɪçt/", "Noun", "A2", "Dự báo thời tiết", "Weather forecast", "Der Wetterbericht meldet Sonnenschein.", "Dự báo thời tiết báo trời nắng."),
    ("Gewitter", "das", "die Gewitter", "/ɡəˈvɪtɐ/", "Noun", "A2", "Cơn dông sấm sét", "Thunderstorm", "Ein schweres Gewitter zieht auf.", "Một cơn dông lớn đang kéo đến."),
    ("Blitz", "der", "die Blitze", "/blɪt͡s/", "Noun", "A2", "Tia chớp", "Lightning", "Ein greller Blitz erhellte die Nacht.", "Một tia chớp sáng lòa bầu trời đêm."),
    ("Donner", "der", "die Donner", "/ˈdɔnɐ/", "Noun", "A2", "Tiếng sấm", "Thunder", "Der laute Donner grollt.", "Tiếng sấm gầm vang rền."),
    ("Nebel", "der", "die Nebel", "/ˈneːbl̩/", "Noun", "A2", "Sương mù", "Fog", "Dichter Nebel verhüllt die Stadt.", "Sương mù dày đặc bao phủ thành phố."),
    ("Grad", "das", "die Grade", "/ɡʁaːt/", "Noun", "A2", "Độ (nhiệt độ)", "Degree", "Heute sind es zwanzig Grad.", "Hôm nay trời hai mươi độ."),
    ("Schatten", "der", "die Schatten", "/ˈʃatn̩/", "Noun", "A2", "Bóng râm, bóng tối", "Shadow / Shade", "Wir ruhen uns im Schatten aus.", "Chúng tôi nghỉ ngơi trong bóng râm."),
    ("Wiese", "die", "die Wiesen", "/ˈviːzə/", "Noun", "A2", "Đồng cỏ", "Meadow", "Kühe weiden auf der grünen Wiese.", "Những con bò gặm cỏ trên đồng xanh.")
]
for item in a2_data:
    add(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9])

# A2 Verbs (60)
verbs_a2 = [
    ("abfahren", "/ˈapˌfaːʁən/", "Khởi hành (xe/tàu)", "to depart", "Der Zug fährt pünktlich ab.", "Tàu khởi hành đúng giờ."),
    ("ankommen", "/ˈanˌkɔmən/", "Đến nơi", "to arrive", "Wir kommen bald in Berlin an.", "Chúng tôi sẽ sớm đến Berlin."),
    ("umsteigen", "/ˈʊmˌʃtaɪ̯ɡn̩/", "Đổi chuyến", "to change trains", "In Frankfurt müssen wir umsteigen.", "Tại Frankfurt chúng tôi phải đổi tàu."),
    ("einsteigen", "/ˈaɪ̯nˌʃtaɪ̯ɡn̩/", "Bước lên xe", "to get in / board", "Alle Fahrgäste bitte einsteigen!", "Xin mời tất cả hành khách lên xe!"),
    ("aussteigen", "/ˈaʊ̯sˌʃtaɪ̯ɡn̩/", "Bước xuống xe", "to get off", "An der Endstation steigen alle aus.", "Ở ga cuối tất cả mọi người bước xuống."),
    ("abholen", "/ˈapˌhoːlən/", "Đón ai đó", "to pick up", "Ich hole dich vom Bahnhof ab.", "Tôi sẽ ra ga đón bạn."),
    ("anrufen", "/ˈanˌʁuːfn̩/", "Gọi điện thoại", "to call", "Ruf mich bitte später an.", "Hãy gọi lại cho tôi sau nhé."),
    ("aufstehen", "/ˈaʊ̯fˌʃteːən/", "Thức dậy", "to get up", "Ich stehe um sechs Uhr auf.", "Tôi thức dậy lúc sáu giờ."),
    ("einkaufen", "/ˈaɪ̯nˌkaʊ̯fn̩/", "Mua sắm", "to shop", "Wir kaufen im Supermarkt ein.", "Chúng tôi đi mua sắm ở siêu thị."),
    ("fernsehen", "/ˈfɛʁnˌzeːən/", "Xem ti vi", "to watch TV", "Er sieht abends selten fern.", "Buổi tối anh ấy hiếm khi xem ti vi."),
    ("mitbringen", "/ˈmɪtˌbʁɪŋən/", "Mang theo cùng", "to bring along", "Bring bitte einen Salat mit.", "Hãy mang theo một món xà lách nhé."),
    ("vorbereiten", "/ˈfoːɐ̯bəˌʁaɪ̯tn̩/", "Chuẩn bị", "to prepare", "Wir bereiten die Prüfung vor.", "Chúng tôi chuẩn bị cho kỳ thi."),
    ("teilnehmen", "/ˈtaɪ̯lˌneːmən/", "Tham gia", "to participate", "Möchtest du am Kurs teilnehmen?", "Bạn có muốn tham gia khóa học không?"),
    ("unterschreiben", "/ʊntɐˈʃʁaɪ̯bn̩/", "Ký tên", "to sign", "Bitte unterschreiben Sie hier.", "Làm ơn ký tên vào đây."),
    ("buchen", "/ˈbuːxn̩/", "Đặt chỗ trước", "to book", "Wir buchen ein Hotelzimmer.", "Chúng tôi đặt phòng khách sạn."),
    ("empfehlen", "/ɛmˈpfeːlən/", "Khuyên bảo, giới thiệu", "to recommend", "Ich empfehle dieses Gericht.", "Tôi giới thiệu món ăn này."),
    ("wiederholen", "/viːdɐˈhoːlən/", "Nhắc lại", "to repeat", "Können Sie das wiederholen?", "Bạn có thể nhắc lại điều đó không?"),
    ("erklären", "/ɛɐ̯ˈklɛːʁən/", "Giải thích", "to explain", "Er erklärt die Grammatik gut.", "Anh ấy giải thích ngữ pháp rất tốt."),
    ("gehören", "/ɡəˈhøːʁən/", "Thuộc về ai", "to belong to", "Das Buch gehört mir.", "Cuốn sách này thuộc về tôi."),
    ("passen", "/ˈpasn̩/", "Vừa vặn, hợp", "to fit / suit", "Die Hose passt mir gut.", "Chiếc quần rất vừa vặn với tôi."),
    ("gefallen", "/ɡəˈfaln̩/", "Làm ai hài lòng", "to please", "Die Stadt gefällt mir sehr.", "Tôi rất thích thành phố này."),
    ("schmecken", "/ˈʃmɛkn̩/", "Có vị ngon", "to taste", "Das Essen schmeckt lecker.", "Đồ ăn rất ngon miệng."),
    ("wehtun", "/ˈveːˌtuːn/", "Đau đớn", "to hurt", "Mein Bein tut weh.", "Chân tôi bị đau."),
    ("fehlen", "/ˈfeːlən/", "Thiếu vắng", "to be missing", "Zwei Schüler fehlen heute.", "Hôm nay vắng hai học sinh."),
    ("interessieren", "/ɪntəʁɛˈsiːʁən/", "Quan tâm", "to interest", "Ich interessiere mich für Kunst.", "Tôi quan tâm đến nghệ thuật."),
    ("freuen", "/ˈfʁɔɪ̯ən/", "Vui mừng", "to look forward / be glad", "Ich freue mich auf den Urlaub.", "Tôi rất mong chờ kỳ nghỉ."),
    ("ärgern", "/ˈɛʁɡɐn/", "Bực tức", "to annoy", "Ärgere dich nicht darüber.", "Đừng bực mình vì chuyện đó."),
    ("erinnern", "/ɛɐ̯ˈʔɪnɐn/", "Gợi nhớ", "to remember", "Ich erinnere mich an den Tag.", "Tôi nhớ lại ngày hôm ấy."),
    ("gewinnen", "/ɡəˈvɪnən/", "Chiến thắng", "to win", "Wir wollen das Spiel gewinnen.", "Chúng tôi muốn thắng trận đấu."),
    ("verlieren", "/fɛɐ̯ˈliːʁən/", "Thua cuộc, làm mất", "to lose", "Ich habe meinen Schlüssel verloren.", "Tôi đã làm mất chìa khóa."),
    ("leihen", "/ˈlaɪ̯ən/", "Vay mượn", "to borrow / lend", "Kannst du mir ein Buch leihen?", "Bạn có thể cho tôi mượn sách không?"),
    ("schenken", "/ˈʃɛŋkn̩/", "Tặng quà", "to gift", "Ich schenke ihr Blumen.", "Tôi tặng hoa cho cô ấy."),
    ("mieten", "/ˈmiːtn̩/", "Thuê", "to rent", "Wir mieten eine Ferienwohnung.", "Chúng tôi thuê một căn hộ nghỉ dưỡng."),
    ("umziehen", "/ˈʊmˌt͡siːən/", "Chuyển nhà, thay đồ", "to move / change clothes", "Wir ziehen nächsten Monat um.", "Tháng sau chúng tôi sẽ chuyển nhà."),
    ("renovieren", "/ʁenoˈviːʁən/", "Sửa sang lại", "to renovate", "Sie renovieren die Küche.", "Họ đang sửa sang lại nhà bếp."),
    ("reparieren", "/ʁepaˈʁiːʁən/", "Sửa chữa", "to repair", "Er repariert das alte Fahrrad.", "Anh ấy sửa chiếc xe đạp cũ."),
    ("duschen", "/ˈduːʃn̩/", "Tắm vòi sen", "to shower", "Ich dusche jeden Morgen.", "Tôi tắm vòi sen mỗi sáng."),
    ("waschen", "/ˈvaʃn̩/", "Giặt giũ, rửa", "to wash", "Sie wäscht die Wäsche.", "Cô ấy đang giặt quần áo."),
    ("putzen", "/ˈpʊt͡sn̩/", "Lau chùi, đánh răng", "to clean", "Er putzt sich die Zähne.", "Anh ấy đang đánh răng."),
    ("aufräumen", "/ˈaʊ̯fˌʁɔɪ̯mən/", "Dọn dẹp", "to tidy up", "Räume bitte dein Zimmer auf.", "Làm ơn dọn dẹp phòng của bạn."),
    ("einladen", "/ˈaɪ̯nˌlaːdn̩/", "Mời", "to invite", "Ich lade dich zur Party ein.", "Tôi mời bạn đến dự tiệc."),
    ("absagen", "/ˈapˌzaːɡn̩/", "Hủy bỏ", "to cancel", "Ich muss den Termin leider absagen.", "Tôi tiếc là phải hủy cuộc hẹn."),
    ("zusagen", "/ˈt͡suːˌzaːɡn̩/", "Đồng ý lời mời", "to accept / confirm", "Er hat die Einladung zugesagt.", "Anh ấy đã đồng ý lời mời."),
    ("stattfinden", "/ˈʃtatˌfɪndn̩/", "Diễn ra", "to take place", "Das Konzert findet morgen statt.", "Buổi hòa nhạc sẽ diễn ra vào ngày mai."),
    ("verbringen", "/fɛɐ̯ˈbʁɪŋən/", "Trải qua (thời gian)", "to spend (time)", "Wir verbringen den Tag am See.", "Chúng tôi dành trọn ngày bên hồ."),
    ("mitkommen", "/ˈmɪtˌkɔmən/", "Đi cùng", "to come along", "Kommst du mit ins Kino?", "Bạn có đi cùng tới rạp phim không?"),
    ("anprobieren", "/ˈanpʁoˌbiːʁən/", "Mặc thử quần áo", "to try on", "Darf ich diese Jacke anprobieren?", "Tôi có thể mặc thử chiếc áo khoác này không?"),
    ("mitmachen", "/ˈmɪtˌmaxn̩/", "Tham gia cùng", "to join in", "Alle dürfen gerne mitmachen.", "Tất cả mọi người đều được hoan nghênh tham gia cùng."),
    ("anfangen", "/ˈanˌfaŋən/", "Bắt đầu", "to begin", "Der Film fängt um acht an.", "Bộ phim bắt đầu lúc tám giờ."),
    ("aufhören", "/ˈaʊ̯fˌhøːʁən/", "Dừng lại", "to stop", "Hör bitte auf damit!", "Làm ơn dừng lại đi!"),
    ("ausfüllen", "/ˈaʊ̯sˌfʏlən/", "Điền vào đơn", "to fill out", "Füllen Sie das Formular aus.", "Hãy điền vào mẫu đơn."),
    ("abgeben", "/ˈapˌɡeːbn̩/", "Nộp bài, gửi đồ", "to hand in", "Geben Sie die Prüfung rechtzeitig ab.", "Hãy nộp bài kiểm tra đúng hạn."),
    ("überweisen", "/yːbɐˈvaɪ̯zn̩/", "Chuyển khoản", "to transfer money", "Ich überweise das Geld heute.", "Hôm nay tôi sẽ chuyển khoản số tiền."),
    ("abheben", "/ˈapˌheːbn̩/", "Rút tiền", "to withdraw", "Ich hebe Geld am Automaten ab.", "Tôi rút tiền tại cây ATM."),
    ("sparen", "/ˈʃpaːʁən/", "Tiết kiệm", "to save", "Er spart für ein neues Auto.", "Anh ấy tiết kiệm tiền mua xe mới."),
    ("wechseln", "/ˈvɛksl̩n/", "Đổi chác", "to change / exchange", "Können Sie mir diesen Schein wechseln?", "Bạn có thể đổi cho tôi tờ tiền này không?"),
    ("gefallen", "/ɡəˈfaln̩/", "Thích", "to like", "Die Musik gefällt mir gut.", "Tôi thích bản nhạc này."),
    ("dauern", "/ˈdaʊ̯ɐn/", "Kéo dài bao lâu", "to last", "Die Fahrt dauert eine Stunde.", "Chuyến đi kéo dài một giờ."),
    ("hoffen", "/ˈhɔfn̩/", "Hi vọng", "to hope", "Ich hoffe auf gutes Wetter.", "Tôi hi vọng thời tiết sẽ đẹp."),
    ("glauben", "/ˈɡlaʊ̯bn̩/", "Tin tưởng", "to believe", "Ich glaube dir jedes Wort.", "Tôi tin bạn từng lời.")
]
for item in verbs_a2:
    add(item[0], None, None, item[1], "Verb", "A2", item[2], item[3], item[4], item[5])

# A2 Adjectives (40)
adjs_a2 = [
    ("pünktlich", "/ˈpʏŋktlɪç/", "Đúng giờ", "punctual", "Der Zug ist fast immer pünktlich.", "Chuyến tàu gần như luôn đúng giờ."),
    ("höflich", "/ˈhøːflɪç/", "Lịch thiệp", "polite", "Sei immer höflich zu den Gästen.", "Hãy luôn lịch sự với khách."),
    ("berühmt", "/bəˈʁyːmt/", "Nổi tiếng", "famous", "Ein berühmter Musiker trat auf.", "Một nhạc sĩ nổi tiếng đã biểu diễn."),
    ("wunderbar", "/ˈvʊndɐbaːɐ̯/", "Tuyệt vời", "wonderful", "Wir hatten eine wunderbare Zeit.", "Chúng tôi đã có khoảng thời gian tuyệt vời."),
    ("gemütlich", "/ɡəˈmyːtlɪç/", "Ấm cúng", "cozy", "Das Wohnzimmer ist sehr gemütlich.", "Phòng khách rất ấm cúng."),
    ("anstrengend", "/ˈanˌʃtʁɛŋənt/", "Vất vả", "exhausting", "Der Arbeitstag war anstrengend.", "Ngày làm việc thật vất vả."),
    ("spannend", "/ˈʃpanənt/", "Hấp dẫn", "exciting", "Das Buch ist von Anfang an spannend.", "Quyển sách hấp dẫn ngay từ đầu."),
    ("langweilig", "/ˈlaŋˌvaɪ̯lɪç/", "Nhàm chán", "boring", "Die Vorlesung war langweilig.", "Bài giảng rất nhàm chán."),
    ("bequem", "/bəˈkveːm/", "Thoải mái", "comfortable", "Dieser Sessel ist herrlich bequem.", "Chiếc ghế bành này thật thoải mái."),
    ("unbequem", "/ˈʊnbəˌkveːm/", "Bất tiện", "uncomfortable", "Die Schuhe sind unbequem.", "Đôi giày đi rất khó chịu."),
    ("fit", "/fɪt/", "Khỏe khoắn", "fit", "Sport hält den Körper fit.", "Thể thao giữ cơ thể khỏe khoắn."),
    ("schlank", "/ʃlaŋk/", "Thon thả", "slim", "Sie hat eine schlanke Figur.", "Cô ấy có vóc dáng thon thả."),
    ("dick", "/dɪk/", "Dày, mập", "thick / fat", "Das Buch ist sehr dick.", "Cuốn sách rất dày."),
    ("dünn", "/dʏn/", "Mỏng, gầy", "thin", "Das Papier ist extrem dünn.", "Tờ giấy cực kỳ mỏng."),
    ("sportlich", "/ˈʃpɔʁtlɪç/", "Thể thao", "athletic", "Er kleidet sich sehr sportlich.", "Anh ấy ăn mặc rất thể thao."),
    ("gefährlich", "/ɡəˈfɛːɐ̯lɪç/", "Nguy hiểm", "dangerous", "Die Straße bei Glatteis ist gefährlich.", "Đường đóng băng rất nguy hiểm."),
    ("sicher", "/ˈzɪçɐ/", "An toàn, chắc chắn", "safe / sure", "Hier bist du in Sicherheit.", "Ở đây bạn được an toàn."),
    ("modern", "/moˈdɛʁn/", "Hiện đại", "modern", "Das Gebäude ist modern gebaut.", "Tòa nhà được xây dựng hiện đại."),
    ("historisch", "/hɪsˈtoːʁɪʃ/", "Lịch sử, cổ kính", "historic", "Die Altstadt ist historisch wertvoll.", "Khu phố cổ có giá trị lịch sử cao."),
    ("sympathisch", "/zʏmˈpaːtɪʃ/", "Dễ mến", "likable", "Sie ist eine sympathische Kollegin.", "Cô ấy là một đồng nghiệp dễ mến."),
    ("nervös", "/nɛʁˈvøːs/", "Hồi hộp", "nervous", "Vor der Prüfung war ich nervös.", "Trước kỳ thi tôi rất hồi hộp."),
    ("ruhig", "/ˈʁuːɪç/", "Yên tĩnh", "quiet / calm", "Auf dem Land ist es sehr ruhig.", "Ở vùng quê rất yên tĩnh."),
    ("neugierig", "/ˈnɔɪ̯ˌɡiːʁɪç/", "Tò mò", "curious", "Kinder sind von Natur aus neugierig.", "Trẻ em vốn có tính tò mò tự nhiên."),
    ("geduldig", "/ɡəˈdʊldɪç/", "Kiên nhẫn", "patient", "Der Lehrer ist sehr geduldig.", "Thầy giáo rất kiên nhẫn."),
    ("fleißig", "/ˈflaɪ̯sɪç/", "Chăm chỉ", "diligent", "Sie lernt fleißig Deutsch.", "Cô ấy học tiếng Đức rất chăm chỉ."),
    ("faul", "/faʊ̯l/", "Lười biếng", "lazy", "Sonntags darf man faul sein.", "Chủ nhật người ta được phép lười biếng."),
    ("klug", "/kluːk/", "Thông minh", "smart", "Er hat eine kluge Entscheidung getroffen.", "Anh ấy đã đưa ra quyết định thông minh."),
    ("dumm", "/dʊm/", "Ngớ ngẩn", "stupid", "Das war ein dummer Fehler.", "Đó là một sai lầm ngớ ngẩn."),
    ("reich", "/ʁaɪ̯ç/", "Giàu có", "rich", "Er ist reich an Erfahrungen.", "Anh ấy giàu kinh nghiệm."),
    ("arm", "/aʁm/", "Nghèo khó", "poor", "Das Land war früher arm.", "Vùng đất trước đây từng nghèo khó."),
    ("verheiratet", "/fɛɐ̯ˈhaɪ̯ʁaːtət/", "Đã kết hôn", "married", "Sie sind seit zehn Jahren verheiratet.", "Họ đã kết hôn được mười năm."),
    ("ledig", "/ˈleːdɪç/", "Độc thân", "single", "Er ist noch ledig.", "Anh ấy vẫn còn độc thân."),
    ("geschieden", "/ɡəˈʃiːdn̩/", "Đã ly hôn", "divorced", "Meine Tante ist geschieden.", "Dì của tôi đã ly hôn."),
    ("zufrieden", "/t͡suˈfʁiːdn̩/", "Hài lòng", "satisfied", "Der Chef ist mit der Arbeit zufrieden.", "Sếp rất hài lòng với công việc."),
    ("unzufrieden", "/ˈʊnt͡suˌfʁiːdn̩/", "Không hài lòng", "dissatisfied", "Die Kunden waren unzufrieden.", "Khách hàng đã không hài lòng."),
    ("wütend", "/ˈvyːtn̩t/", "Giận dữ", "furious", "Er wurde wütend über die Nachricht.", "Anh ấy nổi giận vì tin tức đó."),
    ("überrascht", "/yːbɐˈʁaʃt/", "Ngạc nhiên", "surprised", "Ich war positiv überrascht.", "Tôi đã ngạc nhiên một cách tích cực."),
    ("enttäuscht", "/ɛntˈtɔɪ̯ʃt/", "Thất vọng", "disappointed", "Er war vom Ergebnis enttäuscht.", "Anh ấy thất vọng về kết quả."),
    ("mutig", "/ˈmuːtɪç/", "Can đảm", "brave", "Die Feuerwehrleute sind mutig.", "Các chiến sĩ cứu hỏa rất can đảm."),
    ("feige", "/ˈfaɪ̯ɡə/", "Hèn nhát", "cowardly", "Weglaufen ist feige.", "Bỏ chạy là hèn nhát.")
]
for item in adjs_a2:
    add(item[0], None, None, item[1], "Adjective", "A2", item[2], item[3], item[4], item[5])

print(f"Total entries after A2: {len(vocab)}")

# Save intermediate
with open("/home/jikay/Desktop/LingoLearning/scripts/vocab_check_a2.json", "w") as f:
    json.dump(vocab, f)

