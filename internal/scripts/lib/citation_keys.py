# Shared citation-key helpers for lookup overlay + the verification ledger.
# Keep reporter matching OCR-tolerant (F. 3d / F.3d, Cal.App. / Cal. App.).

from __future__ import annotations

import re

_SEE_RE = re.compile(
    r"^(?:(?:Dismiss|Holding Key Fact)\.\s*)?(?:See|see|SEE)\s+",
)

# Volume + reporter + first page. Spaces inside the reporter are optional so
# index strings like "639 F. 3d 916" and "639 F.3d 916" share a pin key.
_PIN_RE = re.compile(
    r"(\d+)\s+("
    r"U\.?\s*S\.?"
    r"|S\.\s*Ct\."
    r"|L\.\s*Ed\.\s*2d"
    r"|F\.\s*R\.\s*D\."
    r"|F\.\s*Supp\.\s*(?:3d|2d)"
    r"|F\.\s*(?:4th|3d|2d)"
    r"|Cal\.\s*App\.\s*(?:5th|4th|3d|2d)"
    r"|Cal\.\s*(?:5th|4th|3d|2d)"
    r")\s+(\d+)",
    re.I,
)

_WL_RE = re.compile(r"(?:WL|Westlaw)\s*(\d{5,})", re.I)

# Short tokens that should not count as a party-name match.
_NAME_NOISE = {
    "v",
    "vs",
    "inc",
    "llc",
    "ltd",
    "co",
    "corp",
    "the",
    "of",
    "and",
    "see",
    "re",
    "in",
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def strip_see(citation: str) -> str:
    return _SEE_RE.sub("", (citation or "").strip())


def normalize_authority_key(citation: str) -> str:
    """Strip leading See/Dismiss. See and collapse punctuation for matching."""
    return slug(strip_see(citation))


def case_name_key(citation: str) -> str:
    return slug(strip_see(citation).split(",")[0])


def name_tokens(citation: str) -> set[str]:
    return {t for t in case_name_key(citation).split() if len(t) > 2} - _NAME_NOISE


def names_overlap(left: str, right: str) -> bool:
    """True when two captions share a non-noise party token (OCR / truncation)."""
    return bool(name_tokens(left) & name_tokens(right))


def _norm_reporter(raw: str) -> str:
    compact = re.sub(r"[\s.]+", "", raw).lower()
    mapping = {
        "us": "us",
        "sct": "sct",
        "led2d": "led2d",
        "frd": "frd",
        "fsupp3d": "fsupp3d",
        "fsupp2d": "fsupp2d",
        "f4th": "f4th",
        "f3d": "f3d",
        "f2d": "f2d",
        "calapp5th": "calapp5th",
        "calapp4th": "calapp4th",
        "calapp3d": "calapp3d",
        "calapp2d": "calapp2d",
        "cal5th": "cal5th",
        "cal4th": "cal4th",
        "cal3d": "cal3d",
        "cal2d": "cal2d",
    }
    return mapping.get(compact, compact)


def reporter_pin_key(citation: str) -> str | None:
    """Stable volume+reporter+page key, or a Westlaw pin, or None."""
    text = strip_see(citation)
    match = _PIN_RE.search(text)
    if match:
        return f"{match.group(1)} {_norm_reporter(match.group(2))} {match.group(3)}"
    wl = _WL_RE.search(text)
    if wl:
        return f"wl {wl.group(1)}"
    return None
