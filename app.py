import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 基本設定 ---
st.set_page_config(page_title="美.design 人材トリアージApp", layout="wide", page_icon="💎")

# --- 2. デザインの適用 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    .stApp { background-color: #f0f4f8; font-family: 'Noto Sans JP', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #0056b3, #007bff);
        padding: 20px 25px; border-radius: 15px; 
        box-shadow: 0 10px 20px rgba(0,86,179,0.15); margin-bottom: 10px;
    }
    .main-header h1 { color: white !important; margin: 0; font-size: 1.6rem; }
    .evaluation-date { color: #0056b3; font-weight: bold; margin-bottom: 20px; text-align: right; }
    
    h1, h2, h3, h4, h5, .stMarkdown p, label, .st-ae summary p { color: #000000 !important; font-weight: 700 !important; }

    .staff-card {
        background: white; padding: 22px; border-radius: 18px; 
        box-shadow: 0 12px 24px rgba(0,0,0,0.07);
        border: 1px solid #eef2f6; transition: 0.3s; margin-bottom: 10px;
    }
    .triage-badge {
        display: inline-block; padding: 6px 16px; border-radius: 50px !important;
        font-size: 0.85rem; font-weight: 700; color: white; margin-top: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .badge-red { background-color: #FF4D4D; }
    .badge-yellow { background-color: #FFC107; color: #000000 !important; }
    .badge-green { background-color: #2ECC71; }
    .badge-blue { background-color: #3498DB; }

    .staff-memo {
        background-color: #f8fbff; padding: 14px; border-radius: 12px;
        font-size: 0.95rem; color: #000000 !important;
        margin-top: 15px; border-left: 5px solid #0056b3;
    }
    .update-date { font-size: 0.7rem; color: #666; text-align: right; margin-top: 5px; }

    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > textarea {
        background-color: white !important; color: #000000 !important;
        border-radius: 10px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. データベースの初期化と月跨ぎ処理 ---
# --- 3. データベースの初期化と月跨ぎ処理（エラー対策版） ---
this_month = datetime.now().strftime("%Y年%m月")

if 'staff_db' not in st.session_state:
    # 最初の1回目：データを作成
    stores = ["京都店", "表参道店", "新宿店", "心斎橋店", "銀座店"]
    triage_levels = ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"]
    initial_data = []
    for store in stores:
        for j in range(1, 4):
            initial_data.append({
                "ID": f"{store}_{j}", "店舗名": store, "氏名": f"スタッフ {store[0]}{j}",
                "現在のトリアージ": triage_levels[1], "先月の状態": "🟡 黄",
                "店長のメモ": "日々の変化を記録。", "最終更新日": "2026-01-31",
                "データ月": this_month # ここで新しい項目を追加
            })
    st.session_state.staff_db = pd.DataFrame(initial_data)

# 安全装置：もし古いデータが残っていて「データ月」という列がなかったら強制的に作る
if "データ月" not in st.session_state.staff_db.columns:
    st.session_state.staff_db["データ月"] = "2026年01月" # 仮の月を入れる

# 月跨ぎのチェック
last_recorded_month = st.session_state.staff_db["データ月"].iloc[0]
if last_recorded_month != this_month:
    st.session_state.staff_db["先月の状態"] = st.session_state.staff_db["現在のトリアージ"].apply(lambda x: x.split("：")[0])
    st.session_state.staff_db["データ月"] = this_month
    st.toast(f"月が変わりました。先月の評価を反映しました。")

# --- 4. サイドバー：スタッフ管理 ---
with st.sidebar:
    st.header("⚙️ 管理メニュー")
    with st.expander("➕ 新規スタッフ追加"):
        new_name = st.text_input("名前")
        new_store = st.selectbox("配属店舗", ["京都店", "表参道店", "新宿店", "心斎橋店", "銀座店"])
        if st.button("追加実行"):
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

    with st.expander("🗑️ スタッフ削除"):
        del_target = st.selectbox("削除する人", st.session_state.staff_db["氏名"])
        if st.button("削除実行"):
            st.session_state.staff_db = st.session_state.staff_db[st.session_state.staff_db["氏名"] != del_target]
            st.rerun()

# --- 5. メイン画面 ---
st.markdown('<div class="main-header"><h1>💎 美.design 人材トリアージApp</h1></div>', unsafe_allow_html=True)
st.markdown(f'<div class="evaluation-date">📅 現在の評価月: {this_month}度</div>', unsafe_allow_html=True)

selected_store = st.selectbox("表示店舗を選択：", st.session_state.staff_db["店舗名"].unique())
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
                    <span style="font-size: 0.75rem; color: #000; background: #eee; padding: 2px 8px; border-radius: 4px;">先月: {row['先月の状態']}</span>
                </div>
                <div class="triage-badge {badge_cls}">{row['現在のトリアージ']}</div>
                <div class="staff-memo">{row['店長のメモ']}</div>
                <div class="update-date">最終更新: {row['最終更新日']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("編集"):
            new_status = st.selectbox("状態更新", ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"], key=f"s_{row['ID']}", index=["🔴" in row["現在のトリアージ"], "🟡" in row["現在のトリアージ"], "🟢" in row["現在のトリアージ"], "🔵" in row["現在のトリアージ"]].index(True))
            new_memo = st.text_area("メモ", value=row["店長のメモ"], key=f"m_{row['ID']}")
            
            if st.button("保存", key=f"b_{row['ID']}"):
                if "🔵" in new_status and "🔵" not in row["現在のトリアージ"]: st.balloons()
                elif "🟢" in new_status and "🟢" not in row["現在のトリアージ"]: st.snow()
                
                st.session_state.staff_db.loc[original_idx, ["現在のトリアージ", "店長のメモ", "最終更新日"]] = [new_status, new_memo, datetime.now().strftime("%Y-%m-%d")]
                st.rerun()
