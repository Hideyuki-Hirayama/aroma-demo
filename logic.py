# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple
from data import SCORE_TABLE, OIL_TO_CATEGORIES

def exclude_by_disliked_categories(oil: str, disliked_categories: List[str]) -> bool:
    cats = OIL_TO_CATEGORIES.get(oil, set())
    return any(cat in cats for cat in disliked_categories)

def pick_blend(symptom: str, disliked_categories: List[str], diff_threshold: int = 2):
    row: Dict[str, int] = SCORE_TABLE.get(symptom, {})
    if not row:
        return {"error": f"未知の症状です: {symptom}"}

    scored: List[Tuple[str, int]] = []
    for oil, sc in row.items():
        if not exclude_by_disliked_categories(oil, disliked_categories):
            scored.append((oil, sc))

    ranked = sorted(scored, key=lambda x: (-x[1], x[0]))

    result = {
        "ranking": ranked,
        "blend": [],
        "rule": f"差>={diff_threshold} なら 3滴/1滴、差<{diff_threshold} なら 2滴/2滴（合計4滴）"
    }

    if len(ranked) == 0:
        result["error"] = "該当精油がありません（嫌いな香りの系統の見直しをご検討ください）"
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
