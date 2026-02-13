import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 基本設定 ---
st.set_page_config(page_title="美.design 人材トリアージApp", layout="wide", page_icon="💎")
# --- デザインの適用 (CSS) ---
# --- デザインの適用 (CSS: 青×白スタイル) ---
# --- デザインの適用 (青×白・ブラッシュアップ版) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    
    /* --- 基本設定 --- */
    .stApp { background-color: #f0f4f8; font-family: 'Noto Sans JP', sans-serif; }
    
    /* --- ヘッダー（シャドウ強化） --- */
    .main-header {
        background: linear-gradient(135deg, #0056b3, #007bff);
        padding: 20px 25px; border-radius: 15px; 
        box-shadow: 0 10px 20px rgba(0,86,179,0.15); margin-bottom: 30px;
    }
    .main-header h1 { color: white !important; margin: 0; font-size: 1.6rem; }

    /* --- 店舗選択・入力欄（白背景・黒文字・シャドウ） --- */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: white !important;
        color: #000000 !important;
        border-radius: 10px !important;
        border: 1px solid #dbe9f5 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    /* 選択中の文字色も黒に固定 */
    div[data-baseweb="select"] * { color: #000000 !important; }

    /* --- スタッフカード（シャドウ強化・丸み） --- */
    .staff-card {
        background: white; padding: 22px; border-radius: 18px; 
        box-shadow: 0 12px 24px rgba(0,0,0,0.07); /* シャドウを深めに */
        border: 1px solid #eef2f6; transition: 0.3s;
    }
    .staff-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }

    /* --- トリアージバッジ（丸みを最大に：ピル型） --- */
    .triage-badge {
        display: inline-block; padding: 6px 16px; 
        border-radius: 50px !important; /* ここでしっかり丸みを出します */
        font-size: 0.85rem; font-weight: 700; color: white; margin-top: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .badge-red { background-color: #FF4D4D; }
    .badge-yellow { background-color: #FFC107; color: #000000 !important; }
    .badge-green { background-color: #2ECC71; }
    .badge-blue { background-color: #3498DB; }

    /* --- メモ欄 --- */
    .staff-memo {
        background-color: #f8fbff; padding: 14px; border-radius: 12px;
        font-size: 0.95rem; color: #000000 !important;
        margin-top: 15px; border-left: 5px solid #0056b3;
    }

    /* --- 更新ボタン・アコーディオン（文字色を黒に） --- */
    /* st.expanderの見出しテキストを黒に固定 */
    .st-ae summary p { color: #000000 !important; font-weight: bold !important; }
    
    .stButton > button {
        background: linear-gradient(to bottom, #0069d9, #0056b3);
        border: none; border-radius: 10px; padding: 12px;
        box-shadow: 0 6px 15px rgba(0,86,179,0.2); color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. データベースの初期化（仮）---
if 'staff_db' not in st.session_state:
    stores = ["京都店", "表参道店", "新宿店", "心斎橋店", "銀座店"]
    triage_levels = ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"]
    initial_data = []
    # サンプルデータ作成（実際は空で始めてもOK）
    for i, store in enumerate(stores):
        for j in range(1, 7):
            level = triage_levels[(i+j)%4]
            initial_data.append({
                "ID": f"{store}_{j}", "店舗名": store, "氏名": f"スタッフ {store[0]}{j}",
                "現在のトリアージ": level, "先月の状態": triage_levels[(i+j+1)%4].split("：")[0],
                "店長のメモ": "ここに日々の変化を記録します。", "最終更新日": datetime.now().strftime("%Y-%m-%d")
            })
    st.session_state.staff_db = pd.DataFrame(initial_data)

# --- 4. メイン画面 ---
# ヘッダー
st.markdown('<div class="main-header"><h1>💎 美.design 人材トリアージApp</h1></div>', unsafe_allow_html=True)

# 店舗選択と集計バッジ
col1, col2 = st.columns([2, 3])
with col1:
    selected_store = st.selectbox("表示店舗を選択：", st.session_state.staff_db["店舗名"].unique())
with col2:
    # 集計
    df = st.session_state.staff_db[st.session_state.staff_db["店舗名"] == selected_store]
    counts = {"赤":0, "黄":0, "緑":0, "青":0}
    for t in df["現在のトリアージ"]:
        if "赤" in t: counts["赤"]+=1
        elif "黄" in t: counts["黄"]+=1
        elif "緑" in t: counts["緑"]+=1
        elif "青" in t: counts["青"]+=1
    
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; gap: 10px; padding-top: 20px;">
            <span class="triage-badge badge-red">🔴 赤: {counts['赤']}</span>
            <span class="triage-badge badge-yellow">🟡 黄: {counts['黄']}</span>
            <span class="triage-badge badge-green">🟢 緑: {counts['緑']}</span>
            <span class="triage-badge badge-blue">🔵 青: {counts['青']}</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# スタッフカード表示
st.subheader(f"👥 {selected_store} スタッフ一覧")
cols = st.columns(3)

for idx, row in df.iterrows():
    with cols[idx % 3]:
        # 色クラスの判定
        if "赤" in row["現在のトリアージ"]: color_cls = "triage-red"; badge_cls = "badge-red"
        elif "黄" in row["現在のトリアージ"]: color_cls = "triage-yellow"; badge_cls = "badge-yellow"
        elif "緑" in row["現在のトリアージ"]: color_cls = "triage-green"; badge_cls = "badge-green"
        else: color_cls = "triage-blue"; badge_cls = "badge-blue"

        # カード本体
        st.markdown(f"""
            <div class="staff-card {color_cls}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin:0;">{row['氏名']}</h4>
                    <small style="color: #888; background: #eee; padding: 2px 8px; border-radius: 4px;">先月: {row['先月の状態']}</small>
                </div>
                <div><span class="triage-badge {badge_cls}">{row['現在のトリアージ']}</span></div>
                <div class="staff-memo">{row['店長のメモ']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 更新ボタン（モーダル風）
        with st.expander(f"🔄 {row['氏名']} の状態を更新・メモ入力"):
            new_status = st.selectbox("現在の状態", ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"], key=f"s_{row['ID']}")
            new_memo = st.text_area("店長の関わり方・経過メモ", value=row["店長のメモ"], height=100, key=f"m_{row['ID']}")
            
            if st.button("この内容で保存", key=f"b_{row['ID']}"):
                st.session_state.staff_db.loc[st.session_state.staff_db["ID"] == row["ID"], ["現在のトリアージ", "店長のメモ", "最終更新日"]] = [new_status, new_memo, datetime.now().strftime("%Y-%m-%d")]
                st.success("更新しました！")
                st.rerun()
