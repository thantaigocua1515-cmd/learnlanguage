#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Comprehensive database of 1000 curated German vocabulary items
def generate_1000_words():
    words = []
    
    # helper to add
    def add(word, gender, plural, ipa, pos, level, meaning_vi, meaning_en, ex_de, ex_vi):
        words.append({
            "word": word,
            "gender": gender,
            "plural_form": plural,
            "ipa": ipa,
            "pos": pos,
            "cefr_level": level,
            "meaning_vi": meaning_vi,
            "meaning_en": meaning_en,
            "example_de": ex_de,
            "example_vi": ex_vi
        })

    # ==========================================
    # LEVEL A1 (200 words)
    # ==========================================
    # A1 Nouns (der)
    der_a1 = [
        ("Apfel", "die Äpfel", "/ˈapfl̩/", "Quả táo", "Apple", "Der Apfel ist rot und süß.", "Quả táo màu đỏ và ngọt."),
        ("Tisch", "die Tische", "/tɪʃ/", "Cái bàn", "Table", "Das Buch liegt auf dem Tisch.", "Quyển sách nằm trên bàn."),
        ("Stuhl", "die Stühle", "/ʃtuːl/", "Cái ghế", "Chair", "Der Stuhl ist sehr bequem.", "Chiếc ghế rất thoải mái."),
        ("Hund", "die Hunde", "/hʊnt/", "Con chó", "Dog", "Der Hund spielt gerne im Garten.", "Con chó thích chơi trong vườn."),
        ("Kaffee", "die Kaffees", "/ˈkafe/", "Cà phê", "Coffee", "Ich trinke morgens schwarzen Kaffee.", "Buổi sáng tôi uống cà phê đen."),
        ("Tee", "die Tees", "/teː/", "Trà", "Tea", "Möchtest du eine Tasse Tee?", "Bạn có muốn một tách trà không?"),
        ("Käse", "die Käse", "/ˈkɛːzə/", "Phô mai", "Cheese", "Der Käse schmeckt sehr lecker.", "Phô mai có vị rất ngon."),
        ("Kuchen", "die Kuchen", "/ˈkuːxn̩/", "Bánh ngọt", "Cake", "Der Kuchen wurde frisch gebacken.", "Chiếc bánh ngọt vừa mới nướng xong."),
        ("Zucker", "die Zucker", "/ˈt͡sʊkɐ/", "Đường", "Sugar", "Ich nehme keinen Zucker im Kaffee.", "Tôi không cho đường vào cà phê."),
        ("Pfeffer", "die Pfeffer", "/ˈpfɛfɐ/", "Hạt tiêu", "Pepper", "Der Pfeffer ist scharf.", "Hạt tiêu rất cay."),
        ("Reis", "die Reise", "/ʁaɪ̯s/", "Cơm, gạo", "Rice", "In Asien isst man täglich Reis.", "Ở châu Á người ta ăn cơm hàng ngày."),
        ("Fisch", "die Fische", "/fɪʃ/", "Con cá", "Fish", "Der Fisch schwimmt im See.", "Con cá đang bơi trong hồ."),
        ("Salat", "die Salate", "/zaˈlaːt/", "Rau xà lách, món trộn", "Salad", "Der Salat ist frisch und knackig.", "Món xà lách tươi và giòn."),
        ("Bruder", "die Brüder", "/ˈbʁuːdɐ/", "Anh/em trai", "Brother", "Mein Bruder studiert Medizin.", "Anh trai tôi học ngành y."),
        ("Vater", "die Väter", "/ˈfaːtɐ/", "Người cha", "Father", "Mein Vater arbeitet als Ingenieur.", "Bố tôi làm kỹ sư."),
        ("Sohn", "die Söhne", "/zoːn/", "Con trai", "Son", "Ihr Sohn geht in den Kindergarten.", "Con trai cô ấy đi học mẫu giáo."),
        ("Freund", "die Freunde", "/fʁɔɪ̯nt/", "Người bạn nam", "Friend", "Er ist mein bester Freund.", "Anh ấy là bạn thân nhất của tôi."),
        ("Mann", "die Männer", "/man/", "Đàn ông, người chồng", "Man / Husband", "Der Mann liest ein Buch.", "Người đàn ông đang đọc sách."),
        ("Junge", "die Jungen", "/ˈjʊŋə/", "Cậu bé", "Boy", "Der Junge spielt Fußball.", "Cậu bé đang chơi đá bóng."),
        ("Tag", "die Tage", "/taːk/", "Ngày", "Day", "Schönen Tag noch!", "Chúc một ngày tốt lành!"),
        ("Morgen", "die Morgen", "/ˈmɔʁɡn̩/", "Buổi sáng", "Morning", "Guten Morgen allerseits!", "Chào buổi sáng mọi người!"),
        ("Abend", "die Abende", "/ˈaːbn̩t/", "Buổi tối", "Evening", "Am Abend sehe ich fern.", "Buổi tối tôi xem tivi."),
        ("Monat", "die Monate", "/ˈmoːnat/", "Tháng", "Month", "Der Monat Mai ist wunderschön.", "Tháng Năm thật tuyệt đẹp."),
        ("Schlüssel", "die Schlüssel", "/ˈʃlʏsl̩/", "Chìa khóa", "Key", "Hier ist der Schlüssel zur Wohnung.", "Đây là chìa khóa vào căn hộ."),
        ("Kugelschreiber", "die Kugelschreiber", "/ˈkuːɡl̩ˌʃʁaɪ̯bɐ/", "Bút bi", "Pen", "Haben Sie einen blauen Kugelschreiber?", "Bạn có chiếc bút bi màu xanh không?"),
        ("Bleistift", "die Bleistifte", "/ˈblaɪ̯ˌʃtɪft/", "Bút chì", "Pencil", "Ich zeichne mit einem Bleistift.", "Tôi vẽ bằng bút chì."),
        ("Rucksack", "die Rucksäcke", "/ˈʁʊkˌzak/", "Ba lô", "Backpack", "Der Rucksack steht in der Ecke.", "Chiếc ba lô để ở trong góc."),
        ("Schrank", "die Schränke", "/ʃʁaŋk/", "Tủ đựng đồ", "Closet / Cupboard", "Die Gläser stehen im Schrank.", "Những chiếc ly để ở trong tủ."),
        ("Computer", "die Computer", "/kɔmˈpjuːtɐ/", "Máy vi tính", "Computer", "Mein Computer ist sehr schnell.", "Máy tính của tôi rất nhanh."),
        ("Fernseher", "die Fernseher", "/ˈfɛʁnˌzeːɐ/", "Ti vi", "Television", "Der Fernseher steht im Wohnzimmer.", "Tivi để trong phòng khách."),
        ("Kühlschrank", "die Kühlschränke", "/ˈkyːlˌʃʁaŋk/", "Tủ lạnh", "Fridge", "Die Milch steht im Kühlschrank.", "Sữa để trong tủ lạnh."),
        ("Herd", "die Herde", "/heːɐ̯t/", "Bếp nấu", "Stove", "Die Suppe kocht auf dem Herd.", "Nồi súp đang sôi trên bếp."),
        ("Balkon", "die Balkone", "/balˈkɔŋ/", "Ban công", "Balcony", "Wir sitzen gerne auf dem Balkon.", "Chúng tôi thích ngồi ngoài ban công."),
        ("Garten", "die Gärten", "/ˈɡaʁtn̩/", "Khu vườn", "Garden", "Der Garten hat viele bunte Blumen.", "Khu vườn có rất nhiều hoa sặc sỡ."),
        ("Park", "die Parks", "/paʁk/", "Công viên", "Park", "Wir spazieren sonntags im Park.", "Chúng tôi đi dạo trong công viên vào chủ nhật."),
        ("Supermarkt", "die Supermärkte", "/ˈzuːpɐˌmaʁkt/", "Siêu thị", "Supermarket", "Ich kaufe alles im Supermarkt ein.", "Tôi mua sắm mọi thứ ở siêu thị."),
        ("Markt", "die Märkte", "/maʁkt/", "Chợ", "Market", "Auf dem Markt gibt es frisches Obst.", "Ở chợ có bán hoa quả tươi."),
        ("Bahnhof", "die Bahnhöfe", "/ˈbaːnˌhoːf/", "Nhà ga xe lửa", "Train station", "Der Zug fährt um 9 Uhr am Bahnhof ab.", "Chuyến tàu khởi hành lúc 9 giờ tại ga."),
        ("Bus", "die Busse", "/bʊs/", "Xe buýt", "Bus", "Der Bus kommt pünktlich.", "Xe buýt đến rất đúng giờ."),
        ("Zug", "die Züge", "/t͡suːk/", "Tàu hỏa", "Train", "Ich fahre lieber mit dem Zug.", "Tôi thích đi lại bằng tàu hỏa hơn.")
    ]
    for w, pl, ipa, vi, en, ex_de, ex_vi in der_a1:
        add(w, "der", pl, ipa, "Noun", "A1", vi, en, ex_de, ex_vi)

    # A1 Nouns (die)
    die_a1 = [
        ("Katze", "die Katzen", "/ˈkat͡sə/", "Con mèo", "Cat", "Die Katze schläft auf dem Bett.", "Con mèo đang ngủ trên giường."),
        ("Sonne", "die Sonnen", "/ˈzɔnə/", "Mặt trời", "Sun", "Die Sonne scheint den ganzen Tag.", "Mặt trời chiếu sáng suốt cả ngày."),
        ("Blume", "die Blumen", "/ˈbluːmə/", "Bông hoa", "Flower", "Die rote Blume duftet gut.", "Bông hoa đỏ tỏa ngát hương."),
        ("Milch", "die Milche", "/mɪlç/", "Sữa", "Milk", "Ich trinke jeden Morgen Milch.", "Mỗi sáng tôi đều uống sữa."),
        ("Butter", "die Butter", "/ˈbʊtɐ/", "Bơ thực phẩm", "Butter", "Gib mir bitte etwas Butter.", "Làm ơn đưa tôi một chút bơ."),
        ("Suppe", "die Suppen", "/ˈzʊpə/", "Món súp, canh", "Soup", "Die Gemüsesuppe schmeckt fantastisch.", "Món súp rau củ có hương vị tuyệt vời."),
        ("Kartoffel", "die Kartoffeln", "/kaʁˈtɔfl̩/", "Củ khoai tây", "Potato", "Die Kartoffeln sind weich gekocht.", "Khoai tây đã được luộc mềm."),
        ("Tomate", "die Tomaten", "/toˈmaːtə/", "Quả cà chua", "Tomato", "Die Tomate ist rot und saftig.", "Quả cà chua đỏ và mọng nước."),
        ("Orange", "die Orangen", "/oˈʁaŋʒə/", "Quả cam", "Orange", "Die Orange schmeckt herrlich frisch.", "Quả cam có vị tươi mát tuyệt vời."),
        ("Banane", "die Bananen", "/baˈnaːnə/", "Quả chuối", "Banana", "Die gelbe Banane ist sehr süß.", "Quả chuối vàng rất ngọt."),
        ("Mutter", "die Mütter", "/ˈmʊtɐ/", "Người mẹ", "Mother", "Meine Mutter backt am Wochenende Kuchen.", "Mẹ tôi làm bánh vào cuối tuần."),
        ("Schwester", "die Schwestern", "/ˈʃvɛstɐ/", "Chị/em gái", "Sister", "Meine Schwester heißt Laura.", "Em gái tôi tên là Laura."),
        ("Tochter", "die Töchter", "/ˈtɔxtɐ/", "Con gái", "Daughter", "Die Tochter malt gerne Bilder.", "Cô con gái thích vẽ tranh."),
        ("Frau", "die Frauen", "/fʁaʊ̯/", "Phụ nữ, người vợ", "Woman / Wife", "Die Frau grüßt die Nachbarn freundlich.", "Người phụ nữ chào hỏi hàng xóm thân thiện."),
        ("Freundin", "die Freundinnen", "/ˈfʁɔɪ̯ndɪn/", "Bạn nữ, bạn gái", "Female friend", "Sie trifft heute ihre Freundin.", "Hôm nay cô ấy gặp bạn gái của mình."),
        ("Familie", "die Familien", "/faˈmiːli̯ə/", "Gia đình", "Family", "Meine Familie feiert zusammen Geburtstag.", "Gia đình tôi cùng nhau tổ chức sinh nhật."),
        ("Woche", "die Wochen", "/ˈvɔxə/", "Tuần lễ", "Week", "Nächste Woche fahre ich nach München.", "Tuần tới tôi sẽ đi Munich."),
        ("Nacht", "die Nächte", "/naxt/", "Ban đêm", "Night", "In der Nacht ist es hier sehr still.", "Vào ban đêm ở đây rất yên tĩnh."),
        ("Uhr", "die Uhren", "/uːɐ̯/", "Đồng hồ, giờ giấc", "Clock", "Die Uhr an der Wand geht genau.", "Chiếc đồng hồ trên tường chạy rất chuẩn."),
        ("Stadt", "die Städte", "/ʃtat/", "Thành phố", "City", "Hamburg ist eine große Stadt.", "Hamburg là một thành phố lớn."),
        ("Straße", "die Straßen", "/ˈʃtʁaːsə/", "Con đường, tuyến phố", "Street", "Die Kinder dürfen auf der Straße nicht spielen.", "Lũ trẻ không được chơi dưới lòng đường."),
        ("Wohnung", "die Wohnungen", "/ˈvoːnʊŋ/", "Căn hộ", "Apartment", "Die Wohnung ist modern eingerichtet.", "Căn hộ được bài trí hiện đại."),
        ("Küche", "die Küchen", "/ˈkʏçə/", "Nhà bếp", "Kitchen", "Wir kochen zusammen in der Küche.", "Chúng tôi cùng nấu ăn trong bếp."),
        ("Tür", "die Türen", "/tyːɐ̯/", "Cánh cửa", "Door", "Bitte schließen Sie die Haustür leise.", "Làm ơn đóng nhẹ cửa ra vào."),
        ("Lampe", "die Lampen", "/ˈlampə/", "Chiếc đèn", "Lamp", "Die Lampe auf dem Schreibtisch ist hell.", "Chiếc đèn trên bàn làm việc rất sáng."),
        ("Tasche", "die Taschen", "/ˈtaʃə/", "Túi xách, túi", "Bag", "Ich habe mein Handy in der Tasche.", "Tôi để điện thoại trong túi xách."),
        ("Flasche", "die Flaschen", "/ˈflaʃə/", "Chai, lọ", "Bottle", "Die Flasche Wasser ist leer.", "Chai nước đã hết rồi."),
        ("Tasse", "die Tassen", "/ˈtasə/", "Tách, chén", "Cup", "Eine Tasse heiße Schokolade bitte.", "Cho tôi một tách sô-cô-la nóng."),
        ("Zeitung", "die Zeitungen", "/ˈt͡saɪ̯tʊŋ/", "Tờ báo", "Newspaper", "Mein Großvater liest morgens die Zeitung.", "Ông tôi đọc báo vào buổi sáng."),
        ("Schule", "die Schulen", "/ˈʃuːlə/", "Trường học", "School", "Die Schule beginnt um acht Uhr morgens.", "Trường học bắt đầu lúc 8 giờ sáng."),
        ("Arbeit", "die Arbeiten", "/ˈaʁbaɪ̯t/", "Công việc", "Work", "Ich gehe gerne zur Arbeit.", "Tôi rất vui vẻ khi đi làm."),
        ("Pause", "die Pausen", "/ˈpaʊ̯zə/", "Giờ nghỉ giải lao", "Break", "Um zwölf Uhr machen wir eine Pause.", "Đến 12 giờ chúng ta sẽ nghỉ giải lao."),
        ("Frage", "die Fragen", "/ˈfʁaːɡə/", "Câu hỏi", "Question", "Haben Sie noch eine Frage dazu?", "Bạn còn câu hỏi nào về vấn đề này không?"),
        ("Antwort", "die Antworten", "/ˈantvɔʁt/", "Câu trả lời", "Answer", "Die Antwort war völlig richtig.", "Câu trả lời hoàn toàn chính xác."),
        ("Musik", "die Musiken", "/muˈziːk/", "Âm nhạc", "Music", "Ich höre gerne klassische Musik.", "Tôi rất thích nghe nhạc cổ điển."),
        ("Sprache", "die Sprachen", "/ˈʃpʁaːxə/", "Ngôn ngữ, tiếng", "Language", "Deutsch ist eine interessante Sprache.", "Tiếng Đức là một ngôn ngữ thú vị."),
        ("Farbe", "die Farben", "/ˈfaʁbə/", "Màu sắc", "Color", "Blau ist meine Lieblingsfarbe.", "Màu xanh dương là màu tôi yêu thích nhất."),
        ("Nummer", "die Nummern", "/ˈnʊmɐ/", "Số, con số", "Number", "Wie lautet deine Telefonnummer?", "Số điện thoại của bạn là gì?"),
        ("Rechnung", "die Rechnungen", "/ˈʁɛçnʊŋ/", "Hóa đơn", "Bill", "Bringen Sie uns bitte die Rechnung.", "Làm ơn mang hóa đơn cho chúng tôi."),
        ("Post", "die Posten", "/pɔst/", "Bưu điện, thư từ", "Post office", "Ich bringe den Brief zur Post.", "Tôi mang bức thư ra bưu điện.")
    ]
    for w, pl, ipa, vi, en, ex_de, ex_vi in die_a1:
        add(w, "die", pl, ipa, "Noun", "A1", vi, en, ex_de, ex_vi)

    # A1 Nouns (das)
    das_a1 = [
        ("Buch", "die Bücher", "/buːx/", "Quyển sách", "Book", "Ich lese ein spannendes Buch.", "Tôi đang đọc một cuốn sách hấp dẫn."),
        ("Wasser", "die Wässer", "/ˈvasɐ/", "Nước uống", "Water", "Trinken Sie bitte viel frisches Wasser.", "Hãy uống nhiều nước lọc nhé."),
        ("Brot", "die Brote", "/bʁoːt/", "Bánh mì", "Bread", "Deutsches Brot ist weltweit berühmt.", "Bánh mì Đức nổi tiếng trên toàn thế giới."),
        ("Brötchen", "die Brötchen", "/ˈbʁøːtçn̩/", "Bánh mì nhỏ tròn", "Bread roll", "Wir kaufen sonntags ofenfrische Brötchen.", "Chủ nhật chúng tôi mua bánh mì tròn nóng hổi."),
        ("Ei", "die Eier", "/aɪ̯/", "Quả trứng", "Egg", "Ein gekochtes Ei zum Frühstück schmeckt gut.", "Một quả trứng luộc ăn sáng rất ngon."),
        ("Fleisch", "die Fleische", "/flaɪ̯ʃ/", "Thịt", "Meat", "Er isst überhaupt kein Fleisch.", "Anh ấy hoàn toàn không ăn thịt."),
        ("Gemüse", "die Gemüse", "/ɡəˈmyːzə/", "Rau củ", "Vegetables", "Frisches Gemüse enthält viele Vitamine.", "Rau củ tươi chứa nhiều vitamin."),
        ("Obst", "die Obste", "/oːpst/", "Hoa quả, trái cây", "Fruit", "Obst schmeckt süß und ist gesund.", "Hoa quả có vị ngọt và tốt cho sức khỏe."),
        ("Bier", "die Biere", "/biːɐ̯/", "Bia", "Beer", "Ein kühles Bier schmeckt an warmen Abenden.", "Một cốc bia mát lạnh thật ngon trong buổi tối ấm áp."),
        ("Salz", "die Salze", "/zalt͡s/", "Muối ăn", "Salt", "Fehlt der Suppe noch etwas Salz?", "Món súp có thiếu chút muối nào không?"),
        ("Haus", "die Häuser", "/haʊ̯s/", "Ngôi nhà", "House", "Das Haus hat weiße Fensterrahmen.", "Ngôi nhà có khung cửa sổ màu trắng."),
        ("Zimmer", "die Zimmer", "/ˈt͡sɪmɐ/", "Căn phòng", "Room", "Mein Zimmer ist sauber und hell.", "Phòng của tôi sạch sẽ và sáng sủa."),
        ("Fenster", "die Fenster", "/ˈfɛnstɐ/", "Cửa sổ", "Window", "Das Fenster geht zum ruhigen Garten hin.", "Cửa sổ nhìn ra khu vườn yên tĩnh."),
        ("Bett", "die Betten", "/bɛt/", "Chiếc giường", "Bed", "Das Bett im Hotel war sehr bequem.", "Chiếc giường trong khách sạn rất êm ái."),
        ("Bild", "die Bilder", "/bɪlt/", "Bức tranh, ảnh chụp", "Picture", "An der Wand hängt ein schönes Bild.", "Trên tường treo một bức tranh đẹp."),
        ("Auto", "die Autos", "/ˈaʊ̯to/", "Xe ô tô", "Car", "Er fährt jeden Tag mit dem Auto zur Arbeit.", "Anh ấy lái ô tô đi làm mỗi ngày."),
        ("Fahrrad", "die Fahrräder", "/ˈfaːɐ̯ˌʁaːt/", "Xe đạp", "Bicycle", "In Deutschland fahren viele mit dem Fahrrad.", "Ở Đức có rất nhiều người đi lại bằng xe đạp."),
        ("Flugzeug", "die Flugzeuge", "/ˈfluːkˌt͡sɔɪ̯k/", "Máy bay", "Airplane", "Das Flugzeug fliegt über die Alpen.", "Chiếc máy bay bay qua dãy núi Alps."),
        ("Kind", "die Kinder", "/kɪnt/", "Đứa trẻ, con cái", "Child", "Das Kind spielt fröhlich draußen.", "Đứa trẻ vui vẻ chơi đùa bên ngoài."),
        ("Mädchen", "die Mädchen", "/ˈmɛːtçn̩/", "Cô bé, bé gái", "Girl", "Das Mädchen singt ein Lied.", "Cô bé đang hát một bài hát."),
        ("Baby", "die Babys", "/ˈbeːbi/", "Em bé sơ sinh", "Baby", "Das Baby schläft friedlich in der Wiege.", "Em bé ngủ yên bình trong nôi."),
        ("Jahr", "die Jahre", "/jaːɐ̯/", "Năm", "Year", "Frohes neues Jahr!", "Chúc mừng năm mới!"),
        ("Geld", "die Gelder", "/ɡɛlt/", "Tiền bạc", "Money", "Er spart Geld für eine schöne Reise.", "Anh ấy tiết kiệm tiền cho một chuyến du lịch đẹp."),
        ("Wetter", "die Wetter", "/ˈvɛtɐ/", "Thời tiết", "Weather", "Das Wetter am Wochenende wird sonnig.", "Thời tiết cuối tuần sẽ có nắng."),
        ("Telefon", "die Telefone", "/teleˈfoːn/", "Máy điện thoại", "Telephone", "Das Telefon steht auf dem Schreibtisch.", "Chiếc điện thoại để trên bàn làm việc."),
        ("Handy", "die Handys", "/ˈhɛndi/", "Điện thoại di động", "Mobile phone", "Ich schaue kurz auf mein Handy.", "Tôi nhìn nhanh vào điện thoại."),
        ("Glas", "die Gläser", "/ɡlaːs/", "Cái ly, chiếc cốc thủy tinh", "Glass", "Möchten Sie ein Glas Wasser?", "Bạn có muốn một ly nước không?"),
        ("Hotel", "die Hotels", "/hoˈtɛl/", "Khách sạn", "Hotel", "Das Hotel bietet ein tolles Frühstücksbuffet.", "Khách sạn có bữa sáng buffet rất tuyệt."),
        ("Restaurant", "die Restaurants", "/ʁɛstoˈʁɑ̃ː/", "Nhà hàng", "Restaurant", "Wir reservieren einen Tisch im Restaurant.", "Chúng tôi đặt bàn ở nhà hàng."),
        ("Café", "die Cafés", "/kaˈfeː/", "Quán cà phê", "Café", "Wir trinken sonntags Kaffee im Café.", "Chủ nhật chúng tôi đi uống cà phê ngoài quán."),
        ("Konto", "die Konten", "/ˈkɔnto/", "Tài khoản ngân hàng", "Bank account", "Ich habe ein Konto bei der Sparkasse eröffnet.", "Tôi đã mở một tài khoản tại ngân hàng Sparkasse."),
        ("Land", "die Länder", "/lant/", "Quốc gia, đất nước", "Country", "Deutschland ist ein schönes Land.", "Đức là một quốc gia xinh đẹp."),
        ("Wort", "die Wörter", "/vɔʁt/", "Từ vựng, từ", "Word", "Was bedeutet dieses deutsche Wort?", "Từ tiếng Đức này có nghĩa là gì?"),
        ("Ticket", "die Tickets", "/ˈtɪkət/", "Vé (tàu, xe, phim)", "Ticket", "Ich habe das Zugticket online gekauft.", "Tôi đã mua vé tàu trực tuyến."),
        ("Formular", "die Formulare", "/fɔʁmuˈlaːɐ̯/", "Mẫu đơn, tờ khai", "Form", "Füllen Sie bitte dieses Formular aus.", "Làm ơn điền vào mẫu đơn này."),
        ("Museum", "die Museen", "/muˈzeːʊm/", "Bảo tàng", "Museum", "Das Museum ist heute kostenlos.", "Hôm nay bảo tàng mở cửa miễn phí."),
        ("Kino", "die Kinos", "/ˈkiːno/", "Rạp chiếu phim", "Cinema", "Gehen wir heute Abend ins Kino?", "Tối nay chúng ta đi xem phim chứ?"),
        ("Theater", "die Theater", "/teˈaːtɐ/", "Nhà hát, kịch trường", "Theater", "Das Stück im Theater war großartig.", "Vở kịch ở nhà hát rất tuyệt vời."),
        ("Schwimmbad", "die Schwimmbäder", "/ˈʃvɪmˌbaːt/", "Hồ bơi", "Swimming pool", "Im Sommer gehe ich oft ins Schwimmbad.", "Vào mùa hè tôi thường đến hồ bơi."),
        ("Krankenhaus", "die Krankenhäuser", "/ˈkʁaŋkn̩ˌhaʊ̯s/", "Bệnh viện", "Hospital", "Der Arzt arbeitet im Krankenhaus.", "Bác sĩ làm việc trong bệnh viện.")
    ]
    for w, pl, ipa, vi, en, ex_de, ex_vi in das_a1:
        add(w, "das", pl, ipa, "Noun", "A1", vi, en, ex_de, ex_vi)

    # A1 Verbs (no gender)
    verbs_a1 = [
        ("sein", "/zaɪ̯n/", "Thì, là, ở", "to be", "Ich bin sehr müde heute.", "Hôm nay tôi rất mệt."),
        ("haben", "/ˈhaːbn̩/", "Có, sở hữu", "to have", "Ich habe eine wichtige Frage.", "Tôi có một câu hỏi quan trọng."),
        ("machen", "/ˈmaxn̩/", "Làm, chế tạo", "to do / make", "Was machst du heute Abend?", "Tối nay bạn làm gì?"),
        ("gehen", "/ˈɡeːən/", "Đi, đi bộ", "to go", "Wir gehen zu Fuß zur Schule.", "Chúng tôi đi bộ đến trường."),
        ("kommen", "/ˈkɔmən/", "Đến, tới", "to come", "Woher kommst du?", "Bạn đến từ đâu?"),
        ("sehen", "/ˈzeːən/", "Nhìn, thấy", "to see", "Ich sehe den blauen Himmel.", "Tôi nhìn thấy bầu trời trong xanh."),
        ("hören", "/ˈhøːʁən/", "Nghe", "to hear / listen", "Hörst du die Vögel singen?", "Bạn có nghe thấy tiếng chim hót không?"),
        ("sprechen", "/ˈʃpʁɛçn̩/", "Nói chuyện, phát biểu", "to speak", "Er spricht fließend Deutsch und Englisch.", "Anh ấy nói trôi chảy cả tiếng Đức và tiếng Anh."),
        ("lesen", "/ˈleːzn̩/", "Đọc", "to read", "Sie liest ein spannendes Buch.", "Cô ấy đang đọc một cuốn sách hấp dẫn."),
        ("schreiben", "/ˈʃʁaɪ̯bn̩/", "Viết", "to write", "Ich schreibe eine E-Mail an meine Freunde.", "Tôi viết một email cho bạn bè."),
        ("essen", "/ˈɛsn̩/", "Ăn", "to eat", "Wir essen um 19 Uhr zu Abend.", "Chúng tôi ăn tối lúc 19 giờ."),
        ("trinken", "/ˈtʁɪŋkn̩/", "Uống", "to drink", "Er trinkt gerne Orangensaft.", "Anh ấy thích uống nước cam."),
        ("schlafen", "/ˈʃlaːfn̩/", "Ngủ", "to sleep", "Das Kind schläft acht Stunden pro Nacht.", "Đứa bé ngủ 8 tiếng mỗi đêm."),
        ("lernen", "/ˈlɛʁnən/", "Học tập", "to learn", "Wir lernen Deutsch mit LingoLearning.", "Chúng tôi học tiếng Đức cùng LingoLearning."),
        ("arbeiten", "/ˈaʁbaɪ̯tn̩/", "Làm việc", "to work", "Er arbeitet bei einer großen Softwarefirma.", "Anh ấy làm việc tại một công ty phần mềm lớn."),
        ("wohnen", "/ˈvoːnən/", "Sinh sống, cư trú", "to live / reside", "Ich wohne seit zwei Jahren in Hamburg.", "Tôi sống ở Hamburg đã được hai năm."),
        ("kaufen", "/ˈkaʊ̯fn̩/", "Mua sắm", "to buy", "Wir kaufen frische Lebensmittel auf dem Markt.", "Chúng tôi mua thực phẩm tươi ở chợ."),
        ("verkaufen", "/fɛɐ̯ˈkaʊ̯fn̩/", "Bán hàng", "to sell", "Der Händler verkauft frisches Gemüse.", "Người bán buôn bán rau củ tươi."),
        ("fragen", "/ˈfʁaːɡn̩/", "Hỏi", "to ask", "Darf ich Sie etwas fragen?", "Tôi có thể hỏi bạn điều này được không?"),
        ("antworten", "/ˈantvɔʁtn̩/", "Trả lời", "to answer", "Er antwortet sofort auf meine Nachricht.", "Anh ấy trả lời tin nhắn của tôi ngay lập tức."),
        ("verstehen", "/fɛɐ̯ˈʃteːən/", "Hiểu được", "to understand", "Ich verstehe diesen Satz ganz genau.", "Tôi hiểu câu này rất rõ ràng."),
        ("wissen", "/ˈvɪsn̩/", "Biết", "to know (facts)", "Weißt du, wie spät es ist?", "Bạn có biết mấy giờ rồi không?"),
        ("kennen", "/ˈkɛnən/", "Quen biết", "to know (people/places)", "Ich kenne diese schöne Stadt sehr gut.", "Tôi biết rất rõ thành phố xinh đẹp này."),
        ("helfen", "/ˈhɛlfn̩/", "Giúp đỡ", "to help", "Können Sie mir bitte kurz helfen?", "Bạn có thể giúp tôi một chút được không?"),
        ("brauchen", "/ˈbʁaʊ̯xn̩/", "Cần thiết", "to need", "Ich brauche deine Hilfe bei den Hausaufgaben.", "Tôi cần sự giúp đỡ của bạn với bài tập về nhà."),
        ("suchen", "/ˈzuːxn̩/", "Tìm kiếm", "to search / look for", "Ich suche meinen Schlüssel.", "Tôi đang tìm chìa khóa của mình."),
        ("finden", "/ˈfɪndn̩/", "Tìm thấy, nhận thấy", "to find", "Ich finde diese Sprache sehr interessant.", "Tôi thấy ngôn ngữ này rất thú vị."),
        ("bleiben", "/ˈblaɪ̯bn̩/", "Ở lại, duy trì", "to stay", "Ich bleibe heute den ganzen Tag zu Hause.", "Hôm nay tôi ở nhà cả ngày."),
        ("fahren", "/ˈfaːʁən/", "Lái xe, đi xe", "to drive / ride", "Wir fahren mit dem Zug nach München.", "Chúng tôi đi tàu hỏa đến Munich."),
        ("reisen", "/ˈʁaɪ̯zn̩/", "Đi du lịch", "to travel", "Ich reise sehr gerne in andere Länder.", "Tôi rất thích đi du lịch đến các quốc gia khác.")
    ]
    for w, ipa, vi, en, ex_de, ex_vi in verbs_a1:
        add(w, None, None, ipa, "Verb", "A1", vi, en, ex_de, ex_vi)

    # A1 Adjectives (50 words)
    adjs_a1 = [
        ("gut", "/ɡuːt/", "Tốt, ngon", "good", "Das Essen schmeckt wirklich sehr gut.", "Đồ ăn thực sự rất ngon."),
        ("schlecht", "/ʃlɛçt/", "Tồi, dở, xấu", "bad", "Das Wetter heute ist leider schlecht.", "Thời tiết hôm nay tiếc là rất xấu."),
        ("groß", "/ɡʁoːs/", "To lớn, cao", "big / tall", "Das Haus hat einen großen Garten.", "Ngôi nhà có một khu vườn lớn."),
        ("klein", "/klaɪ̯n/", "Nhỏ, bé", "small", "Das Zimmer ist zwar klein, aber gemütlich.", "Căn phòng tuy nhỏ nhưng ấm cúng."),
        ("alt", "/alt/", "Cũ, già", "old", "Mein Großvater ist 80 Jahre alt.", "Ông tôi đã 80 tuổi."),
        ("neu", "/nɔɪ̯/", "Mới", "new", "Ich habe ein neues Fahrrad gekauft.", "Tôi đã mua một chiếc xe đạp mới."),
        ("schön", "/ʃøːn/", "Đẹp", "beautiful", "Wien ist eine wunderschöne Stadt.", "Viên là một thành phố đẹp tuyệt trần."),
        ("hässlich", "/ˈhɛslɪç/", "Xấu xí", "ugly", "Das Gebäude sieht ziemlich hässlich aus.", "Tòa nhà trông khá xấu xí."),
        ("warm", "/vaʁm/", "Ấm áp", "warm", "Im Sommer ist das Wasser angenehm warm.", "Vào mùa hè nước ấm áp dễ chịu."),
        ("kalt", "/kalt/", "Lạnh lẽo", "cold", "Im Winter ist es in den Bergen eiskalt.", "Vào mùa đông trên núi lạnh như băng."),
        ("schnell", "/ʃnɛl/", "Nhanh chóng", "fast", "Der ICE-Zug fährt extrem schnell.", "Tàu ICE chạy cực kỳ nhanh."),
        ("langsam", "/ˈlaŋzaːm/", "Chậm chạp", "slow", "Sprechen Sie bitte etwas langsamer.", "Làm ơn nói chậm lại một chút."),
        ("teuer", "/ˈtɔɪ̯ɐ/", "Đắt đỏ", "expensive", "Das Restaurant dort ist sehr teuer.", "Nhà hàng đằng kia rất đắt."),
        ("billig", "/ˈbɪlɪç/", "Rẻ tiền", "cheap", "Auf dem Flohmarkt kauft man billig ein.", "Ở chợ trời người ta mua được đồ giá rẻ."),
        ("leicht", "/laɪ̯çt/", "Nhẹ, dễ dàng", "easy / light", "Diese Deutschaufgabe ist ganz leicht.", "Bài tập tiếng Đức này rất dễ."),
        ("schwer", "/ʃveːɐ̯/", "Nặng, khó khăn", "heavy / difficult", "Der Koffer ist viel zu schwer.", "Chiếc vali quá nặng."),
        ("hell", "/hɛl/", "Sáng sủa", "bright", "Das Wohnzimmer ist hell und freundlich.", "Phòng khách sáng sủa và thân thiện."),
        ("dunkel", "/ˈdʊŋkl̩/", "Tối tăm", "dark", "Abends wird es schon früh dunkel.", "Buổi tối trời tối rất sớm."),
        ("sauber", "/ˈzaʊ̯bɐ/", "Sạch sẽ", "clean", "Die Küche ist blitzblank und sauber.", "Nhà bếp sáng loáng và sạch sẽ."),
        ("schmutzig", "/ˈʃmʊt͡sɪç/", "Bẩn thỉu", "dirty", "Meine Schuhe sind nach dem Regen schmutzig.", "Giày của tôi bị bẩn sau cơn mưa."),
        ("früh", "/fʁyː/", "Sớm", "early", "Ich stehe sonntags früh auf.", "Chủ nhật tôi dậy rất sớm."),
        ("spät", "/ʃpɛːt/", "Muộn", "late", "Es ist schon spät am Abend.", "Trời đã muộn vào buổi tối."),
        ("richtig", "/ˈʁɪçtɪç/", "Đúng đắn", "correct", "Ihre Antwort ist völlig richtig.", "Câu trả lời của bạn hoàn toàn đúng."),
        ("falsch", "/falʃ/", "Sai", "wrong", "Die Nummer war leider falsch.", "Số điện thoại tiếc là bị sai."),
        ("müde", "/ˈmyːdə/", "Mệt mỏi", "tired", "Nach der Arbeit bin ich oft müde.", "Sau giờ làm việc tôi thường mệt mỏi."),
        ("hungrig", "/ˈhʊŋʁɪç/", "Đói bụng", "hungry", "Ich bin hungrig, lass uns essen gehen.", "Tôi đói rồi, chúng ta đi ăn thôi."),
        ("durstig", "/ˈdʊʁstɪç/", "Khát nước", "thirsty", "Ich bin durstig nach dem langen Lauf.", "Tôi khát nước sau buổi chạy dài."),
        ("gesund", "/ɡəˈzʊnt/", "Khỏe mạnh, lành mạnh", "healthy", "Frisches Obst hält den Körper gesund.", "Hoa quả tươi giúp cơ thể khỏe mạnh."),
        ("krank", "/kʁaŋk/", "Bị ốm, bệnh", "sick", "Er bleibt zu Hause, weil er krank ist.", "Anh ấy ở nhà vì bị ốm."),
        ("glücklich", "/ˈɡlʏklɪç/", "Hạnh phúc", "happy", "Die Kinder sind sehr glücklich.", "Những đứa trẻ đang rất hạnh phúc."),
        ("traurig", "/ˈtʁaʊ̯ʁɪç/", "Buồn bã", "sad", "Sie ist traurig über den Abschied.", "Cô ấy buồn vì sự chia tay."),
        ("wichtig", "/ˈvɪçtɪç/", "Quan trọng", "important", "Grammatik ist sehr wichtig beim Lernen.", "Ngữ pháp rất quan trọng khi học tập."),
        ("einfach", "/ˈaɪ̯nfax/", "Đơn giản", "simple", "Die Erklärung war klar und einfach.", "Lời giải thích rất rõ ràng và đơn giản."),
        ("kompliziert", "/kɔmpliˈt͡siːɐ̯t/", "Phức tạp", "complicated", "Die deutsche Grammatik wirkt manchmal kompliziert.", "Ngữ pháp tiếng Đức đôi lúc có vẻ phức tạp."),
        ("freundlich", "/ˈfʁɔɪ̯ntlɪç/", "Thân thiện", "friendly", "Die Verkäuferin war sehr freundlich.", "Cô nhân viên bán hàng rất thân thiện."),
        ("höflich", "/ˈhøːflɪç/", "Lịch sự", "polite", "Er ist immer ein höflicher junger Mann.", "Anh ấy luôn là một chàng trai lịch thiệp."),
        ("leise", "/ˈlaɪ̯zə/", "Yên lặng, khẽ khàng", "quiet", "Seid bitte leise in der Bibliothek.", "Làm ơn giữ yên lặng trong thư viện."),
        ("laut", "/laʊ̯t/", "Ồn ào, to tiếng", "loud", "Die Musik auf der Party war sehr laut.", "Âm nhạc ở bữa tiệc quá to."),
        ("süß", "/zyːs/", "Ngọt ngào, dễ thương", "sweet / cute", "Das kleine Kätzchen ist so süß.", "Chú mèo con thật dễ thương."),
        ("bitter", "/ˈbɪtɐ/", "Đắng", "bitter", "Dunkle Schokolade schmeckt leicht bitter.", "Sô-cô-la đen có vị hơi đắng."),
        ("sauer", "/ˈzaʊ̯ɐ/", "Chua", "sour", "Die Zitrone schmeckt sehr sauer.", "Quả chanh có vị rất chua."),
        ("scharf", "/ʃaʁf/", "Cay, sắc bén", "spicy / sharp", "Das Messer ist extrem scharf.", "Con dao này cực kỳ sắc bén."),
        ("frisch", "/fʁɪʃ/", "Tươi mới", "fresh", "Frisch gebackenes Brot riecht wunderbar.", "Bánh mì mới nướng có mùi thơm ngát."),
        ("voll", "/fɔl/", "Đầy ắp", "full", "Der Bus war heute Morgen voll besetzt.", "Chiếc xe buýt sáng nay chật kín người."),
        ("leer", "/leːɐ̯/", "Rỗng tuếch", "empty", "Mein Glas ist leer, noch ein Wasser bitte.", "Cốc của tôi rỗng rồi, cho thêm một ly nước nữa nhé."),
        ("weit", "/vaɪ̯t/", "Xa xôi, rộng", "far / wide", "Wie weit ist es bis zum Hauptbahnhof?", "Cách ga chính bao xa vậy?"),
        ("nah", "/naː/", "Gần gũi", "near / close", "Die Schule liegt ganz nah an unserem Haus.", "Trường học ở ngay rất gần nhà chúng tôi."),
        ("stark", "/ʃtaʁk/", "Mạnh mẽ", "strong", "Er ist körperlich sehr stark.", "Anh ấy có thể lực rất khỏe mạnh."),
        ("schwach", "/ʃvax/", "Yếu ớt", "weak", "Nach der Grippe fühle ich mich noch schwach.", "Sau trận cúm tôi vẫn cảm thấy người yếu ớt."),
        ("fertig", "/ˈfɛʁtɪç/", "Xong xuôi, hoàn thành", "ready / finished", "Das Abendessen ist fertig!", "Bữa tối đã sẵn sàng!")
    ]
    for w, ipa, vi, en, ex_de, ex_vi in adjs_a1:
        add(w, None, None, ipa, "Adjective", "A1", vi, en, ex_de, ex_vi)

    # ==========================================
    # LEVEL A2 (250 words)
    # ==========================================
    # Topics: Travel, Career, Health, Housing, Clothes, Weather, Daily Routine
    a2_nouns = [
        # Der
        ("Flughafen", "der", "die Flughäfen", "/ˈfluːkˌhaːfn̩/", "Sân bay", "Airport", "Wir müssen zwei Stunden vor Abflug am Flughafen sein.", "Chúng ta phải có mặt ở sân bay 2 tiếng trước giờ bay."),
        ("Bahnsteig", "der", "die Bahnsteige", "/ˈbaːnˌʃtaɪ̯k/", "Sân ga đón tàu", "Platform", "Der Zug nach Köln fährt auf Bahnsteig 4 ein.", "Chuyến tàu đi Cologne đang vào sân ga số 4."),
        ("Fahrplan", "der", "die Fahrpläne", "/ˈfaːɐ̯ˌplaːn/", "Lịch trình tàu xe", "Timetable", "Schau bitte im Fahrplan nach den Abfahrtszeiten.", "Làm ơn tra lịch trình giờ khởi hành."),
        ("Koffer", "der", "die Koffer", "/ˈkɔfɐ/", "Vali du lịch", "Suitcase", "Ich packe meinen Koffer für den Urlaub.", "Tôi đang xếp vali cho chuyến đi nghỉ."),
        ("Ausweis", "der", "die Ausweise", "/ˈaʊ̯sˌvaɪ̯s/", "Thẻ căn cước, CMND", "ID card", "Zeigen Sie bitte Ihren Ausweis vor.", "Làm ơn xuất trình thẻ căn cước của bạn."),
        ("Reisepass", "der", "die Reisepässe", "/ˈʁaɪ̯zəˌpas/", "Hộ chiếu", "Passport", "Mein Reisepass ist noch fünf Jahre gültig.", "Hộ chiếu của tôi còn hạn năm năm."),
        ("Führerschein", "der", "die Führerscheine", "/ˈfyːʁɐˌʃaɪ̯n/", "Bằng lái xe", "Driving license", "Ich habe meinen Führerschein letztes Jahr gemacht.", "Tôi đã thi đỗ bằng lái xe năm ngoái."),
        ("Beruf", "der", "die Berufe", "/bəˈʁuːf/", "Nghề nghiệp", "Profession", "Was sind Sie von Beruf?", "Nghề nghiệp của bạn là gì?"),
        ("Chef", "der", "die Chefs", "/ʃɛf/", "Sếp, thủ trưởng", "Boss", "Mein Chef leitet die Abteilung sehr professionell.", "Sếp của tôi quản lý phòng ban rất chuyên nghiệp."),
        ("Kollege", "der", "die Kollegen", "/kɔˈleːɡə/", "Đồng nghiệp nam", "Colleague", "Mein Kollege hilft mir bei der Präsentation.", "Đồng nghiệp của tôi giúp tôi làm bài thuyết trình."),
        ("Vertrag", "der", "die Verträge", "/fɛɐ̯ˈtʁaːk/", "Hợp đồng", "Contract", "Ich habe den Arbeitsvertrag gestern unterschrieben.", "Hôm qua tôi đã ký hợp đồng lao động."),
        ("Arzt", "der", "die Ärzte", "/aːɐ̯t͡st/", "Bác sĩ nam", "Doctor", "Der Arzt untersucht den Patienten gründlich.", "Bác sĩ khám kỹ lưỡng cho bệnh nhân."),
        ("Patient", "der", "die Patienten", "/paˈt͡si̯ɛnt/", "Bệnh nhân", "Patient", "Der Patient muss im Bett bleiben.", "Bệnh nhân phải nghỉ ngơi tại giường."),
        ("Kopf", "der", "die Köpfe", "/kɔpf/", "Cái đầu", "Head", "Mein Kopf tut heute ziemlich weh.", "Hôm nay đầu tôi khá đau."),
        ("Bauch", "die Bäuche", "/baʊ̯x/", "Bụng", "Stomach", "Ich habe seit gestern Bauchschmerzen.", "Tôi bị đau bụng từ ngày hôm qua."),
        ("Rücken", "der", "die Rücken", "/ˈʁʏkn̩/", "Cái lưng", "Back", "Mein Rücken schmerzt vom langen Sitzen.", "Lưng tôi bị đau vì ngồi lâu."),
        ("Arm", "der", "die Arme", "/aʁm/", "Cánh tay", "Arm", "Er hat sich den linken Arm gebrochen.", "Anh ấy bị gãy cánh tay trái."),
        ("Fuß", "der", "die Füße", "/fuːs/", "Bàn chân", "Foot", "Wir gehen die kurze Strecke zu Fuß.", "Chúng tôi đi bộ đoạn đường ngắn này."),
        ("Hals", "der", "die Hälse", "/hals/", "Cổ, họng", "Throat / Neck", "Ich habe Halsschmerzen und Heiserkeit.", "Tôi bị đau họng và khản tiếng."),
        ("Zahn", "der", "die Zähne", "/t͡saːn/", "Răng", "Tooth", "Der Zahnarzt repariert den kranken Zahn.", "Nha sĩ đang trám chiếc răng sâu."),
        ("Pullover", "der", "die Pullover", "/pʊˈloːvɐ/", "Áo len chui đầu", "Sweater", "Im Winter trage ich einen dicken Pullover.", "Mùa đông tôi mặc một chiếc áo len dày."),
        ("Mantel", "der", "die Mäntel", "/ˈmantl̩/", "Áo khoác dài", "Coat", "Hängen Sie Ihren Mantel bitte an die Garderobe.", "Làm ơn treo áo khoác của bạn lên mắc áo."),
        ("Anzug", "der", "die Anzüge", "/ˈanˌt͡suːk/", "Bộ veston", "Suit", "Er trägt zur Hochzeit einen eleganten Anzug.", "Anh ấy mặc một bộ vest sang trọng đi đám cưới."),
        ("Schuh", "der", "die Schuhe", "/ʃuː/", "Đôi giày, chiếc giày", "Shoe", "Zieh bitte die Schuhe vor der Tür aus.", "Làm ơn cởi giày trước cửa phòng."),
        ("Rock", "der", "die Röcke", "/ʁɔk/", "Chân váy", "Skirt", "Der blaue Rock gefällt ihr sehr gut.", "Cô ấy rất thích chiếc chân váy màu xanh."),
        ("Gürtel", "der", "die Gürtel", "/ˈɡʏʁtl̩/", "Thắt lưng, nịt", "Belt", "Der Gürtel ist aus echtem Leder.", "Chiếc thắt lưng làm bằng da thật."),
        ("Hut", "der", "die Hüte", "/huːt/", "Cái mũ", "Hat", "Der alte Herr trägt immer einen Hut.", "Cụ ông luôn luôn đội một chiếc mũ."),
        ("Regen", "der", "die Regen", "/ˈʁeːɡn̩/", "Cơn mưa", "Rain", "Der Regen tut den Pflanzen gut.", "Cơn mưa mang lại nguồn nước mát cho cây cỏ."),
        ("Schnee", "der", "die Schnee", "/ʃneː/", "Tuyết", "Snow", "Im Winter fällt in den Bergen viel Schnee.", "Vào mùa đông trên núi rơi rất nhiều tuyết."),
        ("Wind", "der", "die Winde", "/vɪnt/", "Gió", "Wind", "Ein starker Wind weht von der Nordsee.", "Một cơn gió mạnh thổi từ biển Bắc."),
        # Die
        ("Reise", "die", "die Reisen", "/ˈʁaɪ̯zə/", "Chuyến đi, chuyến du lịch", "Journey", "Gute Reise und viel Spaß im Urlaub!", "Chúc chuyến đi tốt đẹp và vui vẻ!"),
        ("Fahrkarte", "die", "die Fahrkarten", "/ˈfaːɐ̯ˌkaʁtə/", "Vé tàu xe", "Ticket", "Haben Sie alle Fahrkarten entwertet?", "Bạn đã dập vé tàu xe chưa?"),
        ("Haltestelle", "die", "die Haltestellen", "/ˈhaltəˌʃtɛlə/", "Trạm dừng (xe buýt/tram)", "Bus stop", "Die Haltestelle liegt direkt vor der Tür.", "Trạm xe buýt nằm ngay trước cửa."),
        ("Auskunft", "die", "die Auskünfte", "/ˈaʊ̯sˌkʊnft/", "Thông tin hướng dẫn", "Information", "Fragen Sie am Schalter nach Auskunft.", "Hãy hỏi thông tin ở quầy hướng dẫn."),
        ("Verspätung", "die", "die Verspätungen", "/fɛɐ̯ˈʃpɛːtʊŋ/", "Sự chậm trễ, trễ giờ", "Delay", "Der Zug hat zehn Minuten Verspätung.", "Chuyến tàu bị trễ mười phút."),
        ("Verbindung", "die", "die Verbindungen", "/fɛɐ̯ˈbɪndʊŋ/", "Sự kết nối, tuyến đường", "Connection", "Es gibt eine direkte Verbindung nach Berlin.", "Có một tuyến chạy thẳng đến Berlin."),
        ("Krankheit", "die", "die Krankheiten", "/ˈkʁaŋkhaɪ̯t/", "Căn bệnh, sự ốm đau", "Illness", "Gegen diese Krankheit gibt es gute Medikamente.", "Có thuốc điều trị tốt cho căn bệnh này."),
        ("Gesundheit", "die", "die Gesundheiten", "/ɡəˈzʊnthaɪ̯t/", "Sức khỏe", "Health", "Gesundheit ist das Wichtigste im Leben.", "Sức khỏe là điều quan trọng nhất trong cuộc sống."),
        ("Medizin", "die", "die Medizinen", "/mediˈt͡siːn/", "Thuốc men, y học", "Medicine", "Nehmen Sie die Medizin dreimal täglich.", "Uống thuốc này ba lần mỗi ngày."),
        ("Tablette", "die", "die Tabletten", "/taˈblɛtə/", "Viên thuốc", "Pill / Tablet", "Die Kopfschmerztablette wirkt schnell.", "Viên thuốc giảm đau đầu có tác dụng nhanh chóng."),
        ("Apotheke", "die", "die Apotheken", "/apoˈteːkə/", "Hiệu thuốc tây", "Pharmacy", "Die Apotheke hat rund um die Uhr Notdienst.", "Hiệu thuốc có ca trực cấp cứu suốt ngày đêm."),
        ("Praxis", "die", "die Praxen", "/ˈpʁaksɪs/", "Phòng khám bác sĩ", "Medical practice", "Die Arztpraxis öffnet um acht Uhr.", "Phòng khám bác sĩ mở cửa lúc 8 giờ."),
        ("Untersuchung", "die", "die Untersuchungen", "/ʊntɐˈzuːxʊŋ/", "Khám bệnh, điều tra", "Examination", "Die Untersuchung dauerte nur zwanzig Minuten.", "Việc khám bệnh chỉ mất hai mươi phút."),
        ("Hand", "die", "die Hände", "/hant/", "Bàn tay", "Hand", "Waschen Sie sich vor dem Essen die Hände.", "Hãy rửa tay trước khi ăn cơm."),
        ("Nase", "die", "die Nasen", "/ˈnaːzə/", "Cái mũi", "Nose", "Meine Nase läuft wegen der Kälte.", "Mũi tôi bị chảy nước vì trời lạnh."),
        ("Brille", "die", "die Brillen", "/ˈbʁɪlə/", "Cặp kính mắt", "Glasses", "Ohne meine Brille kann ich nicht gut lesen.", "Không có kính tôi không đọc được rõ."),
        ("Hose", "die", "die Hosen", "/ˈhoːzə/", "Cái quần", "Trousers / Pants", "Die Hose passt mir perfekt.", "Chiếc quần này vừa vặn với tôi một cách hoàn hảo."),
        ("Jacke", "die", "die Jacken", "/ˈjakə/", "Áo khoác ngắn", "Jacket", "Zieh eine Jacke an, es ist kühl draußen.", "Hãy mặc áo khoác vào, bên ngoài trời mát lạnh."),
        ("Mütze", "die", "die Mützen", "/ˈmʏt͡sə/", "Mũ len ấm", "Beanie / Cap", "Die Mütze hält die Ohren warm.", "Chiếc mũ len giữ ấm cho đôi tai."),
        ("Bluse", "die", "die Blusen", "/ˈbluːzə/", "Áo sơ mi nữ", "Blouse", "Die weiße Bluse sieht sehr elegant aus.", "Chiếc áo sơ mi trắng trông rất thanh lịch."),
        ("Heizung", "die", "die Heizungen", "/ˈhaɪ̯t͡sʊŋ/", "Hệ thống sưởi", "Heating", "Im Winter drehen wir die Heizung auf.", "Vào mùa đông chúng tôi bật sưởi lên."),
        ("Miete", "die", "die Mieten", "/ˈmiːtə/", "Tiền thuê nhà", "Rent", "Die Miete für die Wohnung ist günstig.", "Tiền thuê căn hộ này khá phải chăng."),
        ("Garage", "die", "die Garagen", "/ɡaˈʁaːʒə/", "Gara để xe", "Garage", "Das Auto steht sicher in der Garage.", "Chiếc xe đỗ an toàn trong gara."),
        ("Treppe", "die", "die Treppen", "/ˈtʁɛpə/", "Cầu thang bộ", "Stairs", "Wir nehmen die Treppe statt den Aufzug.", "Chúng tôi đi thang bộ thay vì thang máy."),
        ("Rezeption", "die", "die Rezeptionen", "/ʁet͡sɛpˈt͡si̯oːn/", "Quầy lễ tân", "Reception", "Der Schlüssel liegt an der Rezeption bereit.", "Chìa khóa đã sẵn sàng tại quầy lễ tân."),
        # Das
        ("Gepäck", "das", "die Gepäcke", "/ɡəˈpɛk/", "Hành lý", "Luggage", "Wir geben das Gepäck am Schalter auf.", "Chúng tôi gửi hành lý tại quầy thủ tục."),
        ("Ticket", "das", "die Tickets", "/ˈtɪkət/", "Vé xe, vé máy bay", "Ticket", "Zeigen Sie bitte Ihr Ticket vor.", "Làm ơn xuất trình vé của bạn."),
        ("Gleis", "das", "die Gleise", "/ɡlaɪ̯s/", "Đường ray, sân ga", "Track", "Der Zug fährt von Gleis 3 ab.", "Tàu khởi hành từ đường ray số 3."),
        ("Schiff", "das", "die Schiffe", "/ʃɪf/", "Con tàu, thuyền lớn", "Ship", "Das Schiff fährt über den Bodensee.", "Con tàu lướt trên mặt hồ Bodensee."),
        ("Boot", "das", "die Boote", "/boːt/", "Chiếc thuyền nhỏ", "Boat", "Wir mieten ein kleines Boot am See.", "Chúng tôi thuê một chiếc thuyền nhỏ ở hồ."),
        ("Motorrad", "das", "die Motorräder", "/moˈtoːɐ̯ˌʁaːt/", "Xe mô tô, xe máy", "Motorcycle", "Er fährt sonntags gerne Motorrad.", "Chủ nhật anh ấy thích lái xe mô tô."),
        ("Bein", "das", "die Beine", "/baɪ̯n/", "Cái chân", "Leg", "Nach dem Marathon tun mir die Beine weh.", "Sau cuộc thi marathon chân tôi bị mỏi nhừ."),
        ("Auge", "das", "die Augen", "/ˈaʊ̯ɡə/", "Con mắt", "Eye", "Sie hat wunderschöne blaue Augen.", "Cô ấy có đôi mắt màu xanh tuyệt đẹp."),
        ("Ohr", "das", "die Ohren", "/oːɐ̯/", "Chiếc tai", "Ear", "Der Arzt untersucht das linke Ohr.", "Bác sĩ đang kiểm tra tai bên trái."),
        ("Haar", "das", "die Haare", "/haːɐ̯/", "Tóc, sợi tóc", "Hair", "Sie lässt sich die Haare schneiden.", "Cô ấy đi cắt tóc."),
        ("Herz", "das", "die Herzen", "/hɛʁt͡s/", "Trái tim", "Heart", "Sein Herz schlägt ruhig und kräftig.", "Trái tim anh ấy đập đều đặn và khỏe khoắn."),
        ("Fieber", "das", "die Fieber", "/ˈfiːbɐ/", "Cơn sốt", "Fever", "Das Kind hat hohes Fieber.", "Đứa bé bị sốt cao."),
        ("Medikament", "das", "die Medikamente", "/medikaˈmɛnt/", "Thuốc men", "Medication", "Nehmen Sie dieses Medikament regelmäßig.", "Hãy uống thuốc này đều đặn."),
        ("Pflaster", "das", "die Pflaster", "/ˈpflastɐ/", "Băng cá nhân", "Bandage / Plaster", "Kleben Sie ein Pflaster auf die kleine Wunde.", "Dán một miếng băng cá nhân lên vết thương nhỏ."),
        ("Rezept", "das", "die Rezepte", "/ʁeˈt͡sɛpt/", "Đơn thuốc, công thức nấu ăn", "Prescription / Recipe", "Der Arzt schreibt ein Rezept für die Apotheke.", "Bác sĩ kê đơn thuốc mang ra nhà thuốc."),
        ("Hemd", "das", "die Hemden", "/hɛmt/", "Áo sơ mi nam", "Shirt", "Er bügelt sein weißes Hemd für das Vorstellungsgespräch.", "Anh ấy ủi chiếc áo sơ mi trắng cho buổi phỏng vấn."),
        ("T-Shirt", "das", "die T-Shirts", "/ˈtiːˌʃœːɐ̯t/", "Áo thun, áo phông", "T-shirt", "Im Sommer trage ich gerne bunte T-Shirts.", "Mùa hè tôi thích mặc áo thun nhiều màu sắc."),
        ("Kleid", "das", "die Kleider", "/klaɪ̯t/", "Bộ váy, đầm liền", "Dress", "Sie trägt ein elegantes rotes Kleid.", "Cô ấy mặc một chiếc váy đỏ thanh lịch."),
        ("Geschenk", "das", "die Geschenke", "/ɡəˈʃɛŋk/", "Món quà", "Present / Gift", "Ich habe ein schönes Geschenk für dich.", "Tôi có một món quà đẹp dành cho bạn."),
        ("Gewitter", "das", "die Gewitter", "/ɡəˈvɪtɐ/", "Cơn dông bão sấm chớp", "Thunderstorm", "Am Nachmittag zog ein schweres Gewitter auf.", "Vào buổi chiều một cơn dông lớn kéo đến."),
        ("Klima", "das", "die Klimas", "/ˈkliːma/", "Khí hậu", "Climate", "Das Klima verändert sich weltweit.", "Khí hậu đang biến đổi trên toàn thế giới.")
    ]
    for w, gen, pl, ipa, vi, en, ex_de, ex_vi in a2_nouns:
        add(w, gen, pl, ipa, "Noun", "A2", vi, en, ex_de, ex_vi)

    # A2 Verbs & Adjectives
    a2_verbs_adjs = [
        ("abfahren", "Verb", "/ˈapˌfaːʁən/", "Khởi hành (tàu xe)", "to depart", "Der Zug fährt pünktlich um zehn Uhr ab.", "Chuyến tàu khởi hành đúng 10 giờ."),
        ("ankommen", "Verb", "/ˈanˌkɔmən/", "Đến nơi", "to arrive", "Wann kommt der Flug in Frankfurt an?", "Khi nào chuyến bay đến Frankfurt?"),
        ("umsteigen", "Verb", "/ˈʊmˌʃtaɪ̯ɡn̩/", "Đổi tàu/xe trung chuyển", "to change trains/buses", "Wir müssen in Hannover einmal umsteigen.", "Chúng ta phải đổi tàu một lần ở Hannover."),
        ("einsteigen", "Verb", "/ˈaɪ̯nˌʃtaɪ̯ɡn̩/", "Bước lên tàu xe", "to board / get in", "Bitte alle einsteigen, die Türen schließen!", "Xin mời tất cả lên tàu, cửa chuẩn bị đóng!"),
        ("aussteigen", "Verb", "/ˈaʊ̯sˌʃtaɪ̯ɡn̩/", "Xuống tàu xe", "to get off / exit", "An der nächsten Station steige ich aus.", "Tôi sẽ xuống ở ga kế tiếp."),
        ("abholen", "Verb", "/ˈapˌhoːlən/", "Đón ai đó, lấy đồ", "to pick up", "Ich hole dich vom Bahnhof mit dem Auto ab.", "Tôi sẽ lái ô tô ra ga đón bạn."),
        ("anrufen", "Verb", "/ˈanˌʁuːfn̩/", "Gọi điện thoại cho ai", "to call (phone)", "Ruf mich bitte an, wenn du Zeit hast.", "Hãy gọi cho tôi khi bạn có thời gian nhé."),
        ("aufstehen", "Verb", "/ˈaʊ̯fˌʃteːən/", "Thức dậy, đứng dậy", "to get up / wake up", "Unter der Woche stehe ich um sechs Uhr auf.", "Các ngày trong tuần tôi thức dậy lúc 6 giờ."),
        ("einkaufen", "Verb", "/ˈaɪ̯nˌkaʊ̯fn̩/", "Mua sắm đồ đạc", "to shop / buy groceries", "Samstags kaufen wir für die ganze Woche ein.", "Thứ Bảy chúng tôi mua sắm cho cả tuần."),
        ("fernsehen", "Verb", "/ˈfɛʁnˌzeːən/", "Xem tivi", "to watch TV", "Abends sehe ich gerne die Nachrichten fern.", "Buổi tối tôi thích xem thời sự trên tivi."),
        ("mitbringen", "Verb", "/ˈmɪtˌbʁɪŋən/", "Mang theo cái gì", "to bring along", "Soll ich einen Kuchen zur Party mitbringen?", "Tôi có nên mang theo một chiếc bánh ngọt đến tiệc không?"),
        ("vorbereiten", "Verb", "/ˈfoːɐ̯bəˌʁaɪ̯tn̩/", "Chuẩn bị", "to prepare", "Wir bereiten die Präsentation gemeinsam vor.", "Chúng tôi cùng nhau chuẩn bị bài thuyết trình."),
        ("teilnehmen", "Verb", "/ˈtaɪ̯lˌneːmən/", "Tham gia vào việc gì", "to participate", "Möchtest du am Deutschkurs teilnehmen?", "Bạn có muốn tham gia khóa học tiếng Đức không?"),
        ("unterschreiben", "Verb", "/ʊntɐˈʃʁaɪ̯bn̩/", "Ký tên", "to sign", "Bitte unterschreiben Sie den Vertrag hier unten.", "Làm ơn ký tên vào bản hợp đồng ở góc dưới này."),
        ("buchen", "Verb", "/ˈbuːxn̩/", "Đặt trước (vé, phòng)", "to book / reserve", "Wir haben das Hotelzimmer online gebucht.", "Chúng tôi đã đặt phòng khách sạn trực tuyến."),
        ("empfehlen", "Verb", "/ɛmˈpfeːlən/", "Giới thiệu, khuyên bảo", "to recommend", "Welches Gericht können Sie mir empfehlen?", "Bạn có thể giới thiệu cho tôi món ăn nào ngon không?"),
        ("wiederholen", "Verb", "/viːdɐˈhoːlən/", "Nhắc lại, lặp lại", "to repeat", "Könnten Sie diesen Satz bitte wiederholen?", "Bạn có thể nhắc lại câu này được không?"),
        ("erklären", "Verb", "/ɛɐ̯ˈklɛːʁən/", "Giải thích", "to explain", "Der Lehrer erklärt die Grammatikregel sehr geduldig.", "Thầy giáo giải thích quy tắc ngữ pháp rất kiên nhẫn."),
        ("gehören", "Verb", "/ɡəˈhøːʁən/", "Thuộc về ai đó", "to belong to", "Wem gehört dieses Buch?", "Cuốn sách này thuộc về ai?"),
        ("passen", "Verb", "/ˈpasn̩/", "Vừa vặn, phù hợp", "to fit / suit", "Passt es Ihnen morgen um zehn Uhr?", "10 giờ sáng mai có phù hợp với bạn không?"),
        ("gefallen", "Verb", "/ɡəˈfaln̩/", "Thích, làm ai hài lòng", "to please / like", "Die neue Wohnung gefällt mir sehr gut.", "Tôi rất thích căn hộ mới này."),
        ("schmecken", "Verb", "/ˈʃmɛkn̩/", "Có vị, ngon miệng", "to taste", "Das Essen schmeckt wirklich vorzüglich.", "Đồ ăn có vị thực sự xuất sắc."),
        ("wehtun", "Verb", "/ˈveːˌtuːn/", "Gây đau đớn", "to hurt", "Mein Knie tut seit gestern weh.", "Đầu gối của tôi bị đau từ hôm qua."),
        ("fehlen", "Verb", "/ˈfeːlən/", "Thiếu vắng, vắng mặt", "to lack / miss", "Zwei Schüler fehlen heute krankheitsbedingt.", "Hôm nay hai học sinh vắng mặt do bị ốm."),
        ("interessieren", "Verb", "/ɪntəʁɛˈsiːʁən/", "Quan tâm, chú ý", "to interest", "Ich interessiere mich für deutsche Kultur.", "Tôi quan tâm đến văn hóa Đức."),
        ("freuen", "Verb", "/ˈfʁɔɪ̯ən/", "Vui mừng, mong đợi", "to be glad / look forward", "Ich freue mich riesig auf das Wochenende.", "Tôi rất mong chờ đến ngày cuối tuần."),
        ("ärgern", "Verb", "/ˈɛʁɡɐn/", "Tức giận, bực bội", "to annoy / get angry", "Ärgere dich nicht über kleine Fehler.", "Đừng bực mình vì những lỗi nhỏ."),
        ("erinnern", "Verb", "/ɛɐ̯ˈʔɪnɐn/", "Nhớ lại, nhắc nhở", "to remember / remind", "Erinnerst du dich an unseren Urlaub in Wien?", "Bạn có nhớ kỳ nghỉ của chúng ta ở Viên không?"),
        ("gewinnen", "Verb", "/ɡəˈvɪnən/", "Chiến thắng, trúng giải", "to win", "Unsere Mannschaft hat das Spiel gewonnen.", "Đội bóng của chúng tôi đã giành chiến thắng."),
        ("verlieren", "Verb", "/fɛɐ̯ˈliːʁən/", "Đánh mất, thua cuộc", "to lose", "Ich habe meinen Haustürschlüssel verloren.", "Tôi đã làm mất chìa khóa nhà."),
        # Adjectives
        ("pünktlich", "Adjective", "/ˈpʏŋktlɪç/", "Đúng giờ", "punctual", "Die Züge in der Schweiz sind fast immer pünktlich.", "Tàu hỏa ở Thụy Sĩ gần như luôn đúng giờ."),
        ("höflich", "Adjective", "/ˈhøːflɪç/", "Lịch thiệp", "polite", "Ein höfliches Wort öffnet viele Türen.", "Một lời nói lịch thiệp mở ra nhiều cánh cửa."),
        ("berühmt", "Adjective", "/bəˈʁyːmt/", "Nổi tiếng", "famous", "Mozart ist ein weltberühmter Komponist.", "Mozart là nhà soạn nhạc nổi tiếng thế giới."),
        ("wunderbar", "Adjective", "/ˈvʊndɐbaːɐ̯/", "Kỳ diệu, tuyệt vời", "wonderful", "Wir hatten einen wunderbaren Urlaub in den Bergen.", "Chúng tôi đã có một kỳ nghỉ tuyệt vời trên núi."),
        ("gemütlich", "Adjective", "/ɡəˈmyːtlɪç/", "Ấm cúng, dễ chịu", "cozy", "Das Café ist sehr gemütlich eingerichtet.", "Quán cà phê được bài trí rất ấm cúng."),
        ("anstrengend", "Adjective", "/ˈanˌʃtʁɛŋənt/", "Căng thẳng, vất vả", "exhausting", "Die lange Wanderung war ziemlich anstrengend.", "Chuyến đi bộ đường dài khá mệt và vất vả."),
        ("spannend", "Adjective", "/ˈʃpanənt/", "Hồi hộp, hấp dẫn", "thrilling", "Der Krimi war von Anfang bis Ende spannend.", "Cuốn tiểu thuyết trinh thám hồi hộp từ đầu đến cuối."),
        ("langweilig", "Adjective", "/ˈlaŋˌvaɪ̯lɪç/", "Nhàm chán", "boring", "Der Film war leider stinklangweilig.", "Bộ phim tiếc là buồn ngủ và nhàm chán."),
        ("bequem", "Adjective", "/bəˈkveːm/", "Thoải mái, tiện lợi", "comfortable", "Dieser Sessel ist unglaublich bequem.", "Chiếc ghế bành này thoải mái vô cùng."),
        ("unbequem", "Adjective", "/ˈʊnbəˌkveːm/", "Bất tiện, không êm", "uncomfortable", "Die Holzbank war hart und unbequem.", "Băng ghế gỗ cứng và khó chịu.")
    ]
    for item in a2_verbs_adjs:
        w, pos, ipa, vi, en, ex_de, ex_vi = item
        add(w, None, None, ipa, pos, "A2", vi, en, ex_de, ex_vi)

    # Let's write B1, B2, C1, C2 systemic additions to ensure total hits exactly 1000 items!
    # Let's prepare arrays for B1, B2, C1, C2.
    
    # B1 Words (Education, Career, Society, Environment, Travel, Opinion)
    b1_data = [
        ("Erfahrung", "die", "die Erfahrungen", "/ɛɐ̯ˈfaːʁʊŋ/", "Noun", "Kinh nghiệm, trải nghiệm", "Experience", "Aus dieser Erfahrung habe ich viel gelernt.", "Từ trải nghiệm này tôi đã học được rất nhiều."),
        ("Ergebnis", "das", "die Ergebnisse", "/ɛɐ̯ˈɡeːpnɪs/", "Noun", "Kết quả", "Result", "Das Ergebnis der Prüfung war sehr erfreulich.", "Kết quả bài thi rất đáng mừng."),
        ("Unterschied", "der", "die Unterschiede", "/ˈʊntɐˌʃiːt/", "Noun", "Sự khác biệt", "Difference", "Es gibt einen deutlichen Unterschied zwischen beiden.", "Có sự khác biệt rõ rệt giữa hai bên."),
        ("Möglichkeit", "die", "die Möglichkeiten", "/ˈmøːklɪçkaɪ̯t/", "Noun", "Cơ hội, khả năng", "Possibility", "Wir haben viele Möglichkeiten, das Problem zu lösen.", "Chúng ta có nhiều khả năng để giải quyết vấn đề."),
        ("Entscheidung", "die", "die Entscheidungen", "/ɛntˈʃaɪ̯dʊŋ/", "Noun", "Quyết định", "Decision", "Das war eine schwierige Entscheidung für die Familie.", "Đó là một quyết định khó khăn cho gia đình."),
        ("Vorschlag", "der", "die Vorschläge", "/ˈfoːɐ̯ˌʃlaːk/", "Noun", "Lời đề xuất, gợi ý", "Suggestion", "Dein Vorschlag klingt sehr vernünftig.", "Đề xuất của bạn nghe rất hợp lý."),
        ("Meinung", "die", "die Meinungen", "/ˈmaɪ̯nʊŋ/", "Noun", "Ý kiến, quan điểm", "Opinion", "Meiner Meinung nach sollten wir zustimmen.", "Theo quan điểm của tôi, chúng ta nên đồng ý."),
        ("Grund", "der", "die Gründe", "/ɡʁʊnt/", "Noun", "Lý do, nguyên nhân", "Reason", "Aus welchem Grund kommst du so spät?", "Vì lý do gì mà bạn đến muộn thế?"),
        ("Zukunft", "die", "die Zukünfte", "/ˈt͡suːkʊnft/", "Noun", "Tương lai", "Future", "Wir blicken optimistisch in die Zukunft.", "Chúng tôi nhìn vào tương lai với sự lạc quan."),
        ("Vergangenheit", "die", "die Vergangenheiten", "/fɛɐ̯ˈɡaŋənhaɪ̯t/", "Noun", "Quá khứ", "Past", "Man sollte aus der Vergangenheit lernen.", "Người ta nên học hỏi từ quá khứ."),
        ("Gesellschaft", "die", "die Gesellschaften", "/ɡəˈzɛlʃaft/", "Noun", "Xã hội, công ty", "Society", "Jeder trägt Verantwortung in der Gesellschaft.", "Mỗi người đều gánh vác trách nhiệm trong xã hội."),
        ("Umwelt", "die", "die Umwelten", "/ˈʊmˌvɛlt/", "Noun", "Môi trường tự nhiên", "Environment", "Wir müssen die Umwelt für unsere Kinder schützen.", "Chúng ta phải bảo vệ môi trường cho con cháu mình."),
        ("Ausbildung", "die", "die Ausbildungen", "/ˈaʊ̯sˌbɪldʊŋ/", "Noun", "Đào tạo nghề", "Vocational training", "Er macht eine Ausbildung zum Mechatroniker.", "Anh ấy đang học nghề cơ điện tử."),
        ("Studium", "das", "die Studien", "/ˈʃtuːdi̯ʊm/", "Noun", "Việc học đại học", "University studies", "Nach dem Abitur begann sie ihr Studium.", "Sau khi tốt nghiệp cấp 3, cô ấy bắt đầu học đại học."),
        ("Bewerbung", "die", "die Bewerbungen", "/bəˈvɛʁbʊŋ/", "Noun", "Hồ sơ ứng tuyển", "Job application", "Ich habe meine Bewerbung per E-Mail abgeschickt.", "Tôi đã gửi hồ sơ ứng tuyển qua email."),
        ("Lebenslauf", "der", "die Lebensläufe", "/ˈleːbn̩sˌlaʊ̯f/", "Noun", "Sơ yếu lý lịch, CV", "Curriculum Vitae", "Ein lückenloser Lebenslauf ist von Vorteil.", "Một bản CV liền mạch rõ ràng là một lợi thế."),
        ("Gehalt", "das", "die Gehälter", "/ɡəˈhalt/", "Noun", "Tiền lương", "Salary", "Das Gehalt wird am Monatsende überwiesen.", "Tiền lương sẽ được chuyển khoản vào cuối tháng."),
        ("Erfolg", "der", "die Erfolge", "/ɛɐ̯ˈfɔlk/", "Noun", "Thành công", "Success", "Fleiß ist der Schlüssel zum beruflichen Erfolg.", "Chăm chỉ là chìa khóa dẫn tới thành công trong công việc."),
        ("Ziel", "das", "die Ziele", "/t͡siːl/", "Noun", "Mục tiêu, đích đến", "Goal / Target", "Man muss klare Ziele vor Augen haben.", "Người ta cần phải có những mục tiêu rõ ràng."),
        ("Gefahr", "die", "die Gefahren", "/ɡəˈfaːɐ̯/", "Noun", "Nguy hiểm, mối đe dọa", "Danger", "Hier besteht keine Gefahr für Fußgänger.", "Ở đây không có mối nguy hiểm nào cho người đi bộ.")
    ]
    for w, gen, pl, ipa, pos, vi, en, ex_de, ex_vi in b1_data:
        add(w, gen, pl, ipa, pos, "B1", vi, en, ex_de, ex_vi)

    # B2 Words (Advanced Discussion, Society, Science, Politics, Formal)
    b2_data = [
        ("Zusammenhang", "der", "die Zusammenhänge", "/t͡suˈzamənˌhaŋ/", "Noun", "Mối liên hệ, ngữ cảnh", "Correlation / Context", "In diesem Zusammenhang gibt es neue Erkenntnisse.", "Trong mối liên hệ này đã có những nhận thức mới."),
        ("Verantwortung", "die", "die Verantwortungen", "/fɛɐ̯ˈʔantvɔʁtʊŋ/", "Noun", "Trách nhiệm", "Responsibility", "Führungskräfte tragen eine hohe Verantwortung.", "Các nhà lãnh đạo gánh vác trách nhiệm rất lớn."),
        ("Voraussetzung", "die", "die Voraussetzungen", "/foˈʁaʊ̯sˌzɛt͡sʊŋ/", "Noun", "Điều kiện tiên quyết", "Prerequisite", "Gute Deutschkenntnisse sind eine wichtige Voraussetzung.", "Trình độ tiếng Đức tốt là điều kiện tiên quyết quan trọng."),
        ("Bedeutung", "die", "die Bedeutungen", "/bəˈdɔɪ̯tʊŋ/", "Noun", "Ý nghĩa, tầm quan trọng", "Significance", "Dieses Abkommen ist von enormer Bedeutung.", "Hiệp định này có ý nghĩa to lớn."),
        ("Wirtschaft", "die", "die Wirtschaften", "/ˈvɪʁtʃaft/", "Noun", "Nền kinh tế", "Economy", "Die Wirtschaft erholt sich nach der Krise rasch.", "Nền kinh tế phục hồi nhanh chóng sau khủng hoảng."),
        ("Wissenschaft", "die", "die Wissenschaften", "/ˈvɪsn̩ʃaft/", "Noun", "Khoa học", "Science", "Die moderne Wissenschaft macht erstaunliche Fortschritte.", "Khoa học hiện đại đạt được những bước tiến đáng kinh ngạc."),
        ("Forschung", "die", "die Forschungen", "/ˈfɔʁʃʊŋ/", "Noun", "Nghiên cứu khoa học", "Research", "Das Institut betreibt intensive Krebsforschung.", "Viện đang tiến hành nghiên cứu chuyên sâu về ung thư."),
        ("Entwicklung", "die", "die Entwicklungen", "/ɛntˈvɪklʊŋ/", "Noun", "Sự phát triển", "Development", "Die technologische Entwicklung schreitet voran.", "Sự phát triển công nghệ đang tiến bước mạnh mẽ."),
        ("Verhalten", "das", "die Verhalten", "/fɛɐ̯ˈhaltn̩/", "Noun", "Hành vi, thái độ", "Behavior", "Sein Verhalten war in dieser Situation vorbildlich.", "Hành vi của anh ấy trong tình huống đó thật đáng khen ngợi."),
        ("Einfluss", "der", "die Einflüsse", "/ˈaɪ̯nˌflʊs/", "Noun", "Sự ảnh hưởng, tầm tác động", "Influence", "Soziale Medien haben großen Einfluss auf Jugendliche.", "Mạng xã hội có ảnh hưởng lớn tới thanh thiếu niên."),
        ("Maßnahme", "die", "die Maßnahmen", "/ˈmaːsˌnaːmə/", "Noun", "Biện pháp, giải pháp", "Measure", "Die Regierung ergreift strenge Schutzmaßnahmen.", "Chính phủ đang áp dụng các biện pháp bảo vệ nghiêm ngặt."),
        ("Herausforderung", "die", "die Herausforderungen", "/hɛˈʁaʊ̯sˌfɔʁdəʁʊŋ/", "Noun", "Thách thức, thử thách", "Challenge", "Der Klimawandel ist eine globale Herausforderung.", "Biến đổi khí hậu là một thách thức mang tính toàn cầu.")
    ]
    for w, gen, pl, ipa, pos, vi, en, ex_de, ex_vi in b2_data:
        add(w, gen, pl, ipa, pos, "B2", vi, en, ex_de, ex_vi)

    # C1 Words (Academic, Nuances, Rhetoric, Abstract)
    c1_data = [
        ("Widerspruch", "der", "die Widersprüche", "/ˈviːdɐˌʃpʁʊx/", "Noun", "Sự mâu thuẫn, phản bác", "Contradiction", "Die Theorie steht im offenen Widerspruch zur Praxis.", "Lý thuyết này mâu thuẫn rõ rệt với thực tiễn."),
        ("Schlussfolgerung", "die", "die Schlussfolgerungen", "/ˈʃlʊsˌfɔlɡəʁʊŋ/", "Noun", "Kết luận logic, suy luận", "Conclusion", "Welche Schlussfolgerung lässt sich daraus ziehen?", "Có thể rút ra kết luận logic nào từ điều đó?"),
        ("Erkenntnis", "die", "die Erkenntnisse", "/ɛɐ̯ˈkɛntnɪs/", "Noun", "Nhận thức, phát kiến sâu sắc", "Insight / Realization", "Neuere wissenschaftliche Erkenntnisse bestätigen diese These.", "Những nhận thức khoa học mới đã xác nhận luận điểm này."),
        ("Differenzierung", "die", "die Differenzierungen", "/dɪfəʁɛnˈt͡siːʁʊŋ/", "Noun", "Sự phân biệt tinh tế", "Differentiation", "Das Thema erfordert eine differenzierte Betrachtung.", "Chủ đề này đòi hỏi sự xem xét tinh tế nhiều mặt."),
        ("Hypothese", "die", "die Hypothesen", "/hypoˈteːzə/", "Noun", "Giả thuyết khoa học", "Hypothesis", "Die Forscher überprüfen derzeit ihre Hypothese.", "Các nhà nghiên cứu đang kiểm chứng lại giả thuyết của họ."),
        ("Diskrepanz", "die", "die Diskrepanzen", "/dɪskʁeˈpant͡s/", "Noun", "Sự sai lệch, độ chênh lệch", "Discrepancy", "Es besteht eine deutliche Diskrepanz zwischen Wort und Tat.", "Có sự chênh lệch rõ ràng giữa lời nói và việc làm.")
    ]
    for w, gen, pl, ipa, pos, vi, en, ex_de, ex_vi in c1_data:
        add(w, gen, pl, ipa, pos, "C1", vi, en, ex_de, ex_vi)

    # C2 Words (Mastery, Cultural nuance, Philosophical, High Register)
    c2_data = [
        ("Weltanschauung", "die", "die Weltanschauungen", "/ˈvɛltʔanˌʃaʊ̯ʊŋ/", "Noun", "Thế giới quan triết học", "Worldview", "Seine humanistische Weltanschauung prägte sein Handeln.", "Thế giới quan nhân văn của ông đã định hình mọi hành động."),
        ("Geistesblitz", "der", "die Geistesblitze", "/ˈɡaɪ̯stəsˌblɪt͡s/", "Noun", "Ý tưởng lóe sáng bất chợt", "Brainwave", "Inmitten der Nacht hatte der Erfinder einen Geistesblitz.", "Nửa đêm nhà phát minh chợt nảy ra một ý tưởng sáng chói."),
        ("Kummerspeck", "der", "die Kummerspecke", "/ˈkʊmɐˌʃpɛk/", "Noun", "Tăng cân vì stress/buồn phiền", "Grief bacon (stress weight)", "Nach der Trennung legte er sich etwas Kummerspeck zu.", "Sau cuộc chia tay anh ấy bị tăng cân vì buồn phiền."),
        ("Schadenfreude", "die", "die Schadenfreuden", "/ˈʃaːdn̩ˌfʁɔɪ̯də/", "Noun", "Sự hả hê trước rủi ro của người khác", "Malicious joy", "Schadenfreude gilt als verpönte Charaktereigenschaft.", "Sự hả hê khi người khác gặp rủi ro là một tính cách bị chê trách."),
        ("Fingerspitzengefühl", "das", "die Fingerspitzengefühle", "/ˈfɪŋɐʃpɪt͡sn̩ɡəˌfyːl/", "Noun", "Sự tinh tế, khéo léo trong xử lý tình huống", "Intuitive tact", "Diplomatische Verhandlungen erfordern viel Fingerspitzengefühl.", "Các cuộc đàm phán ngoại giao đòi hỏi sự khéo léo tinh tế tột bậc.")
    ]
    for w, gen, pl, ipa, pos, vi, en, ex_de, ex_vi in c2_data:
        add(w, gen, pl, ipa, pos, "C2", vi, en, ex_de, ex_vi)

    return words

# We now generate systemic vocabulary items up to 1000 items
base_words = generate_1000_words()
print(f"Base words manually handcrafted: {len(base_words)}")
