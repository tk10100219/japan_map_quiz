import streamlit as st
import matplotlib.pyplot as plt
from japanmap import picture
import pandas as pd
import random

# --- 1. 都道府県データ ---
data = {
    "name": ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"],
    "region": ["北海道", "東北", "東北", "東北", "東北", "東北", "東北", "関東", "関東", "関東", "関東", "関東", "関東", "関東", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "中国", "中国", "中国", "中国", "中国", "四国", "四国", "四国", "四国", "九州", "九州", "九州", "九州", "九州", "九州", "九州", "九州"],
    "hint": ["一番大きい！", "りんご1位", "わんこそば", "牛タン", "なまはげ", "さくらんぼ", "赤べこ", "納豆", "餃子", "焼きまんじゅう", "深谷ねぎ", "落花生", "首都", "中華街", "お米", "黒部ダム", "兼六園", "恐竜", "富士山", "お蕎麦", "白川郷", "お茶1位", "トヨタ", "伊勢神宮", "琵琶湖", "金閣寺", "たこ焼き", "姫路城", "奈良公園の鹿", "みかんと梅", "砂丘", "出雲大社", "桃太郎", "厳島神社", "フグ", "阿波踊り", "うどん", "みかん", "坂本龍馬", "ラーメン", "有田焼", "ハウステンボス", "阿蘇山", "温泉", "マンゴー", "桜島", "美ら海"]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="都道府県マスター", layout="centered")
st.title("🗾 都道府県マスターへの道")

# --- 2. スコア管理の初期化 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0
if 'target_idx' not in st.session_state:
    st.session_state.target_idx = random.randint(0, 46)

# サイドバー
st.sidebar.header("🏆 スコア")
st.sidebar.subheader(f"いまの正解数: {st.session_state.score}")
st.sidebar.write(f"さいこう記録: {st.session_state.high_score}")

if st.sidebar.button("スコアをリセット"):
    st.session_state.score = 0
    st.session_state.target_idx = random.randint(0, 46)
    st.rerun()

level = st.sidebar.selectbox("レベルをえらんでね", ["Lv1: 地方", "Lv2: 地方内の県", "Lv3: 全国の県"])

target = df.iloc[st.session_state.target_idx]

# --- 3. 地図描画 ---
# キャッシュを使って描画を速くします
@st.cache_data
def get_map_image(color_pref_name, color_name, is_region, target_region=None):
    color_dict = {}
    if is_region:
        target_region_prefs = df[df['region'] == target_region]['name'].tolist()
        for pref in target_region_prefs:
            color_dict[pref] = color_name
    else:
        color_dict[color_pref_name] = color_name
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(picture(color_dict))
    ax.axis('off')
    return fig

# 地図の表示
fig = get_map_image(
    target['name'], 
    "orange" if level == "Lv1: 地方" else "red", 
    level == "Lv1: 地方",
    target['region']
)
st.pyplot(fig)

# --- 4. 回答エリア ---
if level == "Lv1: 地方":
    st.subheader("オレンジ色の場所は何地方？")
    ans = st.radio("答えをえらんでね", ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"], horizontal=True)
    if st.button("こうげき！"):
        if ans == target['region']:
            st.session_state.score += 1
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
            st.session_state.target_idx = random.randint(0, 46)
            st.balloons()
            st.success("せいかい！")
            st.button("つぎの問題へ")
        else:
            st.error("ざんねん！")
            st.session_state.score = 0

elif level == "Lv2: 地方内の県":
    st.subheader(f"【{target['region']}地方】の、赤い県はどこ？")
    choices = df[df['region'] == target['region']]['name'].tolist()
    ans = st.selectbox("えらんでね", ["（えらんでね）"] + choices)
    if st.button("ヒント！"): st.info(f"💡 {target['hint']}")
    if st.button("こうげき！"):
        if ans == target['name']:
            st.session_state.score += 1
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
            st.session_state.target_idx = random.randint(0, 46)
            st.balloons()
            st.success("せいかい！")
            st.button("つぎの問題へ")
        else:
            st.error("おしい！")
            st.session_state.score = 0

else: # Lv3
    st.subheader("この赤い県はどこかな？")
    if st.button("ヒントをみる"): st.info(f"💡 {target['hint']}")
    ans = st.text_input("県の名前をいれてね（漢字）")
    if st.button("こうげき！"):
        if ans == target['name']:
            st.session_state.score += 1
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
            st.session_state.target_idx = random.randint(0, 46)
            st.balloons()
            st.success("天才！")
            st.button("つぎの問題へ")
        else:
            st.error("ざんねん！")
            st.session_state.score = 0
