# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple
from data import SCORE_TABLE

def pick_blend(
    symptom: str,
    disliked_oils: List[str],
    diff_threshold: int = 2,
    total_drops: int = 4,   # ← 合計滴数をここで指定（デフォルト12）
):
    """
    単一の症状に対して、苦手な精油を除外後、上位2種と滴数を返す。
    滴数は 3:1 または 2:2 の比率を、合計 total_drops にスケールして割り当てます。
    """
    row: Dict[str, int] = SCORE_TABLE.get(symptom, {})
    if not row:
        return {"error": f"未知の症状です: {symptom}"}

    # 苦手を除外
    scored: List[Tuple[str, int]] = [(oil, sc) for oil, sc in row.items() if oil not in disliked_oils]

    # スコア降順、同点は名前順
    ranked = sorted(scored, key=lambda x: (-x[1], x[0]))

    # ルール説明（実効滴数も明記）
    # 3:1 → 12滴なら 9滴/3滴、2:2 → 12滴なら 6滴/6滴
    rule_text = (
        f"差>={diff_threshold} なら 3:1 比率（例: 合計{total_drops}滴なら 9滴/3滴）、"
        f"差<{diff_threshold} なら 2:2 比率（例: 合計{total_drops}滴なら 6滴/6滴）"
    )

    result = {
        "ranking": ranked,
        "blend": [],
        "rule": rule_text
    }

    if len(ranked) == 0:
        result["error"] = "該当精油がありません（苦手な精油の見直しをご検討ください）"
        return result

    if len(ranked) == 1:
        oil1, _ = ranked[0]
        result["blend"] = [(oil1, total_drops)]
        result["note"] = f"1種類のみのため単独{total_drops}滴としました。"
        return result

    (o1, s1), (o2, s2) = ranked[0], ranked[1]

    # 比率を決定（3:1 または 2:2）
    base_ratio = (3, 1) if (s1 - s2) >= diff_threshold else (2, 2)
    ratio_sum = sum(base_ratio)

    # 合計滴数にスケール
    scale = total_drops // ratio_sum          # 12//4 = 3
    rem   = total_drops - ratio_sum * scale   # 余り（今回は0）

    drops1 = base_ratio[0] * scale
    drops2 = base_ratio[1] * scale

    # 余りが出たときは上位から優先配分（今回は12なので余り0のはず）
    while rem > 0:
        drops1 += 1
        rem -= 1
        if rem > 0:
            drops2 += 1
            rem -= 1

    result["blend"] = [(o1, drops1), (o2, drops2)]
    return result
