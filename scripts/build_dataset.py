#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compile a rich, authentic dataset of 1000 German vocabulary items.
CEFR distribution:
- A1: 250 words
- A2: 250 words
- B1: 250 words
- B2: 150 words
- C1: 70 words
- C2: 30 words
Total: 1000 words
"""

import json

entries = []
seen = set()

def item(word, gender, plural, ipa, pos, lvl, vi, en, ex_de, ex_vi):
    if word in seen:
        return
    seen.add(word)
    entries.append({
        "word": word,
        "gender": gender,
        "plural_form": plural,
        "ipa": ipa,
        "pos": pos,
        "cefr_level": lvl,
        "meaning_vi": vi,
        "meaning_en": en,
        "example_de": ex_de,
        "example_vi": ex_vi
    })

# ==========================================
# 1. A1 LEVEL (250 WORDS)
# ==========================================
# Der nouns (60)
der_a1 = [
    ("Apfel", "die Äpfel", "/ˈapfl̩/", "Quả táo", "Apple", "Der Apfel schmeckt süß und saftig.", "Quả táo có vị ngọt và mọng nước."),
    ("Tisch", "die Tische", "/tɪʃ/", "Cái bàn", "Table", "Das Buch liegt auf dem Tisch.", "Quyển sách nằm trên bàn."),
    ("Stuhl", "die Stühle", "/ʃtuːl/", "Cái ghế", "Chair", "Der Stuhl ist sehr bequem.", "Chiếc ghế rất thoải mái."),
    ("Hund", "die Hunde", "/hʊnt/", "Con chó", "Dog", "Der Hund läuft im Garten herum.", "Con chó chạy quanh vườn."),
    ("Kaffee", "die Kaffees", "/ˈkafe/", "Cà phê", "Coffee", "Ich trinke morgens schwarzen Kaffee.", "Buổi sáng tôi uống cà phê đen."),
    ("Tee", "die Tees", "/teː/", "Trà", "Tea", "Eine Tasse heißer Tee wärmt gut.", "Một tách trà nóng giữ ấm rất tốt."),
    ("Käse", "die Käse", "/ˈkɛːzə/", "Phô mai", "Cheese", "Der Käse schmeckt sehr würzig.", "Phô mai có vị béo đậm đà."),
    ("Kuchen", "die Kuchen", "/ˈkuːxn̩/", "Bánh ngọt", "Cake", "Der Kuchen wurde frisch gebacken.", "Chiếc bánh ngọt vừa được nướng mới."),
    ("Zucker", "die Zucker", "/ˈt͡sʊkɐ/", "Đường", "Sugar", "Ich nehme Zucker in meinen Kaffee.", "Tôi cho đường vào cà phê."),
    ("Pfeffer", "die Pfeffer", "/ˈpfɛfɐ/", "Hạt tiêu", "Pepper", "Der schwarze Pfeffer ist sehr scharf.", "Hạt tiêu đen rất cay."),
    ("Reis", "die Reise", "/ʁaɪ̯s/", "Cơm, gạo", "Rice", "In Asien essen viele Menschen Reis.", "Ở châu Á nhiều người ăn cơm."),
    ("Fisch", "die Fische", "/fɪʃ/", "Con cá", "Fish", "Der Fisch schwimmt munter im Fluss.", "Con cá bơi lội tung tăng dưới sông."),
    ("Salat", "die Salate", "/zaˈlaːt/", "Rau xà lách, món trộn", "Salad", "Der grüne Salat ist knackig und frisch.", "Món xà lách xanh tươi giòn."),
    ("Bruder", "die Brüder", "/ˈbʁuːdɐ/", "Anh/em trai", "Brother", "Mein Bruder wohnt und arbeitet in Köln.", "Anh trai tôi sống và làm việc ở Köln."),
    ("Vater", "die Väter", "/ˈfaːtɐ/", "Người cha", "Father", "Mein Vater liest abends gerne.", "Bố tôi thích đọc sách vào buổi tối."),
    ("Sohn", "die Söhne", "/zoːn/", "Con trai", "Son", "Ihr Sohn geht schon zur Schule.", "Con trai cô ấy đã đi học."),
    ("Freund", "die Freunde", "/fʁɔɪ̯nt/", "Bạn nam, bạn bè", "Friend", "Er ist mein bester Freund seit Jahren.", "Anh ấy là bạn thân nhất của tôi từ nhiều năm."),
    ("Mann", "die Männer", "/man/", "Đàn ông, người chồng", "Man / Husband", "Der Mann wartet vor dem Geschäft.", "Người đàn ông đang đứng đợi trước cửa hàng."),
    ("Junge", "die Jungen", "/ˈjʊŋə/", "Cậu bé", "Boy", "Der Junge spielt draußen Fußball.", "Cậu bé đang chơi đá bóng bên ngoài."),
    ("Tag", "die Tage", "/taːk/", "Ngày", "Day", "Ich wünsche dir einen schönen Tag!", "Tôi chúc bạn một ngày tốt lành!"),
    ("Morgen", "die Morgen", "/ˈmɔʁɡn̩/", "Buổi sáng", "Morning", "Am frühen Morgen ist es herrlich still.", "Vào sáng sớm không gian tĩnh lặng tuyệt vời."),
    ("Abend", "die Abende", "/ˈaːbn̩t/", "Buổi tối", "Evening", "Am Abend treffen wir uns im Restaurant.", "Buổi tối chúng ta gặp nhau ở nhà hàng."),
    ("Monat", "die Monate", "/ˈmoːnat/", "Tháng", "Month", "Der Monat Mai bringt schönes Wetter.", "Tháng Năm mang lại thời tiết đẹp."),
    ("Schlüssel", "die Schlüssel", "/ˈʃlʏsl̩/", "Chìa khóa", "Key", "Hast du meinen Schlüssel gesehen?", "Bạn có nhìn thấy chìa khóa của tôi đâu không?"),
    ("Kugelschreiber", "die Kugelschreiber", "/ˈkuːɡl̩ˌʃʁaɪ̯bɐ/", "Bút bi", "Pen", "Der Kugelschreiber schreibt sehr flüssig.", "Bút bi viết rất trơn tru."),
    ("Bleistift", "die Bleistifte", "/ˈblaɪ̯ˌʃtɪft/", "Bút chì", "Pencil", "Ich zeichne den Plan mit Bleistift.", "Tôi vẽ bản kế hoạch bằng bút chì."),
    ("Rucksack", "die Rucksäcke", "/ˈʁʊkˌzak/", "Ba lô", "Backpack", "Der Rucksack ist ziemlich schwer.", "Chiếc ba lô khá nặng."),
    ("Schrank", "die Schränke", "/ʃʁaŋk/", "Tủ đựng đồ", "Wardrobe", "Die Gläser stehen ordentlich im Schrank.", "Những chiếc ly xếp gọn gàng trong tủ."),
    ("Computer", "die Computer", "/kɔmˈpjuːtɐ/", "Máy vi tính", "Computer", "Mein neuer Computer läuft sehr schnell.", "Chiếc máy tính mới của tôi chạy rất nhanh."),
    ("Fernseher", "die Fernseher", "/ˈfɛʁnˌzeːɐ/", "Ti vi", "Television", "Der Fernseher steht im Wohnzimmer.", "Ti vi đặt trong phòng khách."),
    ("Kühlschrank", "die Kühlschränke", "/ˈkyːlˌʃʁaŋk/", "Tủ lạnh", "Fridge", "Die Milch steht kühl im Kühlschrank.", "Sữa để mát trong tủ lạnh."),
    ("Herd", "die Herde", "/heːɐ̯t/", "Bếp nấu", "Stove", "Die Suppe kocht auf dem heißen Herd.", "Nồi súp đang sôi trên bếp nóng."),
    ("Balkon", "der", "die Balkone", "/balˈkɔŋ/", "Ban công", "Balcony", "Wir trinken Kaffee auf dem Balkon.", "Chúng tôi uống cà phê ngoài ban công."),
    ("Garten", "die Gärten", "/ˈɡaʁtn̩/", "Khu vườn", "Garden", "Der Garten steht voller bunter Blumen.", "Khu vườn nở đầy hoa sặc sỡ."),
    ("Park", "die Parks", "/paʁk/", "Công viên", "Park", "Am Sonntag spazieren wir im Stadtpark.", "Chủ nhật chúng tôi đi dạo trong công viên thành phố."),
    ("Supermarkt", "die Supermärkte", "/ˈzuːpɐˌmaʁkt/", "Siêu thị", "Supermarket", "Ich kaufe im Supermarkt um die Ecke ein.", "Tôi mua đồ ở siêu thị ngay góc phố."),
    ("Markt", "die Märkte", "/maʁkt/", "Chợ", "Market", "Auf dem Markt gibt es frische Früchte.", "Ở chợ có bán hoa quả tươi."),
    ("Bahnhof", "die Bahnhöfe", "/ˈbaːnˌhoːf/", "Nhà ga xe lửa", "Train station", "Wir treffen uns pünktlich am Bahnhof.", "Chúng ta gặp nhau đúng giờ ở nhà ga."),
    ("Bus", "die Busse", "/bʊs/", "Xe buýt", "Bus", "Der Bus fährt alle zehn Minuten ab.", "Xe buýt khởi hành cứ 10 phút một chuyến."),
    ("Zug", "die Züge", "/t͡suːk/", "Tàu hỏa", "Train", "Der Zug nach München hat keine Verspätung.", "Chuyến tàu đi Munich không bị trễ."),
    ("Brief", "die Briefe", "/bʁiːf/", "Lá thư", "Letter", "Ich habe einen Brief aus Deutschland bekommen.", "Tôi đã nhận được một lá thư từ nước Đức."),
    ("Name", "die Namen", "/ˈnaːmə/", "Cái tên", "Name", "Wie lautet Ihr vollständiger Name?", "Tên đầy đủ của bạn là gì?"),
    ("Euro", "die Euros", "/ˈɔɪ̯ʁo/", "Đồng Euro", "Euro", "Das Buch kostet fünfzehn Euro.", "Cuốn sách này giá 15 Euro."),
    ("Preis", "die Preise", "/pʁaɪ̯s/", "Giá cả", "Price", "Der Preis für das Zimmer ist angemessen.", "Giá tiền cho căn phòng này rất hợp lý."),
    ("Termin", "die Termine", "/tɛʁˈmiːn/", "Cuộc hẹn", "Appointment", "Ich habe morgen einen Termin beim Arzt.", "Ngày mai tôi có cuộc hẹn với bác sĩ."),
    ("Urlaub", "die Urlaube", "/ˈuːɐ̯laʊ̯p/", "Kỳ nghỉ phép", "Vacation", "Im Sommer machen wir Urlaub am Meer.", "Mùa hè chúng tôi đi nghỉ mát ở biển."),
    ("Spaziergang", "die Spaziergänge", "/ʃpaˈt͡siːɐ̯ˌɡaŋ/", "Cuộc đi dạo", "Walk", "Ein Spaziergang an der Luft tut gut.", "Một chuyến đi dạo ngoài trời rất có ích."),
    ("Sport", "die Sporte", "/ʃpɔʁt/", "Thể thao", "Sport", "Sport hält den Körper fit und gesund.", "Thể thao giúp cơ thể cân đối và khỏe mạnh."),
    ("Fußball", "die Fußbälle", "/ˈfuːsˌbal/", "Môn bóng đá, quả bóng", "Football", "In Deutschland ist Fußball sehr beliebt.", "Ở Đức bóng đá rất được ưa chuộng."),
    ("Himmel", "die Himmel", "/ˈhɪml̩/", "Bầu trời", "Sky", "Die Sonne scheint am blauen Himmel.", "Mặt trời chiếu sáng trên bầu trời xanh."),
    ("Mond", "die Monde", "/moːnt/", "Mặt trăng", "Moon", "Der Mond leuchtet hell in der Nacht.", "Mặt trăng chiếu sáng rực rỡ trong đêm."),
    ("Stern", "die Sterne", "/ʃtɛʁn/", "Ngôi sao", "Star", "Wir zählen die Sterne am Nachthimmel.", "Chúng tôi đếm những vì sao trên bầu trời đêm."),
    ("Wald", "die Wälder", "/valt/", "Khu rừng", "Forest", "Der Wald riecht nach Moos und Holz.", "Khu rừng có mùi rêu và gỗ."),
    ("Berg", "die Berge", "/bɛʁk/", "Ngọn núi", "Mountain", "Wir wandern auf den höchsten Berg.", "Chúng tôi leo lên ngọn núi cao nhất."),
    ("See", "die Seen", "/zeː/", "Hồ nước", "Lake", "Das Wasser im See ist glasklar.", "Nước trong hồ trong vắt như pha lê."),
    ("Fluss", "die Flüsse", "/flʊs/", "Dòng sông", "River", "Der Fluss fließt durch die Stadtmitte.", "Dòng sông chảy qua trung tâm thành phố."),
    ("Baum", "die Bäume", "/baʊ̯m/", "Cái cây", "Tree", "Der alte Baum spendet angenehmen Schatten.", "Cây cổ thụ tỏa bóng râm mát mẻ."),
    ("Vogel", "die Vögel", "/ˈfoːɡl̩/", "Con chim", "Bird", "Der kleine Vogel sitzt auf dem Ast.", "Chú chim nhỏ đậu trên cành cây."),
    ("Wein", "die Weine", "/vaɪ̯n/", "Rượu vang", "Wine", "Ein Glas Rotwein zum Essen schmeckt prima.", "Một ly rượu vang đỏ dùng kèm bữa ăn rất ngon."),
    ("Saft", "die Säfte", "/zaft/", "Nước ép", "Juice", "Apfelsaft ist mein liebstes Getränk.", "Nước ép táo là đồ uống yêu thích nhất của tôi.")
]
for w, pl, ipa, vi, en, ex_de, ex_vi in der_a1:
    item(w, "der", pl, ipa, "Noun", "A1", vi, en, ex_de, ex_vi)

# Die nouns (60)
die_a1 = [
    ("Katze", "die Katzen", "/ˈkat͡sə/", "Con mèo", "Cat", "Die Katze schläft friedlich auf dem Sofa.", "Con mèo ngủ yên bình trên sô pha."),
    ("Sonne", "die Sonnen", "/ˈzɔnə/", "Mặt trời", "Sun", "Die warme Sonne scheint den ganzen Tag.", "Mặt trời ấm áp chiếu sáng cả ngày."),
    ("Blume", "die Blumen", "/ˈbluːmə/", "Bông hoa", "Flower", "Die rote Blume duftet herrlich.", "Bông hoa màu đỏ tỏa ngát hương thơm."),
    ("Milch", "die Milche", "/mɪlç/", "Sữa", "Milk", "Frische Milch steht im Kühlschrank.", "Sữa tươi để trong tủ lạnh."),
    ("Butter", "die Butter", "/ˈbʊtɐ/", "Bơ thực phẩm", "Butter", "Streichen Sie bitte etwas Butter aufs Brot.", "Làm ơn phết một ít bơ lên bánh mì."),
    ("Suppe", "die Suppen", "/ˈzʊpə/", "Món súp, canh", "Soup", "Die Hühnersuppe hilft gegen Erkältung.", "Món súp gà giúp trị cảm cúm."),
    ("Kartoffel", "die Kartoffeln", "/kaʁˈtɔfl̩/", "Củ khoai tây", "Potato", "Die Kartoffeln kochen im heißen Wasser.", "Khoai tây đang sôi trong nước nóng."),
    ("Tomate", "die Tomaten", "/toˈmaːtə/", "Quả cà chua", "Tomato", "Die Tomate ist rot und voller Geschmack.", "Quả cà chua đỏ mọng và đậm vị."),
    ("Orange", "die Orangen", "/oˈʁaŋʒə/", "Quả cam", "Orange", "Die Orange enthält viel gesundes Vitamin C.", "Quả cam chứa nhiều vitamin C tốt cho sức khỏe."),
    ("Banane", "die Bananen", "/baˈnaːnə/", "Quả chuối", "Banana", "Bananen liefern schnelle Energie beim Sport.", "Chuối cung cấp năng lượng nhanh chóng khi chơi thể thao."),
    ("Mutter", "die Mütter", "/ˈmʊtɐ/", "Người mẹ", "Mother", "Meine Mutter backt am Sonntag Kuchen.", "Mẹ tôi làm bánh ngọt vào chủ nhật."),
    ("Schwester", "die Schwestern", "/ˈʃvɛstɐ/", "Chị/em gái", "Sister", "Meine Schwester studiert Informatik.", "Em gái tôi học ngành công nghệ thông tin."),
    ("Tochter", "die Töchter", "/ˈtɔxtɐ/", "Con gái", "Daughter", "Die kleine Tochter spielt mit Puppen.", "Bé gái chơi đùa với những con búp bê."),
    ("Frau", "die Frauen", "/fʁaʊ̯/", "Phụ nữ, người vợ", "Woman / Wife", "Die Frau leitet das neue Projekt.", "Người phụ nữ đang lãnh đạo dự án mới."),
    ("Freundin", "die Freundinnen", "/ˈfʁɔɪ̯ndɪn/", "Bạn nữ", "Female friend", "Das ist meine beste Freundin Julia.", "Đây là Julia, bạn thân nhất của tôi."),
    ("Familie", "die Familien", "/faˈmiːli̯ə/", "Gia đình", "Family", "Meine Familie feiert zusammen Weihnachten.", "Gia đình tôi cùng nhau đón Giáng sinh."),
    ("Woche", "die Wochen", "/ˈvɔxə/", "Tuần lễ", "Week", "Eine Woche vergeht wie im Flug.", "Một tuần trôi qua nhanh như chớp mắt."),
    ("Nacht", "die Nächte", "/naxt/", "Ban đêm", "Night", "Gute Nacht und träum was Schönes!", "Chúc ngủ ngon và mơ giấc mơ đẹp!"),
    ("Uhr", "die Uhren", "/uːɐ̯/", "Đồng hồ, giờ giấc", "Clock", "Wie viel Uhr ist es jetzt genau?", "Bây giờ chính xác là mấy giờ rồi?"),
    ("Stadt", "die Städte", "/ʃtat/", "Thành phố", "City", "Berlin ist eine sehr lebendige Stadt.", "Berlin là một thành phố vô cùng sôi động."),
    ("Straße", "die Straßen", "/ˈʃtʁaːsə/", "Con đường, phố", "Street", "Die Straße führt direkt zum Marktplatz.", "Con đường dẫn thẳng tới quảng trường chợ."),
    ("Wohnung", "die Wohnungen", "/ˈvoːnʊŋ/", "Căn hộ", "Apartment", "Unsere Wohnung hat einen tollen Ausblick.", "Căn hộ của chúng tôi có tầm nhìn rất đẹp."),
    ("Küche", "die Küchen", "/ˈkʏçə/", "Nhà bếp", "Kitchen", "In der Küche kochen wir zusammen.", "Trong bếp chúng tôi cùng nhau nấu nướng."),
    ("Tür", "die Türen", "/tyːɐ̯/", "Cánh cửa", "Door", "Bitte schließen Sie die Tür leise.", "Làm ơn đóng cửa khẽ khàng."),
    ("Lampe", "die Lampen", "/ˈlampə/", "Chiếc đèn", "Lamp", "Die Lampe auf dem Tisch spendet Licht.", "Chiếc đèn trên bàn tỏa ra ánh sáng."),
    ("Tasche", "die Taschen", "/ˈtaʃə/", "Túi xách", "Bag", "Ich trage meine Tasche über der Schulter.", "Tôi đeo chiếc túi qua vai."),
    ("Flasche", "die Flaschen", "/ˈflaʃə/", "Chai, lọ", "Bottle", "Eine Flasche stilles Wasser bitte.", "Cho tôi một chai nước lọc không ga."),
    ("Tasse", "die Tassen", "/ˈtasə/", "Tách, chén", "Cup", "Eine Tasse warmer Kaffee weckt die Sinne.", "Một tách cà phê ấm đánh thức các giác quan."),
    ("Zeitung", "die Zeitungen", "/ˈt͡saɪ̯tʊŋ/", "Tờ báo", "Newspaper", "Er liest die Zeitung auf dem Weg zur Arbeit.", "Anh ấy đọc báo trên đường đi làm."),
    ("Schule", "die Schulen", "/ˈʃuːlə/", "Trường học", "School", "Die Schule beginnt um acht Uhr morgens.", "Trường học bắt đầu lúc 8 giờ sáng."),
    ("Arbeit", "die Arbeiten", "/ˈaʁbaɪ̯t/", "Công việc", "Work", "Die Arbeit im Team macht großen Spaß.", "Làm việc theo nhóm mang lại niềm vui lớn."),
    ("Pause", "die Pausen", "/ˈpaʊ̯zə/", "Giờ nghỉ giải lao", "Break", "In der Pause trinken wir Kaffee.", "Trong giờ nghỉ chúng tôi uống cà phê."),
    ("Frage", "die Fragen", "/ˈfʁaːɡə/", "Câu hỏi", "Question", "Darf ich Ihnen eine kurze Frage stellen?", "Tôi có thể đặt cho bạn một câu hỏi ngắn không?"),
    ("Antwort", "die Antworten", "/ˈantvɔʁt/", "Câu trả lời", "Answer", "Die Antwort war völlig verständlich.", "Câu trả lời hoàn toàn dễ hiểu."),
    ("Musik", "die Musiken", "/muˈziːk/", "Âm nhạc", "Music", "Musik entspannt Körper und Geist.", "Âm nhạc giúp thư giãn thể chất và tâm hồn."),
    ("Sprache", "die Sprachen", "/ˈʃpʁaːxə/", "Ngôn ngữ", "Language", "Deutsch ist eine ausdrucksstarke Sprache.", "Tiếng Đức là một ngôn ngữ giàu sức biểu cảm."),
    ("Farbe", "die Farben", "/ˈfaʁbə/", "Màu sắc", "Color", "Welche Farbe gefällt dir am besten?", "Bạn thích màu sắc nào nhất?"),
    ("Nummer", "die Nummern", "/ˈnʊmɐ/", "Số, con số", "Number", "Geben Sie bitte Ihre Telefonnummer an.", "Làm ơn cung cấp số điện thoại của bạn."),
    ("Rechnung", "die Rechnungen", "/ˈʁɛçnʊŋ/", "Hóa đơn", "Bill", "Bringen Sie uns bitte die Rechnung.", "Làm ơn mang hóa đơn cho chúng tôi."),
    ("Post", "die Posten", "/pɔst/", "Bưu điện", "Post office", "Ich bringe das Paket zur Post.", "Tôi mang kiện hàng ra bưu điện."),
    ("Bank", "die Banken", "/baŋk/", "Ngân hàng, ghế băng", "Bank", "Das Geld liegt sicher auf der Bank.", "Tiền bạc gửi an toàn trong ngân hàng."),
    ("Apotheke", "die Apotheken", "/apoˈteːkə/", "Hiệu thuốc", "Pharmacy", "In der Apotheke kaufe ich Schmerzmittel.", "Ở hiệu thuốc tôi mua thuốc giảm đau."),
    ("Bäckerei", "die Bäckereien", "/bɛkəˈʁaɪ̯/", "Tiệm bánh mì", "Bakery", "Die Bäckerei backt frische Brötchen.", "Tiệm bánh nướng những ổ bánh mì tròn nóng hổi."),
    ("Kirche", "die Kirchen", "/ˈkɪʁçə/", "Nhà thờ", "Church", "Die alte Kirche steht mitten im Dorf.", "Nhà thờ cổ kính nằm giữa làng."),
    ("Kreuzung", "die Kreuzungen", "/ˈkʁɔɪ̯t͡sʊŋ/", "Ngã tư đường", "Intersection", "Biegen Sie an der Kreuzung rechts ab.", "Hãy rẽ phải tại ngã tư đường."),
    ("Ampel", "die Ampeln", "/ˈampl̩/", "Đèn giao thông", "Traffic light", "Die Ampel schaltet auf Grün um.", "Đèn giao thông chuyển sang màu xanh."),
    ("Haltestelle", "die Haltestellen", "/ˈhaltəˌʃtɛlə/", "Trạm dừng xe", "Stop", "Der Bus hält an dieser Haltestelle.", "Xe buýt dừng ở trạm này."),
    ("Fahrkarte", "die Fahrkarten", "/ˈfaːɐ̯ˌkaʁtə/", "Vé tàu xe", "Ticket", "Ich kaufe eine Fahrkarte am Automaten.", "Tôi mua vé tàu xe tại máy bán tự động."),
    ("Wand", "die Wände", "/vant/", "Bức tường", "Wall", "Das Foto hängt an der weißen Wand.", "Bức ảnh treo trên bức tường màu trắng."),
    ("Decke", "die Decken", "/ˈdɛkə/", "Trần nhà, cái chăn", "Ceiling / Blanket", "Die Decke im Schlafzimmer ist hoch.", "Trần phòng ngủ rất cao."),
    ("Heizung", "die Heizungen", "/ˈhaɪ̯t͡sʊŋ/", "Hệ thống sưởi", "Heating", "Im kalten Winter drehen wir die Heizung auf.", "Vào mùa đông lạnh chúng tôi bật lò sưởi."),
    ("Klasse", "die Klassen", "/ˈklasə/", "Lớp học", "Class", "Unsere Klasse besteht aus zwanzig Schülern.", "Lớp chúng tôi gồm hai mươi học sinh."),
    ("Prüfung", "die Prüfungen", "/ˈpʁyːfʊŋ/", "Kỳ thi, bài kiểm tra", "Exam", "Ich bereite mich auf die A1-Prüfung vor.", "Tôi đang chuẩn bị cho kỳ thi A1."),
    ("Übung", "die Übungen", "/ˈyːbʊŋ/", "Bài tập rèn luyện", "Exercise", "Übung macht bekanntlich den Meister.", "Có công mài sắt có ngày nên kim."),
    ("Hausaufgabe", "die Hausaufgaben", "/ˈhaʊ̯sˌaʊ̯fɡaːbə/", "Bài tập về nhà", "Homework", "Die Hausaufgabe war nicht allzu schwer.", "Bài tập về nhà không quá khó."),
    ("Sache", "die Sachen", "/ˈzaxə/", "Đồ vật, sự việc", "Thing", "Packe bitte deine Sachen zusammen.", "Làm ơn thu dọn đồ đạc của bạn lại."),
    ("Welt", "die Welten", "/vɛlt/", "Thế giới", "World", "Die Welt ist voller wunderbarer Orte.", "Thế giới có muôn vàn địa điểm kỳ thú."),
    ("Natur", "die Naturen", "/naˈtuːɐ̯/", "Thiên nhiên", "Nature", "Wir verbringen den Tag draußen in der Natur.", "Chúng tôi dành cả ngày ngoài thiên nhiên."),
    ("Luft", "die Lüfte", "/lʊft/", "Không khí", "Air", "Frische Luft tut den Lungen gut.", "Không khí trong lành rất tốt cho phổi."),
    ("Wurst", "die Würste", "/vʊʁst/", "Xúc xích", "Sausage", "Thüringer Rostbratwurst ist weltbekannt.", "Xúc xích nướng Thüringen nổi tiếng toàn cầu.")
]
for w, pl, ipa, vi, en, ex_de, ex_vi in die_a1:
    item(w, "die", pl, ipa, "Noun", "A1", vi, en, ex_de, ex_vi)

# Das nouns (60)
das_a1 = [
    ("Buch", "die Bücher", "/buːx/", "Quyển sách", "Book", "Ich lese gerne ein spannendes Buch.", "Tôi thích đọc một cuốn sách hấp dẫn."),
    ("Wasser", "die Wässer", "/ˈvasɐ/", "Nước lọc", "Water", "Trinken Sie ausreichend klares Wasser.", "Hãy uống đủ nước lọc tinh khiết."),
    ("Brot", "die Brote", "/bʁoːt/", "Bánh mì", "Bread", "Frisches deutsches Brot riecht wunderbar.", "Bánh mì Đức tươi mới thơm phức."),
    ("Brötchen", "die Brötchen", "/ˈbʁøːtçn̩/", "Bánh mì tròn nhỏ", "Bread roll", "Wir frühstücken mit knusprigen Brötchen.", "Chúng tôi ăn sáng với bánh mì tròn giòn rụm."),
    ("Ei", "die Eier", "/aɪ̯/", "Quả trứng", "Egg", "Ein gekochtes Ei zum Frühstück schmeckt gut.", "Một quả trứng luộc ăn sáng rất ngon."),
    ("Fleisch", "die Fleische", "/flaɪ̯ʃ/", "Thịt", "Meat", "Das Fleisch wird in der Pfanne gebraten.", "Thịt được áp chảo chín tới."),
    ("Gemüse", "die Gemüse", "/ɡəˈmyːzə/", "Rau củ", "Vegetables", "Gemüse gehört zu jeder gesunden Mahlzeit.", "Rau củ là phần không thể thiếu trong bữa ăn lành mạnh."),
    ("Obst", "die Obste", "/oːpst/", "Hoa quả", "Fruit", "Obst liefert wertvolle Vitamine.", "Hoa quả cung cấp vitamin quý giá."),
    ("Bier", "die Biere", "/biːɐ̯/", "Bia", "Beer", "Ein kühles Bier schmeckt zum Feierabend.", "Một cốc bia mát lạnh thật tuyệt sau giờ tan ca."),
    ("Salz", "die Salze", "/zalt͡s/", "Muối ăn", "Salt", "Geben Sie bitte eine Prise Salz hinzu.", "Làm ơn cho thêm một nhúm muối."),
    ("Haus", "die Häuser", "/haʊ̯s/", "Ngôi nhà", "House", "Das Haus hat ein rotes Ziegeldach.", "Ngôi nhà có mái ngói màu đỏ."),
    ("Zimmer", "die Zimmer", "/ˈt͡sɪmɐ/", "Căn phòng", "Room", "Das Zimmer ist gemütlich eingerichtet.", "Căn phòng được bài trí ấm cúng."),
    ("Fenster", "die Fenster", "/ˈfɛnstɐ/", "Cửa sổ", "Window", "Das Fenster lässt viel Sonnenlicht herein.", "Cửa sổ đón nhiều ánh nắng rọi vào."),
    ("Bett", "die Betten", "/bɛt/", "Chiếc giường", "Bed", "Das Hotelbett war herrlich bequem.", "Chiếc giường khách sạn nằm rất êm ái."),
    ("Bild", "die Bilder", "/bɪlt/", "Bức tranh, ảnh", "Picture", "Das bunte Bild hängt an der Wohnzimmerwand.", "Bức tranh nhiều màu treo trên tường phòng khách."),
    ("Auto", "die Autos", "/ˈaʊ̯to/", "Xe ô tô", "Car", "Er fährt jeden Morgen mit dem Auto zur Arbeit.", "Anh ấy lái ô tô đi làm mỗi sáng."),
    ("Fahrrad", "die Fahrräder", "/ˈfaːɐ̯ˌʁaːt/", "Xe đạp", "Bicycle", "In Deutschland fahren viele mit dem Fahrrad.", "Ở Đức rất nhiều người đi lại bằng xe đạp."),
    ("Flugzeug", "die Flugzeuge", "/ˈfluːkˌt͡sɔɪ̯k/", "Máy bay", "Airplane", "Das Flugzeug startet vom Terminal 1.", "Máy bay cất cánh từ nhà ga số 1."),
    ("Kind", "die Kinder", "/kɪnt/", "Đứa trẻ, con cái", "Child", "Das Kind spielt vergnügt im Park.", "Đứa trẻ chơi đùa vui vẻ trong công viên."),
    ("Mädchen", "die Mädchen", "/ˈmɛːtçn̩/", "Cô bé, bé gái", "Girl", "Das Mädchen liest eine schöne Geschichte.", "Cô bé đang đọc một câu chuyện hay."),
    ("Baby", "die Babys", "/ˈbeːbi/", "Em bé sơ sinh", "Baby", "Das Baby schläft friedlich in den Armen.", "Em bé ngủ yên bình trong vòng tay mẹ."),
    ("Jahr", "die Jahre", "/jaːɐ̯/", "Năm", "Year", "Wir wünschen Ihnen ein glückliches neues Jahr!", "Chúng tôi chúc bạn một năm mới an khang!"),
    ("Geld", "die Gelder", "/ɡɛlt/", "Tiền bạc", "Money", "Er spart Geld für den Sommerurlaub.", "Anh ấy tiết kiệm tiền cho kỳ nghỉ hè."),
    ("Wetter", "die Wetter", "/ˈvɛtɐ/", "Thời tiết", "Weather", "Das Wetter am Wochenende wird traumhaft schön.", "Thời tiết cuối tuần sẽ đẹp như mơ."),
    ("Telefon", "die Telefone", "/teleˈfoːn/", "Máy điện thoại", "Telephone", "Das Telefon steht auf dem Bürotisch.", "Chiếc điện thoại đặt trên bàn văn phòng."),
    ("Handy", "die Handys", "/ˈhɛndi/", "Điện thoại di động", "Mobile phone", "Ich lade mein Handy über Nacht auf.", "Tôi sạc điện thoại qua đêm."),
    ("Glas", "die Gläser", "/ɡlaːs/", "Cái ly thủy tinh", "Glass", "Ein Glas frischer Orangensaft schmeckt super.", "Một ly nước cam tươi có hương vị tuyệt vời."),
    ("Hotel", "die Hotels", "/hoˈtɛl/", "Khách sạn", "Hotel", "Das Hotel liegt im historischen Stadtzentrum.", "Khách sạn nằm ở trung tâm phố cổ."),
    ("Restaurant", "die Restaurants", "/ʁɛstoˈʁɑ̃ː/", "Nhà hàng", "Restaurant", "Wir reservieren einen Tisch im Restaurant.", "Chúng tôi đặt bàn ở nhà hàng."),
    ("Café", "die Cafés", "/kaˈfeː/", "Quán cà phê", "Café", "Wir trinken am Nachmittag Kaffee im Café.", "Buổi chiều chúng tôi uống cà phê ngoài quán."),
    ("Konto", "die Konten", "/ˈkɔnto/", "Tài khoản ngân hàng", "Bank account", "Ich habe ein Girokonto bei der Bank.", "Tôi có một tài khoản vãng lai ở ngân hàng."),
    ("Land", "die Länder", "/lant/", "Đất nước, vùng quê", "Country", "Deutschland ist ein waldreiches Land.", "Nước Đức là một quốc gia nhiều rừng rậm."),
    ("Wort", "die Wörter", "/vɔʁt/", "Từ vựng", "Word", "Was bedeutet dieses deutsche Wort?", "Từ tiếng Đức này có nghĩa là gì?"),
    ("Ticket", "die Tickets", "/ˈtɪkət/", "Vé tàu xe, vé vào cửa", "Ticket", "Ich habe das Bahnticket online gekauft.", "Tôi đã mua vé tàu trực tuyến."),
    ("Formular", "die Formulare", "/fɔʁmuˈlaːɐ̯/", "Mẫu đơn khai", "Form", "Bitte füllen Sie das Anmeldeformular aus.", "Làm ơn điền vào phiếu đăng ký."),
    ("Museum", "die Museen", "/muˈzeːʊm/", "Bảo tàng", "Museum", "Das Museum zeigt berühmte Kunstwerke.", "Bảo tàng trưng bày các tác phẩm nghệ thuật danh tiếng."),
    ("Kino", "die Kinos", "/ˈkiːno/", "Rạp chiếu phim", "Cinema", "Gehen wir heute Abend ins Kino?", "Tối nay chúng ta đi xem phim chiếu rạp chứ?"),
    ("Theater", "die Theater", "/teˈaːtɐ/", "Nhà hát, sân khấu kịch", "Theater", "Das Theaterstück begeisterte das Publikum.", "Vở kịch nhà hát làm khán giả vô cùng hào hứng."),
    ("Schwimmbad", "die Schwimmbäder", "/ˈʃvɪmˌbaːt/", "Hồ bơi", "Swimming pool", "Im Sommer gehen wir oft ins Schwimmbad.", "Mùa hè chúng tôi hay đến hồ bơi."),
    ("Krankenhaus", "die Krankenhäuser", "/ˈkʁaŋkn̩ˌhaʊ̯s/", "Bệnh viện", "Hospital", "Der Patient wurde ins Krankenhaus gebracht.", "Bệnh nhân đã được chuyển tới bệnh viện."),
    ("Gespräch", "die Gespräche", "/ɡəˈʃpʁɛːç/", "Cuộc trò chuyện", "Conversation", "Wir hatten ein sehr angenehmes Gespräch.", "Chúng tôi đã có một cuộc nói chuyện rất thú vị."),
    ("Thema", "die Themen", "/ˈteːma/", "Chủ đề", "Topic", "Das Thema der heutigen Stunde ist Grammatik.", "Chủ đề của buổi học hôm nay là ngữ pháp."),
    ("Problem", "die Probleme", "/pʁoˈbleːm/", "Vấn đề khó khăn", "Problem", "Kein Problem, das schaffen wir gemeinsam!", "Không vấn đề gì, chúng ta sẽ cùng nhau giải quyết!"),
    ("Beispiel", "die Beispiele", "/ˈbaɪ̯ˌʃpiːl/", "Ví dụ minh họa", "Example", "Nennen Sie bitte ein anschauliches Beispiel.", "Làm ơn nêu một ví dụ minh họa trực quan."),
    ("Frühstück", "die Frühstücke", "/ˈfʁyːˌʃtʏk/", "Bữa ăn sáng", "Breakfast", "Zum Frühstück esse ich Müsli und Obst.", "Bữa sáng tôi ăn ngũ cốc trộn hoa quả."),
    ("Mittagessen", "die Mittagessen", "/ˈmɪtaːkˌʔɛsn̩/", "Bữa ăn trưa", "Lunch", "Um zwölf Uhr gibt es Mittagessen.", "Lúc 12 giờ có bữa trưa."),
    ("Abendessen", "die Abendessen", "/ˈaːbn̩tˌʔɛsn̩/", "Bữa ăn tối", "Dinner", "Das Abendessen schmeckt allen sehr gut.", "Bữa ăn tối mọi người đều thấy rất ngon miệng."),
    ("Geschenk", "die Geschenke", "/ɡəˈʃɛŋk/", "Món quà tặng", "Gift", "Ich habe ein schönes Geschenk für dich.", "Tôi có một món quà đẹp dành tặng bạn."),
    ("Tier", "die Tiere", "/tiːɐ̯/", "Động vật, con vật", "Animal", "Hunde sind sehr treue Tiere.", "Chó là loài động vật rất trung thành."),
    ("Pferd", "die Pferde", "/pfeːɐ̯t/", "Con ngựa", "Horse", "Das weiße Pferd läuft schnell über die Wiese.", "Con ngựa trắng chạy nhanh qua đồng cỏ."),
    ("Schaf", "die Schafe", "/ʃaːf/", "Con cừu", "Sheep", "Die Schafe grasen friedlich auf dem Hügel.", "Những chú cừu gặm cỏ thanh bình trên đồi."),
    ("Schwein", "die Schweine", "/ʃvaɪ̯n/", "Con lợn, heo", "Pig", "Das Schwein wühlt im Schlamm.", "Con lợn ủi trong bùn."),
    ("Huhn", "die Hühner", "/huːn/", "Con gà", "Chicken", "Das Huhn legt jeden Morgen ein Ei.", "Con gà đẻ một quả trứng mỗi sáng."),
    ("Meer", "die Meere", "/meːɐ̯/", "Biển cả", "Sea", "Das Meer ist heute ruhig und blau.", "Biển hôm nay lặng sóng và xanh biếc."),
    ("Schiff", "die Schiffe", "/ʃɪf/", "Tàu thủy", "Ship", "Das Schiff fährt über den Ozean.", "Con tàu vượt qua đại dương."),
    ("Boot", "die Boote", "/boːt/", "Thuyền nhỏ", "Boat", "Wir rudern mit dem Boot auf dem See.", "Chúng tôi chèo thuyền nhỏ trên hồ."),
    ("Dorf", "die Dörfer", "/dɔʁf/", "Ngôi làng", "Village", "Das Dorf liegt malerisch zwischen Bergen.", "Ngôi làng nằm thơ mộng giữa những ngọn núi."),
    ("Zentrum", "die Zentren", "/ˈt͡sɛntʁʊm/", "Trung tâm", "Center", "Das Hotel liegt direkt im Stadtzentrum.", "Khách sạn nằm ngay trung tâm thành phố."),
    ("Kleid", "die Kleider", "/klaɪ̯t/", "Bộ váy, đầm", "Dress", "Sie trägt ein wunderschönes Sommerkleid.", "Cô ấy mặc một chiếc váy mùa hè tuyệt đẹp."),
    ("Hemd", "die Hemden", "/hɛmt/", "Áo sơ mi nam", "Shirt", "Er zieht zur Feier ein weißes Hemd an.", "Anh ấy mặc chiếc sơ mi trắng tới dự tiệc.")
]
for w, pl, ipa, vi, en, ex_de, ex_vi in das_a1:
    item(w, "das", pl, ipa, "Noun", "A1", vi, en, ex_de, ex_vi)

# A1 Verbs (40)
verbs_a1 = [
    ("sein", "/zaɪ̯n/", "Thì, là, ở", "to be", "Ich bin glücklich.", "Tôi đang hạnh phúc."),
    ("haben", "/ˈhaːbn̩/", "Có, sở hữu", "to have", "Wir haben viel Zeit.", "Chúng tôi có nhiều thời gian."),
    ("machen", "/ˈmaxn̩/", "Làm, chế tạo", "to do / make", "Was machst du heute?", "Hôm nay bạn làm gì?"),
    ("gehen", "/ˈɡeːən/", "Đi bộ, đi lại", "to go", "Wir gehen zu Fuß.", "Chúng tôi đi bộ."),
    ("kommen", "/ˈkɔmən/", "Đến, tới", "to come", "Er kommt aus Vietnam.", "Anh ấy đến từ Việt Nam."),
    ("sehen", "/ˈzeːən/", "Nhìn thấy", "to see", "Ich sehe die Berge.", "Tôi nhìn thấy những ngọn núi."),
    ("hören", "/ˈhøːʁən/", "Nghe", "to hear", "Ich höre gerne Musik.", "Tôi thích nghe nhạc."),
    ("sprechen", "/ˈʃpʁɛçn̩/", "Nói chuyện", "to speak", "Sie spricht Deutsch.", "Cô ấy nói tiếng Đức."),
    ("lesen", "/ˈleːzn̩/", "Đọc sách", "to read", "Er liest ein Buch.", "Anh ấy đọc sách."),
    ("schreiben", "/ˈʃʁaɪ̯bn̩/", "Viết chữ", "to write", "Ich schreibe einen Brief.", "Tôi viết một lá thư."),
    ("essen", "/ˈɛsn̩/", "Ăn", "to eat", "Wir essen zu Mittag.", "Chúng tôi ăn trưa."),
    ("trinken", "/ˈtʁɪŋkn̩/", "Uống", "to drink", "Ich trinke Wasser.", "Tôi uống nước."),
    ("schlafen", "/ˈʃlaːfn̩/", "Ngủ", "to sleep", "Das Kind schläft tief.", "Đứa bé ngủ say."),
    ("lernen", "/ˈlɛʁnən/", "Học tập", "to learn", "Wir lernen fleißig.", "Chúng tôi học hành chăm chỉ."),
    ("arbeiten", "/ˈaʁbaɪ̯tn̩/", "Làm việc", "to work", "Er arbeitet im Büro.", "Anh ấy làm việc ở văn phòng."),
    ("wohnen", "/ˈvoːnən/", "Cư trú, ở", "to live", "Ich wohne in Berlin.", "Tôi sống ở Berlin."),
    ("kaufen", "/ˈkaʊ̯fn̩/", "Mua sắm", "to buy", "Wir kaufen Brot.", "Chúng tôi mua bánh mì."),
    ("verkaufen", "/fɛɐ̯ˈkaʊ̯fn̩/", "Bán hàng", "to sell", "Er verkauft Autos.", "Anh ấy bán xe hơi."),
    ("fragen", "/ˈfʁaːɡn̩/", "Hỏi", "to ask", "Darf ich fragen?", "Tôi có thể hỏi được không?"),
    ("antworten", "/ˈantvɔʁtn̩/", "Trả lời", "to answer", "Sie antwortet schnell.", "Cô ấy trả lời nhanh chóng."),
    ("verstehen", "/fɛɐ̯ˈʃteːən/", "Hiểu được", "to understand", "Ich verstehe das Wort.", "Tôi hiểu từ này."),
    ("wissen", "/ˈvɪsn̩/", "Biết (sự thật)", "to know", "Ich weiß es nicht.", "Tôi không biết điều đó."),
    ("kennen", "/ˈkɛnən/", "Quen biết", "to know", "Ich kenne ihn gut.", "Tôi biết rõ anh ấy."),
    ("helfen", "/ˈhɛlfn̩/", "Giúp đỡ", "to help", "Können Sie mir helfen?", "Bạn có thể giúp tôi không?"),
    ("brauchen", "/ˈbʁaʊ̯xn̩/", "Cần thiết", "to need", "Ich brauche Hilfe.", "Tôi cần sự giúp đỡ."),
    ("suchen", "/ˈzuːxn̩/", "Tìm kiếm", "to look for", "Ich suche meinen Stift.", "Tôi đang tìm cây bút."),
    ("finden", "/ˈfɪndn̩/", "Tìm thấy", "to find", "Ich finde den Weg.", "Tôi tìm thấy đường đi."),
    ("bleiben", "/ˈblaɪ̯bn̩/", "Ở lại", "to stay", "Ich bleibe hier.", "Tôi ở lại đây."),
    ("fahren", "/ˈfaːʁən/", "Lái xe, đi xe", "to drive", "Wir fahren mit dem Zug.", "Chúng tôi đi bằng tàu hỏa."),
    ("fliegen", "/ˈfliːɡn̩/", "Bay", "to fly", "Wir fliegen nach Rom.", "Chúng tôi bay đến Rome."),
    ("schwimmen", "/ˈʃvɪmən/", "Bơi lội", "to swim", "Die Kinder schwimmen gern.", "Lũ trẻ thích bơi lội."),
    ("kochen", "/ˈkɔxn̩/", "Nấu ăn", "to cook", "Er kocht gerne Suppe.", "Anh ấy thích nấu súp."),
    ("backen", "/ˈbakn̩/", "Nướng bánh", "to bake", "Wir backen frisches Brot.", "Chúng tôi nướng bánh mì tươi."),
    ("öffnen", "/ˈœfnən/", "Mở ra", "to open", "Er öffnet das Fenster.", "Anh ấy mở cửa sổ."),
    ("schließen", "/ˈʃliːsn̩/", "Đóng lại", "to close", "Bitte die Tür schließen.", "Làm ơn đóng cửa lại."),
    ("bezahlen", "/bəˈt͡saːlən/", "Thanh toán", "to pay", "Ich bezahle bar.", "Tôi trả bằng tiền mặt."),
    ("kosten", "/ˈkɔstn̩/", "Có giá là", "to cost", "Was kostet das?", "Cái này giá bao nhiêu?"),
    ("lieben", "/ˈliːbn̩/", "Yêu thương", "to love", "Ich liebe dich.", "Tôi yêu bạn."),
    ("lachen", "/ˈlaxn̩/", "Cười", "to laugh", "Alle lachen fröhlich.", "Mọi người đều cười vui vẻ."),
    ("weinen", "/ˈvaɪ̯nən/", "Khóc", "to cry", "Das Kind weint leise.", "Đứa bé khóc thút thít.")
]
for w, ipa, vi, en, ex_de, ex_vi in verbs_a1:
    item(w, None, None, ipa, "Verb", "A1", vi, en, ex_de, ex_vi)

# A1 Adjectives (30)
adjs_a1 = [
    ("gut", "/ɡuːt/", "Tốt, ngon", "good", "Das Essen ist sehr gut.", "Đồ ăn rất ngon."),
    ("schlecht", "/ʃlɛçt/", "Tồi, xấu", "bad", "Das Wetter ist schlecht.", "Thời tiết xấu."),
    ("groß", "/ɡʁoːs/", "Lớn, to, cao", "big", "Das Haus ist sehr groß.", "Ngôi nhà rất lớn."),
    ("klein", "/klaɪ̯n/", "Nhỏ, bé", "small", "Das Zimmer ist klein.", "Căn phòng nhỏ bé."),
    ("alt", "/alt/", "Cũ, già", "old", "Die Stadt ist sehr alt.", "Thành phố rất cổ kính."),
    ("neu", "/nɔɪ̯/", "Mới mẻ", "new", "Das Auto ist ganz neu.", "Chiếc xe còn rất mới."),
    ("schön", "/ʃøːn/", "Đẹp đẽ", "beautiful", "Wien ist eine schöne Stadt.", "Viên là một thành phố đẹp."),
    ("warm", "/vaʁm/", "Ấm áp", "warm", "Der Sommer ist warm.", "Mùa hè ấm áp."),
    ("kalt", "/kalt/", "Lạnh giá", "cold", "Das Wasser ist eiskalt.", "Nước lạnh như băng."),
    ("schnell", "/ʃnɛl/", "Nhanh chóng", "fast", "Der Zug fährt schnell.", "Con tàu chạy nhanh."),
    ("langsam", "/ˈlaŋzaːm/", "Chậm chạp", "slow", "Er spricht langsam.", "Anh ấy nói chậm rãi."),
    ("teuer", "/ˈtɔɪ̯ɐ/", "Đắt đỏ", "expensive", "Das Hotel ist zu teuer.", "Khách sạn quá đắt."),
    ("billig", "/ˈbɪlɪç/", "Rẻ tiền", "cheap", "Das Ticket ist billig.", "Tấm vé rất rẻ."),
    ("leicht", "/laɪ̯çt/", "Dễ, nhẹ", "easy / light", "Deutsch lernen ist leicht.", "Học tiếng Đức rất dễ."),
    ("schwer", "/ʃveːɐ̯/", "Khó, nặng", "hard / heavy", "Der Koffer ist schwer.", "Chiếc vali rất nặng."),
    ("hell", "/hɛl/", "Sáng sủa", "bright", "Das Zimmer ist hell.", "Căn phòng sáng sủa."),
    ("dunkel", "/ˈdʊŋkl̩/", "Tối tăm", "dark", "Es wird draußen dunkel.", "Bên ngoài trời đang tối dần."),
    ("sauber", "/ˈzaʊ̯bɐ/", "Sạch sẽ", "clean", "Die Küche ist sauber.", "Nhà bếp sạch sẽ."),
    ("schmutzig", "/ˈʃmʊt͡sɪç/", "Bẩn thỉu", "dirty", "Die Schuhe sind schmutzig.", "Đôi giày bị bẩn."),
    ("müde", "/ˈmyːdə/", "Mệt mỏi", "tired", "Ich bin sehr müde.", "Tôi rất mệt."),
    ("hungrig", "/ˈhʊŋʁɪç/", "Đói bụng", "hungry", "Ich bin hungrig.", "Tôi đói bụng."),
    ("durstig", "/ˈdʊʁstɪç/", "Khát nước", "thirsty", "Bist du durstig?", "Bạn có khát nước không?"),
    ("glücklich", "/ˈɡlʏklɪç/", "Hạnh phúc", "happy", "Wir sind glücklich.", "Chúng tôi rất hạnh phúc."),
    ("traurig", "/ˈtʁaʊ̯ʁɪç/", "Buồn bã", "sad", "Sie ist heute traurig.", "Hôm nay cô ấy buồn."),
    ("wichtig", "/ˈvɪçtɪç/", "Quan trọng", "important", "Grammatik ist wichtig.", "Ngữ pháp rất quan trọng."),
    ("einfach", "/ˈaɪ̯nfax/", "Đơn giản", "simple", "Die Regel ist einfach.", "Quy tắc rất đơn giản."),
    ("freundlich", "/ˈfʁɔɪ̯ntlɪç/", "Thân thiện", "friendly", "Der Kellner ist freundlich.", "Người phục vụ rất thân thiện."),
    ("leise", "/ˈlaɪ̯zə/", "Yên lặng", "quiet", "Sei bitte leise.", "Làm ơn giữ yên lặng."),
    ("laut", "/laʊ̯t/", "Ồn ào", "loud", "Die Musik ist zu laut.", "Âm nhạc quá ồn ào."),
    ("fertig", "/ˈfɛʁtɪç/", "Hoàn thành", "ready", "Das Essen ist fertig.", "Đồ ăn đã sẵn sàng.")
]
for w, ipa, vi, en, ex_de, ex_vi in adjs_a1:
    item(w, None, None, ipa, "Adjective", "A1", vi, en, ex_de, ex_vi)

print(f"Total entries after A1: {len(entries)}")

# Write base progress to check
with open("/home/jikay/Desktop/LingoLearning/scripts/vocab_check.json", "w") as f:
    json.dump(entries, f)
