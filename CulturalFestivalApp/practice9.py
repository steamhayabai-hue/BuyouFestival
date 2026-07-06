# 9 仕様変更②（ログイン機能、投票機能の削除）

# 9 ログイン画面で、ログイン判定をせずにボタンを押したら画面遷移させる（１）
# 9 ログイン画面を表示せずに、最初からメイン画面に画面遷移させる（２）
# 9 投票機能は、メニュー画面とメニューバーから、遷移させるボタンをなくして表示させないようにする（３）

#import
import streamlit as st
import time # 3 追加
import os # 4 追加
from PIL import Image, ImageDraw # 6 追加

# 4 現在のファイル（app.py）のパスを構築
current_dir = os.path.dirname(os.path.abspath(__file__))

# 7 後でinject_fadein_css()（フェードインのcss）
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

# 7 後でinject_fadeout_css()（フェードアウトのcss）
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

# 7 後でinject_zoom_css()（ズームインのcss）
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

# 7 後でset_main_background()（背景画像をフェードイン、フェードアウトする関数）
import base64
def set_main_background():
    image_path="images/メイン画像.png"
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

# 3 後でログイン認証用のuserデータ
users = {"user1": "pass1", "user2": "pass2"}

# 4 後でクラス企画のclass_projectデータ
# 8 クラス企画の最後にカテゴリーを追加
# クラス企画情報（クラス名：企画名, 概要, 詳細, 画像, カテゴリー）
class_project = {
    "1-1": ["お化け屋敷", "お化け屋敷！ドキドキの体験をお楽しみください。", "暗い教室の中で、本格的な演出と仕掛けが満載のお化け屋敷を体験できます。", "images/class_1_1.jpg", "遊ぶ"],
    "1-2": ["カフェ", "カフェ☕️でゆったりと休憩しませんか？", "手作りスイーツとドリンクを提供する、落ち着いた空間のカフェです。", "images/class_1_2.jpg", "食べる"],
    "1-3": ["縁日屋台", "縁日風屋台！射的やヨーヨー釣りもあります。", "日本の伝統的な縁日を再現した屋台で、楽しいゲームや景品が盛りだくさん。", "images/class_3_1.jpg", "遊ぶ"],
    "図書室": ["武将フェア", "武将フェア開催！ゆかりの文書を辿ろう。", "戦国武将に関する書籍や展示を集めたフェア。解説パネルも充実。", "images/class_3_1.jpg", "見る"],
    "音楽室": ["音楽フェス", "軽音楽部による音楽フェス！熱く盛りあがろう。", "校内バンドやゲストが出演する音楽イベント。手拍子・声援大歓迎！", "images/class_3_1.jpg", "見る"],
    "図工室": ["ものづくり体験", "廃材を使った日曜大工、フライパン製作", "工具を使って本格的なDIYが体験できます。お土産に持ち帰り可能。", "images/class_3_1.jpg", "遊ぶ"],
    "家庭科室": ["お菓子教室", "お菓子作り教室！美味しいクッキーの焼き方を伝授", "家庭科部監修のお菓子作り体験。レシピ付きで自宅でも再現OK。", "images/class_3_1.jpg", "食べる"],
    "理科室": ["ハピエネ", "空気砲を作ろう！その他電流による実験もあります。", "科学部による体験型の実験展示。安全で楽しい実験がいっぱい。", "images/class_3_1.jpg", "見る"],
    "トイレ": ["トイレ", "お手洗いはこちら", "校内の各階に配置されています。安心してご利用ください。", "images/class_3_1.jpg", "見る"]
}


# 5 後でイベント企画のevent_projectデータ
# イベント企画情報（企画名: [日程, 時間場所, 概要, 詳細]）
event_project = {
    "ステージ発表": ["1日目", "10:00〜 体育館", "生徒会によるバンド演奏など", "迫力のバンドパフォーマンスやダンスが披露されるステージイベントです。", "images/event_stage.jpg"],
    "ダンス発表": ["1日目", "11:00〜 中庭", "ダンス部によるパフォーマンス", "多彩なジャンルのダンスを披露！息の合った動きに注目。", "images/event_dance.jpg"],
    "演劇": ["2日目", "13:00〜 多目的室", "演劇部によるオリジナル劇", "感動的なストーリーで観客を魅了する演劇部渾身の舞台。", "images/event_show.jpg"],
    "英語スピーチ": ["2日目", "14:00〜 視聴覚室", "英語スピーチコンテスト", "生徒による英語スピーチの発表会です。優秀作品の表彰もあります。", "images/event_english.jpg"],
    "合唱コンクール": ["3日目", "09:30〜 音楽室", "全クラス参加の合唱コンテスト", "クラスごとの合唱発表。審査員による講評と表彰式も行われます。", "images/event_music.jpg"],
    "閉会式": ["3日目", "15:00〜 体育館", "文化祭の締めくくり", "表彰式・感謝の挨拶・全体写真撮影など、文化祭のフィナーレです。", "images/event_sport.jpg"]
}

# 9（2） 最初からメイン画面を表示させる
# 3 後でセッション状態の初期化
if 'logged_in' not in st.session_state:
    # 9（２）session_stateのlogged_inを最初からTrueにしておく
    # logged_inがFalse→ログイン画面、True→メイン画面 になるため
    st.session_state.logged_in = True

# 以下、画面を作成
# ログイン画面
def login():
    st.title("🎌 文化祭案内アプリ")
    st.subheader("ログインしてください")

    # 9（１） ログイン用の入力欄をコメントアウト
    # username = st.text_input("ユーザー名")
    # password = st.text_input("パスワード", type="password")

    # 9（１） ログインボタンを押したら、判定を行わずに次の画面に遷移させる（該当箇所をコメントアウト）
    # 3 後でログイン機能に変更
    if st.button("ログイン"):
        # 9（1）if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.page = "main"  # ✅ メインページへ遷移
            st.rerun()  # ✅ ここで画面再描画（ログイン画面を即消す）
        # else:
            # st.error("ユーザー名またはパスワードが間違っています。")


# メイン画面
def main_page():
    # 7 後で文字または画像のフェードイン、フェードアウトに変更
    # st.title("🌟 文化祭アプリ！")
    # st.write("画面左のメニューから、各機能に移動できます。")
    set_main_background()

    # 3 後で自動での画面遷移
    time.sleep(5)
    st.session_state.page = "menu"
    st.rerun()


# メニュー画面
def menu_page():
    # 7 あとでズームイン処理のcss（inject_zoom_css()）+ボタン表示にラグを追加（time.sleep(0.5)）
    inject_zoom_css()
    
    st.header("📋 メニュー")
    st.write("文化祭に関する各ページに移動できます。")    

    if st.button("🎪 クラス企画一覧"):
        st.session_state.page = "class_list"# 3 押したら画面遷移する処理に後で変更
        st.rerun()
    
    if st.button("📅 イベント一覧"):
        st.session_state.page = "event_list"# 3 押したら画面遷移する処理に後で変更
        st.rerun()
    
    if st.button("🏫 校内マップ"):
        st.session_state.page = "map"# 3 押したら画面遷移する処理に後で変更
        st.rerun()
    
    if st.button("🎉 メッセージページ"):
        st.session_state.page = "message"# 3 押したら画面遷移する処理に後で変更
        st.rerun()
    
    # 9（３） 投票結果へ遷移させるためのボタンをコメントアウトして、表示させないようにする
    # if st.button("🗳 投票結果"):
    #     st.session_state.page = "vote_result"# 3 押したら画面遷移する処理に後で変更
    #     st.rerun()

# メッセージページ
def message_page():
    st.title("🎉 来場者へのメッセージ")
    st.write("ようこそ文化祭へ！楽しい企画が盛りだくさんです。ぜひ最後までお楽しみください。")


# 8 地図の選択を追加。また、class_categories（学年カテゴリごとの部屋名）を追加して、カテゴリごとにどのクラスがあるかを保存。
# 校内マップ画面
def map_page():
    st.header("🏫 校内マップ")

    # 地図の選択
    map_options = {
        "学校全体図": "images/学校全体図.jpg",
        "校舎全体": "images/校舎全体.jpg",
        "第１・３校舎": "images/第１・３校舎.jpg",
        "第２校舎": "images/第２校舎 - 4.jpg",
        "模擬店": "images/模擬店.jpg"
    }
    selected_map = st.radio("地図を選んでください", list(map_options.keys()), horizontal=True)

    # 地図に応じた選択肢のフィルタリング
    available_categories = []
    if selected_map == "校舎全体":
        available_categories = []
    elif selected_map == "第１・３校舎":
        available_categories = ["中学1年","中学2年","中学3年","高校1年","高校2年","高校3年","第1,3校舎その他"]
    elif selected_map == "第２校舎":
        available_categories = []
    elif selected_map == "学校全体図":
        available_categories = []
    elif selected_map == "模擬店":
        available_categories = []

    # 学年カテゴリの選択
    selected_grade = st.selectbox("学年・その他カテゴリを選択", ["選択してください"] + available_categories)

    # 学年カテゴリごとの部屋名
    class_categories = {
        "中学1年": ["1-A", "1-B"],
        "中学2年": ["2-A", "2-B"],
        "中学3年": ["3-A", "3-B"],
        "高校1年": ["1-1", "1-2", "1-3"],
        "高校2年": ["2-1", "2-2", "2-3"],
        "高校3年": ["3-1", "3-2", "3-3", "3-5", "3-6", "3-7", "3-8", "3-9", "3-10", "3-11", "3-12", "3-13", "3-14", "3-15"],
        "第1,3校舎その他": ["物理室", "生物科学室", "被服室", "STELA3", "STELA2", "STELA1", "書道室", "保健室", "小応接室", "職員室", "事務室", "会議室", "体育館", "多目的室", "男子トイレ", "女子トイレ"]
    }

    # クラス・部屋の選択
    selected_room = None
    if selected_grade != "選択してください":
        rooms = class_categories.get(selected_grade, [])
        selected_room = st.selectbox("クラス・部屋名を選んでください", ["選択してください"] + rooms)
        if selected_room == "選択してください":
            selected_room = None

    # 地図画像の読み込みと表示
    image_path = os.path.join(current_dir, map_options[selected_map])
    base_image = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", base_image.size, (255, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 教室座標（今は地図に依存せず共通にしてます）
    room_locations = {
        #第1校舎
        #4階
        "3-15": [(312, 285, 393, 375)],
        "3-14": [(399, 285, 485, 375)],
        "3-13": [(491, 285, 578, 375)],
        "3-12": [(584, 285, 660, 375)],
        "3-11": [(665, 285, 745, 375)],
        "3-10": [(750, 285, 831, 375)],
        #3階
        "3-9": [(312, 411, 406, 486)],
        "3-8": [(412, 411, 494, 486)],
        "3-7": [(312, 609, 393, 696)],
        "3-6": [(399, 609, 484, 696)],
        "3-5": [(490, 609, 577, 696)],
        "3-3": [(584, 609, 658, 696)],
        "3-2": [(664, 609, 746, 696)],
        "3-1": [(752, 609, 831, 696)],
        #2階
        "2-3": [(310, 943, 392, 1026)],
        "2-2": [(397, 943, 481, 1026)],
        "2-1": [(487, 943, 575, 1026)],
        "1-3": [(582, 943, 656, 1026)],
        "1-2": [(662, 943, 743, 1026)],
        "1-1": [(750, 943, 831, 1026)],
        #1階

        #第3校舎
        #3階
        "3-A": [(270, 1732, 351, 1796)],
        "3-B": [(270, 1801, 351, 1863)],
        "2-A": [(270, 1870, 351, 1930)],
        #2階
        "1-A": [(429, 1732, 510, 1796)],
        "1-B": [(429, 1801, 510, 1863)],
        "2-B": [(429, 1870, 510, 1930)],
        #1階

        #第1校舎
        #4階
        "物理室": [(586, 83, 686, 159)],
        "生物科学室": [(736, 83, 831, 159)],
        #3階
        "被服室": [(557, 411, 654, 486)],
        #2階
        "STELA3": [(310, 734, 388, 811)],
        "STELA2": [(394, 734, 491, 811)],
        "STELA1": [(497, 734, 598, 811)],
        "書道室": [(722, 734, 831, 811)],
        #1階
        "保健室": [(362, 1107, 423, 1183)],
        "小応接室": [(613, 1107, 706, 1183)],
        "職員室": [(367, 1311, 621, 1393)],
        "事務室": [(716, 1311, 775, 1393)],
        #その他
        "会議室": [(907, 385, 963, 690)],
        "体育館": [(1043, 438, 1376, 781)],

        #第3校舎
        "多目的室": [(584, 1811, 665, 1930)],

        "男子トイレ":[
            #第1校舎
            #4階
            (407, 187, 460, 262),
            #3階
            (407, 514, 460, 588),
            #2階
            (407, 839, 460, 913),
            #1階
            (365, 1213, 460, 1288),


            #第3校舎
            #3階
            (270, 1672, 351, 1727),
            #2階
            (428, 1672, 510, 1727),
            #1階
            (584, 1672, 665, 1727),
        ],
        "女子トイレ":[
            #第1校舎
            #4階
            (667, 187, 715, 262),
            #3階
            (667, 514, 715, 588),
            #2階
            (667, 839, 715, 913),
            #1階
            (667, 1213, 715, 1288),

            #第3校舎
            #3階
            (270, 1672, 351, 1727),
            #2階
            (428, 1672, 510, 1727),
            #1階
            (584, 1672, 665, 1727)
       ]
    }

    # 赤枠でハイライト
    if selected_room and selected_room in room_locations:
        # 1つの部屋が選ばれていればその部屋だけを赤枠
        for box in room_locations[selected_room]:
            draw.rectangle(box, fill=(255, 0, 0, 100))
    
    elif selected_grade != "選択してください" and selected_room is None:
        # クラス・部屋が未選択なら、カテゴリ内の全クラス・部屋を赤枠表示
        rooms = class_categories.get(selected_grade, [])
        for room in rooms:
            if room in room_locations:
                for box in room_locations[room]:
                    draw.rectangle(box, fill=(255, 0, 0, 100))


    combined = Image.alpha_composite(base_image, overlay)
    st.image(combined, use_container_width=True)

    # 部屋情報の表示
    if selected_room and selected_room in class_project:
        title, desc, _, _, _ = class_project[selected_room]
        st.subheader(f"{selected_room}：{title}")
        st.write(desc)
        if st.button(f"{selected_room} の企画を見る", key=f"map_{selected_room}"):
            st.session_state.selected_class = selected_room
            st.session_state.page = "class_detail"
            st.session_state.map = True
            st.rerun()




# 8 クラス企画一覧でカテゴリーごとに企画を取得する
# クラス企画一覧
def class_list_page():
    st.title("🏫 クラス企画一覧")

    # カテゴリを選ぶ（ラジオボタン）
    selected_category = st.radio("カテゴリで絞り込み", ["すべて", "遊ぶ", "見る", "食べる"], horizontal=True)

    # 該当カテゴリに属するクラス名だけ抽出
    class_names = [
        name for name, data in class_project.items()
        if selected_category == "すべて" or data[4] == selected_category
    ]

    # プルダウンでさらに絞り込む
    selected_class = st.selectbox("クラスを選んでください", ["選択してください"] + class_names)

    # 「選択してください」の場合：カテゴリ内のすべて表示
    if selected_class == "選択してください":
        for name in class_names:
            title, desc, _, _, _ = class_project[name]
            st.subheader(f"{name}：{title}")
            st.write(desc)
            if st.button(f"{name} の企画を見る", key=f"class_{name}"):
                st.session_state.selected_class = name
                st.session_state.page = "class_detail"
                st.session_state.map = False
                st.rerun()
            st.write("---")

    # プルダウンで1つ選ばれた場合のみ表示
    else:
        title, desc, _, _, _ = class_project[selected_class]
        st.subheader(f"{selected_class}：{title}")
        st.write(desc)
        if st.button(f"{selected_class} の企画を見る", key=f"class_{selected_class}"):
            st.session_state.selected_class = selected_class
            st.session_state.page = "class_detail"
            st.session_state.map = False
            st.rerun()



# クラス企画詳細
def class_detail_page():
    st.title("🎪 クラス企画詳細")

    # 4 後で企画一覧、校内マップ一覧で押したボタンの企画詳細を表示
    class_name = st.session_state.get("selected_class", "不明なクラス")
    # 8 class_projectで追加したカテゴリー分、取得する要素数を増やす
    title, desc, detail, image_path, _ = class_project.get(class_name, ["不明", "情報が見つかりませんでした。", "", None, ""])
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

    # 5 後で検索結果に応じたデータを表示する処理を記載
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
    
    # 5 後で企画一覧ページで選んだ企画の詳細を表示
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
    st.write(results)


# サイドバー（メニュー）
def sidebar():
    st.sidebar.title("📌 メニュー")
    if st.sidebar.button("メイン画面"):
        st.session_state.page = "main"# 3 後でメイン画像に遷移する処理に変更
        st.rerun()
    if st.sidebar.button("メニュー一覧"):
        st.session_state.page = "menu"# 3 後でメニュー一覧画像に遷移する処理に変更
        st.rerun()
    if st.sidebar.button("来場メッセージ"):
        st.session_state.page = "message"# 3 後で来場メッセージ画像に遷移する処理に変更
        st.rerun()
    if st.sidebar.button("校内マップ"):
        st.session_state.page = "map"# 3 後で校内マップ画像に遷移する処理に変更
        st.rerun()
    if st.sidebar.button("クラス企画一覧"):
        st.session_state.page = "class_list"# 3 後でクラス企画一覧画像に遷移する処理に変更
        st.rerun()
    if st.sidebar.button("イベント一覧"):
        st.session_state.page = "event_list"# 3 後でイベント一覧画像に遷移する処理に変更
        st.rerun()
    # 9（３） メニューバーの投票結果ボタンを削除
    # if st.sidebar.button("投票結果"):
    #     st.session_state.page = "vote_result"# 3 後で投票結果画像に遷移する処理に変更
    #     st.rerun()

    # 9（２） ログアウトボタンを削除する
    # if st.sidebar.button("ログアウト"):
    #     st.session_state.logged_in = False # 3 後でログアウトする処理に変更
    #     st.session_state.page = "main"
    #     st.rerun()

# 3 後で画面遷移のためのmain()メソッどを作成
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


main() # 3 画面操作をmain()に変更