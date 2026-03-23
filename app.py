
import streamlit as st
import matplotlib.pyplot as plt
from japanmap import picture
import pandas as pd
import random
import io

# データ
data = {
    "name": ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"],
    "region": ["北海道", "東北", "東北", "東北", "東北", "東北", "東北", "関東", "関東", "関東", "関東", "関東", "関東", "関東", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "中国", "中国", "中国", "中国", "中国", "四国", "四国", "四国", "四国", "九州", "九州", "九州", "九州", "九州", "九州", "九州", "九州"],
    "hint": ["一番大きい！", "りんご1位", "わんこそば", "牛タン", "なまはげ", "さくらんぼ", "赤べこ", "納豆", "餃子", "焼きまんじゅう", "深谷ねぎ", "落花生", "首都", "中華街", "お米", "石川のとなり", "兼六園", "恐竜", "富士山", "お蕎麦", "白川郷", "お茶1位", "トヨタ", "伊勢神宮", "琵琶湖", "金閣寺", "たこ焼き", "姫路城", "奈良公園の鹿", "みかんと梅", "砂丘", "出雲大社", "桃太郎", "厳島神社", "フグ", "阿波踊り", "うどん", "みかん", "坂本龍馬", "ラーメン", "有田焼", "ハウステンボス", "阿蘇山", "温泉", "マンゴー", "桜島", "美ら海"]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="都道府県クイズ", layout="centered")

# 状態保持
if 'score' not in st.session_state: st.session_state.score = 0
if 'target_idx' not in st.session_state: st.session_state.target_idx = random.randint(0, 46)

# --- サイドバー (レベル選択) ---
level = st.sidebar.selectbox("レベルをえらんでね", ["Lv1: 地方", "Lv2: 地方内の県", "Lv3: 全国の県"])
st.sidebar.write(f"今の正解数: {st.session_state.score}")

target = df.iloc[st.session_state.target_idx]

# --- メイン画面 ---
# 地図
color_dict = {p: "orange" for p in df[df['region']==target['region']]['name']} if level == "Lv1: 地方" else {target['name']: "red"}
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(picture(color_dict))
ax.axis('off')
st.pyplot(fig)

# クイズ
if level == "Lv1: 地方":
    st.subheader("オレンジ色の場所は何地方？")
    choices = ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"]
    ans = st.radio("答えをえらんでね", choices, horizontal=True)
else:
    st.subheader("赤い場所はどこかな？")
    if st.button("💡 ヒントをみる"):
        st.info(f"ヒント：{target['hint']}")
    ans = st.text_input("答えを漢字でいれてね")

if st.button("こうげき！"):
    correct = (level == "Lv1: 地方" and ans == target['region']) or (ans == target['name'])
    if correct:
        st.balloons()
        st.success("せいかい！")
        st.session_state.score += 1
        st.session_state.target_idx = random.randint(0, 46)
        st.button("つぎへ")
    else:
        st.error("ざんねん！")
        st.session_state.score = 0
    