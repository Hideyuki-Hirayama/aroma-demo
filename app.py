# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from data import SYMPTOMS, OILS, SCORE_TABLE  # ← ここを簡素化（OIL_TO_CATEGORIES等は不要）
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
        alcohol = st.selectbox("お酒は飲みますか？", ["いいえ", "はい"])
        coffee = st.selectbox("コーヒーは好きですか？", ["いいえ", "はい"])
    with col2:
        sweets = st.selectbox("甘いものは好きですか？", ["いいえ", "はい"])
        dislike_perfume = st.selectbox("香水は嫌いですか？", ["いいえ", "はい"])
        # ここを「苦手な精油」に変更
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

    st.subheader("結果")

    # ランキング表（系統列は削除）
    df_rank = pd.DataFrame([
        {"精油": oil, "スコア": score}
        for (oil, score) in res.get("ranking", [])
    ])
    if not df_rank.empty:
        st.markdown("**候補ランキング**")
        st.dataframe(df_rank, use_container_width=True)

    # ブレンド結果
    if "error" in res:
        st.error(res["error"])
    else:
        st.success("ブレンドが決定しました。")
        blend_df = pd.DataFrame([{"精油": oil, "滴数": drops} for oil, drops in res["blend"]])
        st.table(blend_df)
        st.caption(res["rule"])
        if "note" in res:
            st.info(res["note"])

    # 安全に関する注意（最低限）
    st.divider()
    st.caption("""
**注意**: 本提案はデモです。既往・服薬・妊娠授乳・小児/高齢者・皮膚疾患等がある場合は、使用可否や希釈率を専門家に確認してください。目に入らないように注意してください。異常時は中止してください。医療判断を置き換えるものではありません。
""")

# 参考：スコア表を確認できるように（列は精油のみ）
with st.expander("スコア表（症状×精油）を表示", expanded=False):
    st.dataframe(
        pd.DataFrame(SCORE_TABLE).T[["ラベンダー","オレンジ","ゼラニウム","フランキンセンス"]],
        use_container_width=True
    )
