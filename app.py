import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 基本設定 ---
st.set_page_config(page_title="美.design 人材トリアージApp", layout="wide", page_icon="💎")

# --- 2. デザインの適用 (CSS) ---
# --- デザインの適用 (CSS) ---
# --- デザインの適用 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    
    /* 全体の背景と文字色を黒に固定 */
    .stApp { 
        background-color: #F4F7F6; 
        font-family: 'Noto Sans JP', sans-serif;
        color: #000000 !important; /* 基本の文字を黒に */
    }

    /* 全ヘッダー（h1, h2, h3, h4）を黒に */
    h1, h2, h3, h4, .stMarkdown p { 
        color: #000000 !important; 
        font-weight: 700 !important; 
    }

    /* ヘッダー部分 */
    .main-header {
        background: white; padding: 15px 25px; border-radius: 12px; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    .main-header h1 { color: #000000 !important; }

    /* スタッフカード */
    .staff-card {
        background: white; padding: 20px; border-radius: 12px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #ddd;
    }

    /* メモ欄の文字を真っ黒に */
    .staff-memo {
        background-color: #F9F9F9; padding: 12px; border-radius: 8px;
        font-size: 0.95rem; 
        color: #000000 !important; /* ここをグレーから黒に変更 */
        margin-top: 15px; border-left: 4px solid #333;
    }

    /* 先月の状態ラベル */
    .last-month-label {
        color: #000000 !important;
        font-weight: bold;
    }

    /* トリアージバッジ（ここだけは読みやすさのため背景色に合わせて白文字を維持） */
    .badge-red, .badge-green, .badge-blue { color: white !important; }
    .badge-yellow { color: #000000 !important; } /* 黄色バッジだけは黒文字 */
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
