import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 基本設定 ---
st.set_page_config(page_title="美.design 人材トリアージApp", layout="wide", page_icon="💎")

# --- 2. ユーザー管理 ---
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
            input { caret-color: #1a2a3a !important; }
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

# --- 4. デザイン設定 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    
    .stApp { background-color: #f4f9ff; font-family: 'Noto Sans JP', sans-serif; }
    h1, h2, h3, h4, h5, p, span, label, div { color: #1a2a3a !important; }

    /* サイドバー */
    section[data-testid="stSidebar"] {
        min-width: 300px !important;
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

    /* スタッフカード */
    .staff-card {
        background: #ffffff; padding: 20px;
        border-radius: 20px; border: 1px solid #e1eaf2;
        box-shadow: 0 10px 25px rgba(26, 42, 58, 0.05); margin-bottom: 20px;
        position: relative; transition: transform 0.2s;
    }
    .staff-card:hover { transform: translateY(-5px); }

    /* 入力フォーム */
    input, textarea, select, div[data-baseweb="select"] > div {
        background-color: #ffffff !important; 
        color: #1a2a3a !important; 
        caret-color: #1a2a3a !important;
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

    /* --- スタイリッシュなボタン --- */
    div.stButton > button {
        background: linear-gradient(135deg, #0061ff 0%, #60efff 100%) !important;
        color: white !important; border: none !important;
        border-radius: 50px !important; padding: 0.5rem 1.2rem !important;
        font-weight: bold !important; letter-spacing: 0.05em !important;
        box-shadow: 0 4px 15px rgba(0, 97, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(0, 97, 255, 0.5) !important;
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

# --- 6. ポップアップ編集画面の定義 (st.dialog) ---
@st.dialog("📝 スタッフ評価の編集")
def edit_dialog(row, idx):
    st.markdown(f"**{row['店舗名']} / {row['氏名']}** さんの評価を更新します。")
    
    # 入力フォーム
    new_status = st.selectbox("現在の状態", 
        ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"],
        index=["🔴" in row["現在のトリアージ"], "🟡" in row["現在のトリアージ"], "🟢" in row["現在のトリアージ"], "🔵" in row["現在のトリアージ"]].index(True)
    )
    new_memo = st.text_area("店長メモ", value=row["店長のメモ"], height=150)
    
    # 保存ボタン
    if st.button("保存して閉じる", use_container_width=True):
        # 演出
        if "🔵" in new_status and "🔵" not in row["現在のトリアージ"]: st.balloons()
        elif "🟢" in new_status and "🟢" not in row["現在のトリアージ"]: st.snow()
        
        # データ更新
        st.session_state.staff_db.loc[idx, ["現在のトリアージ", "店長のメモ", "最終更新日"]] = [new_status, new_memo, datetime.now().strftime("%Y-%m-%d")]
        st.rerun()

# --- 7. サイドバー ---
with st.sidebar:
    st.markdown("### ⚙️ 管理メニュー")
    
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

    if user["role"] == "admin":
        with st.expander("🗑️ スタッフ削除 (管理者)"):
            del_target = st.selectbox("削除対象", st.session_state.staff_db["氏名"], key="del_unique")
            if st.button("削除実行", key="del_btn"):
                st.session_state.staff_db = st.session_state.staff_db[st.session_state.staff_db["氏名"] != del_target]
                st.rerun()

    st.markdown("<br>" * 15, unsafe_allow_html=True) 
    st.markdown("---") 
    if st.button("ログアウト", key="logout_btn"):
        st.session_state.user_info = None
        st.rerun()

# --- 8. メイン画面 ---
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
            # バッジ判定
            t_str = row["現在のトリアージ"]
            if "赤" in t_str: b_cls = "badge-red"
            elif "黄" in t_str: b_cls = "badge-yellow"
            elif "緑" in t_str: b_cls = "badge-green"
            else: b_cls = "badge-blue"
            
            # カード表示
            st.markdown(f"""
                <div class="staff-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin:0;">{row['氏名']}</h4>
                        <span style="font-size: 0.75rem; color: #888; background: #f0f0f0; padding: 3px 8px; border-radius: 5px;">先月: {row['先月の状態']}</span>
                    </div>
                    <span class="triage-badge {b_cls}">{row['現在のトリアージ']}</span>
                    <div style="background-color: #f0f7ff; padding: 15px; border-radius: 12px; font-size: 0.9rem; margin-top: 15px; border-left: 5px solid #0056b3; margin-bottom: 15px;">
                        {row['店長のメモ']}
                    </div>
                    <div style="text-align: right; font-size: 0.7rem; color: #aaa; margin-bottom: 10px;">最終更新: {row['最終更新日']}</div>
                </div>
            """, unsafe_allow_html=True)

            # ポップアップを呼び出すボタン（ここが修正箇所です）
            if st.button("編集する", key=f"edit_{row['ID']}", use_container_width=True):
                edit_dialog(row, original_idx)
