from PIL import Image, ImageDraw
import streamlit as st
import os
base_image = Image.open("images/kousya.jpg").convert("RGBA")

overlay =Image.new("RGBA",base_image.size,(255,0,0,0))

draw = ImageDraw.Draw(overlay)

box = (865,600,945,670)

draw.rectangle(box,fill=(255,0,0,100))

combined = Image.alpha_composite(base_image,overlay)

combined.show()

category = st.selectbox("表示カテゴリ",["選択してください","全て","クラス","特別教室"],index=0)

search_term = st.texxt_input("クラス名や部屋名を検索（例：トイレ、３年１組など）")

image_path = "images/kousya.jpg"

image_path = os.path.join(current_dir,image_path)

