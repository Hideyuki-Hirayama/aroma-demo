# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple
from data import SCORE_TABLE

def pick_blend(symptom: str, disliked_oils: List[str]):
    """
    単一の症状に対して、苦手な精油を除外後、
    上位2種を各3滴ずつ（合計6滴）で返す。
    """
    row: Dict[str, int] = SCORE_TABLE.get(symptom, {})
    if not row:
        return {"error": f"未知の症状です: {symptom}"}

    # 苦手な精油を除外
    scored: List[Tuple[str, int]] = [(oil, sc) for oil, sc in row.items() if oil not in disliked_oils]

    # スコア降順、同点は名前順
    ranked = sorted(scored, key=lambda x: (-x[1], x[0]))

    result = {
        "ranking": ranked,
        "blend": [],
        "rule": "上位2種を各3滴ずつブレンド（合計6滴）"
    }

    if len(ranked) == 0:
        result["error"] = "該当精油がありません（苦手な精油の見直しをご検討ください）"
        return result

    if len(ranked) == 1:
        oil1, _ = ranked[0]
        result["blend"] = [(oil1, 6)]
        result["note"] = "1種類のみのため単独6滴としました。"
        return result

    # 上位2つを各3滴
    (o1, _), (o2, _) = ranked[0], ranked[1]
    result["blend"] = [(o1, 3), (o2, 3)]
    return result
