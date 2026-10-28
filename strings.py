"""Per-language UI strings. Same keys in every language. Casual, friendly tone."""

NAMES = {
    "hi": "हिंदी",
    "en": "English",
    "vi": "Tiếng Việt",
    "id": "Bahasa Indonesia",
    "ar": "العربية",
}

# Shown when the user has not picked a language yet (all five, one per line).
PROMPT = "भाषा चुनो 👇\nChoose your language 👇\nChọn ngôn ngữ 👇\nPilih bahasamu 👇\nاختر لغتك 👇"

DEFAULT_LANG = "en"

STRINGS = {
    "hi": {
        "welcome": (
            "शब्द युद्ध - शब्दों वाला 1 vs 1 खेल\n\n"
            "हर राउंड में 2 खिलाड़ियों को एक जैसे 7 अक्षर मिलते हैं। उनसे बनने वाला सबसे लंबा सही शब्द भेजो। "
            "कम आने वाले अक्षरों पर बोनस अंक मिलता है। 5 राउंड x 60 सेकंड, सबसे ज़्यादा कुल अंक वाला जीतता है।\n\n"
            "/play - मैच ढूंढो (सेव की हुई भाषा में)\n"
            "/play en - अंग्रेज़ी मैच\n"
            "/play hi - हिंदी मैच\n"
            "/play vi - वियतनामी मैच\n"
            "/play id - इंडोनेशियाई मैच\n"
            "/play ar - अरबी मैच\n"
            "/leaderboard - टॉप खिलाड़ी\n"
            "/referral - अपना रेफ़रल लिंक और कमीशन देखो\n"
            "/myid - अपना यूज़र आईडी देखो\n"
            "/cancel - कतार से बाहर निकलो\n\n"
            "मैच खेलने से पहले इस चैट में Start दबाओ, नहीं तो बॉट तुम्हें मैसेज नहीं भेज पाएगा।\n\n"
            "नीचे से भाषा बदल सकते हो।"
        ),
        "lang_set": "भाषा बदल गई: {name}।",
        "ref_line": "\n\nतुम्हें किसी दोस्त ने बुलाया है। अब से तुम्हारे खेल की एंट्री पर उसे कमीशन मिलेगा।",
        "play_hint": "टिप: अभी तक कोई भाषा नहीं चुनी, तो यह अंग्रेज़ी मैच है। भाषा बदलने के लिए /start भेजो।",
        "play_bad": "/play, /play en, /play hi, /play vi, /play id या /play ar लिखो",
        "in_match": "तुम पहले से एक मैच में हो। पहले उसे खत्म करो।",
        "in_queue": "तुम पहले से कतार में हो। बाहर निकलने के लिए /cancel करो।",
        "fee_fail": "एंट्री फीस नहीं कट पाई। फिर से कोशिश करो।",
        "searching": "{name} मैच के लिए विरोधी ढूंढ रहे हैं... बाहर निकलने के लिए /cancel करो",
        "match_found": "{other} के साथ मैच मिल गया! {rounds} राउंड x {secs} सेकंड। शब्द मैसेज में भेजो। हर राउंड का सबसे अच्छा शब्द गिना जाएगा।",
        "round_start": "राउंड {n}/{total} - समय: {secs} सेकंड\nअक्षर: {letters}\nअभी सबसे लंबा सही शब्द भेजो।",
        "round_end": "राउंड {n} खत्म।\nतुम: {mine} (+{pts})\n{other}: {theirs} (+{opp_pts})\nकुल स्कोर: तुम {my_total} - {their_total}",
        "nothing": "कुछ नहीं",
        "final": "फाइनल: तुम {mine} - {other} {theirs}. {result}. फिर से /play या /leaderboard देखो",
        "res_draw": "बराबरी रही",
        "res_win": "तुम जीत गए!",
        "res_lose": "तुम हार गए",
        "no_match": "अभी कोई मैच नहीं चल रहा। मैच ढूंढने के लिए /play करो।",
        "round_closed": "राउंड अभी नहीं चल रहा। अगले राउंड का इंतज़ार करो।",
        "err_short": "बहुत छोटा (कम से कम {n} अक्षर)",
        "err_not_in_list": "शब्द सूची में नहीं है",
        "err_letters": "इस राउंड के अक्षरों में नहीं है",
        "word_best": "{word} +{pts} (इस राउंड में तुम्हारा सबसे अच्छा)",
        "word_lower": "{word} +{pts} (तुम्हारे सबसे अच्छे {best} से कम)",
        "word_bad": "नहीं: {reason}",
        "empty_list": "शब्द सूची खाली है, मैच रद्द कर दिया गया।",
        "cancel_in_match": "तुम अभी मैच में हो। मैच खत्म होने तक रुकना होगा।",
        "cancel_done": "कतार से बाहर निकल गए।",
        "not_queued": "तुम कतार में नहीं हो।",
        "leader_title": "लीडरबोर्ड (पहले जीत, फिर अंक)",
        "leader_empty": "अभी तक कोई मैच नहीं खेला गया।",
        "leader_line": "{i}. {name} - {wins} जीत, {points} अंक, {matches} मैच",
        "myid": "तुम्हारा यूज़र आईडी: {uid}\n\nइसी से तुम्हारा रेफ़रल लिंक बनता है:\nhttps://t.me/{bot}?start=ref_{uid}",
        "ref_title": "तुम्हारा रेफ़रल सिस्टम",
        "ref_link": "तुम्हारा लिंक:",
        "ref_intro": "जो दोस्त इस लिंक से जुड़ेगा और मैच खेलेगा, उसकी हर एंट्री फीस पर तुम्हें कमीशन मिलेगा:",
        "ref_l1": "लेवल 1 (सीधा दोस्त): {pct} कमीशन",
        "ref_l2": "लेवल 2 (दोस्त का दोस्त): {pct} कमीशन",
        "ref_l3": "लेवल 3 (दोस्त के दोस्त का दोस्त): {pct} कमीशन",
        "ref_fee": "कुल एंट्री फीस का {total} कमीशन में जाता है। एंट्री {fee} की है, तो लेवल 1 पर {l1}, लेवल 2 पर {l2}, लेवल 3 पर {l3} मिलेगा।",
        "ref_net": "तुम्हारे नेटवर्क में:",
        "ref_lvl_people": "लेवल {n}: {c} लोग",
        "ref_earned": "अभी तक की कमाई (लेजर में पेंडिंग):",
        "ref_lvl_earned": "लेवल {n}: {amt}",
        "ref_total": "कुल: {amt}",
        "ref_pending": "अभी ये कमीशन पेंडिंग हैं। Pi पेमेंट चालू होने के बाद ही ये असली में मिलेंगे।",
    },
    "en": {
        "welcome": (
            "Shabd Yuddh - word duel, 1 vs 1\n\n"
            "Each round both players get the same 7 letters. Send the longest valid word you can make from them. "
            "Rare letters give bonus points. 5 rounds x 60 seconds, most total points wins.\n\n"
            "/play - find a match (in your saved language)\n"
            "/play en - English match\n"
            "/play hi - Hindi match\n"
            "/play vi - Vietnamese match\n"
            "/play id - Indonesian match\n"
            "/play ar - Arabic match\n"
            "/leaderboard - top players\n"
            "/referral - your referral link and earnings\n"
            "/myid - your user id\n"
            "/cancel - leave the queue\n\n"
            "Tap Start in this chat before playing, otherwise the bot can't message you.\n\n"
            "Tap a language below to change it."
        ),
        "lang_set": "Language set to {name}.",
        "ref_line": "\n\nSomeone invited you here. From now on they earn commission on your match entries.",
        "play_hint": "Tip: no language picked yet, so this is an English match. Send /start to choose your language.",
        "play_bad": "Use /play, /play en, /play hi, /play vi, /play id or /play ar",
        "in_match": "You're already in a match. Finish it first.",
        "in_queue": "You're already in the queue. Use /cancel to leave.",
        "fee_fail": "Couldn't take the entry fee. Try again.",
        "searching": "Looking for a {name} match... use /cancel to leave",
        "match_found": "Matched with {other}! {rounds} rounds x {secs} seconds. Send words as messages. Your best word each round counts.",
        "round_start": "Round {n}/{total} - time: {secs} seconds\nLetters: {letters}\nSend your longest valid word now.",
        "round_end": "Round {n} over.\nYou: {mine} (+{pts})\n{other}: {theirs} (+{opp_pts})\nTotal: you {my_total} - {their_total}",
        "nothing": "nothing",
        "final": "Final: you {mine} - {other} {theirs}. {result}. Play again with /play or check /leaderboard",
        "res_draw": "It's a draw",
        "res_win": "You won!",
        "res_lose": "You lost",
        "no_match": "No match going on. Use /play to find one.",
        "round_closed": "No round running right now. Wait for the next one.",
        "err_short": "Too short (min {n} letters)",
        "err_not_in_list": "Not in the word list",
        "err_letters": "Uses letters that aren't in this round",
        "word_best": "{word} +{pts} (your best this round)",
        "word_lower": "{word} +{pts} (less than your best {best})",
        "word_bad": "No: {reason}",
        "empty_list": "Word list is empty, match cancelled.",
        "cancel_in_match": "You're in a match. Wait till it ends.",
        "cancel_done": "Left the queue.",
        "not_queued": "You're not in the queue.",
        "leader_title": "Leaderboard (wins first, then points)",
        "leader_empty": "No matches played yet.",
        "leader_line": "{i}. {name} - {wins} wins, {points} pts, {matches} matches",
        "myid": "Your user id: {uid}\n\nYour referral link is made from this:\nhttps://t.me/{bot}?start=ref_{uid}",
        "ref_title": "Your referral system",
        "ref_link": "Your link:",
        "ref_intro": "Whenever a friend joins through this link and plays, you get commission on their entry fee:",
        "ref_l1": "Level 1 (direct friend): {pct} commission",
        "ref_l2": "Level 2 (friend of a friend): {pct} commission",
        "ref_l3": "Level 3 (friend of a friend of a friend): {pct} commission",
        "ref_fee": "{total} of the entry fee goes to commission. Entry is {fee}, so level 1 gets {l1}, level 2 gets {l2}, level 3 gets {l3}.",
        "ref_net": "Your network:",
        "ref_lvl_people": "Level {n}: {c} people",
        "ref_earned": "Earned so far (pending in ledger):",
        "ref_lvl_earned": "Level {n}: {amt}",
        "ref_total": "Total: {amt}",
        "ref_pending": "These are pending for now. They become real once Pi payments go live.",
    },
    "vi": {
        "welcome": (
            "Shabd Yuddh - trò đấu chữ 1 đấu 1\n\n"
            "Mỗi vòng, 2 người chơi nhận cùng 7 chữ cái. Gửi từ dài nhất bạn ghép được từ các chữ đó. "
            "Chữ hiếm được cộng thêm điểm. 5 vòng x 60 giây, ai nhiều điểm nhất thắng.\n\n"
            "/play - tìm trận theo ngôn ngữ đã lưu\n"
            "/play en - trận tiếng Anh\n"
            "/play hi - trận tiếng Hindi\n"
            "/play vi - trận tiếng Việt\n"
            "/play id - trận tiếng Indonesia\n"
            "/play ar - trận tiếng Ả Rập\n"
            "/leaderboard - bảng xếp hạng\n"
            "/referral - link giới thiệu và hoa hồng\n"
            "/myid - xem ID của bạn\n"
            "/cancel - rời hàng chờ\n\n"
            "Nhớ bấm Start trong chat này trước khi chơi, không thì bot không nhắn được cho bạn.\n\n"
            "Bấm nút bên dưới để đổi ngôn ngữ."
        ),
        "lang_set": "Đã đổi sang {name}.",
        "ref_line": "\n\nCó người mời bạn vào đây. Từ giờ, người đó sẽ nhận hoa hồng từ lượt vào trận của bạn.",
        "play_hint": "Mẹo: bạn chưa chọn ngôn ngữ nên đây là trận tiếng Anh. Gửi /start để chọn ngôn ngữ.",
        "play_bad": "Gõ /play, /play en, /play hi, /play vi, /play id hoặc /play ar",
        "in_match": "Bạn đang trong một trận rồi. Chơi xong đã.",
        "in_queue": "Bạn đang trong hàng chờ rồi. Gõ /cancel để rời.",
        "fee_fail": "Không trừ được phí vào trận. Thử lại nhé.",
        "searching": "Đang tìm đối thủ cho trận {name}... gõ /cancel để rời",
        "match_found": "Ghép được với {other} rồi! {rounds} vòng x {secs} giây. Gửi từ vào tin nhắn. Từ tốt nhất của mỗi vòng được tính.",
        "round_start": "Vòng {n}/{total} - thời gian: {secs} giây\nChữ cái: {letters}\nGửi từ dài nhất bạn ghép được ngay.",
        "round_end": "Hết vòng {n}.\nBạn: {mine} (+{pts})\n{other}: {theirs} (+{opp_pts})\nTổng: bạn {my_total} - {their_total}",
        "nothing": "không có",
        "final": "Kết quả: bạn {mine} - {other} {theirs}. {result}. Chơi tiếp bằng /play hoặc xem /leaderboard",
        "res_draw": "Hòa nhau",
        "res_win": "Bạn thắng rồi!",
        "res_lose": "Bạn thua rồi",
        "no_match": "Chưa có trận nào đang chạy. Gõ /play để tìm trận.",
        "round_closed": "Chưa có vòng nào đang chạy. Đợi vòng sau nhé.",
        "err_short": "Ngắn quá (tối thiểu {n} chữ cái)",
        "err_not_in_list": "Từ này không có trong danh sách",
        "err_letters": "Dùng chữ cái không có trong vòng này",
        "word_best": "{word} +{pts} (từ tốt nhất của bạn trong vòng này)",
        "word_lower": "{word} +{pts} (thấp hơn từ tốt nhất {best})",
        "word_bad": "Không: {reason}",
        "empty_list": "Danh sách từ trống, trận bị hủy.",
        "cancel_in_match": "Bạn đang trong trận. Đợi trận kết thúc đã.",
        "cancel_done": "Đã rời hàng chờ.",
        "not_queued": "Bạn không có trong hàng chờ.",
        "leader_title": "Bảng xếp hạng (thắng trước, rồi tới điểm)",
        "leader_empty": "Chưa có trận nào được chơi.",
        "leader_line": "{i}. {name} - {wins} thắng, {points} điểm, {matches} trận",
        "myid": "ID của bạn: {uid}\n\nLink giới thiệu của bạn được tạo từ ID này:\nhttps://t.me/{bot}?start=ref_{uid}",
        "ref_title": "Hệ thống giới thiệu của bạn",
        "ref_link": "Link của bạn:",
        "ref_intro": "Mỗi khi bạn bè vào qua link này và chơi, bạn nhận hoa hồng từ phí vào trận của họ:",
        "ref_l1": "Cấp 1 (bạn trực tiếp): hoa hồng {pct}",
        "ref_l2": "Cấp 2 (bạn của bạn): hoa hồng {pct}",
        "ref_l3": "Cấp 3 (bạn của bạn của bạn): hoa hồng {pct}",
        "ref_fee": "{total} phí vào trận được chia làm hoa hồng. Phí vào trận là {fee}, nên cấp 1 nhận {l1}, cấp 2 nhận {l2}, cấp 3 nhận {l3}.",
        "ref_net": "Mạng lưới của bạn:",
        "ref_lvl_people": "Cấp {n}: {c} người",
        "ref_earned": "Đã kiếm được (đang chờ trong sổ):",
        "ref_lvl_earned": "Cấp {n}: {amt}",
        "ref_total": "Tổng: {amt}",
        "ref_pending": "Hiện các khoản này đang chờ. Sẽ thành tiền thật khi thanh toán Pi được bật.",
    },
    "id": {
        "welcome": (
            "Shabd Yuddh - duel kata 1 lawan 1\n\n"
            "Setiap ronde, 2 pemain dapat 7 huruf yang sama. Kirim kata terpanjang yang benar dari huruf-huruf itu. "
            "Huruf yang jarang dapat bonus poin. 5 ronde x 60 detik, total poin terbanyak menang.\n\n"
            "/play - cari match (pakai bahasa yang tersimpan)\n"
            "/play en - match bahasa Inggris\n"
            "/play hi - match bahasa Hindi\n"
            "/play vi - match bahasa Vietnam\n"
            "/play id - match bahasa Indonesia\n"
            "/play ar - match bahasa Arab\n"
            "/leaderboard - pemain teratas\n"
            "/referral - link referral dan komisi\n"
            "/myid - lihat id kamu\n"
            "/cancel - keluar dari antrean\n\n"
            "Tekan Start di chat ini sebelum main, kalau tidak bot tidak bisa kirim pesan ke kamu.\n\n"
            "Pilih bahasa di tombol bawah untuk mengganti."
        ),
        "lang_set": "Bahasa diganti ke {name}.",
        "ref_line": "\n\nKamu diajak teman. Mulai sekarang dia dapat komisi dari setiap entry match kamu.",
        "play_hint": "Tips: kamu belum pilih bahasa, jadi ini match bahasa Inggris. Kirim /start untuk memilih bahasa.",
        "play_bad": "Ketik /play, /play en, /play hi, /play vi, /play id atau /play ar",
        "in_match": "Kamu sudah di dalam match. Selesaikan dulu.",
        "in_queue": "Kamu sudah di antrean. Ketik /cancel untuk keluar.",
        "fee_fail": "Biaya entry gagal dipotong. Coba lagi.",
        "searching": "Mencari lawan untuk match {name}... ketik /cancel untuk keluar",
        "match_found": "Dapat lawan: {other}! {rounds} ronde x {secs} detik. Kirim kata sebagai pesan. Kata terbaikmu tiap ronde yang dihitung.",
        "round_start": "Ronde {n}/{total} - waktu: {secs} detik\nHuruf: {letters}\nKirim kata terpanjang yang benar sekarang.",
        "round_end": "Ronde {n} selesai.\nKamu: {mine} (+{pts})\n{other}: {theirs} (+{opp_pts})\nTotal: kamu {my_total} - {their_total}",
        "nothing": "tidak ada",
        "final": "Hasil akhir: kamu {mine} - {other} {theirs}. {result}. Main lagi dengan /play atau cek /leaderboard",
        "res_draw": "Seri",
        "res_win": "Kamu menang!",
        "res_lose": "Kamu kalah",
        "no_match": "Tidak ada match yang berjalan. Ketik /play untuk cari match.",
        "round_closed": "Tidak ada ronde yang berjalan. Tunggu ronde berikutnya.",
        "err_short": "Terlalu pendek (min {n} huruf)",
        "err_not_in_list": "Tidak ada di daftar kata",
        "err_letters": "Pakai huruf yang tidak ada di ronde ini",
        "word_best": "{word} +{pts} (terbaikmu di ronde ini)",
        "word_lower": "{word} +{pts} (kurang dari terbaikmu {best})",
        "word_bad": "Tidak: {reason}",
        "empty_list": "Daftar kata kosong, match dibatalkan.",
        "cancel_in_match": "Kamu sedang di match. Tunggu sampai selesai.",
        "cancel_done": "Sudah keluar dari antrean.",
        "not_queued": "Kamu tidak ada di antrean.",
        "leader_title": "Papan peringkat (menang dulu, lalu poin)",
        "leader_empty": "Belum ada match yang dimainkan.",
        "leader_line": "{i}. {name} - {wins} menang, {points} poin, {matches} match",
        "myid": "ID kamu: {uid}\n\nLink referral kamu dibuat dari ID ini:\nhttps://t.me/{bot}?start=ref_{uid}",
        "ref_title": "Sistem referral kamu",
        "ref_link": "Link kamu:",
        "ref_intro": "Setiap teman yang masuk lewat link ini dan main, kamu dapat komisi dari biaya entry-nya:",
        "ref_l1": "Level 1 (teman langsung): komisi {pct}",
        "ref_l2": "Level 2 (teman dari teman): komisi {pct}",
        "ref_l3": "Level 3 (teman dari teman dari teman): komisi {pct}",
        "ref_fee": "{total} dari biaya entry masuk ke komisi. Entry {fee}, jadi level 1 dapat {l1}, level 2 dapat {l2}, level 3 dapat {l3}.",
        "ref_net": "Jaringan kamu:",
        "ref_lvl_people": "Level {n}: {c} orang",
        "ref_earned": "Sudah dapat (pending di buku):",
        "ref_lvl_earned": "Level {n}: {amt}",
        "ref_total": "Total: {amt}",
        "ref_pending": "Komisi ini masih pending. Akan jadi nyata setelah pembayaran Pi aktif.",
    },
    "ar": {
        "welcome": (
            "Shabd Yuddh - مبارزة كلمات 1 ضد 1\n\n"
            "في كل جولة يحصل اللاعبان على نفس الحروف السبعة. أرسل أطول كلمة صحيحة يمكنك تكوينها منها. "
            "الحروف النادرة تعطي نقاطاً إضافية. 5 جولات x 60 ثانية، والأعلى مجموعاً يفوز.\n\n"
            "/play - ابحث عن مباراة (بحسب لغتك المحفوظة)\n"
            "/play en - مباراة إنجليزية\n"
            "/play hi - مباراة هندية\n"
            "/play vi - مباراة فيتنامية\n"
            "/play id - مباراة إندونيسية\n"
            "/play ar - مباراة عربية\n"
            "/leaderboard - أفضل اللاعبين\n"
            "/referral - رابط الإحالة والعمولات\n"
            "/myid - معرّفك\n"
            "/cancel - اخرج من قائمة الانتظار\n\n"
            "اضغط Start في هذه المحادثة قبل اللعب، وإلا لن يتمكن البوت من مراسلتك.\n\n"
            "اختر لغة من الأزرار بالأسفل لتغييرها."
        ),
        "lang_set": "تم تغيير اللغة إلى {name}.",
        "ref_line": "\n\nدعاك صديق إلى هنا. من الآن سيحصل على عمولة من رسوم دخول مبارياتك.",
        "play_hint": "نصيحة: لم تختر لغة بعد، لذلك هذه مباراة إنجليزية. أرسل /start لاختيار لغتك.",
        "play_bad": "اكتب /play أو /play en أو /play hi أو /play vi أو /play id أو /play ar",
        "in_match": "أنت في مباراة بالفعل. أنهِها أولاً.",
        "in_queue": "أنت في قائمة الانتظار بالفعل. اكتب /cancel للخروج.",
        "fee_fail": "تعذّر خصم رسوم الدخول. حاول مرة أخرى.",
        "searching": "نبحث عن منافس لمباراة {name}... اكتب /cancel للخروج",
        "match_found": "تم العثور على منافس: {other}! {rounds} جولات x {secs} ثانية. أرسل الكلمات كرسائل. تُحسب أفضل كلمة لك في كل جولة.",
        "round_start": "الجولة {n}/{total} - الوقت: {secs} ثانية\nالحروف: {letters}\nأرسل أطول كلمة صحيحة الآن.",
        "round_end": "انتهت الجولة {n}.\nأنت: {mine} (+{pts})\n{other}: {theirs} (+{opp_pts})\nالمجموع: أنت {my_total} - {their_total}",
        "nothing": "لا شيء",
        "final": "النتيجة النهائية: أنت {mine} - {other} {theirs}. {result}. العب مجدداً بـ /play أو راجع /leaderboard",
        "res_draw": "تعادل",
        "res_win": "فزت!",
        "res_lose": "خسرت",
        "no_match": "لا توجد مباراة جارية. اكتب /play للبحث عن مباراة.",
        "round_closed": "لا توجد جولة جارية الآن. انتظر الجولة التالية.",
        "err_short": "قصيرة جداً (على الأقل {n} حروف)",
        "err_not_in_list": "الكلمة ليست في القائمة",
        "err_letters": "تستخدم حروفاً ليست في هذه الجولة",
        "word_best": "{word} +{pts} (أفضل كلمة لك في هذه الجولة)",
        "word_lower": "{word} +{pts} (أقل من أفضل كلمة لك {best})",
        "word_bad": "لا: {reason}",
        "empty_list": "قائمة الكلمات فارغة، تم إلغاء المباراة.",
        "cancel_in_match": "أنت في مباراة. انتظر حتى تنتهي.",
        "cancel_done": "تم الخروج من قائمة الانتظار.",
        "not_queued": "أنت لست في قائمة الانتظار.",
        "leader_title": "لوحة الصدارة (الفوز أولاً ثم النقاط)",
        "leader_empty": "لم تُلعب أي مباراة بعد.",
        "leader_line": "{i}. {name} - {wins} فوز، {points} نقطة، {matches} مباراة",
        "myid": "معرّفك: {uid}\n\nرابط الإحالة الخاص بك يُصنع من هذا المعرّف:\nhttps://t.me/{bot}?start=ref_{uid}",
        "ref_title": "نظام الإحالة الخاص بك",
        "ref_link": "رابطك:",
        "ref_intro": "كلما دخل صديق عبر هذا الرابط ولعب، تحصل على عمولة من رسوم دخوله:",
        "ref_l1": "المستوى 1 (صديق مباشر): عمولة {pct}",
        "ref_l2": "المستوى 2 (صديق الصديق): عمولة {pct}",
        "ref_l3": "المستوى 3 (صديق الصديق للصديق): عمولة {pct}",
        "ref_fee": "يذهب {total} من رسوم الدخول إلى العمولات. رسوم الدخول {fee}، لذا يحصل المستوى 1 على {l1}، والمستوى 2 على {l2}، والمستوى 3 على {l3}.",
        "ref_net": "شبكتك:",
        "ref_lvl_people": "المستوى {n}: {c} أشخاص",
        "ref_earned": "المكسب حتى الآن (معلّق في السجل):",
        "ref_lvl_earned": "المستوى {n}: {amt}",
        "ref_total": "المجموع: {amt}",
        "ref_pending": "هذه العمولات معلّقة حالياً. ستصبح حقيقية عند تفعيل دفع Pi.",
    },
}


def t(lang, key, **kw):
    """Look up a UI string in lang, falling back to English, then format placeholders."""
    text = STRINGS.get(lang, {}).get(key) or STRINGS[DEFAULT_LANG][key]
    return text.format(**kw) if kw else text
