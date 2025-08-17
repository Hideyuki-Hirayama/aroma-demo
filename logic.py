# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple
from data import SCORE_TABLE

def pick_blend(symptom: str, disliked_oils: List[str], diff_threshold: int = 2):
    """
    単一の症状に対して、苦手な精油を除外後、上位2種と滴数を返す。
    """
    row: Dict[str, int] = SCORE_TABLE.get(symptom, {})
    if not row:
        return {"error": f"未知の症状です: {symptom}"}

    # 苦手を除外
    scored: List[Tuple[str, int]] = [(oil, sc) for oil, sc in row.items() if oil not in disliked_oils]

    # スコア降順、同点は名前順
    ranked = sorted(scored, key=lambda x: (-x[1], x[0]))

    result = {
        "ranking": ranked,
        "blend": [],
        "rule": f"差>={diff_threshold} なら 3滴/1滴、差<{diff_threshold} なら 2滴/2滴（合計4滴）"
    }

    if len(ranked) == 0:
        result["error"] = "該当精油がありません（苦手な精油の見直しをご検討ください）"
        return result

    if len(ranked) == 1:
        oil1, _ = ranked[0]
        result["blend"] = [(oil1, 4)]
        result["note"] = "1種類のみのため単独4滴としました。"
        return result

    (o1, s1), (o2, s2) = ranked[0], ranked[1]
    drops = (3, 1) if (s1 - s2) >= diff_threshold else (2, 2)
    result["blend"] = [(o1, drops[0]), (o2, drops[1])]
    return result
