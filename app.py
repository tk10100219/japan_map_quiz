import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
import requests

# 1. データの準備
data = {
    "name": ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"],
    "region": ["北海道", "東北", "東北", "東北", "東北", "東北", "東北", "関東", "関東", "関東", "関東", "関東", "関東", "関東", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "中国", "中国", "中国", "中国", "中国", "四国", "四国", "四国", "四_国", "九州", "九州", "九州", "九州", "九州", "九州", "九州", "九州"],
    "hint": ["一番大きい！", "りんご1位", "わんこそば", "牛タン", "なまはげ", "さくらんぼ", "赤べこ", "納豆", "餃子", "焼きまんじゅう", "深谷ねぎ", "落花生", "首都", "中華街", "お米", "石川のとなり", "兼六園", "恐竜", "富士山", "お蕎麦", "白川郷", "お茶1位", "トヨタ", "伊勢神宮", "琵琶湖", "金閣寺", "たこ焼き", "姫路城", "奈良公園の鹿", "みかんと梅", "砂丘", "出雲大社", "桃太郎", "厳島神社", "フグ", "阿波踊り", "うどん", "みかん", "坂本龍馬", "ラーメン", "有田焼", "ハウステンボス", "阿蘇山", "温泉", "マンゴー", "桜島", "美ら海"]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="都道府県クイズ", layout="centered")

# 2. 状態保持
if 'score' not in st.session_state: st.session_state.score = 0
if 'target_idx' not in st.session_state: st.session_state.target_idx = random.randint(0, 46)

level = st.sidebar.selectbox("レベルをえらんでね", ["Lv1: 地方", "Lv2: 都道府県（えらぶ）", "Lv3: 都道府県（かく）"])
st.sidebar.write(f"今の正解数: {st.session_state.score}")

target = df.iloc[st.session_state.target_idx]

# --- メイン画面 ---
st.title("🗾 都道府県クイズ")

# 【解決策】地図データをその場でダウンロードして「色を塗る対象」を100%一致させる
@st.cache_data
def get_geojson():
    url = "https://raw.githubusercontent.com/smartnews-archive/japan-geojson/master/japan.json"
    return requests.get(url).json()

try:
    geojson = get_geojson()
    
    df['color_val'] = 0
    if level == "Lv1: 地方":
        df.loc[df['region'] == target['region'], 'color_val'] = 1
    else:
        df.loc[df['name'] == target['name'], 'color_val'] = 2

    # 真っ白を防ぐため、mapboxを使わない「Choropleth」形式に変更
    fig = go.Figure(go.Choropleth(
        geojson=geojson,
        locations=df['name'],
        z=df['color_val'],
        featureidkey="properties.name",
        colorscale=[[0, "#f8f9fa"], [0.5, "orange"], [1, "red"]],
        showscale=False,
        marker_line_color='gray',
        marker_line_width=0.5,
        hoverinfo='none'
    ))

    fig.update_geos(
        visible=False, 
        projection_type="mercator",
        fitbounds="locations"
    )

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

except:
    st.error("地図の読み込みに失敗しました。再読み込みしてください。")

# 3. クイズ部分
if level == "Lv1: 地方":
    st.subheader("オレンジ色の場所は何地方？")
    choices = ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"]
    ans = st.radio("答えをえらんでね", choices, key="lv1", horizontal=True)
elif level == "Lv2: 都道府県（えらぶ）":
    st.subheader("赤い場所はどこかな？")
    if st.button("💡 ヒントをみる"): st.info(f"ヒント：{target['hint']}")
    all_names = df['name'].tolist()
    wrong = random.sample([n for n in all_names if n != target['name']], 3)
    choices = random.sample([target['name']] + wrong, 4)
    ans = st.radio("答えをえらんでね", choices, key="lv2", horizontal=True)
else:
    st.subheader("赤い場所はどこかな？")
    if st.button("💡 ヒントをみる"): st.info(f"ヒント：{target['hint']}")
    ans = st.text_input("答えを漢字でいれてね")

if st.button("こうげき！"):
    is_correct = (ans == target['region']) if level == "Lv1: 地方" else (ans == target['name'])
    if is_correct:
        st.balloons()
        st.success("せいかい！")
        st.session_state.score += 1
        st.session_state.target_idx = random.randint(0, 46)
        if st.button("次の問題へ"): st.rerun()
    else:
        st.error(f"ざんねん！ 正解は {target['region'] if level=='Lv1: 地方' else target['name']}")
        st.session_state.score = 0
