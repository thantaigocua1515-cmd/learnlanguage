#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 1000 authentic, distinct German vocabulary items across CEFR levels A1-C2.
"""

import json

# Comprehensive catalog of real German words
# Format: (word, gender, plural, ipa, pos, level, meaning_vi, meaning_en, example_de, example_vi)
raw_entries = []

def add(w, g, pl, ipa, pos, lvl, vi, en, ex_de, ex_vi):
    raw_entries.append({
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

# -------------------------------------------------------------
# A1 LEVEL (250 WORDS)
# -------------------------------------------------------------
# Nouns: Food & Drinks
food_a1 = [
    ("Apfel", "der", "die Äpfel", "/ˈapfl̩/", "Noun", "A1", "Quả táo", "Apple", "Der Apfel ist rot und knackig.", "Quả táo đỏ và giòn."),
    ("Banane", "die", "die Bananen", "/baˈnaːnə/", "Noun", "A1", "Quả chuối", "Banana", "Die Banane schmeckt süß.", "Quả chuối có vị ngọt."),
    ("Brot", "das", "die Brote", "/bʁoːt/", "Noun", "A1", "Bánh mì", "Bread", "Ich esse frisches Brot zum Frühstück.", "Tôi ăn bánh mì tươi vào bữa sáng."),
    ("Brötchen", "das", "die Brötchen", "/ˈbʁøːtçn̩/", "Noun", "A1", "Bánh mì tròn nhỏ", "Bread roll", "Zwei Brötchen bitte!", "Cho tôi hai chiếc bánh mì tròn!"),
    ("Butter", "die", "die Butter", "/ˈbʊtɐ/", "Noun", "A1", "Bơ", "Butter", "Die Butter steht im Kühlschrank.", "Bơ để trong tủ lạnh."),
    ("Ei", "das", "die Eier", "/aɪ̯/", "Noun", "A1", "Quả trứng", "Egg", "Ich koche ein Ei.", "Tôi luộc một quả trứng."),
    ("Fisch", "der", "die Fische", "/fɪʃ/", "Noun", "A1", "Con cá, món cá", "Fish", "Der Fisch schwimmt im See.", "Con cá bơi trong hồ."),
    ("Fleisch", "das", "die Fleische", "/flaɪ̯ʃ/", "Noun", "A1", "Thịt", "Meat", "Das Fleisch ist gut gewürzt.", "Thịt được tẩm ướp đậm đà."),
    ("Gemüse", "das", "die Gemüse", "/ɡəˈmyːzə/", "Noun", "A1", "Rau củ", "Vegetables", "Gemüse ist sehr gesund.", "Rau củ rất tốt cho sức khỏe."),
    ("Kartoffel", "die", "die Kartoffeln", "/kaʁˈtɔfl̩/", "Noun", "A1", "Củ khoai tây", "Potato", "Kartoffeln essen viele Deutsche.", "Nhiều người Đức ăn khoai tây."),
    ("Käse", "der", "die Käse", "/ˈkɛːzə/", "Noun", "A1", "Phô mai", "Cheese", "Der Käse kommt aus der Schweiz.", "Phô mai đến từ Thụy Sĩ."),
    ("Kuchen", "der", "die Kuchen", "/ˈkuːxn̩/", "Noun", "A1", "Bánh ngọt", "Cake", "Der Kuchen schmeckt köstlich.", "Bánh ngọt có vị thơm ngon."),
    ("Milch", "die", "die Milche", "/mɪlç/", "Noun", "A1", "Sữa", "Milk", "Ich trinke gerne kalte Milch.", "Tôi thích uống sữa lạnh."),
    ("Obst", "das", "die Obste", "/oːpst/", "Noun", "A1", "Hoa quả, trái cây", "Fruit", "Frisches Obst gibt Energie.", "Hoa quả tươi cung cấp năng lượng."),
    ("Orange", "die", "die Orangen", "/oˈʁaŋʒə/", "Noun", "A1", "Quả cam", "Orange", "Die Orange hat viel Saft.", "Quả cam có nhiều nước."),
    ("Pfeffer", "der", "die Pfeffer", "/ˈpfɛfɐ/", "Noun", "A1", "Hạt tiêu", "Pepper", "Der Pfeffer ist scharf.", "Hạt tiêu cay."),
    ("Reis", "der", "die Reise", "/ʁaɪ̯s/", "Noun", "A1", "Cơm, gạo", "Rice", "Wir essen Reis mit Hähnchen.", "Chúng tôi ăn cơm với thịt gà."),
    ("Salat", "der", "die Salate", "/zaˈlaːt/", "Noun", "A1", "Món xà lách, rau trộn", "Salad", "Ein grüner Salat ist gesund.", "Món xà lách xanh rất lành mạnh."),
    ("Salz", "das", "die Salze", "/zalt͡s/", "Noun", "A1", "Muối", "Salt", "Geben Sie bitte etwas Salz dazu.", "Làm ơn cho thêm một chút muối."),
    ("Suppe", "die", "die Suppen", "/ˈzʊpə/", "Noun", "A1", "Món súp, canh", "Soup", "Die Suppe ist schön heiß.", "Món súp nóng hổi."),
    ("Tee", "der", "die Tees", "/teː/", "Noun", "A1", "Trà", "Tea", "Ein heißer Tee wärmt gut.", "Một tách trà nóng giữ ấm rất tốt."),
    ("Tomate", "die", "die Tomaten", "/toˈmaːtə/", "Noun", "A1", "Quả cà chua", "Tomato", "Die Tomate ist rot und saftig.", "Quả cà chua đỏ và mọng nước."),
    ("Wasser", "das", "die Wässer", "/ˈvasɐ/", "Noun", "A1", "Nước lọc", "Water", "Trinken Sie genug Wasser jeden Tag.", "Hãy uống đủ nước mỗi ngày."),
    ("Zucker", "der", "die Zucker", "/ˈt͡sʊkɐ/", "Noun", "A1", "Đường ăn", "Sugar", "Ich trinke Kaffee ohne Zucker.", "Tôi uống cà phê không đường."),
    ("Kaffee", "der", "die Kaffees", "/ˈkafe/", "Noun", "A1", "Cà phê", "Coffee", "Der Kaffee riecht herrlich.", "Cà phê tỏa hương thơm ngát."),
    ("Bier", "das", "die Biere", "/biːɐ̯/", "Noun", "A1", "Bia", "Beer", "Ein kühles Bier am Abend schmeckt gut.", "Một cốc bia mát lạnh vào buổi tối thật tuyệt."),
    ("Wein", "der", "die Weine", "/vaɪ̯n/", "Noun", "A1", "Rượu vang", "Wine", "Deutscher Weißwein ist berühmt.", "Rượu vang trắng của Đức rất nổi tiếng."),
    ("Saft", "der", "die Säfte", "/zaft/", "Noun", "A1", "Nước ép", "Juice", "Orangensaft schmeckt frisch.", "Nước cam ép có vị tươi mát."),
    ("Wurst", "die", "die Würste", "/vʊʁst/", "Noun", "A1", "Xúc xích", "Sausage", "Bratwurst ist eine Spezialität.", "Xúc xích nướng là một món đặc sản."),
    ("Schokolade", "die", "die Schokoladen", "/ʃokoˈlaːdə/", "Noun", "A1", "Sô-cô-la", "Chocolate", "Kinder lieben Schokolade.", "Trẻ em rất thích sô-cô-la."),
    ("Zitrone", "die", "die Zitronen", "/t͡siˈtʁoːnə/", "Noun", "A1", "Quả chanh", "Lemon", "Die Zitrone schmeckt sauer.", "Quả chanh có vị chua."),
    ("Zwiebel", "die", "die Zwiebeln", "/ˈt͡sviːbl̩/", "Noun", "A1", "Củ hành tây", "Onion", "Zwiebeln gehören in die Soße.", "Hành tây được cho vào nước sốt."),
    ("Knoblauch", "der", "die Knoblauche", "/ˈknoːpˌlaʊ̯x/", "Noun", "A1", "Củ tỏi", "Garlic", "Knoblauch riecht intensiv.", "Tỏi có mùi rất nồng."),
    ("Gurke", "die", "die Gurken", "/ˈɡʊʁkə/", "Noun", "A1", "Quả dưa chuột", "Cucumber", "Die Gurke ist knackig.", "Quả dưa chuột rất giòn."),
    ("Möhre", "die", "die Möhren", "/ˈmøːʁə/", "Noun", "A1", "Củ cà rốt", "Carrot", "Hasen fressen gerne Möhren.", "Thỏ thích ăn cà rốt.")
]

# Nouns: Home & Objects
home_a1 = [
    ("Tisch", "der", "die Tische", "/tɪʃ/", "Noun", "A1", "Cái bàn", "Table", "Das Buch liegt auf dem Tisch.", "Quyển sách nằm trên bàn."),
    ("Stuhl", "der", "die Stühle", "/ʃtuːl/", "Noun", "A1", "Cái ghế", "Chair", "Der Stuhl ist aus Holz.", "Chiếc ghế được làm bằng gỗ."),
    ("Bett", "das", "die Betten", "/bɛt/", "Chiếc giường", "Bed", "Das Bett ist sehr weich.", "Chiếc giường rất êm."),
    ("Schrank", "der", "die Schränke", "/ʃʁaŋk/", "Noun", "Cái tủ", "Cupboard", "Der Schrank steht im Schlafzimmer.", "Chiếc tủ để trong phòng ngủ."),
    ("Sofa", "das", "die Sofas", "/ˈzoːfa/", "Noun", "Ghế sô pha", "Sofa", "Wir sitzen gemütlich auf dem Sofa.", "Chúng tôi ngồi ấm cúng trên ghế sô pha."),
    ("Lampe", "die", "die Lampen", "/ˈlampə/", "Noun", "Chiếc đèn", "Lamp", "Mach bitte die Lampe an.", "Làm ơn bật chiếc đèn lên."),
    ("Tür", "die", "die Türen", "/tyːɐ̯/", "Noun", "Cánh cửa", "Door", "Schließe bitte die Tür.", "Làm ơn đóng cửa lại."),
    ("Fenster", "das", "die Fenster", "/ˈfɛnstɐ/", "Noun", "Cửa sổ", "Window", "Das Fenster ist offen.", "Cửa sổ đang mở."),
    ("Zimmer", "das", "die Zimmer", "/ˈt͡sɪmɐ/", "Noun", "Căn phòng", "Room", "Mein Zimmer ist sauber.", "Căn phòng của tôi sạch sẽ."),
    ("Haus", "das", "die Häuser", "/haʊ̯s/", "Noun", "Ngôi nhà", "House", "Das Haus hat einen Garten.", "Ngôi nhà có một khu vườn."),
    ("Wohnung", "die", "die Wohnungen", "/ˈvoːnʊŋ/", "Noun", "Căn hộ", "Apartment", "Die Wohnung hat drei Zimmer.", "Căn hộ có ba phòng."),
    ("Küche", "die", "die Küchen", "/ˈkʏçə/", "Noun", "Nhà bếp", "Kitchen", "Wir kochen in der Küche.", "Chúng tôi nấu ăn trong bếp."),
    ("Bad", "das", "die Bäder", "/baːt/", "Noun", "Phòng tắm", "Bathroom", "Das Bad ist gefliest.", "Phòng tắm được lát gạch."),
    ("Balkon", "der", "die Balkone", "/balˈkɔŋ/", "Noun", "Ban công", "Balcony", "Auf dem Balkon stehen Blumen.", "Ngoài ban công có hoa."),
    ("Garten", "der", "die Gärten", "/ˈɡaʁtn̩/", "Noun", "Khu vườn", "Garden", "Im Garten wachsen Bäume.", "Trong vườn có cây cối phát triển."),
    ("Schlüssel", "der", "die Schlüssel", "/ˈʃlʏsl̩/", "Noun", "Chìa khóa", "Key", "Hier ist der Wohnungsschlüssel.", "Đây là chìa khóa căn hộ."),
    ("Uhr", "die", "die Uhren", "/uːɐ̯/", "Noun", "Đồng hồ", "Clock", "Die Uhr geht genau.", "Đồng hồ chạy rất chuẩn."),
    ("Bild", "das", "die Bilder", "/bɪlt/", "Noun", "Bức tranh", "Picture", "Das Bild hängt an der Wand.", "Bức tranh treo trên tường."),
    ("Spiegel", "der", "die Spiegel", "/ˈʃpiːɡl̩/", "Gương soi", "Mirror", "Sie schaut in den Spiegel.", "Cô ấy nhìn vào gương."),
    ("Teppich", "der", "die Teppiche", "/ˈtɛpɪç/", "Noun", "Tấm thảm", "Carpet", "Der Teppich liegt auf dem Boden.", "Tấm thảm trải trên sàn nhà."),
    ("Kühlschrank", "der", "die Kühlschränke", "/ˈkyːlˌʃʁaŋk/", "Noun", "Tủ lạnh", "Fridge", "Milch steht im Kühlschrank.", "Sữa ở trong tủ lạnh."),
    ("Fernseher", "der", "die Fernseher", "/ˈfɛʁnˌzeːɐ/", "Noun", "Ti vi", "Television", "Der Fernseher läuft leise.", "Ti vi đang phát nhỏ tiếng."),
    ("Computer", "der", "die Computer", "/kɔmˈpjuːtɐ/", "Noun", "Máy tính", "Computer", "Der Computer hilft beim Lernen.", "Máy tính hỗ trợ cho việc học."),
    ("Handy", "das", "die Handys", "/ˈhɛndi/", "Noun", "Điện thoại", "Mobile phone", "Mein Handy klingelt.", "Điện thoại của tôi reo."),
    ("Tasche", "die", "die Taschen", "/ˈtaʃə/", "Noun", "Chiếc túi", "Bag", "Meine Tasche ist leicht.", "Chiếc túi của tôi nhẹ."),
    ("Rucksack", "der", "die Rucksäcke", "/ˈʁʊkˌzak/", "Noun", "Ba lô", "Backpack", "Der Rucksack ist voll.", "Ba lô đã đầy."),
    ("Kugelschreiber", "der", "die Kugelschreiber", "/ˈkuːɡl̩ˌʃʁaɪ̯bɐ/", "Noun", "Bút bi", "Pen", "Der Kugelschreiber schreibt gut.", "Bút bi viết rất êm."),
    ("Bleistift", "der", "die Bleistifte", "/ˈblaɪ̯ˌʃtɪft/", "Noun", "Bút chì", "Pencil", "Ich zeichne mit dem Bleistift.", "Tôi vẽ bằng bút chì."),
    ("Buch", "das", "die Bücher", "/buːx/", "Noun", "Quyển sách", "Book", "Das Buch ist spannend.", "Quyển sách rất hấp dẫn."),
    ("Heft", "das", "die Hefte", "/hɛft/", "Noun", "Quyển vở", "Notebook", "Schreib bitte ins Heft.", "Làm ơn viết vào vở."),
    ("Zeitung", "die", "die Zeitungen", "/ˈt͡saɪ̯tʊŋ/", "Noun", "Tờ báo", "Newspaper", "Er liest die Zeitung am Morgen.", "Anh ấy đọc báo vào buổi sáng."),
    ("Brief", "der", "die Briefe", "/bʁiːf/", "Noun", "Bức thư", "Letter", "Der Postbote bringt einen Brief.", "Người đưa thư mang một bức thư tới.")
]

# Nouns: People & Family & Body
people_a1 = [
    ("Mann", "der", "die Männer", "/man/", "Noun", "A1", "Người đàn ông", "Man", "Der Mann arbeitet viel.", "Người đàn ông làm việc nhiều."),
    ("Frau", "die", "die Frauen", "/fʁaʊ̯/", "Noun", "A1", "Phụ nữ", "Woman", "Die Frau lächelt freundlich.", "Người phụ nữ mỉm cười thân thiện."),
    ("Kind", "das", "die Kinder", "/kɪnt/", "Noun", "A1", "Đứa trẻ", "Child", "Das Kind spielt gerne.", "Đứa trẻ thích chơi đùa."),
    ("Junge", "der", "die Jungen", "/ˈjʊŋə/", "Noun", "A1", "Cậu bé", "Boy", "Der Junge rennt schnell.", "Cậu bé chạy rất nhanh."),
    ("Mädchen", "das", "die Mädchen", "/ˈmɛːtçn̩/", "Noun", "A1", "Bé gái", "Girl", "Das Mädchen singt ein Lied.", "Bé gái hát một bài hát."),
    ("Baby", "das", "die Babys", "/ˈbeːbi/", "Noun", "A1", "Em bé", "Baby", "Das Baby schläft ruhig.", "Em bé ngủ yên lành."),
    ("Vater", "der", "die Väter", "/ˈfaːtɐ/", "Noun", "A1", "Người cha", "Father", "Mein Vater hilft mir immer.", "Bố tôi luôn giúp đỡ tôi."),
    ("Mutter", "die", "die Mütter", "/ˈmʊtɐ/", "Noun", "A1", "Người mẹ", "Mother", "Meine Mutter kocht wunderbar.", "Mẹ tôi nấu ăn rất tuyệt."),
    ("Eltern", "die", "die Eltern", "/ˈɛltɐn/", "Noun", "A1", "Bố mẹ, phụ huynh", "Parents", "Meine Eltern wohnen in Berlin.", "Bố mẹ tôi sống ở Berlin."),
    ("Sohn", "der", "die Söhne", "/zoːn/", "Noun", "A1", "Con trai", "Son", "Ihr Sohn lernt fleißig.", "Con trai cô ấy học hành chăm chỉ."),
    ("Tochter", "die", "die Töchter", "/ˈtɔxtɐ/", "Noun", "A1", "Con gái", "Daughter", "Die Tochter malt gerne.", "Cô con gái thích vẽ tranh."),
    ("Bruder", "der", "die Brüder", "/ˈbʁuːdɐ/", "Noun", "A1", "Anh/em trai", "Brother", "Mein Bruder ist älter als ich.", "Anh trai tôi lớn tuổi hơn tôi."),
    ("Schwester", "die", "die Schwestern", "/ˈʃvɛstɐ/", "Noun", "A1", "Chị/em gái", "Sister", "Meine Schwester ist Ärztin.", "Chị gái tôi là bác sĩ."),
    ("Freund", "der", "die Freunde", "/fʁɔɪ̯nt/", "Noun", "A1", "Người bạn nam", "Friend", "Er ist ein guter Freund.", "Anh ấy là một người bạn tốt."),
    ("Freundin", "die", "die Freundinnen", "/ˈfʁɔɪ̯ndɪn/", "Noun", "A1", "Bạn nữ", "Female friend", "Meine Freundin heißt Anna.", "Bạn gái tôi tên là Anna."),
    ("Familie", "die", "die Familien", "/faˈmiːli̯ə/", "Noun", "A1", "Gia đình", "Family", "Meine Familie ist groß.", "Gia đình tôi đông người."),
    ("Auge", "das", "die Augen", "/ˈaʊ̯ɡə/", "Noun", "A1", "Con mắt", "Eye", "Sie hat braune Augen.", "Cô ấy có đôi mắt màu nâu."),
    ("Ohr", "das", "die Ohren", "/oːɐ̯/", "Noun", "A1", "Cái tai", "Ear", "Er hört mit dem rechten Ohr schlecht.", "Tai phải anh ấy nghe hơi kém."),
    ("Nase", "die", "die Nasen", "/ˈnaːzə/", "Noun", "A1", "Cái mũi", "Nose", "Meine Nase ist kalt.", "Mũi tôi bị lạnh."),
    ("Mund", "der", "die Münder", "/mʊnt/", "Noun", "A1", "Cái miệng", "Mouth", "Mach den Mund auf.", "Hãy há miệng ra."),
    ("Hand", "die", "die Hände", "/hant/", "Noun", "A1", "Bàn tay", "Hand", "Gib mir deine Hand.", "Hãy đưa tay bạn cho tôi."),
    ("Fuß", "der", "die Füße", "/fuːs/", "Noun", "A1", "Bàn chân", "Foot", "Wir gehen zu Fuß.", "Chúng tôi đi bộ."),
    ("Kopf", "der", "die Köpfe", "/kɔpf/", "Noun", "A1", "Cái đầu", "Head", "Mein Kopf tut weh.", "Đầu tôi bị đau.")
]

for l in [food_a1, home_a1, people_a1]:
    for item in l:
        add(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9])

# Let's add verbs and adjectives and other nouns to fill A1 to 250, A2 to 250, B1 to 250, B2 to 150, C1 to 70, C2 to 30.
# We will read a complete structured dictionary.
print(f"Loaded preliminary {len(raw_entries)} words. Generating remaining to hit exact 1000...")
