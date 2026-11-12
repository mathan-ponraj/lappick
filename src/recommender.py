"""Content-based laptop recommender.

Reads specs out of the listing text (name + highlights), turns each laptop into
a small feature vector, then:
  * recommend()  - filters by hard requirements and ranks by a use-case weighted score
  * similar_to() - cosine similarity between feature vectors ("more like this")

Only numpy and pandas are needed. Swap recommend() for a trained model later
without touching the app: it just needs to return the same columns.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Use cases: how much each feature matters (each row sums to 1.0)
# --------------------------------------------------------------------------
USE_CASES: dict[str, dict] = {
    "Student & everyday": {
        "blurb": "Browsing, classes, documents, streaming. Light, long-lasting and fair on price.",
        "weights": {"perf": .15, "ram": .15, "storage": .10, "gpu": 0, "portable": .25, "rating": .10, "value": .25},
    },
    "Coding & ML": {
        "blurb": "Notebooks, containers, local models. CPU and RAM first, a GPU helps.",
        "weights": {"perf": .28, "ram": .30, "storage": .10, "gpu": .12, "portable": .05, "rating": .05, "value": .10},
    },
    "Gaming": {
        "blurb": "A dedicated GPU and a fast CPU matter most. Portability barely counts.",
        "weights": {"perf": .25, "ram": .10, "storage": .05, "gpu": .40, "portable": 0, "rating": .05, "value": .15},
    },
    "Creative & video": {
        "blurb": "Editing and design. Strong CPU, plenty of RAM and storage, GPU helps.",
        "weights": {"perf": .25, "ram": .20, "storage": .15, "gpu": .15, "portable": .05, "rating": .05, "value": .15},
    },
    "Business & travel": {
        "blurb": "Carry it everywhere. Compact screen, reliable, sensible price.",
        "weights": {"perf": .15, "ram": .10, "storage": .10, "gpu": 0, "portable": .35, "rating": .10, "value": .20},
    },
}

# --------------------------------------------------------------------------
# Spec parsing
# --------------------------------------------------------------------------
_SIZE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(TB|GB)", re.I)
_INCH_RE = re.compile(r"(\d{2}(?:\.\d+)?)\s*(?:inches|inch|\")", re.I)
_CMS_RE = re.compile(r"(\d{2}\.\d+)\s*cms", re.I)
_PROC_RE = re.compile(r"Processor:\s*(.+?)(?:\s+(?:Display|Memory|Graphics|Storage|Operating)\s*:|$)", re.I)
_GPU_RE = re.compile(r"\b(rtx|gtx|geforce|radeon rx|arc a\d)", re.I)
_GAMING_RE = re.compile(r"\b(gaming|victus|tuf|rog|legion|nitro|loq|predator|alienware|omen)\b", re.I)


def _ram_storage(text: str) -> tuple[float, float]:
    vals = [float(n) * (1024 if u.upper() == "TB" else 1) for n, u in _SIZE_RE.findall(text)]
    ram = next((v for v in vals if 4 <= v <= 64), np.nan)
    storage = max([v for v in vals if v >= 128], default=np.nan)
    return ram, storage


def _screen(text: str) -> float:
    m = _INCH_RE.search(text)
    if m:
        return float(m.group(1))
    m = _CMS_RE.search(text)
    return round(float(m.group(1)) / 2.54, 1) if m else np.nan


def _cpu_tier(text: str) -> int:
    t = text.lower()
    if re.search(r"\bm[1-5]\s*(pro|max|ultra)", t):
        return 5
    if re.search(r"\bm[1-5]\b", t):
        return 4
    if re.search(r"apple a1[0-9]\b|\ba1[0-9]\s*pro", t):  # Apple A-series (MacBook Neo etc.)
        return 3
    if re.search(r"ryzen\s*9|\bi9\b|ultra\s*9|core\s*9", t):
        return 5
    if re.search(r"ryzen\s*7|\bi7\b|ultra\s*7|core\s*7|snapdragon x elite", t):
        return 4
    if re.search(r"ryzen\s*5|\bi5\b|ultra\s*5|core\s*5|snapdragon x", t):
        return 3
    if re.search(r"ryzen\s*3|\bi3\b|core\s*3", t):
        return 2
    if re.search(r"celeron|pentium|athlon|n[0-9]{3}\b", t):
        return 1
    return 2


def parse_specs(df: pd.DataFrame) -> pd.DataFrame:
    """Add numeric spec columns parsed from name + highlights."""
    out = df.copy()
    name = out.get("name", pd.Series("", index=out.index)).fillna("").astype(str)
    hl = out.get("highlights", pd.Series("", index=out.index)).fillna("").astype(str)
    text = (name + " " + hl)

    rs = text.map(_ram_storage)
    out["ram_gb"] = rs.map(lambda x: x[0])
    out["storage_gb"] = rs.map(lambda x: x[1])
    out["screen_in"] = text.map(_screen)
    out["cpu_tier"] = text.map(_cpu_tier)
    out["has_gpu"] = text.map(lambda s: bool(_GPU_RE.search(s)))
    out["gaming"] = text.map(lambda s: bool(_GAMING_RE.search(s)))
    out["touch"] = text.str.contains("touch", case=False, regex=False)
    out["processor"] = hl.map(lambda s: (_PROC_RE.search(s).group(1).strip() if _PROC_RE.search(s) else ""))

    for col in ["price_inr", "mrp_inr", "rating", "ratings_count"]:
        out[col] = pd.to_numeric(out.get(col), errors="coerce")
    disc = out.get("discount")
    out["discount_num"] = (
        pd.to_numeric(disc.astype(str).str.replace("%", "", regex=False), errors="coerce") if disc is not None else np.nan
    )
    out["_text"] = text.str.lower()
    return out


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------
def _features(df: pd.DataFrame, budget: float | None) -> pd.DataFrame:
    f = pd.DataFrame(index=df.index)
    f["perf"] = df["cpu_tier"] / 5
    f["ram"] = (df["ram_gb"].clip(upper=32) / 32).fillna(0.25)
    f["storage"] = (df["storage_gb"].clip(upper=1024) / 1024).fillna(0.25)
    f["gpu"] = np.where(df["has_gpu"], 1.0, np.where(df["gaming"], 0.6, 0.0))
    scr = df["screen_in"]
    portable = np.select([scr <= 14.5, scr <= 15.7], [1.0, 0.7], default=0.4)
    f["portable"] = np.where(scr.isna(), 0.5, portable)
    rated = df["rating"].where(df["ratings_count"].fillna(0) > 0)
    f["rating"] = (rated / 5).fillna(0.5)
    if budget:
        f["value"] = ((budget - df["price_inr"]) / budget).clip(0, 1).fillna(0)
    else:
        f["value"] = 0.0
    return f


def _storage_label(gb) -> str:
    if pd.isna(gb):
        return "storage n/a"
    return f"{gb / 1024:g}TB" if gb >= 1024 else f"{gb:g}GB"


def _reason(key: str, row: pd.Series, budget: float) -> str:
    if key == "perf":
        proc = row.get("processor") or ""
        return (proc[:30] if proc else "Fast processor")
    if key == "ram":
        return f"{row['ram_gb']:g}GB RAM"
    if key == "storage":
        return f"{_storage_label(row['storage_gb'])} storage"
    if key == "gpu":
        return "Dedicated GPU" if row["has_gpu"] else "Gaming-class build"
    if key == "portable":
        return f"{row['screen_in']:g}\" screen, easy to carry" if pd.notna(row["screen_in"]) else "Portable"
    if key == "rating":
        return f"Rated {row['rating']:.1f}★"
    return f"₹{max(budget - row['price_inr'], 0):,.0f} under budget"


def recommend(
    df: pd.DataFrame,
    use_case: str,
    budget: float,
    min_ram: float = 0,
    min_storage: float = 0,
    need_gpu: bool = False,
    need_touch: bool = False,
    brands: list[str] | None = None,
    keywords: str = "",
    top_n: int = 8,
) -> pd.DataFrame:
    """Filter by hard requirements, then rank by use-case weighted score (0-100)."""
    weights = USE_CASES[use_case]["weights"]
    d = df[df["price_inr"].notna() & (df["price_inr"] <= budget)]
    if min_ram:
        d = d[d["ram_gb"] >= min_ram]
    if min_storage:
        d = d[d["storage_gb"] >= min_storage]
    if need_gpu:
        d = d[d["has_gpu"]]
    if need_touch:
        d = d[d["touch"]]
    if brands:
        d = d[d["brand"].astype(str).isin(brands)]
    if d.empty:
        return d.assign(match=pd.Series(dtype=float), reasons=pd.Series(dtype=object))

    f = _features(d, budget)
    score = sum(f[k] * w for k, w in weights.items())

    tokens = [t for t in re.split(r"[^a-z0-9]+", keywords.lower()) if len(t) >= 2]
    if tokens:
        hits = d["_text"].map(lambda s: sum(t in s for t in tokens))
        score = score + 0.04 * hits.clip(upper=3)

    d = d.assign(match=(score.clip(upper=1) * 100).round(0))
    contrib = pd.DataFrame({k: f[k] * w for k, w in weights.items() if w > 0})

    def top_reasons(idx) -> list[str]:
        row = d.loc[idx]
        order = contrib.loc[idx].sort_values(ascending=False).index
        out = []
        for k in order:
            if k == "rating" and not (pd.notna(row["rating"]) and row["rating"] > 0 and row["ratings_count"] > 0):
                continue
            if f.loc[idx, k] >= 0.5 and not (k == "value" and row["price_inr"] >= budget):
                out.append(_reason(k, row, budget))
            if len(out) == 3:
                break
        return out

    d["reasons"] = [top_reasons(i) for i in d.index]
    return d.sort_values(["match", "price_inr"], ascending=[False, True]).head(top_n)


# --------------------------------------------------------------------------
# Similar laptops (cosine similarity on spec vectors)
# --------------------------------------------------------------------------
def similar_to(df: pd.DataFrame, pid: str, n: int = 4) -> pd.DataFrame:
    f = _features(df, None).drop(columns=["value", "rating"])
    f["price"] = (df["price_inr"] / df["price_inr"].max()).fillna(0.5)
    m = f.to_numpy(dtype=float)
    pos = df.index.get_loc(df.index[df["pid"] == pid][0])
    v = m[pos]
    norms = np.linalg.norm(m, axis=1) * np.linalg.norm(v)
    sim = np.divide(m @ v, norms, out=np.zeros(len(m)), where=norms > 0)
    sim[pos] = -1
    top = np.argsort(sim)[::-1][:n]
    res = df.iloc[top].copy()
    res["match"] = (sim[top] * 100).round(0)
    return res
