import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 基本設定 ---
st.set_page_config(page_title="美.design 人材トリアージApp", layout="wide", page_icon="💎")

# --- 2. ユーザー管理（IDとパスワードと権限の台帳） ---
USERS = {
    "manager": {"pass": "admin9999", "role": "admin", "assigned_store": "全店舗"},
    "kyoto":   {"pass": "kyoto001",  "role": "store", "assigned_store": "京都店"},
    "omote":   {"pass": "omote002",  "role": "store", "assigned_store": "表参道店"},
    "shinjuku":{"pass": "shin003",   "role": "store", "assigned_store": "新宿店"},
}

# --- 3. ログイン機能 ---
def check_login():
    if "user_info" not in st.session_state:
        st.session_state.user_info = None

    if st.session_state.user_info is None:
        st.markdown("""
            <style>
            .stApp { background-color: #f4f9ff; }
            /* ログイン画面の入力カーソルも見やすく */
            input { caret-color: #000000 !important; }
            </style>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center;'><h1>💎 美.design Login</h1></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("ユーザーID", placeholder="例: manager")
            password = st.text_input("パスワード", type="password")
            
            if st.button("ログイン", use_container_width=True):
                if username in USERS and USERS[username]["pass"] == password:
                    st.session_state.user_info = USERS[username]
                    st.rerun()
                else:
                    st.error("IDまたはパスワードが違います")
        return False
    return True

if not check_login():
    st.stop()

user = st.session_state.user_info

# --- 4. デザイン適用 (カーソル修正済み) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    
    .stApp { background-color: #f4f9ff; font-family: 'Noto Sans JP', sans-serif; }
    h1, h2, h3, h4, h5, p, span, label, div { color: #1a2a3a !important; }

    /* サイドバー */
    section[data-testid="stSidebar"] {
        background: rgba(240, 248, 255, 0.9) !important;
        backdrop-filter: blur(12px); border-right: 1px solid white;
    }

    /* ヘッダー */
    .main-header {
        background: linear-gradient(135deg, #0056b3 0%, #007bff 100%);
        padding: 20px 30px; border-radius: 15px; 
        box-shadow: 0 10px 20px rgba(0, 86, 179, 0.15); margin-bottom: 30px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .main-header h1 { color: #ffffff !important; margin: 0; font-size: 1.5rem; }
    .user-status { color: white !important; font-size: 0.9rem; background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px;}

    /* カードデザイン */
    .staff-card {
        background: #ffffff; padding: 25px 25px 5px 25px;
        border-radius: 20px 20px 0 0; border: 1px solid #e1eaf2; border-bottom: none;
        margin-bottom: -16px !important; position: relative; z-index: 1;
    }
    
    /* Expanderデザイン */
    [data-testid="stExpander"] {
        background-color: #ffffff !important; border: 1px solid #e1eaf2; border-top: none;
        border-radius: 0 0 20px 20px; box-shadow: 0 10px 25px rgba(26, 42, 58, 0.05); margin-top: 0 !important;
    }
    [data-testid="stExpander"] summary { color: #5a6a7a !important; background-color: #ffffff !important; padding-left: 25px; }
    [data-testid="stExpander"] summary:hover { color: #0056b3 !important; }

    /* --- 【修正】入力フォームの設定 --- */
    input, textarea, select, div[data-baseweb="select"] > div {
        background-color: #ffffff !important; 
        color: #1a2a3a !important; 
        caret-color: #1a2a3a !important; /* ★ここが修正ポイント：カーソルを黒くする！ */
        border-color: #dbe9f5 !important;
    }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }

    /* バッジ */
    .triage-badge {
        display: inline-block; padding: 6px 15px; border-radius: 50px;
        font-size: 0.8rem; font-weight: bold; color: #ffffff !important;
        margin-top: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    span.badge-red { background-color: #FF4D4D !important; color: white !important; }
    span.badge-green { background-color: #2ECC71 !important; color: white !important; }
    span.badge-blue { background-color: #3498DB !important; color: white !important; }
    span.badge-yellow { background-color: #FFC107 !important; color: #1a2a3a !important; }

    /* ボタン */
    div.stButton > button {
        background: linear-gradient(135deg, #0061ff 0%, #60efff 100%) !important;
        color: white !important; border: none !important;
        border-radius: 50px !important; padding: 0.6rem 1.5rem !important;
        font-weight: bold !important; letter-spacing: 0.05em !important;
        box-shadow: 0 4px 15px rgba(0, 97, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(0, 97, 255, 0.5) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 10px rgba(0, 97, 255, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. データ初期化 ---
this_month = datetime.now().strftime("%Y年%m月")

if 'staff_db' not in st.session_state:
    stores = ["京都店", "表参道店", "新宿店", "心斎橋店", "銀座店"]
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

# --- 6. サイドバー ---
with st.sidebar:
    st.markdown("### ⚙️ 管理メニュー")
    
    # 新規追加
    with st.expander("➕ 新規スタッフ追加", expanded=True):
        new_name = st.text_input("氏名", placeholder="氏名を入力")
        
        if user["role"] == "admin":
            new_store = st.selectbox("店舗", st.session_state.staff_db["店舗名"].unique())
        else:
            new_store = user["assigned_store"]
            st.info(f"店舗: {new_store}")

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

    # 削除機能 (管理者のみ)
    if user["role"] == "admin":
        with st.expander("🗑️ スタッフ削除 (管理者)"):
            del_target = st.selectbox("削除対象", st.session_state.staff_db["氏名"], key="delete_select_unique")
            if st.button("削除実行", key="del_btn"):
                st.session_state.staff_db = st.session_state.staff_db[st.session_state.staff_db["氏名"] != del_target]
                st.rerun()

    # レイアウト調整（ログアウトボタンを下へ）
    st.markdown("<br>" * 15, unsafe_allow_html=True) 
    st.markdown("---") 

    if st.button("ログアウト", key="logout_btn"):
        st.session_state.user_info = None
        st.rerun()

# --- 7. メイン画面 ---
st.markdown(f"""
    <div class="main-header">
        <h1>💎 美.design 人材トリアージApp</h1>
        <span class="user-status">👤 {user['assigned_store']} ({user['role']})</span>
    </div>
    """, unsafe_allow_html=True)

if user["role"] == "admin":
    selected_store = st.selectbox("表示店舗：", st.session_state.staff_db["店舗名"].unique())
else:
    selected_store = user["assigned_store"]
    st.markdown(f"### 🏠 {selected_store} のスタッフ一覧")

df = st.session_state.staff_db[st.session_state.staff_db["店舗名"] == selected_store]

st.subheader(f"👥 {selected_store} 一覧")
cols = st.columns(3)

if len(df) == 0:
    st.info("スタッフがまだ登録されていません。")
else:
    for idx, (original_idx, row) in enumerate(df.iterrows()):
        with cols[idx % 3]:
            # バッジクラス
            t_str = row["現在のトリアージ"]
            if "赤" in t_str: b_cls = "badge-red"
            elif "黄" in t_str: b_cls = "badge-yellow"
            elif "緑" in t_str: b_cls = "badge-green"
            else: b_cls = "badge-blue"
            
            st.markdown(f"""
                <div class="staff-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin:0;">{row['氏名']}</h4>
                        <span style="font-size: 0.75rem; color: #888; background: #f0f0f0; padding: 3px 8px; border-radius: 5px;">先月: {row['先月の状態']}</span>
                    </div>
                    <span class="triage-badge {b_cls}">{row['現在のトリアージ']}</span>
                    <div style="background-color: #f0f7ff; padding: 15px; border-radius: 12px; font-size: 0.9rem; margin-top: 15px; border-left: 5px solid #0056b3;">
                        {row['店長のメモ']}
                    </div>
                    <div style="text-align: right; font-size: 0.7rem; color: #aaa; margin-top: 5px;">最終更新: {row['最終更新日']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("編集"):
                new_status = st.selectbox("評価更新", ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"], key=f"s_{row['ID']}", index=["🔴" in row["現在のトリアージ"], "🟡" in row["現在のトリアージ"], "🟢" in row["現在のトリアージ"], "🔵" in row["現在のトリアージ"]].index(True))
                new_memo = st.text_area("メモ", value=row["店長のメモ"], key=f"m_{row['ID']}")
                
                if st.button("保存する", key=f"b_{row['ID']}"):
                    if "🔵" in new_status and "🔵" not in row["現在のトリアージ"]: st.balloons()
                    elif "🟢" in new_status and "🟢" not in row["現在のトリアージ"]: st.snow()
                    st.session_state.staff_db.loc[original_idx, ["現在のトリアージ", "店長のメモ", "最終更新日"]] = [new_status, new_memo, datetime.now().strftime("%Y-%m-%d")]
                    st.rerun()
