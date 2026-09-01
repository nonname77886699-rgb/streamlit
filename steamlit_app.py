import streamlit as st
import pandas as pd

st.title("用Streamlit架設網站")

st.write("歡迎使用Streamlit！")

with st.sidebar:
    st.header("側邊欄")
    st.write("這裡可以放置篩選器或其他控制元件。")