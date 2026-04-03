import streamlit as st
import matplotlib.pyplot as plt
from japanmap import picture
import pandas as pd
import random

# --- 1. データ準備 ---
data = {
    "name": ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"],
    "region": ["北海道", "東北", "東北", "東北", "東北", "東北", "東北", "関東", "関東", "関東", "関東", "関東", "関東", "関東", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "中国", "中国", "中国", "中国", "中国", "四国", "四国", "四国", "四国", "九州", "九州", "九州", "九州", "九州", "九州", "九州", "九州"],
    "hint": ["一番大きい！", "りんご1位", "わんこそば", "牛タン", "なまはげ", "さくらんぼ", "赤べこ", "納豆", "餃子", "焼きまんじゅう", "深谷ねぎ", "落花生", "首都", "中華街", "お米", "黒部ダム", "兼六園", "恐竜", "富士山", "お蕎麦", "白川郷", "お茶1位", "トヨタ", "伊勢神宮", "琵琶湖", "金閣寺", "たこ焼き", "姫路城", "奈良公園の鹿", "みかんと梅", "砂丘", "出雲大社", "桃太郎", "厳島神社", "フグ", "阿波踊り", "うどん", "みかん", "坂本龍馬", "ラーメン", "有田焼", "ハウステンボス", "阿蘇山", "温泉", "マンゴー", "桜島", "美ら海"]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="都道府県マスター", layout="wide")
st.title("🗾 都道府県マスターへの道")

# 状態管理
if 'target_idx' not in st.session_state:
    st.session_state.target_idx = random.randint(0, 46)
if 'score' not in st.session_state:
    st.session_state.score = 0

tab1, tab2 = st.tabs(["📖 地図でおぼえる", "🎯 クイズに挑戦"])

# --- タブ1: おぼえる (変更なし) ---
with tab1:
    st.subheader("地方をえらんで、場所を確認しよう！")
    col1, col2 = st.columns([2, 1])
    with col2:
        study_reg = st.selectbox("おぼえたい地方", ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"])
        target_prefs = df[df['region'] == study_reg]['name'].tolist()
        selected_pref = st.radio("詳しく見たい県をえらんでね", target_prefs)
    with col1:
        color_dict = {p: "lightblue" for p in target_prefs}
        color_dict[selected_pref] = "red"
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(picture(color_dict))
        ax.axis('off')
        st.pyplot(fig)
        st.success(f"いま赤くなっているのが **【 {selected_pref} 】** だよ！")

# --- タブ2: クイズに挑戦 ---
with tab2:
    st.sidebar.header("🏆 設定とスコア")
    level = st.sidebar.selectbox("レベルをえらんでね", ["レベル1: 地方あて", "レベル2: 地方を限定して都道府県あて", "レベル3: 全国の都道府県あて"])
    st.sidebar.write(f"今の正解数: {st.session_state.score}")

    target = df.iloc[st.session_state.target_idx]

    q_col1, q_col2 = st.columns([2, 1])

    with q_col1:
        fig_q, ax_q = plt.subplots(figsize=(8, 8))
        if level == "レベル1: 地方あて":
            # 地方全体をオレンジに塗る
            q_color_dict = {p: "orange" for p in df[df['region'] == target['region']]['name']}
        else:
            # ターゲットの県だけ赤く塗る
            q_color_dict = {target['name']: "red"}

        ax_q.imshow(picture(q_color_dict))
        ax_q.axis('off')
        st.pyplot(fig_q)

    with q_col2:
        if level == "レベル1: 地方あて":
            st.subheader("オレンジ色の場所は何地方かな？")
            ans = st.selectbox("答えをえらんでね", ["（えらんでね）", "北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"])
            correct_ans = target['region']

        elif level == "レベル2: 地方を限定して都道府県あて":
            quiz_region = st.selectbox("特訓したい地方をえらんでね", ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"])
            # 選んだ地方に合わせて問題を出し直す
            if target['region'] != quiz_region:
                region_prefs = df[df['region'] == quiz_region].index.tolist()
                st.session_state.target_idx = random.choice(region_prefs)
                st.rerun()

            st.subheader(f"【{quiz_region}地方】の赤い県はどこかな？")
            ans = st.selectbox("答えをえらんでね", ["（えらんでね）"] + sorted(df[df['region'] == quiz_region]['name'].tolist()))
            correct_ans = target['name']

        else: # レベル3
            st.subheader("全国のなかから答えよう！この赤い県はどこ？")
            ans = st.selectbox("答えをえらんでね", ["（えらんでね）"] + sorted(df['name'].tolist()))
            correct_ans = target['name']

        if st.button("ヒントをみる"):
            st.info(f"ヒント：{target['hint']}")

        if st.button("こうげき！"):
            if ans == correct_ans:
                st.balloons()
                st.success(f"せいかい！ これは「{correct_ans}」だよ！")
                st.session_state.score += 1
                st.session_state.target_idx = random.randint(0, 46)
                st.button("つぎの問題へ")
            elif ans == "（えらんでね）":
                st.warning("答えをえらんでね！")
            else:
                st.error("ざんねん！左の地図を見て「おぼえる」タブで確認してみよう。")
                st.session_state.score = 0
