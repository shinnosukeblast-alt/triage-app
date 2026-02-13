import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 基本設定 ---
st.set_page_config(page_title="美.design 人材トリアージApp", layout="wide", page_icon="💎")

# --- 2. デザインの適用 (アイスブルー × ホワイト・プロフェッショナル版) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    
    /* 全体の背景：透明感のある非常に薄い青 */
    .stApp { background-color: #f4f9ff; font-family: 'Noto Sans JP', sans-serif; }
    
    /* テキストカラー：以前選定した深く品のあるチャコールネイビー */
    h1, h2, h3, h4, h5, p, label, .st-ae summary p { 
        color: #1a2a3a !important; 
        font-weight: 700 !important; 
    }

    /* --- サイドバー：ガラス風（アイスブルー・グラデーション） --- */
    section[data-testid="stSidebar"] {
        background: rgba(240, 248, 255, 0.6) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 5px 0 20px rgba(0, 86, 179, 0.05);
    }

    /* エクスパンダー（黒背景部分）の文字色を白に固定 */
    .st-ae summary p, .st-ae summary svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* --- メインヘッダー：信頼感のあるブルーグラデーション --- */
    .main-header {
        background: linear-gradient(135deg, #0056b3 0%, #007bff 100%);
        padding: 24px 30px; border-radius: 20px; 
        box-shadow: 0 12px 30px rgba(0, 86, 179, 0.2); margin-bottom: 15px;
    }
    .main-header h1 { color: #ffffff !important; margin: 0; font-size: 1.8rem; letter-spacing: 0.05em; }

    /* --- スタッフカード：清潔感のある白とソフトなシャドウ --- */
    .staff-card {
        background: #ffffff; padding: 26px; border-radius: 24px; 
        box-shadow: 0 10px 25px rgba(26, 42, 58, 0.04);
        border: 1px solid #e1eaf2; transition: all 0.3s ease; margin-bottom: 15px;
    }
    .staff-card:hover { transform: translateY(-5px); box-shadow: 0 18px 35px rgba(26, 42, 58, 0.1); }

    /* --- ボタン：きれいな薄い青のグラデーション（白文字） --- */
    .stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        border: none; border-radius: 14px; padding: 14px;
        box-shadow: 0 8px 20px rgba(79, 172, 254, 0.3); 
        color: #ffffff !important; font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 25px rgba(79, 172, 254, 0.5);
        filter: brightness(1.08);
    }

    /* トリアージバッジ（丸みを帯びたデザイン） */
    .triage-badge {
        display: inline-block; padding: 7px 18px; border-radius: 50px !important;
        font-size: 0.85rem; font-weight: 700; color: #ffffff !important; margin-top: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .badge-yellow { color: #1a2a3a !important; background-color: #FFC107; }
    
    /* メモエリア：アイスブルー背景 */
    .memo-container {
        background-color: #f0f7ff; padding: 18px; border-radius: 16px; 
        font-size: 0.95rem; color: #1a2a3a; margin-top: 18px; 
        border-left: 6px solid #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. データベースの初期化と月跨ぎ処理 ---
this_month = datetime.now().strftime("%Y年%m月")

if 'staff_db' not in st.session_state:
    stores = ["京都店", "表参道店", "新宿店", "心斎橋店", "銀座店"] # 37店舗展開中
    triage_levels = ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"]
    initial_data = []
    for store in stores:
        for j in range(1, 4):
            initial_data.append({
                "ID": f"{store}_{j}", "店舗名": store, "氏名": f"スタッフ {store[0]}{j}",
                "現在のトリアージ": triage_levels[1], "先月の状態": "🟡 黄",
                "店長のメモ": "日々の変化をここに記録。", "最終更新日": datetime.now().strftime("%Y-%m-%d"),
                "データ月": this_month
            })
    st.session_state.staff_db = pd.DataFrame(initial_data)

# --- 4. サイドバー：スタッフ管理 ---
with st.sidebar:
    st.markdown("<h2 style='margin-top:0;'>⚙️ 管理メニュー</h2>", unsafe_allow_html=True)
    with st.expander("➕ 新規スタッフ追加"):
        new_name = st.text_input("氏名", placeholder="氏名を入力")
        new_store = st.selectbox("配属店舗", ["京都店", "表参道店", "新宿店", "心斎橋店", "銀座店"])
        if st.button("追加実行", key="add_btn"):
            if new_name:
                new_entry = {
                    "ID": f"{new_store}_{datetime.now().timestamp()}",
                    "店舗名": new_store, "氏名": new_name,
                    "現在のトリアージ": "🟡 黄：育成・伴走", "先月の状態": "-",
                    "店長のメモ": "新規登録。", "最終更新日": datetime.now().strftime("%Y-%m-%d"),
                    "データ月": this_month
                }
                st.session_state.staff_db = pd.concat([st.session_state.staff_db, pd.DataFrame([new_entry])], ignore_index=True)
                st.rerun()

    with st.expander("🗑️ スタッフ消去"):
        del_target = st.selectbox("削除対象を選択", st.session_state.staff_db["氏名"])
        if st.button("削除実行", key="del_btn"):
            st.session_state.staff_db = st.session_state.staff_db[st.session_state.staff_db["氏名"] != del_target]
            st.rerun()

# --- 5. メイン画面 ---
st.markdown('<div class="main-header"><h1>💎 美.design 人材トリアージApp</h1></div>', unsafe_allow_html=True)
st.markdown(f'<div style="color: #0056b3; font-weight: bold; text-align: right; margin-bottom:15px; font-size: 1.1rem;">📅 評価月: {this_month}度</div>', unsafe_allow_html=True)

selected_store = st.selectbox("表示店舗：", st.session_state.staff_db["店舗名"].unique())
df = st.session_state.staff_db[st.session_state.staff_db["店舗名"] == selected_store]

st.subheader(f"👥 {selected_store} 一覧")
cols = st.columns(3)

for idx, (original_idx, row) in enumerate(df.iterrows()):
    with cols[idx % 3]:
        badge_cls = "badge-red" if "赤" in row["現在のトリアージ"] else "badge-yellow" if "黄" in row["現在のトリアージ"] else "badge-green" if "緑" in row["現在のトリアージ"] else "badge-blue"
        
        st.markdown(f"""
            <div class="staff-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin:0;">{row['氏名']}</h4>
                    <span style="font-size: 0.75rem; color: #5a6a7a; background: #eef4f9; padding: 4px 10px; border-radius: 8px;">先月: {row['先月の状態']}</span>
                </div>
                <div class="triage-badge {badge_cls}">{row['現在のトリアージ']}</div>
                <div class="memo-container">{row['店長のメモ']}</div>
                <div style="text-align: right; margin-top: 12px; font-size: 0.75rem; color: #5a6a7a;">最終更新: {row['最終更新日']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("編集"):
            new_status = st.selectbox("評価の更新", ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"], key=f"s_{row['ID']}", index=["🔴" in row["現在のトリアージ"], "🟡" in row["現在のトリアージ"], "🟢" in row["現在のトリアージ"], "🔵" in row["現在のトリアージ"]].index(True))
            new_memo = st.text_area("店長メモ", value=row["店長のメモ"], key=f"m_{row['ID']}", height=120)
            
            if st.button("保存する", key=f"b_{row['ID']}"):
                if "🔵" in new_status and "🔵" not in row["現在のトリアージ"]: st.balloons()
                elif "🟢" in new_status and "🟢" not in row["現在のトリアージ"]: st.snow()
                st.session_state.staff_db.loc[original_idx, ["現在のトリアージ", "店長のメモ", "最終更新日"]] = [new_status, new_memo, datetime.now().strftime("%Y-%m-%d")]
                st.rerun()
