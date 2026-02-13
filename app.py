import streamlit as st
import pandas as pd
from datetime import datetime

# 画面の設定
st.set_page_config(page_title="美.design 人材トリアージ", layout="wide")

# スタイル調整
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #2c3e50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- データベースの初期化 ---
if 'staff_db' not in st.session_state:
    stores = ["京都店", "表参道店", "新宿店", "心斎橋店", "銀座店"]
    initial_data = []
    for store in stores:
        for i in range(1, 8):
            initial_data.append({
                "ID": f"{store}_{i}",
                "店舗名": store,
                "氏名": f"スタッフ {store[0]}{i}",
                "現在のトリアージ": "🟢 緑：任せてOK",
                "先月の状態": "🟡 黄",
                "店長のメモ": "ここに変化を記録します。",
                "最終更新日": datetime.now().strftime("%Y-%m-%d")
            })
    st.session_state.staff_db = pd.DataFrame(initial_data)

st.title("💎 美.design 人材トリアージ管理")

selected_store = st.selectbox("表示する店舗を選択してください", st.session_state.staff_db["店舗名"].unique())
df = st.session_state.staff_db[st.session_state.staff_db["店舗名"] == selected_store]

st.subheader(f"👥 {selected_store} スタッフ一覧")
cols = st.columns(3)

for idx, row in df.iterrows():
    with cols[idx % 3]:
        color = "#dc3545" if "赤" in row["現在のトリアージ"] else "#ffc107" if "黄" in row["現在のトリアージ"] else "#198754" if "緑" in row["現在のトリアージ"] else "#0d6efd"
        st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 12px; border-left: 5px solid {color}; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <h4 style="margin-bottom:0;">{row['氏名']}</h4>
                <small style="color: #888;">先月: {row['先月の状態']}</small>
                <div style="margin: 10px 0;"><span style="background: {color}; color: {'white' if color != '#ffc107' else 'black'}; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">{row['現在のトリアージ']}</span></div>
                <p style="font-size: 0.85rem; color: #555; background: #f9f9f9; padding: 10px; border-radius: 5px;">{row['店長のメモ']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander(f"{row['氏名']} の更新"):
            new_status = st.selectbox("現在の状態", ["🔴 赤：今すぐ介入", "🟡 黄：育成・伴走", "🟢 緑：任せてOK", "🔵 青：次の店長候補"], key=f"status_{row['ID']}")
            new_memo = st.text_area("メモ", value=row["店長のメモ"], key=f"memo_{row['ID']}")
            if st.button("保存", key=f"btn_{row['ID']}"):
                st.session_state.staff_db.loc[st.session_state.staff_db["ID"] == row["ID"], ["現在のトリアージ", "店長のメモ"]] = [new_status, new_memo]
                st.success("更新完了！")
                st.rerun()
