import streamlit as st
import time
from PIL import Image, ImageDraw
import os

# 現在のファイル（app.py）のパスを構築
current_dir = os.path.dirname(os.path.abspath(__file__))

def inject_fadein_css():
    st.markdown("""
        <style>
        .fadein {
            opacity: 0;
            animation: fadeIn 2s ease-in-out forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        </style>
    """, unsafe_allow_html=True)

def inject_fadeout_css():
    st.markdown("""
        <style>
        .fadeout {
            opacity: 1;
            animation: fadeOut 2s ease-in-out forwards;
        }

        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        </style>
    """, unsafe_allow_html=True)

def inject_zoom_css():
    st.markdown("""
        <style>
        /* ボタン全体をズームイン */
        div.stButton {
            animation: zoomIn 0.6s ease forwards;
            transform: scale(0.8);
        }

        @keyframes zoomIn {
            0% {
                opacity: 0;
                transform: scale(0.8);
            }
            100% {
                opacity: 1;
                transform: scale(1);
            }
        }
        </style>
    """, unsafe_allow_html=True)



import base64
def set_main_background():
    image_path="images/door.jpg"
    image_path = os.path.join(current_dir, image_path)
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        @keyframes fadeOut {{
            from {{ opacity: 1; }}
            to {{ opacity: 0; }}
        }}

        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            animation: fadeIn 2s ease-in-out forwards, fadeOut 2s ease-in-out 3s forwards;

        }}
        </style>
        """,
        unsafe_allow_html=True
    )



# ユーザー情報（簡易的にユーザー名とパスワードを設定）
users = {"user1": "pass1", "user2": "pass2"}

# クラス企画情報（拡張：企画名, 概要, 詳細, 画像）
class_project = {
    "1年1組": ["お化け屋敷", "お化け屋敷！ドキドキの体験をお楽しみください。", "暗い教室の中で、本格的な演出と仕掛けが満載のお化け屋敷を体験できます。", "images/class_1_1.jpg"],
    "1年2組": ["カフェ", "カフェ☕️でゆったりと休憩しませんか？", "手作りスイーツとドリンクを提供する、落ち着いた空間のカフェです。", "images/class_1_2.jpg"],
    "3年1組": ["縁日屋台", "縁日風屋台！射的やヨーヨー釣りもあります。", "日本の伝統的な縁日を再現した屋台で、楽しいゲームや景品が盛りだくさん。", "images/class_3_1.jpg"],
    "図書室": ["武将フェア", "武将フェア開催！ゆかりの文書を辿ろう。", "戦国武将に関する書籍や展示を集めたフェア。解説パネルも充実。", "images/class_3_1.jpg"],
    "音楽室": ["音楽フェス", "軽音楽部による音楽フェス！熱く盛りあがろう。", "校内バンドやゲストが出演する音楽イベント。手拍子・声援大歓迎！", "images/class_3_1.jpg"],
    "図工室": ["ものづくり体験", "廃材を使った日曜大工、フライパン製作", "工具を使って本格的なDIYが体験できます。お土産に持ち帰り可能。", "images/class_3_1.jpg"],
    "家庭科室": ["お菓子教室", "お菓子作り教室！美味しいクッキーの焼き方を伝授", "家庭科部監修のお菓子作り体験。レシピ付きで自宅でも再現OK。", "images/class_3_1.jpg"],
    "理科室": ["ハピエネ", "空気砲を作ろう！その他電流による実験もあります。", "科学部による体験型の実験展示。安全で楽しい実験がいっぱい。", "images/class_3_1.jpg"],
    "トイレ": ["トイレ", "お手洗いはこちら", "校内の各階に配置されています。安心してご利用ください。", "images/class_3_1.jpg"]
}

# イベント企画情報（企画名: [日程, 時間場所, 概要, 詳細]）
event_project = {
    "ステージ発表": ["1日目", "10:00〜 体育館", "生徒会によるバンド演奏など", "迫力のバンドパフォーマンスやダンスが披露されるステージイベントです。", "images/event_stage.jpg"],
    "ダンス発表": ["1日目", "11:00〜 中庭", "ダンス部によるパフォーマンス", "多彩なジャンルのダンスを披露！息の合った動きに注目。", "images/event_dance.jpg"],
    "演劇": ["2日目", "13:00〜 多目的室", "演劇部によるオリジナル劇", "感動的なストーリーで観客を魅了する演劇部渾身の舞台。", "images/event_show.jpg"],
    "英語スピーチ": ["2日目", "14:00〜 視聴覚室", "英語スピーチコンテスト", "生徒による英語スピーチの発表会です。優秀作品の表彰もあります。", "images/event_english.jpg"],
    "合唱コンクール": ["3日目", "09:30〜 音楽室", "全クラス参加の合唱コンテスト", "クラスごとの合唱発表。審査員による講評と表彰式も行われます。", "images/event_music.jpg"],
    "閉会式": ["3日目", "15:00〜 体育館", "文化祭の締めくくり", "表彰式・感謝の挨拶・全体写真撮影など、文化祭のフィナーレです。", "images/event_sport.jpg"]
}


# セッション状態の初期化
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


# 以下、画面を作成
# ログイン画面
def login():
    st.title("🎌 文化祭案内アプリ")
    st.subheader("ログインしてください")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")

    if st.button("ログイン"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.page = "main"  # ✅ メインページへ遷移
            st.rerun()  # ✅ ここで画面再描画（ログイン画面を即消す）
        else:
            st.error("ユーザー名またはパスワードが間違っています。")


# メイン画面
def main_page():
    # time.sleep(1)
    # st.markdown('<h1 class="fadein fadeout">🌟 ようこそ、武陽祭へ！</h1>', unsafe_allow_html=True)
    # inject_fadein_css()
    # time.sleep(2)
    # inject_fadeout_css()
    set_main_background()

    time.sleep(5)
    st.session_state.page = "menu"
    st.rerun()


# メニュー画面
def menu_page():
    inject_zoom_css()

    st.header("📋 メニュー")
    st.write("文化祭に関する各ページに移動できます。")

    if st.button("🎪 クラス企画一覧"):
        st.session_state.page = "class_list"
        st.rerun()
    time.sleep(0.5)
    if st.button("📅 イベント一覧"):
        st.session_state.page = "event_list"
        st.rerun()
    time.sleep(0.5)
    if st.button("🏫 校内マップ"):
        st.session_state.page = "map"
        st.rerun()
    time.sleep(0.5)
    if st.button("🎉 メッセージページ"):
        st.session_state.page = "message"
        st.rerun()
    time.sleep(0.5)
    if st.button("🗳 投票結果"):
        st.session_state.page = "vote_result"
        st.rerun()



# メッセージページ
def message_page():
    st.title("🎉 来場者へのメッセージ")
    st.write("ようこそ文化祭へ！楽しい企画が盛りだくさんです。ぜひ最後までお楽しみください。")


# 校内マップ画面
def map_page():
    st.header("🏫 校内マップ")

    category = st.selectbox("表示カテゴリ", ["選択してください","すべて", "クラス", "特別教室"], index=0)
    search_term = st.text_input("クラス名や部屋名を検索（例：トイレ、3年1組など）")

    image_path = "images/kousya.jpg"
    image_path = os.path.join(current_dir, image_path)
    base_image = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", base_image.size, (255, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    room_locations = {
        "クラス": {
            "1年1組": [(945, 600, 1025, 670)],
            "1年2組": [(865, 600, 945, 670)],
            "3年1組": [(160, 220, 220, 260)],
        },
        "特別教室": {
            "図書室": [(600, 60, 680, 100)],
            "音楽室": [(960, 60, 1050, 100)],
            "図工室": [(480, 230, 560, 270)],
            "家庭科室": [(560, 230, 640, 270)],
            "理科室": [(800, 230, 880, 270)],
            "トイレ": [
                (20, 30, 80, 70), (880, 30, 940, 70),
                (20, 230, 80, 270), (880, 230, 940, 270),
                (20, 430, 80, 470)
            ],
        }
    }

    highlighted = []
    for cat, rooms in room_locations.items():
        if category == "すべて" or category == cat:
            for room, boxes in rooms.items():
                if search_term in room:
                    highlighted.append((room, boxes))

    for room, boxes in highlighted:
        for box in boxes:
            draw.rectangle(box, fill=(255, 0, 0, 100))

    combined = Image.alpha_composite(base_image, overlay)
    st.image(combined, use_container_width=True)

    st.write("地図上の場所を参考にして、各クラスの企画紹介ページへ移動できます。")

    for room, _ in highlighted:
        if room in class_project:
            title, desc, _, _ = class_project[room]
            st.subheader(f"{room}：{title}")
            st.write(desc)
            if st.button(f"{room} の企画を見る", key=f"map_{room}"):
                st.session_state.selected_class = room
                st.session_state.page = "class_detail"
                st.session_state.map = True
                st.rerun()
            st.write("---------------------")


# クラス企画一覧
def class_list_page():
    st.title("🏫 クラス企画一覧")
    search = st.text_input("キーワードで検索")
    for room, (title, desc, _, _) in class_project.items():
        if search in room or search in title:
            st.subheader(f"{room}：{title}")
            st.write(desc)
            if st.button(f"{room} の企画を見る", key=f"class_{room}"):
                st.session_state.selected_class = room
                st.session_state.page = "class_detail"
                st.session_state.map = False
                st.rerun()
            st.write("---------------------")



# クラス企画詳細
def class_detail_page():
    st.title("🎪 クラス企画詳細")
    class_name = st.session_state.get("selected_class", "不明なクラス")
    title, desc, detail, image_path = class_project.get(class_name, ["不明", "情報が見つかりませんでした。", "", None])
    image_path = os.path.join(current_dir, image_path)
    st.subheader(f"{class_name}：{title}")
    st.write(desc)
    st.markdown("---")
    st.write(detail)

    if image_path:
        st.image(image_path, caption=f"{class_name} の展示写真", use_container_width=True)

    if st.session_state.map:
        if st.button("← マップに戻る"):
            st.session_state.page = "map"
            st.rerun()
    else:
        if st.button("← クラス一覧に戻る"):
            st.session_state.page = "class_list"
            st.rerun()



# イベント一覧
def event_list_page():
    st.title("📅 イベント一覧")
    day = st.selectbox("日程を選択", ["すべて", "1日目", "2日目", "3日目"])
    search = st.text_input("イベント名で検索")
    for name, (event_day, time_place, summary, _, _) in event_project.items():
        if (day == "すべて" or event_day == day) and (search in name):
            st.subheader(name)
            st.write(f"🗓 {event_day}　🕒 {time_place}")
            st.write(summary)
            if st.button(f"{name} の詳細を見る", key=f"event_{name}"):
                st.session_state.selected_event = name
                st.session_state.page = "event_detail"
                st.rerun()
            st.write("---------------------")

# イベント詳細
def event_detail_page():
    st.title("🎭 イベント詳細")
    name = st.session_state.get("selected_event", "不明なイベント")
    event_day, time_place, _, detail, image_path = event_project.get(name, ["日程不明", "時間不明", "", "詳細情報はありません。", None])
    image_path = os.path.join(current_dir, image_path)
    st.subheader(name)
    st.write(f"🗓 {event_day}　🕒 {time_place}")
    st.markdown("---")
    st.write(detail)

    if image_path:
        st.image(image_path, caption=f"{name} の様子", use_container_width=True)

    if st.button("← イベント一覧に戻る"):
        st.session_state.page = "event_list"
        st.rerun()


# クラス投票結果ページ
def class_vote_result_page():
    st.title("🗳 クラス企画投票結果")
    results = {
        "1年A組": 45,
        "1年B組": 52,
        "2年A組": 38,
        "2年B組": 60
    }
    st.subheader("投票数ランキング")
    st.write(results)


# サイドバー（メニュー）
def sidebar():
    st.sidebar.title("📌 メニュー")
    if st.sidebar.button("メイン画面"):
        st.session_state.page = "main"
        st.rerun()
    if st.sidebar.button("メニュー一覧"):
        st.session_state.page = "menu"
        st.rerun()
    if st.sidebar.button("来場メッセージ"):
        st.session_state.page = "message"
        st.rerun()
    if st.sidebar.button("校内マップ"):
        st.session_state.page = "map"
        st.rerun()
    if st.sidebar.button("クラス企画一覧"):
        st.session_state.page = "class_list"
        st.rerun()
    if st.sidebar.button("イベント一覧"):
        st.session_state.page = "event_list"
        st.rerun()
    if st.sidebar.button("投票結果"):
        st.session_state.page = "vote_result"
        st.rerun()

    if st.sidebar.button("ログアウト"):
        st.session_state.logged_in = False
        st.session_state.page = "main"
        st.rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
        return  # ログインしていない場合は他の描画をしない

    # 以下ログイン後のページ表示処理
    if 'page' not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page not in ['main', 'menu']:
        sidebar()

    if st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "menu":
        menu_page()
    elif st.session_state.page == "message":
        message_page()
    elif st.session_state.page == "map":
        map_page()
    elif st.session_state.page == "class_list":
        class_list_page()
    elif st.session_state.page == "class_detail":
        class_detail_page()
    elif st.session_state.page == "event_list":
        event_list_page()
    elif st.session_state.page == "event_detail":
        event_detail_page()
    elif st.session_state.page == "vote_result":
        class_vote_result_page()


main()