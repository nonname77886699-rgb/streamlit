import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. 頁面基本設定
st.set_page_config(
    page_title="企業營運與氣候風險監控儀表板",
    page_icon="📊",
    layout="wide"
)

# 2. 模擬資料庫 (模擬各地區營運與氣候異常指數)
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=100, freq="D")
    regions = ["北美資料中心", "歐洲資料中心", "亞太製造基地"]
    
    data = []
    for date in dates:
        for region in regions:
            data.append({
                "日期": date,
                "營運據點": region,
                "營運營收_USD": np.random.randint(5000, 20000),
                "電力消耗_kWh": np.random.randint(10000, 50000),
                "極端氣候風險指數": np.round(np.random.uniform(1.0, 10.0), 1)
            })
    return pd.DataFrame(data)

df = load_data()

# 3. 側邊欄：動態篩選器 (等於 Power BI 切片器)
st.sidebar.header("🔍 數據篩選面板")
selected_regions = st.sidebar.multiselect(
    "選擇營運據點：",
    options=df["營運據點"].unique(),
    default=df["營運據點"].unique()
)

risk_threshold = st.sidebar.slider(
    "氣候風險預警門檻 (1-10)：",
    min_value=1.0,
    max_value=10.0,
    value=7.5
)

# 根據篩選條件過濾資料
filtered_df = df[
    (df["營運據點"].isin(selected_regions)) & 
    (df["極端氣候風險指數"] >= risk_threshold)
]

# 4. 主頁面標題與簡介
st.title("⚡ 跨國營運與氣候極端風險儀表板")
st.markdown("本報表動態整合各地區營運數據與氣候風險警示，協助管理者進行供應鏈與營運防護決策。")

st.divider()

# 5. 核心指標卡 (KPI Cards)
col1, col2, col3 = st.columns(3)

total_revenue = filtered_df["營運營收_USD"].sum()
total_power = filtered_df["電力消耗_kWh"].sum()
high_risk_count = len(filtered_df)

col1.metric("風險區間總營收", f"${total_revenue:,.0f}")
col2.metric("總電力耗用量", f"{total_power:,.0f} kWh")
col3.metric("高風險觸發天數", f"{high_risk_count} 天", delta_color="inverse")

# 6. 動態圖表 (Plotly 互動圖表)
st.subheader("📈 電力消耗與氣候風險趨勢")

fig = px.scatter(
    filtered_df,
    x="日期",
    y="電力消耗_kWh",
    size="極端氣候風險指數",
    color="營運據點",
    hover_name="營運據點",
    title="每日電力消耗 vs 氣候風險氣泡圖 (氣泡大小代表風險等級)",
    labels={"電力消耗_kWh": "電力消耗 (kWh)", "極端氣候風險指數": "風險指數"}
)

st.plotly_chart(fig, width='stretch')

# 7. 底層明細資料表
with st.expander("📄 檢視篩選後原始數據明細"):
    st.dataframe(filtered_df, width='stretch')