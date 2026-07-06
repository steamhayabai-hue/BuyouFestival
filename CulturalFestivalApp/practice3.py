# セッション管理
# 画面遷移
# ログイン機能

# webサイトはリロードを行うとデータが初期化される
# セッションに値を保存することで、リロード後のデータを保持することができる
# 例）ログイン情報、表示表示する画面など

#import
import streamlit as st
import time # 3 追加

# 4 現在のファイル（app.py）のパスを構築

# 7 後でinject_fadein_css()（フェードインのcss）

# 7 後でinject_fadeout_css()（フェードアウトのcss）

# 7 後でinject_zoom_css()（ズームインのcss）

# 7 後でset_main_background()（背景画像をフェードイン、フェードアウトする関数）

# 3 後でログイン認証用のuserデータ
users = {"user1": "pass1", "user2": "pass2"}

# 4 後でクラス企画のclass_projectデータ

# 5 後でイベント企画のevent_projectデータ

# 3 後でセッション状態の初期化
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 以下、画面を作成
# ログイン画面
def login():
    st.title("🎌 文化祭案内アプリ")
    st.subheader("ログインしてください")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")

    # 3 後でログイン機能に変更
    if st.button("ログイン"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.page = "main"  # ✅ メインページへ遷移
            st.rerun()  # ✅ ここで画面再描画
        else:
            st.error("ユーザー名またはパスワードが間違っています。")


# メイン画面
def main_page():
    # 7 後で文字または画像のフェードイン、フェードアウトに変更
    st.title("🌟 文化祭アプリ！")
    st.write("画面左のメニューから、各機能に移動できます。")

    # 3 後で自動での画面遷移
    time.sleep(5)
    st.session_state.page = "menu"
    st.rerun()


# メニュー画面
def menu_page():
    # 7 あとでズームイン処理のcss（inject_zoom_css()）+ボタン表示にラグを追加（time.sleep(0.5)）
    
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
    
    if st.button("🗳 投票結果"):
        st.session_state.page = "vote_result"# 3 押したら画面遷移する処理に後で変更
        st.rerun()

# メッセージページ
def message_page():
    st.title("🎉 来場者へのメッセージ")
    st.write("ようこそ文化祭へ！楽しい企画が盛りだくさんです。ぜひ最後までお楽しみください。")

# 校内マップ画面
def map_page():
    st.header("🏫 校内マップ")

    # 6 後で表示カテゴリのセレクトボックスcategory
    # 6 後で部屋名の検索ボックスsearch_term

    # 6 後でオーバーレイ画像の作成
    st.image("images/map.png", use_container_width=True)
    st.write("地図上の場所を参考にして、各クラスの企画紹介ページへ移動できます。")

    # 6 後で検索条件に応じて、表示するボタンを変える
    if st.button("1年A組の企画を見る"):
        st.write('1-Aの企画')
    if st.button("1年B組の企画を見る"):
        st.write('1-Bの企画')


# 2 クラス企画一覧ページ
def class_list_page():
    st.title("🏫 クラス企画一覧")
    search = st.text_input("キーワードで検索")

    # 4 後で検索結果に応じて一覧を表示する処理に変更
    if st.button(f"{search} の企画を見る", key=f"class_{search}"):
        st.write(f"{search}の詳細に画面遷移しました。")


# 2 クラス企画詳細
def class_detail_page():
    st.title("🎪 クラス企画詳細")
    
    # 4 後で企画一覧、校内マップ一覧で押したボタンの企画詳細を表示

# イベント一覧
def event_list_page():
    st.title("📅 イベント一覧")
    day = st.selectbox("日程を選択", ["すべて", "1日目", "2日目", "3日目"])
    search = st.text_input("イベント名で検索")

    # 5 後で検索結果に応じたデータを表示する処理を記載



# イベント詳細
def event_detail_page():
    st.title("🎭 イベント詳細")
    
    # 5 後で企画一覧ページで選んだ企画の詳細を表示


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
    if st.sidebar.button("投票結果"):
        st.session_state.page = "vote_result"# 3 後で投票結果画像に遷移する処理に変更
        st.rerun()

    if st.sidebar.button("ログアウト"):
        st.session_state.logged_in = False # 3 後でログアウトする処理に変更
        st.session_state.page = "main"
        st.rerun()

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