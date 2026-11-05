#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 1000 curated, high-quality German vocabulary items across CEFR levels A1, A2, B1, B2, C1, C2.
"""

import json

# Categorized dictionary base data
VOCAB_RAW = [
    # --- A1 NOUNS (der/die/das) ---
    ("Apfel", "der", "die Äpfel", "/ˈapfl̩/", "Noun", "A1", "Quả táo", "Apple", "Der Apfel ist saftig und süß.", "Quả táo mọng nước và ngọt."),
    ("Tisch", "der", "die Tische", "/tɪʃ/", "Noun", "A1", "Cái bàn", "Table", "Das Buch liegt auf dem Tisch.", "Quyển sách nằm trên bàn."),
    ("Stuhl", "der", "die Stühle", "/ʃtuːl/", "Noun", "A1", "Cái ghế", "Chair", "Der Stuhl ist sehr bequem.", "Chiếc ghế rất thoải mái."),
    ("Hund", "der", "die Hunde", "/hʊnt/", "Noun", "A1", "Con chó", "Dog", "Der Hund läuft im Garten.", "Con chó chạy trong vườn."),
    ("Kaffee", "der", "die Kaffees", "/ˈkafe/", "Noun", "A1", "Cà phê", "Coffee", "Der Kaffee riecht herrlich.", "Cà phê có mùi thơm tuyệt vời."),
    ("Tee", "der", "die Tees", "/teː/", "Noun", "A1", "Trà", "Tea", "Trinkst du lieber Tee oder Kaffee?", "Bạn thích uống trà hay cà phê hơn?"),
    ("Käse", "der", "die Käse", "/ˈkɛːzə/", "Noun", "A1", "Phô mai", "Cheese", "Der Käse schmeckt würzig.", "Phô mai có vị béo đậm đà."),
    ("Kuchen", "der", "die Kuchen", "/ˈkuːxn̩/", "Noun", "A1", "Bánh ngọt", "Cake", "Der Kuchen schmeckt lecker.", "Bánh ngọt rất ngon."),
    ("Zucker", "der", "die Zucker", "/ˈt͡sʊkɐ/", "Noun", "A1", "Đường", "Sugar", "Ich nehme Zucker in den Tee.", "Tôi cho đường vào trà."),
    ("Pfeffer", "der", "die Pfeffer", "/ˈpfɛfɐ/", "Noun", "A1", "Hạt tiêu", "Pepper", "Der Pfeffer ist sehr scharf.", "Hạt tiêu rất cay."),
    ("Reis", "der", "die Reise", "/ʁaɪ̯s/", "Noun", "A1", "Gạo, cơm", "Rice", "Wir kochen heute Reis mit Gemüse.", "Hôm nay chúng tôi nấu cơm với rau."),
    ("Fisch", "der", "die Fische", "/fɪʃ/", "Noun", "A1", "Con cá", "Fish", "Der Fisch schwimmt im Wasser.", "Con cá bơi trong nước."),
    ("Salat", "der", "die Salate", "/zaˈlaːt/", "Noun", "A1", "Món xà lách", "Salad", "Ich esse einen frischen Salat.", "Tôi ăn món xà lách tươi."),
    ("Bruder", "der", "die Brüder", "/ˈbʁuːdɐ/", "Noun", "A1", "Anh/em trai", "Brother", "Mein Bruder wohnt in Berlin.", "Anh trai tôi sống ở Berlin."),
    ("Vater", "der", "die Väter", "/ˈfaːtɐ/", "Noun", "A1", "Người cha", "Father", "Mein Vater liest die Zeitung.", "Bố tôi đang đọc báo."),
    ("Sohn", "der", "die Söhne", "/zoːn/", "Noun", "A1", "Con trai", "Son", "Ihr Sohn geht in die Schule.", "Con trai cô ấy đi học."),
    ("Freund", "der", "die Freunde", "/fʁɔɪ̯nt/", "Noun", "A1", "Bạn trai, người bạn", "Friend", "Er ist mein bester Freund.", "Anh ấy là bạn thân nhất của tôi."),
    ("Mann", "der", "die Männer", "/man/", "Noun", "A1", "Người đàn ông, người chồng", "Man / Husband", "Der Mann arbeitet im Büro.", "Người đàn ông làm việc ở văn phòng."),
    ("Junge", "der", "die Jungen", "/ˈjʊŋə/", "Noun", "A1", "Cậu bé", "Boy", "Der Junge spielt Fußball.", "Cậu bé đang chơi bóng đá."),
    ("Tag", "der", "die Tage", "/taːk/", "Noun", "A1", "Ngày", "Day", "Ich wünsche dir einen schönen Tag.", "Tôi chúc bạn một ngày tốt lành."),
    ("Morgen", "der", "die Morgen", "/ˈmɔʁɡn̩/", "Noun", "A1", "Buổi sáng", "Morning", "Guten Morgen, wie geht es dir?", "Chào buổi sáng, bạn khỏe không?"),
    ("Abend", "der", "die Abende", "/ˈaːbn̩t/", "Noun", "A1", "Buổi tối", "Evening", "Am Abend koche ich gerne.", "Vào buổi tối tôi thích nấu ăn."),
    ("Monat", "der", "die Monate", "/ˈmoːnat/", "Noun", "A1", "Tháng", "Month", "Ein Monat hat vier Wochen.", "Một tháng có bốn tuần."),
    ("Schlüssel", "der", "die Schlüssel", "/ˈʃlʏsl̩/", "Noun", "A1", "Chìa khóa", "Key", "Wo ist mein Schlüssel?", "Chìa khóa của tôi ở đâu?"),
    ("Kugelschreiber", "der", "die Kugelschreiber", "/ˈkuːɡl̩ˌʃʁaɪ̯bɐ/", "Noun", "A1", "Bút bi", "Pen", "Haben Sie einen Kugelschreiber?", "Bạn có chiếc bút bi nào không?"),
    ("Bleistift", "der", "die Bleistifte", "/ˈblaɪ̯ˌʃtɪft/", "Noun", "A1", "Bút chì", "Pencil", "Der Bleistift ist neu.", "Cây bút chì còn mới."),
    ("Rucksack", "der", "die Rucksäcke", "/ˈʁʊkˌzak/", "Noun", "A1", "Ba lô", "Backpack", "Der Rucksack ist ziemlich schwer.", "Chiếc ba lô khá nặng."),
    ("Schrank", "der", "die Schränke", "/ʃʁaŋk/", "Noun", "A1", "Cái tủ", "Wardrobe / Cupboard", "Die Kleidung hängt im Schrank.", "Quần áo treo trong tủ."),
    ("Computer", "der", "die Computer", "/kɔmˈpjuːtɐ/", "Noun", "A1", "Máy tính", "Computer", "Ich brauche einen Computer für die Arbeit.", "Tôi cần một chiếc máy tính cho công việc."),
    ("Fernseher", "der", "die Fernseher", "/ˈfɛʁnˌzeːɐ/", "Noun", "A1", "Tivi", "Television", "Der Fernseher ist ausgeschaltet.", "Chiếc tivi đã tắt."),

    # --- A1 DIE NOUNS ---
    ("Katze", "die", "die Katzen", "/ˈkat͡sə/", "Noun", "A1", "Con mèo", "Cat", "Die Katze schläft auf dem Sofa.", "Con mèo đang ngủ trên sô-pha."),
    ("Sonne", "die", "die Sonnen", "/ˈzɔnə/", "Noun", "A1", "Mặt trời", "Sun", "Die Sonne scheint hell.", "Mặt trời chiếu sáng rực rỡ."),
    ("Blume", "die", "die Blumen", "/ˈbluːmə/", "Noun", "A1", "Bông hoa", "Flower", "Die Blume riecht gut.", "Bông hoa có mùi thơm."),
    ("Milch", "die", "die Milche", "/mɪlç/", "Noun", "A1", "Sữa", "Milk", "Ich trinke gerne frische Milch.", "Tôi thích uống sữa tươi."),
    ("Butter", "die", "die Butter", "/ˈbʊtɐ/", "Noun", "A1", "Bơ", "Butter", "Die Butter ist im Kühlschrank.", "Bơ ở trong tủ lạnh."),
    ("Suppe", "die", "die Suppen", "/ˈzʊpə/", "Noun", "A1", "Món súp, canh", "Soup", "Die Gemüsesuppe schmeckt heiß gut.", "Món súp rau ăn nóng rất ngon."),
    ("Kartoffel", "die", "die Kartoffeln", "/kaʁˈtɔfl̩/", "Noun", "A1", "Khoai tây", "Potato", "Die Kartoffeln werden gekocht.", "Khoai tây đang được luộc."),
    ("Tomate", "die", "die Tomaten", "/toˈmaːtə/", "Noun", "A1", "Cà chua", "Tomato", "Die Tomate ist rot und reif.", "Quả cà chua đỏ và chín mọng."),
    ("Orange", "die", "die Orangen", "/oˈʁaŋʒə/", "Noun", "A1", "Quả cam", "Orange", "Die Orange enthält viel Vitamin C.", "Quả cam chứa nhiều vitamin C."),
    ("Banane", "die", "die Bananen", "/baˈnaːnə/", "Noun", "A1", "Quả chuối", "Banana", "Affen essen gerne Bananen.", "Những chú khỉ thích ăn chuối."),
    ("Mutter", "die", "die Mütter", "/ˈmʊtɐ/", "Noun", "A1", "Người mẹ", "Mother", "Meine Mutter kocht sehr gut.", "Mẹ tôi nấu ăn rất ngon."),
    ("Schwester", "die", "die Schwestern", "/ˈʃvɛstɐ/", "Noun", "A1", "Chị/em gái", "Sister", "Meine Schwester lernt Deutsch.", "Em gái tôi đang học tiếng Đức."),
    ("Tochter", "die", "die Töchter", "/ˈtɔxtɐ/", "Noun", "A1", "Con gái", "Daughter", "Die Tochter malt ein schönes Bild.", "Cô con gái vẽ một bức tranh đẹp."),
    ("Frau", "die", "die Frauen", "/fʁaʊ̯/", "Noun", "A1", "Phụ nữ, người vợ", "Woman / Wife", "Die Frau arbeitet als Lehrerin.", "Người phụ nữ làm nghề giáo viên."),
    ("Freundin", "die", "die Freundinnen", "/ˈfʁɔɪ̯ndɪn/", "Noun", "A1", "Bạn nữ, bạn gái", "Female friend", "Das ist meine Freundin Anna.", "Đây là bạn gái tôi Anna."),
    ("Familie", "die", "die Familien", "/faˈmiːli̯ə/", "Noun", "A1", "Gia đình", "Family", "Meine Familie ist groß.", "Gia đình tôi rất đông người."),
    ("Woche", "die", "die Wochen", "/ˈvɔxə/", "Noun", "A1", "Tuần", "Week", "Eine Woche hat sieben Tage.", "Một tuần có bảy ngày."),
    ("Nacht", "die", "die Nächte", "/naxt/", "Noun", "A1", "Đêm", "Night", "Gute Nacht und schlaf gut!", "Chúc ngủ ngon và ngủ thật say!"),
    ("Uhr", "die", "die Uhren", "/uːɐ̯/", "Noun", "A1", "Đồng hồ, giờ", "Clock / O'clock", "Wie viel Uhr ist es?", "Bây giờ là mấy giờ rồi?"),
    ("Stadt", "die", "die Städte", "/ʃtat/", "Noun", "A1", "Thành phố", "City", "Wien ist eine schöne Stadt.", "Viên là một thành phố xinh đẹp."),
    ("Straße", "die", "die Straßen", "/ˈʃtʁaːsə/", "Noun", "A1", "Con đường, phố", "Street", "Die Straße ist breit und sauber.", "Con đường rộng và sạch sẽ."),
    ("Wohnung", "die", "die Wohnungen", "/ˈvoːnʊŋ/", "Noun", "A1", "Căn hộ", "Apartment", "Unsere Wohnung hat drei Zimmer.", "Căn hộ của chúng tôi có ba phòng."),
    ("Küche", "die", "die Küchen", "/ˈkʏçə/", "Noun", "A1", "Nhà bếp", "Kitchen", "Wir essen oft in der Küche.", "Chúng tôi thường ăn trong bếp."),
    ("Tür", "die", "die Türen", "/tyːɐ̯/", "Noun", "A1", "Cánh cửa", "Door", "Bitte schließen Sie die Tür.", "Làm ơn đóng cửa lại."),
    ("Lampe", "die", "die Lampen", "/ˈlampə/", "Noun", "A1", "Cái đèn", "Lamp", "Die Lampe spendet warmes Licht.", "Chiếc đèn tỏa ánh sáng ấm áp."),
    ("Tasche", "die", "die Taschen", "/ˈtaʃə/", "Noun", "A1", "Chiếc túi, túi xách", "Bag", "Ich habe meine Tasche vergessen.", "Tôi đã để quên túi xách."),
    ("Flasche", "die", "die Flaschen", "/ˈflaʃə/", "Noun", "A1", "Chai nước, bình", "Bottle", "Eine Flasche Mineralwasser bitte.", "Cho tôi một chai nước khoáng."),
    ("Tasse", "die", "die Tassen", "/ˈtasə/", "Noun", "A1", "Cái tách, chén", "Cup", "Möchtest du eine Tasse Tee?", "Bạn có muốn một tách trà không?"),
    ("Zeitung", "die", "die Zeitungen", "/ˈt͡saɪ̯tʊŋ/", "Noun", "A1", "Tờ báo", "Newspaper", "Er liest täglich die Zeitung.", "Anh ấy đọc báo hàng ngày."),
    ("Schule", "die", "die Schulen", "/ˈʃuːlə/", "Noun", "A1", "Trường học", "School", "Die Kinder gehen zur Schule.", "Lũ trẻ đang đi học."),

    # --- A1 DAS NOUNS ---
    ("Buch", "das", "die Bücher", "/buːx/", "Noun", "A1", "Quyển sách", "Book", "Ich lese gerne ein gutes Buch.", "Tôi thích đọc một cuốn sách hay."),
    ("Wasser", "das", "die Wässer", "/ˈvasɐ/", "Noun", "A1", "Nước", "Water", "Trinken Sie genug Wasser jeden Tag.", "Hãy uống đủ nước mỗi ngày."),
    ("Brot", "das", "die Brote", "/bʁoːt/", "Noun", "A1", "Bánh mì", "Bread", "Das Brot riecht frisch.", "Bánh mì có mùi thơm mới nướng."),
    ("Brötchen", "das", "die Brötchen", "/ˈbʁøːtçn̩/", "Noun", "A1", "Bánh mì tròn nhỏ", "Bread roll", "Zum Frühstück esse ich zwei Brötchen.", "Bữa sáng tôi ăn hai cái bánh mì nhỏ."),
    ("Ei", "das", "die Eier", "/aɪ̯/", "Noun", "A1", "Quả trứng", "Egg", "Möchtest du ein gekochtes Ei?", "Bạn có muốn một quả trứng luộc không?"),
    ("Fleisch", "das", "die Fleische", "/flaɪ̯ʃ/", "Noun", "A1", "Thịt", "Meat", "Das Fleisch ist gut gewürzt.", "Thịt được ướp gia vị đậm đà."),
    ("Gemüse", "das", "die Gemüse", "/ɡəˈmyːzə/", "Noun", "A1", "Rau củ", "Vegetables", "Gemüse ist gesund für den Körper.", "Rau củ rất tốt cho sức khỏe cơ thể."),
    ("Obst", "das", "die Obste", "/oːpst/", "Noun", "A1", "Trái cây", "Fruit", "Wir kaufen frisches Obst auf dem Markt.", "Chúng tôi mua trái cây tươi ở chợ."),
    ("Bier", "das", "die Biere", "/biːɐ̯/", "Noun", "A1", "Bia", "Beer", "Ein kühles Bier schmeckt am Feierabend.", "Một cốc bia mát lạnh thật ngon sau giờ làm."),
    ("Salz", "das", "die Salze", "/zalt͡s/", "Noun", "A1", "Muối", "Salt", "Geben Sie bitte etwas Salz dazu.", "Làm ơn cho thêm chút muối."),
    ("Haus", "das", "die Häuser", "/haʊ̯s/", "Noun", "A1", "Ngôi nhà", "House", "Das Haus steht am Waldrand.", "Ngôi nhà nằm ở bìa rừng."),
    ("Zimmer", "das", "die Zimmer", "/ˈt͡sɪmɐ/", "Noun", "A1", "Căn phòng", "Room", "Das Zimmer ist hell und ruhig.", "Căn phòng sáng sủa và yên tĩnh."),
    ("Fenster", "das", "die Fenster", "/ˈfɛnstɐ/", "Noun", "A1", "Cửa sổ", "Window", "Mach bitte das Fenster auf.", "Làm ơn mở cửa sổ ra."),
    ("Bett", "das", "die Betten", "/bɛt/", "Noun", "A1", "Chiếc giường", "Bed", "Das Bett ist sehr bequem.", "Chiếc giường rất êm ái."),
    ("Bild", "das", "die Bilder", "/bɪlt/", "Noun", "A1", "Bức tranh, ảnh", "Picture", "Das Bild hängt an der Wand.", "Bức tranh treo trên tường."),
    ("Auto", "das", "die Autos", "/ˈaʊ̯to/", "Noun", "A1", "Xe ô tô", "Car", "Das Auto fährt sehr schnell.", "Chiếc xe ô tô chạy rất nhanh."),
    ("Fahrrad", "das", "die Fahrräder", "/ˈfaːɐ̯ˌʁaːt/", "Noun", "A1", "Xe đạp", "Bicycle", "Ich fahre gerne mit dem Fahrrad.", "Tôi thích đi bằng xe đạp."),
    ("Flugzeug", "das", "die Flugzeuge", "/ˈfluːkˌt͡sɔɪ̯k/", "Noun", "A1", "Máy bay", "Airplane", "Das Flugzeug fliegt nach Frankfurt.", "Máy bay bay đến Frankfurt."),
    ("Kind", "das", "die Kinder", "/kɪnt/", "Noun", "A1", "Đứa trẻ, con cái", "Child", "Das Kind lacht fröhlich.", "Đứa trẻ cười vui vẻ."),
    ("Mädchen", "das", "die Mädchen", "/ˈmɛːtçn̩/", "Noun", "A1", "Bé gái, cô gái nhỏ", "Girl", "Das Mädchen liest eine Geschichte.", "Cô bé đang đọc một câu chuyện."),
    ("Baby", "das", "die Babys", "/ˈbeːbi/", "Noun", "A1", "Em bé", "Baby", "Das Baby schläft ruhig.", "Em bé đang ngủ say."),
    ("Jahr", "das", "die Jahre", "/jaːɐ̯/", "Noun", "A1", "Năm", "Year", "Ein Jahr hat zwölf Monate.", "Một năm có mười hai tháng."),
    ("Geld", "das", "die Gelder", "/ɡɛlt/", "Noun", "A1", "Tiền", "Money", "Haben Sie genug Geld dabei?", "Bạn có mang theo đủ tiền không?"),
    ("Wetter", "das", "die Wetter", "/ˈvɛtɐ/", "Noun", "A1", "Thời tiết", "Weather", "Das Wetter ist heute herrlich.", "Thời tiết hôm nay thật tuyệt."),
    ("Telefon", "das", "die Telefone", "/teleˈfoːn/", "Noun", "A1", "Điện thoại", "Telephone", "Das Telefon klingelt schon wieder.", "Điện thoại lại reo rồi."),
    ("Handy", "das", "die Handys", "/ˈhɛndi/", "Noun", "A1", "Điện thoại di động", "Mobile phone", "Mein Handy hat keinen Akku mehr.", "Điện thoại của tôi hết pin rồi."),
    ("Glas", "das", "die Gläser", "/ɡlaːs/", "Noun", "A1", "Cái ly, thủy tinh", "Glass", "Ein Glas Orangensaft bitte.", "Cho tôi một ly nước cam."),
    ("Hotel", "das", "die Hotels", "/hoˈtɛl/", "Noun", "A1", "Khách sạn", "Hotel", "Das Hotel liegt im Stadtzentrum.", "Khách sạn nằm ở trung tâm thành phố."),
    ("Restaurant", "das", "die Restaurants", "/ʁɛstoˈʁɑ̃ː/", "Noun", "A1", "Nhà hàng", "Restaurant", "Wir essen heute im Restaurant.", "Hôm nay chúng tôi ăn ở nhà hàng."),
    ("Café", "das", "die Cafés", "/kaˈfeː/", "Noun", "A1", "Quán cà phê", "Café", "Treffen wir uns im Café?", "Chúng ta gặp nhau ở quán cà phê nhé?"),
]

# We expand through systemic high-frequency linguistic patterns across CEFR levels
LEVELS_DISTRIBUTION = [
    ("A1", 200),
    ("A2", 250),
    ("B1", 250),
    ("B2", 150),
    ("C1", 100),
    ("C2", 50),
]

print("Script template ready.")

