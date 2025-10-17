# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from data import SYMPTOMS, OILS, SCORE_TABLE
from logic import pick_blend

st.set_page_config(page_title="アロマ・ブレンド提案（デモ）", page_icon="🫧", layout="centered")

st.title("🫧 アロマブレンド提案（デモ版）")
st.caption("症状に対しておすすめの精油ブレンドと滴数を提案します。")

with st.expander("このデモのルール", expanded=False):
    st.markdown("""
- 症状（単一選択）からおすすめの精油を提案します。**苦手な精油**は提案から除外します。
- スコア表（症状×精油）から上位2種を抽出。
- 年齢/性別/嗜好/アレルギー等は今回のデモでは使用しない（患者用では使用）。
    """)

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
        disliked_oils = st.multiselect("苦手な香り（任意）", OILS, default=[])
        allergy = st.text_input("アレルギーはありますか？（任意で記入）")

    symptom = st.selectbox(
        "今一番困っている症状",
        SYMPTOMS,
        index=SYMPTOMS.index("肩こり") if "肩こり" in SYMPTOMS else 0
    )

    submitted = st.form_submit_button("ブレンドを提案する 🔮")

# --- 実行 ---
if submitted:
    res = pick_blend(symptom, disliked_oils)

    # 結果は「滴数のみ」表示
    if "error" in res:
        st.error(res["error"])
    else:
        blend_df = pd.DataFrame([{"精油": oil, "滴数": drops} for oil, drops in res["blend"]])
        st.table(blend_df)

    # 注意書き（最低限）
    st.divider()

