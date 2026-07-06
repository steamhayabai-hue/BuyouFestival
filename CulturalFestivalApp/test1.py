import streamlit as st

def login():
    st.title("文化祭案内アプリ")
    st.subheader("ログインしてください")
    username=st.text_input("ユーザー名")
    password=st.text_input("パスワード",type="password")

    if st.button("ログイン"):
        st.write('ログインしたよ')



def main_page():
    st.title("文化祭アプリ")
    st.write("画面の左メニューから、各機能に移動できます。")

menu="ログイン画面"

if menu=="ログイン画面":
    login()
elif menu=="メインページ":
    main_page()















