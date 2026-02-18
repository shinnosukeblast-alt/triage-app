import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 基本設定 ---
st.set_page_config(page_title="美.design 人材トリアージApp", layout="wide", page_icon="💎")

# --- 2. デザイン修正 (一体化・白背景・バッジ修正) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    
    .stApp { background-color: #f4f9ff; font-family: 'Noto Sans JP', sans-serif; }
    
    /* 全体の文字色を黒系に統一 */
    h1, h2, h3, h4, h5, p, span, label, div { 
        color: #1a2a3a !important; 
    }

    /* --- サイドバー --- */
    section[data-testid="stSidebar"] {
        background: rgba(240, 248, 255, 0.8) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid white;
    }

    /* --- メインヘッダー --- */
    .main-header {
        background: linear-gradient(135deg, #0056b3 0%, #007bff 100%);
        padding: 20px 30px; border-radius: 15px; 
        box-shadow: 0 10px 20px rgba(0, 86, 179, 0.15); margin-bottom: 30px;
    }
    .main-header h1 { color: #ffffff !important; margin: 0; font-size: 1.5rem; }

    /* --- スタッフカード (上半分) --- */
    .staff-card {
        background: #ffffff;
        padding: 25px 25px 5px 25px; /* 下の余白を極小に */
        border-top-left-radius: 20px;
        border-top-right-radius: 20px;
        border-bottom-left-radius: 0 !important; /* 下の角を直角に */
        border-bottom-right-radius: 0 !important;
        border: 1px solid #e1eaf2;
        border-bottom: none !important; /* 下線を消す */
        margin-bottom: -16px !important; /* ネガティブマージンで下の要素を引き上げる */
        position: relative;
        z-index: 1;
    }

    /* --- Expander (下半分・編集エリア) --- */
    /* StreamlitのExpanderの枠線をカスタマイズしてカードの下部に見せる */
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e1eaf2 !important;
        border-top: none !important; /* 上線を消す */
        border-bottom-left-radius: 20px !important;
        border-bottom-right-radius: 20px !important;
        border-top-left-radius: 0 !important;
        border-top-right-radius: 0 !important;
        box-shadow: 0 10px 25px rgba(26, 42, 58, 0.05);
        margin-top: 0 !important;
    }

    /* Expanderのヘッダー部分（「編集」の文字があるバー） */
    [data-testid="stExpander"] summary {
        color: #5a6a7a !important; /* 文字色をグレーに */
        background-color: #ffffff !important; /* 背景を白に！ */
        padding-left: 25px !important;
        border-radius: 0 !important;
        transition: color 0.3s;
    }
    [data-testid="stExpander"] summary:hover {
        color: #0056b3 !important; /* ホバー時は青 */
    }
    [data-testid="stExpander"] summary:focus {
        color: #0056b3 !important; 
    }
    /* 矢印アイコンの色 */
    [data-testid="stExpander"] summary svg {
        fill: #5a6a7a !important;
    }

    /* Expanderの中身（入力フォーム周り） */
    [data-testid="stExpander"] div[role="group"] {
        padding: 0 25px 25px 25px !important;
        background-color: #ffffff !important;
    }

    /* --- 入力フォームの完全白化 --- */
    /* 入力欄の背景を白、文字を黒に強制 */
    input, textarea, select, div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1a2a3a !important;
        border-color: #dbe9f5 !important;
    }
    /* ドロップダウンの選択肢背景 */
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
    }

    /* --- バッジ (色修正) --- */
    .triage-badge {
        display: inline-block; padding: 6px 15px; border-radius: 50px;
        font-size: 0.8rem; font-weight: bold; color: #ffffff !important;
        margin-top: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    /* 具体的なクラス定義 (優先度高) */
    span.badge-red { background-color: #FF4D4D !important; color: white !important; }
    span.badge-green { background-color: #2ECC71 !important; color: white !important; }
    span.badge-blue { background-color: #3498DB !important; color: white !important; }
    span.badge-yellow { background-color: #FFC107 !important; color: #1a2a3a !important; }

    /* メモ表示欄 */
    .memo-display {
        background-color: #f0f7ff; padding: 15px; border-radius: 12px;
        font-size: 0.9rem; color: #1a2a3a; margin-top: 15px;
        border-left: 5px solid #0056b3;
    }
    
    /* 保存ボタン */
    div.stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important; border: none; font-weight: bold;
        box-shadow: 0 4px 10px rgba(0, 150, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. データ初期化 ---
this_month = datetime.now().strftime("%Y年%m月")

if 'staff_db' not in st.session_state:
    stores = ["京都店", "表参道店", "新宿店", "心斎橋店", "銀座店"]
    triage_levels = ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"]
    initial_data = []
    for store in stores:
        for j in range(1, 4):
            initial_data.append({
                "ID": f"{store}_{j}", "店舗名": store, "氏名": f"スタッフ {store[0]}{j}",
                "現在のトリアージ": "🟡 黄：育成・伴走", "先月の状態": "🟡 黄",
                "店長のメモ": "日々の変化をここに記録。", "最終更新日": datetime.now().strftime("%Y-%m-%d"),
                "データ月": this_month
            })
    st.session_state.staff_db = pd.DataFrame(initial_data)

# --- 4. サイドバー ---
with st.sidebar:
    st.markdown("### ⚙️ 管理メニュー")
    with st.expander("➕ 新規スタッフ追加"):
        new_name = st.text_input("氏名", placeholder="氏名を入力")
        new_store = st.selectbox("配属店舗", ["京都店", "表参道店", "新宿店", "心斎橋店", "銀座店"])
        if st.button("追加実行", key="add"):
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
        del_target = st.selectbox("削除対象", st.session_state.staff_db["氏名"])
        if st.button("削除実行", key="del"):
            st.session_state.staff_db = st.session_state.staff_db[st.session_state.staff_db["氏名"] != del_target]
            st.rerun()

# --- 5. メイン画面 ---
st.markdown('<div class="main-header"><h1>💎 美.design 人材トリアージApp</h1></div>', unsafe_allow_html=True)

selected_store = st.selectbox("表示店舗：", st.session_state.staff_db["店舗名"].unique())
df = st.session_state.staff_db[st.session_state.staff_db["店舗名"] == selected_store]

st.subheader(f"👥 {selected_store} 一覧")
cols = st.columns(3)

for idx, (original_idx, row) in enumerate(df.iterrows()):
    with cols[idx % 3]:
        # バッジクラスの割り当て
        t_str = row["現在のトリアージ"]
        if "赤" in t_str: b_cls = "badge-red"
        elif "黄" in t_str: b_cls = "badge-yellow"
        elif "緑" in t_str: b_cls = "badge-green"
        else: b_cls = "badge-blue"
        
        # --- カード表示 (上部) ---
        st.markdown(f"""
            <div class="staff-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin:0;">{row['氏名']}</h4>
                    <span style="font-size: 0.75rem; color: #888; background: #f0f0f0; padding: 3px 8px; border-radius: 5px;">先月: {row['先月の状態']}</span>
                </div>
                <span class="triage-badge {b_cls}">{row['現在のトリアージ']}</span>
                <div class="memo-display">{row['店長のメモ']}</div>
                <div style="text-align: right; font-size: 0.7rem; color: #aaa; margin-top: 5px;">最終更新: {row['最終更新日']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # --- 編集エリア (下部) ---
        with st.expander("編集"):
            new_status = st.selectbox("評価更新", ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"], key=f"s_{row['ID']}", index=["🔴" in row["現在のトリアージ"], "🟡" in row["現在のトリアージ"], "🟢" in row["現在のトリアージ"], "🔵" in row["現在のトリアージ"]].index(True))
            new_memo = st.text_area("メモ", value=row["店長のメモ"], key=f"m_{row['ID']}")
            
            if st.button("保存する", key=f"b_{row['ID']}"):
                if "🔵" in new_status and "🔵" not in row["現在のトリアージ"]: st.balloons()
                elif "🟢" in new_status and "🟢" not in row["現在のトリアージ"]: st.snow()
                st.session_state.staff_db.loc[original_idx, ["現在のトリアージ", "店長のメモ", "最終更新日"]] = [new_status, new_memo, datetime.now().strftime("%Y-%m-%d")]
                st.rerun()
