# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from data import SYMPTOMS, OILS, SCORE_TABLE
from logic import pick_blend

st.set_page_config(page_title="アロマ・ブレンド提案（デモ）", page_icon="🫧", layout="centered")

st.title("🫧 アロマブレンド提案（デモ版）")
st.caption("症状に対しておすすめの精油ブレンドと滴数を提案します。")

# --- フォーム（入力） ---
st.subheader("質問票")
with st.form("input_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("年齢", min_value=0, max_value=120, value=40, step=1)
        sex = st.selectbox("性別", ["男性", "女性"])
        smoke = st.selectbox("たばこは吸いますか？", ["いいえ", "はい"])
        coffee = st.selectbox("コーヒーは好きですか？", ["いいえ", "はい"])
    with col2:
        sweets = st.selectbox("甘いものは好きですか？", ["いいえ", "はい"])
        perfume_like = st.selectbox("香水は好きですか？", ["いいえ", "はい"])
        disliked_oils = st.multiselect("苦手な香り（任意）", OILS, default=[])

    symptom = st.selectbox(
        "今一番困っている症状",
        SYMPTOMS,
        index=SYMPTOMS.index("肩こり") if "肩こり" in SYMPTOMS else 0
    )

    submitted = st.form_submit_button("ブレンドを提案する 🔮")

# --- 実行 ---
if submitted:
    res = pick_blend(symptom, disliked_oils)

    if "error" in res:
        st.error(res["error"])
    else:
        blend_df = pd.DataFrame([{"精油": oil, "滴数": drops} for oil, drops in res["blend"]])
        st.table(blend_df)
