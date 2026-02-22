import cyrtranslit  # type: ignore[import-untyped]
from thefuzz import fuzz, process  # type: ignore[import-untyped]


def transliterate_and_normalize(text: str) -> str:
    try:
        return cyrtranslit.to_cyrillic(text, "mk").casefold().strip()
    except Exception:
        return text.casefold().strip()


def match_query_to_candidates(
    query: str,
    candidates: list[str],
    fuzzy_threshold: int = 80,
    suggestion_threshold: int = 50,
    max_suggestions: int = 3,
) -> dict[str, object]:
    norm_query = transliterate_and_normalize(query)
    norm_candidates = [transliterate_and_normalize(c) for c in candidates]
    for i, norm_cand in enumerate(norm_candidates):
        if norm_cand == norm_query:
            return {
                "match": candidates[i],
                "score": 100,
                "exact": True,
                "suggestions": [],
                "match_type": "exact",
            }
    best = process.extractOne(norm_query, norm_candidates, scorer=fuzz.WRatio)
    if best is None:
        return {
            "match": None,
            "score": 0,
            "exact": False,
            "suggestions": [],
            "match_type": "none",
        }
    _, best_score, best_index = best[0], best[1], norm_candidates.index(best[0])
    if best_score >= fuzzy_threshold:
        return {
            "match": candidates[best_index],
            "score": best_score,
            "exact": False,
            "suggestions": [],
            "match_type": "fuzzy",
        }
    all_matches = process.extract(
        norm_query,
        norm_candidates,
        scorer=fuzz.WRatio,
    )
    suggestions = []
    for match_text, score in all_matches:
        idx = norm_candidates.index(match_text)
        if score >= suggestion_threshold and idx != best_index:
            suggestions.append(candidates[idx])
        if len(suggestions) >= max_suggestions:
            break
    return {
        "match": candidates[best_index],
        "score": best_score,
        "exact": False,
        "suggestions": suggestions,
        "match_type": "fallback",
    }
