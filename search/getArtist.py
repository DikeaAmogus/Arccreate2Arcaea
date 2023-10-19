# Note: This is just the base of the search_artist adding. If you want more then add it by yourself.


def search_artist(artist):
    search_artist = {}
    switch = {
        "CK": {"ja": ["しーけー"], "ko": ["시케"]},
        "xi": {"ja": ["さい"], "ko": ["사이"]},
        "3R2": {"ja": ["すりーあーるつー"], "ko": ["스리 알 투"]},
        "Sta": {"ja": ["すた"], "ko": ["스타"]},
        "uma": {"ja": ["ゆーま", "ゆうま"], "ko": ["우마"]},
        "Aoi": {"ja": ["あおい"], "ko": ["아오이"]},
        "USAO": {"ja": ["うさお"], "ko": ["우사오"]},
        "LeaF": {"ja": ["りーふ"], "ko": ["리프"]},
        "Hyun": {"ja": ["ひゅん"], "ko": ["휸", "현"]},
        "Yooh": {"ja": ["ゆー"], "ko": ["유"]},
        "ETIA.": {"ja": ["えちあ"], "ko": ["에치아"]},
        "Puru": {"ja": ["ぷる"], "ko": ["푸루"]},
        "Frums": {"ja": ["ふらむす"], "ko": ["프럼스"]},
        "Laur": {"ja": ["らうる"], "ko": ["라우르"]},
        "Maozon": {"ja": ["まおぞん"], "ko": ["마오존"]},
        "Street": {"ja": ["すとりーと"], "ko": ["스트릿", "스트리트"]},
        "Sakuzyo": {"ja": ["さくじょ"], "ko": ["사쿠죠"]},
        "Kobaryo": {"ja": ["こばりょー"], "ko": ["코바료"]},
        "WAiKURO": {"ja": ["わいくろ"], "ko": ["와이쿠로"]},
        "EBIMAYO": {"ja": ["えびまよ"], "ko": ["에비마요"]},
        "Camellia": {"en": ["kameria"], "ja": ["かめりあ"], "ko": ["카메리아"]},
        "REDALiCE": {"ja": ["れっどありす"], "ko": ["레드앨리스"]},
        "ARForest": {"ja": ["えーあーるふぉれすと"], "ko": ["에이알 포레스트"]},
        "Kurokotei": {"ja": ["黒皇帝"], "ko": ["쿠로코테이", "흑황제"]},
        "Silentroom": {"ja": ["さいれんとるーむ"], "ko": ["사일런트 룸"]},
        "DJ Myosuke": {
            "ja": ["でぃーじぇーみょーすけ", "でぃーじぇーみょうすけ", "でぃーじぇいみょーすけ", "でぃーじぇいみょうすけ"],
            "ko": ["디제이 묘스케"],
        },
        "t+pazolite": {"ja": ["とぱぞらいと"], "ko": ["토파졸라이트"]},
        "Juggernaut.": {"ja": ["じゃがーのーと"], "ko": ["저거넛", "저거너트"]},
        "Blacklolita": {"ja": ["ぶらっくろりーた"], "ko": ["블랙로리타", "블랙롤리타"]},
        "HiTECH NINJA": {"ja": ["はいてっくにんじゃ"], "ko": ["하이테크 닌자"]},
        "Team Grimoire": {"ja": ["ちーむぐりもわーる", "ちーむぐりもあ"], "ko": ["팀 그리모어"]},
        "Akira Complex": {"ja": ["あきらこんぷれっくす"], "ko": ["아키라 컴플렉스"]},
        "sasakure.uk": {"ja": ["ささくれゆーけー"], "ko": ["사사쿠레 유케이"]},
        "tj.hangneil": {"ja": ["てぃーじぇーはんぐねいる"], "ko": ["티제이 행네일"]},
        "sky_delta": {"ja": ["すかいでるた"], "ko": ["스카이 델타"]},
        "Massive New Krew": {"ja": ["まっしぶにゅーくるー"], "ko": ["매시브 뉴 크루", "매시브 뉴 크류"]},
        "void (Mournfinale)": {"ja": ["ぼいど", "ゔぉいど"], "ko": ["보이드"]},
        "Alice Schach and the Magic Orchestra": {
            "en": ["arisushahha to mahou no gakudan"],
            "ja": ["ありすしゃっはとまほうのがくだん", "アリスシャッハと魔法の楽団"],
            "ko": ["아리스샤하토 마호노 가쿠단", "앨리스 샤하와 마법의 오케스트라"],
        },
        "黒皇帝": {"en": ["kurokotei"], "ja": ["くろこうてい"], "ko": ["쿠로코테이", "흑황제"]},
        "かめりあ(EDP)": {"en": ["kameria", "camellia"], "ko": ["카메리아"]},
        "かめりあ": {"en": ["kameria", "camellia"], "ko": ["카메리아"]},
        "しーけー": {"en": ["shiikei", "ck"], "ko": ["시케"]},
        "ぺのれり": {"en": ["penoreri"], "ko": ["페노레리"]},
        "モリモリあつし": {"en": ["morimori atsushi"], "ko": ["모리모리 아츠시"]},
        "アリスシャッハと魔法の楽団": {
            "en": [
                "alice schach and the magic orchestra",
                "arisushahha to mahou no gakudan",
            ],
            "ja": ["ありすしゃっはとまほうのがくだん"],
            "ko": ["아리스샤하토 마호노 가쿠단", "앨리스 샤하와 마법의 오케스트라"],
        },
    }
    search_artist = switch.get(artist, {})
    return search_artist
