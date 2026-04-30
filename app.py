import streamlit as st
import matplotlib.pyplot as plt
from japanmap import picture
import pandas as pd
import random
import time
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# --- 1. データ準備 ---
data = {
    "name": ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"],
    "region": ["北海道", "東北", "東北", "東北", "東北", "東北", "東北", "関東", "関東", "関東", "関東", "関東", "関東", "関東", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "中部", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "近畿", "中国", "中国", "中国", "中国", "中国", "四国", "四国", "四国", "四国", "九州", "九州", "九州", "九州", "九州", "九州", "九州", "九州"],
    "hint": ["一番大きい！", "りんご1位", "わんこそば", "牛タン", "なまはげ", "さくらんぼ", "赤べこ", "納豆", "餃子", "焼きまんじゅう", "深谷ねぎ", "落花生", "首都", "中華街", "お米", "黒部ダム", "兼六園", "恐竜", "富士山", "お蕎麦", "白川郷", "お茶1位", "トヨタ", "伊勢神宮", "琵琶湖", "金閣寺", "たこ焼き", "姫路城", "公園の鹿", "みかんと梅", "砂丘", "出雲大社", "桃太郎", "厳島神社", "フグ", "阿波踊り", "うどん", "みかん", "坂本龍馬", "屋台ラーメン", "有田焼", "カステラ", "阿蘇山", "温泉", "マンゴー", "桜島", "美ら海"]
}
df = pd.DataFrame(data)

# --- ランキング管理用関数 ---
RANKING_FILE = "ranking_tenka.csv"

def load_ranking():
    if os.path.exists(RANKING_FILE):
        return pd.read_csv(RANKING_FILE)
    return pd.DataFrame(columns=["名前", "地方", "タイム(秒)"])

def save_ranking(name, region, score):
    rdf = load_ranking()
    new_data = pd.DataFrame([[name, region, round(score, 2)]], columns=["名前", "地方", "タイム(秒)"])
    rdf = pd.concat([rdf, new_data], ignore_index=True)
    rdf.to_csv(RANKING_FILE, index=False)

st.set_page_config(page_title="都道府県マスター", layout="wide")
st.title("🗾 都道府県マスターへの道")

# --- セッション状態の管理 ---
if 'target_idx' not in st.session_state:
    st.session_state.target_idx = random.randint(0, 46)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'tenka_start_time' not in st.session_state:
    st.session_state.tenka_start_time = None
if 'remaining_prefs' not in st.session_state:
    st.session_state.remaining_prefs = []
if 'tenka_status' not in st.session_state:
    st.session_state.tenka_status = "idle" # idle, playing, finished

# --- サイドバー：ランキング表示 ---
st.sidebar.header("🏆 天下統一ランキング")
rank_df = load_ranking()
view_reg = st.sidebar.selectbox("記録を見る地方", ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"], key="rank_view")
if not rank_df.empty:
    filtered_rank = rank_df[rank_df["地方"] == view_reg].sort_values(by="タイム(秒)").head(5)
    if not filtered_rank.empty:
        filtered_rank.index = range(1, len(filtered_rank)+1)
        st.sidebar.table(filtered_rank[["名前", "タイム(秒)"]])
    else:
        st.sidebar.write("まだ統一者がいません")

tab1, tab2, tab3 = st.tabs(["📖 地図でおぼえる", "🎯 クイズに挑戦", "⚔️ Level 天下統一"])

# --- タブ1: おぼえる ---
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
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(picture(color_dict))
        ax.axis('off')
        st.pyplot(fig)
        st.success(f"いま赤くなっているのが **【 {selected_pref} 】** だよ！")

# --- タブ2: クイズに挑戦 (通常モード) ---
with tab2:
    level = st.sidebar.selectbox("レベル", ["レベル1: 地方あて", "レベル2: 都道府県あて(地方限定)", "レベル3: 都道府県あて(全国)"])
    target = df.iloc[st.session_state.target_idx]
    q_col1, q_col2 = st.columns([2, 1])

    with q_col1:
        fig_q, ax_q = plt.subplots(figsize=(6, 6))
        q_color_dict = {p: "orange" for p in df[df['region'] == target['region']]['name']} if "レベル1" in level else {target['name']: "red"}
        ax_q.imshow(picture(q_color_dict))
        ax_q.axis('off')
        st.pyplot(fig_q)

    with q_col2:
        if "レベル1" in level:
            st.subheader("何地方かな？")
            ans = st.selectbox("答え", ["（えらんでね）", "北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"])
            correct_ans = target['region']
        elif "レベル2" in level:
            quiz_region = st.selectbox("特訓地方", ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"], key="q2")
            if target['region'] != quiz_region:
                st.session_state.target_idx = random.choice(df[df['region'] == quiz_region].index.tolist())
                st.rerun()
            st.subheader(f"【{quiz_region}】の赤い県は？")
            ans = st.selectbox("答え", ["（えらんでね）"] + sorted(df[df['region'] == quiz_region]['name'].tolist()))
            correct_ans = target['name']
        else:
            st.subheader("この赤い県はどこ？")
            ans = st.selectbox("答え", ["（えらんでね）"] + sorted(df['name'].tolist()))
            correct_ans = target['name']

        if st.button("こうげき！", key="normal_atk"):
            if ans == correct_ans:
                st.success("せいかい！")
                st.session_state.score += 1
                st.session_state.target_idx = random.randint(0, 46)
                st.rerun()
            else:
                st.error(f"ざんねん！正解は「{correct_ans}」だったよ！")
                st.session_state.score = 0

# --- タブ3: Level 天下統一 (タイムアタック) ---
with tab3:
    st.header("⚔️ 地方を統一せよ！タイムアタック")
    
    if st.session_state.tenka_status == "idle":
        u_name = st.text_input("軍師の名前を入力せよ", value="", placeholder="名前をいれてね")
        t_reg = st.selectbox("統一を目指す地方", ["東北", "関東", "中部", "近畿", "中国", "四国", "九州"])
        
        if st.button("⚔️ 出陣！"):
            if u_name.strip() == "":
                st.warning("名前を入力してください")
            else:
                st.session_state.tenka_user = u_name
                st.session_state.tenka_region = t_reg
                st.session_state.remaining_prefs = df[df['region'] == t_reg]['name'].tolist()
                random.shuffle(st.session_state.remaining_prefs)
                st.session_state.tenka_start_time = time.time()
                st.session_state.tenka_status = "playing"
                st.rerun()

    elif st.session_state.tenka_status == "playing":
        current_p = st.session_state.remaining_prefs[0]
        st.subheader(f"【{st.session_state.tenka_region}】を統一せよ！ 残り: {len(st.session_state.remaining_prefs)}県")
        
        t_col1, t_col2 = st.columns([2, 1])
        with t_col1:
            fig_t, ax_t = plt.subplots(figsize=(6, 6))
            ax_t.imshow(picture({current_p: "red"}))
            ax_t.axis('off')
            st.pyplot(fig_t)
        
        with t_col2:
            ans_t = st.selectbox("この県はどこ？", ["（えらんでね）"] + sorted(df[df['region'] == st.session_state.tenka_region]['name'].tolist()), key="tenka_ans")
            if st.button("決定！", key="tenka_btn"):
                if ans_t == current_p:
                    st.success(f"⭕️ 正解！ {current_p} 攻略！")
                    st.session_state.remaining_prefs.pop(0)
                    if not st.session_state.remaining_prefs:
                        st.session_state.tenka_end_time = time.time()
                        st.session_state.tenka_status = "finished"
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(f"❌ まちがい！ 正解は【{current_p}】だよ。")
                    st.info("正解するまで次に進めないぞ！がんばれ！")
                    # ここで st.rerun() をあえて行わないことで、間違いメッセージを表示したままにします

    elif st.session_state.tenka_status == "finished":
        final_time = st.session_state.tenka_end_time - st.session_state.tenka_start_time
        st.balloons()
        st.header(f"🎊 {st.session_state.tenka_region} 統一完了！")
        st.subheader(f"記録: {final_time:.2f} 秒")
        
        # 保存
        save_ranking(st.session_state.tenka_user, st.session_state.tenka_region, final_time)
        st.session_state.tenka_status = "idle"
        st.button("もう一度挑戦 / 他の地方へ")
