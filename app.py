# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from data import SYMPTOMS, OILS, SCORE_TABLE  # ← ここを簡素化（OIL_TO_CATEGORIES等は不要）
from logic import pick_blend

st.set_page_config(page_title="アロマ・ブレンド提案（デモ）", page_icon="🫧", layout="centered")

st.title("🫧 アロマ・ブレンド提案（デモ版）")
st.caption("症状と“苦手な精油”だけで、上位2種の精油と滴数を自動提案します。")

with st.expander("このデモのルール", expanded=False):
    st.markdown("""
- 入力は**症状（単一選択）**。**苦手な精油**は提案から除外します。
- スコア表（症状×精油）から上位2種を抽出。
- **スコア差が2以上**: 上位=3滴、2位=1滴。**差が2未満**: 2滴ずつ。
- 1種しか残らなければ**単独4滴**。0種なら「該当なし」。
- 年齢/性別/嗜好/アレルギー等は今回のデモではロジックに未使用（将来拡張用）。
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
        disliked_oils = st.mult_
