import html
import os
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.croma_client import search_laptops
from src.data_utils import normalize_products, save_products
from src.recommender import USE_CASES, parse_specs, recommend, similar_to

load_dotenv()

st.set_page_config(page_title="LapPick | Find your laptop", page_icon="💻", layout="wide", initial_sidebar_state="collapsed")

LIME = "#E4FF1A"
SAVED_CSV = Path("data/live_laptops.csv")

# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Manrope:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');
:root {{ --lime: {LIME}; --bg: #0A0A0A; --panel: #141414; --line: #262626; --muted: #9a9a9a; }}
html, body, [data-testid="stAppViewContainer"], .stApp {{ background: var(--bg) !important; color: #fff; font-family: 'Manrope', sans-serif; }}
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer, [data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display: none !important; }}
.block-container {{ max-width: 1240px; padding: 0 24px 60px 24px !important; }}
html {{ scroll-behavior: smooth; }}
.mono {{ font-family: 'Space Mono', monospace; letter-spacing: .08em; text-transform: uppercase; font-size: 11px; }}
.lime {{ color: var(--lime); }}
.display {{ font-family: 'Barlow Condensed', sans-serif; font-weight: 800; text-transform: uppercase; line-height: .9; margin: 0; }}

.ticker {{ background: var(--lime); color: #0A0A0A; display: flex; justify-content: space-between; padding: 9px 24px; margin: 0 -24px; font-family: 'Space Mono', monospace; font-weight: 700; font-size: 11px; letter-spacing: .08em; text-transform: uppercase; }}
.nav-wrap {{ display: flex; justify-content: space-between; align-items: center; padding: 22px 0 0; }}
.logo {{ font-family: 'Barlow Condensed'; font-weight: 800; font-size: 34px; font-style: italic; letter-spacing: -.5px; }}
.nav {{ display: flex; gap: 6px; background: rgba(20,20,20,.85); border: 1px solid var(--line); border-radius: 999px; padding: 6px; }}
.nav a {{ color: var(--muted); text-decoration: none; padding: 10px 18px; border-radius: 999px; font-family: 'Space Mono'; font-size: 11px; letter-spacing: .08em; text-transform: uppercase; }}
.nav a:hover, .nav a.on {{ background: #232323; color: var(--lime); }}
.pill-r {{ font-family: 'Space Mono'; font-size: 11px; text-transform: uppercase; letter-spacing: .08em; }}
.pill-r b {{ background: var(--lime); color: #000; border-radius: 999px; padding: 3px 9px; margin-left: 8px; }}

.hero {{ position: relative; padding: 80px 0 70px; border-bottom: 1px solid var(--line); overflow: hidden; }}
.hero .ghost {{ position: absolute; top: 60px; left: -10px; font-size: clamp(120px, 26vw, 380px); color: #181818; z-index: 0; white-space: nowrap; }}
.hero .inner {{ position: relative; z-index: 1; }}
.hero .h1 {{ font-size: clamp(64px, 12.5vw, 180px); }}
.hero .sub {{ color: #cfcfcf; font-size: 17px; line-height: 1.6; margin-top: 26px; max-width: 520px; }}
.badge {{ position: absolute; right: 40px; bottom: 70px; width: 156px; height: 156px; border-radius: 50%; background: var(--lime); color: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; transform: rotate(10deg); text-align: center; z-index: 2; }}
.badge .big {{ font-family: 'Barlow Condensed'; font-weight: 800; font-size: 52px; line-height: .9; }}
.badge .mono {{ font-size: 9px; font-weight: 700; }}
.tags {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 28px; }}
.tag {{ border: 1px solid var(--line); padding: 8px 14px; font-family: 'Space Mono'; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: #ddd; }}

.brands {{ display: flex; justify-content: space-around; flex-wrap: wrap; gap: 16px; padding: 34px 0; border-bottom: 1px solid var(--line); color: #8a8a8a; font-family: 'Barlow Condensed'; font-weight: 700; font-size: 26px; text-transform: uppercase; letter-spacing: .04em; }}

.sec {{ padding-top: 70px; }}
.sec .eyebrow {{ color: var(--lime); }}
.sec h2 {{ font-size: clamp(44px, 6vw, 80px); margin-top: 12px; }}
.sec p.lead {{ color: var(--muted); margin-top: 12px; font-size: 14px; max-width: 560px; }}

label, [data-testid="stWidgetLabel"] p {{ font-family: 'Space Mono' !important; text-transform: uppercase; font-size: 10px !important; letter-spacing: .08em; color: var(--muted) !important; }}
div[data-baseweb="input"], div[data-baseweb="select"] > div {{ background: var(--panel) !important; border: 1px solid var(--line) !important; border-radius: 0 !important; color: #fff !important; }}
input {{ color: #fff !important; }}
.stButton > button, .stDownloadButton > button {{ background: var(--lime) !important; color: #0A0A0A !important; border: 0 !important; border-radius: 0 !important; font-family: 'Space Mono' !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: .08em; font-size: 12px !important; padding: 14px 20px !important; width: 100%; }}
.stButton > button:hover, .stDownloadButton > button:hover {{ background: #fff !important; color: #000 !important; }}
[data-testid="stRadio"] > div {{ gap: 8px; flex-wrap: wrap; }}
[data-testid="stRadio"] label {{ background: transparent; border: 1px solid var(--line); padding: 8px 14px; margin: 0 !important; cursor: pointer; }}
[data-testid="stRadio"] label > div:first-child {{ display: none; }}
[data-testid="stRadio"] label:has(input:checked) {{ background: var(--lime); }}
[data-testid="stRadio"] label:has(input:checked) p {{ color: #000 !important; font-weight: 700; }}
[data-testid="stRadio"] label p {{ font-size: 11px !important; color: #ddd !important; }}
[data-testid="stExpander"] {{ background: var(--panel); border: 1px solid var(--line); border-radius: 0; }}
[data-testid="stAlert"] {{ border-radius: 0; background: var(--panel); border: 1px solid var(--line); }}
[data-testid="stSlider"] [role="slider"] {{ background: var(--lime) !important; }}
[data-baseweb="tag"] {{ background: var(--lime) !important; color: #000 !important; border-radius: 0 !important; }}
[data-baseweb="tag"] span {{ color: #000 !important; }}

.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px; margin-top: 24px; }}
.card {{ display: block; text-decoration: none; color: #fff; }}
.card .img {{ position: relative; background: #d9d9d9; aspect-ratio: 1/1; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
.card .img img {{ width: 82%; height: 82%; object-fit: contain; transition: transform .3s; }}
.card:hover .img img {{ transform: scale(1.06); }}
.card .off {{ position: absolute; top: 10px; left: 10px; background: var(--lime); color: #000; font-family: 'Space Mono'; font-weight: 700; font-size: 11px; padding: 4px 8px; }}
.card .go {{ position: absolute; right: 10px; bottom: 10px; background: #fff; color: #000; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; font-weight: 700; }}
.card:hover .go {{ background: var(--lime); }}
.card .meta {{ display: flex; justify-content: space-between; margin-top: 12px; color: var(--muted); }}
.card .name {{ font-weight: 700; font-size: 14px; margin-top: 6px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; min-height: 40px; }}
.card .spec {{ margin-top: 6px; color: var(--muted); font-family: 'Space Mono'; font-size: 11px; }}
.card .price {{ margin-top: 8px; font-family: 'Space Mono'; font-weight: 700; color: var(--lime); font-size: 15px; }}
.card .price s {{ color: #6a6a6a; font-weight: 400; font-size: 12px; margin-left: 8px; }}
.card .price em {{ color: #fff; font-style: normal; font-size: 11px; margin-left: 8px; }}
.bar {{ height: 3px; background: var(--line); margin-top: 10px; }}
.bar i {{ display: block; height: 3px; background: var(--lime); }}
.why {{ margin-top: 8px; display: flex; flex-wrap: wrap; gap: 5px; }}
.why span {{ border: 1px solid var(--line); padding: 3px 7px; font-size: 10px; color: #cfcfcf; font-family: 'Space Mono'; }}
.noimg {{ color: #777; font-family: 'Space Mono'; font-size: 11px; }}

.pick {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0; margin-top: 28px; border: 1px solid var(--line); }}
.pick .img {{ background: #d9d9d9; display: flex; align-items: center; justify-content: center; min-height: 380px; position: relative; }}
.pick .img img {{ width: 80%; max-height: 360px; object-fit: contain; }}
.pick .body {{ padding: 36px; display: flex; flex-direction: column; gap: 14px; }}
.pick .score {{ font-family: 'Barlow Condensed'; font-weight: 800; font-size: 96px; line-height: .85; color: var(--lime); }}
.pick .title {{ font-size: 22px; font-weight: 700; line-height: 1.3; }}
.pick .p {{ font-family: 'Space Mono'; font-weight: 700; font-size: 22px; color: var(--lime); }}
.pick .p s {{ color: #6a6a6a; font-size: 14px; font-weight: 400; margin-left: 10px; }}
.pick a.cta {{ display: inline-block; background: var(--lime); color: #000; text-decoration: none; padding: 14px 20px; font-family: 'Space Mono'; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; align-self: flex-start; }}
.pick a.cta:hover {{ background: #fff; }}

.cmp {{ width: 100%; border-collapse: collapse; margin-top: 24px; }}
.cmp th, .cmp td {{ border-top: 1px solid var(--line); padding: 12px 10px; text-align: left; vertical-align: top; font-size: 13px; }}
.cmp th.rowh {{ font-family: 'Space Mono'; font-size: 10px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); font-weight: 400; width: 140px; }}
.cmp .ci {{ background: #d9d9d9; height: 120px; display: flex; align-items: center; justify-content: center; margin-bottom: 8px; }}
.cmp .ci img {{ max-width: 80%; max-height: 100px; object-fit: contain; }}

.how {{ background: var(--lime); color: #0A0A0A; margin: 80px -24px 0; padding: 80px 24px; }}
.how .inner {{ max-width: 1192px; margin: 0 auto; }}
.how h2 {{ font-size: clamp(54px, 8vw, 110px); }}
.how .steps {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 40px; }}
.how .st {{ border-top: 2px solid #0A0A0A; padding-top: 14px; }}
.how .st .n {{ font-family: 'Space Mono'; font-size: 11px; font-weight: 700; }}
.how .st .t {{ font-family: 'Barlow Condensed'; font-weight: 800; font-size: 32px; text-transform: uppercase; margin: 6px 0; }}
.how .st p {{ line-height: 1.6; font-size: 14px; }}
.foot {{ color: #666; font-size: 12px; padding-top: 24px; }}

@media (max-width: 820px) {{
  .nav, .badge {{ display: none; }}
  .pick {{ grid-template-columns: 1fr; }}
  .how .steps {{ grid-template-columns: 1fr; }}
  .ticker span:nth-child(2) {{ display: none; }}
  .cmp {{ display: block; overflow-x: auto; }}
}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def esc(value) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    return html.escape(str(value), quote=True)


def inr(value) -> str:
    try:
        return f"₹{float(value):,.0f}"
    except (TypeError, ValueError):
        return "—"


def storage_label(gb) -> str:
    if pd.isna(gb):
        return "—"
    return f"{gb / 1024:g}TB" if gb >= 1024 else f"{gb:g}GB"


def load_saved_catalog() -> list[dict]:
    """Reuse previously fetched listings so the store works without spending API credits."""
    if not SAVED_CSV.exists():
        return []
    try:
        old = pd.read_csv(SAVED_CSV)
    except Exception:
        return []
    if "fetched_at" in old:
        old = old.sort_values("fetched_at")
    if "product_code" in old:
        old = old.drop_duplicates(subset="product_code", keep="last")
    return old.to_dict("records")


def build_catalog(products: list[dict]) -> pd.DataFrame:
    df = parse_specs(pd.DataFrame(products)).reset_index(drop=True)
    code = df["product_code"].astype(str) if "product_code" in df else pd.Series(df.index.astype(str))
    df["pid"] = np.where(code.isin(["nan", "None", ""]), "row-" + df.index.astype(str), code)
    return df.drop_duplicates(subset="pid", keep="last").reset_index(drop=True)


def card_html(row: pd.Series, match=None, reasons=None, match_label="match") -> str:
    img = row.get("image_url")
    img_tag = (
        f'<img src="{esc(img)}" alt="{esc(row.get("name"))}" loading="lazy" referrerpolicy="no-referrer">'
        if isinstance(img, str) and img.startswith("http")
        else '<span class="noimg">NO IMAGE</span>'
    )
    off = row.get("discount_num")
    if match is not None:
        tag = f'<div class="off">{int(match)}% {match_label}</div>'
    elif pd.notna(off) and off > 0:
        tag = f'<div class="off">-{int(off)}%</div>'
    else:
        tag = ""
    rating = row.get("rating")
    rating_tag = f"★ {rating:.1f}" if pd.notna(rating) and rating > 0 else "NEW"
    mrp, price = row.get("mrp_inr"), row.get("price_inr")
    mrp_tag = f"<s>{inr(mrp)}</s>" if pd.notna(mrp) and pd.notna(price) and mrp > price else ""
    off_txt = f"<em>-{int(off)}%</em>" if match is not None and pd.notna(off) and off > 0 else ""
    bits = []
    if pd.notna(row.get("ram_gb")):
        bits.append(f'{row["ram_gb"]:g}GB')
    if pd.notna(row.get("storage_gb")):
        bits.append(storage_label(row["storage_gb"]))
    if pd.notna(row.get("screen_in")):
        bits.append(f'{row["screen_in"]:g}"')
    spec = " · ".join(bits)
    bar = f'<div class="bar"><i style="width:{int(match)}%"></i></div>' if match is not None else ""
    why = "".join(f"<span>{esc(r)}</span>" for r in (reasons or []))
    why = f'<div class="why">{why}</div>' if why else ""
    url = esc(row.get("product_url")) or "#"
    return (
        f'<a class="card" href="{url}" target="_blank" rel="noopener noreferrer">'
        f'<div class="img">{tag}{img_tag}<div class="go">↗</div></div>'
        f'<div class="meta mono"><span>{esc(row.get("brand"))}</span><span>{rating_tag}</span></div>'
        f'<div class="name">{esc(row.get("name"))}</div>'
        f'<div class="spec">{esc(spec)}</div>'
        f'<div class="price">{inr(price)}{mrp_tag}{off_txt}</div>{bar}{why}</a>'
    )


def grid_html(cards: list[str]) -> str:
    return '<div class="grid">' + "".join(cards) + "</div>"


def top_pick_html(row: pd.Series) -> str:
    img = row.get("image_url")
    img_tag = f'<img src="{esc(img)}" alt="{esc(row.get("name"))}" referrerpolicy="no-referrer">' if isinstance(img, str) and img.startswith("http") else '<span class="noimg">NO IMAGE</span>'
    mrp, price = row.get("mrp_inr"), row.get("price_inr")
    mrp_tag = f"<s>{inr(mrp)}</s>" if pd.notna(mrp) and pd.notna(price) and mrp > price else ""
    why = "".join(f"<span>{esc(r)}</span>" for r in row["reasons"])
    return (
        '<div class="pick">'
        f'<div class="img">{img_tag}</div>'
        '<div class="body">'
        '<div class="mono lime">● Your top pick</div>'
        f'<div class="score">{int(row["match"])}%</div>'
        '<div class="mono" style="color:#9a9a9a">match score</div>'
        f'<div class="title">{esc(row.get("name"))}</div>'
        f'<div class="p">{inr(price)}{mrp_tag}</div>'
        f'<div class="why">{why}</div>'
        f'<a class="cta" href="{esc(row.get("product_url")) or "#"}" target="_blank" rel="noopener noreferrer">View on Croma ↗</a>'
        "</div></div>"
    )


def compare_html(rows: pd.DataFrame) -> str:
    def cell(label, fn):
        return f'<tr><th class="rowh">{label}</th>' + "".join(f"<td>{fn(r)}</td>" for _, r in rows.iterrows()) + "</tr>"

    head = "<tr><th></th>" + "".join(
        f'<th><div class="ci">'
        + (f'<img src="{esc(r.get("image_url"))}" referrerpolicy="no-referrer">' if isinstance(r.get("image_url"), str) else "")
        + f'</div>{esc(r.get("name"))}</th>'
        for _, r in rows.iterrows()
    ) + "</tr>"
    body = "".join([
        cell("Price", lambda r: f'<b class="lime">{inr(r["price_inr"])}</b>'),
        cell("MRP", lambda r: inr(r["mrp_inr"])),
        cell("Discount", lambda r: f'{int(r["discount_num"])}%' if pd.notna(r["discount_num"]) else "—"),
        cell("Processor", lambda r: esc(r["processor"]) or "—"),
        cell("RAM", lambda r: f'{r["ram_gb"]:g}GB' if pd.notna(r["ram_gb"]) else "—"),
        cell("Storage", lambda r: storage_label(r["storage_gb"])),
        cell("Screen", lambda r: f'{r["screen_in"]:g}"' if pd.notna(r["screen_in"]) else "—"),
        cell("Dedicated GPU", lambda r: "Yes" if r["has_gpu"] else "No"),
        cell("Rating", lambda r: f'★ {r["rating"]:.1f}' if pd.notna(r["rating"]) and r["rating"] > 0 else "—"),
        cell("Warranty", lambda r: f'{r["warranty_months"]:g} months' if pd.notna(pd.to_numeric(r.get("warranty_months"), errors="coerce")) else "—"),
        cell("Buy", lambda r: f'<a class="lime" href="{esc(r.get("product_url"))}" target="_blank" rel="noopener noreferrer">Croma ↗</a>'),
    ])
    return f'<table class="cmp">{head}{body}</table>'


# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------
if "products" not in st.session_state:
    saved = load_saved_catalog()
    if saved:
        st.session_state["products"] = saved
        st.session_state["api_meta"] = {"fetched_at": "saved catalog", "credits_used": "0"}

products = st.session_state.get("products", [])
catalog = build_catalog(products) if products else pd.DataFrame()
n_items = len(catalog)
shortlist_n = len(st.session_state.get("shortlist", []))

# --------------------------------------------------------------------------
# Header + hero
# --------------------------------------------------------------------------
badge_big = str(n_items) if n_items else "0"
st.markdown(
    f"""
<div class="ticker"><span>Live prices from Croma</span><span>Smart laptop matching</span><span>Prices change · verify before you buy</span></div>
<div class="nav-wrap">
  <div class="logo">LapPick</div>
  <div class="nav"><a class="on" href="#match">The Match</a><a href="#browse">All Laptops</a><a href="#compare">Compare</a><a href="#how">How it works</a></div>
  <div class="pill-r">Shortlist<b>{shortlist_n}</b></div>
</div>
<div class="hero" id="top">
  <div class="ghost display">PICK</div>
  <div class="inner">
    <div class="mono lime">● The laptop recommendation engine</div>
    <div class="mono" style="margin-top:22px;color:#cfcfcf;">Good specs. Right price.</div>
    <div class="display h1" style="margin-top:14px;">FIND YOUR<br><span class="lime">LAPTOP.</span></div>
    <div class="sub">Tell us what you'll use it for and what you can spend. LapPick reads the specs on every live listing and lines up the best fits for you.</div>
    <div class="tags"><span class="tag">Student</span><span class="tag">Coding &amp; ML</span><span class="tag">Gaming</span><span class="tag">Creative</span><span class="tag">Business</span></div>
  </div>
  <div class="badge"><div class="mono">Ranking</div><div class="big">{esc(badge_big)}</div><div class="mono">Laptops</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Catalog controls
# --------------------------------------------------------------------------
api_key = os.getenv("APISH_KEY", "").strip()
st.markdown(
    '<div class="sec" id="match"><div class="mono eyebrow">The match / 001</div>'
    '<h2 class="display">Tell us what you do.<br><span class="lime">We pick the laptop.</span></h2>'
    '<p class="lead">Set your use, budget and must-haves. Results update as you change them.</p></div>',
    unsafe_allow_html=True,
)

with st.expander(f"Catalog · {n_items} laptops loaded", expanded=not n_items):
    if not api_key:
        st.warning("APISH_KEY not found in .env, so live fetching is off. Saved listings (if any) still work.")
    k1, k2, k3, k4 = st.columns([3, 1, 2, 2])
    query = k1.text_input("Search term", value="laptop")
    pages = k2.number_input("Pages", min_value=1, max_value=5, value=1, step=1, help="Each page is one API request and uses credits.")
    sort = k3.selectbox("Sort by (API)", ["relevance", "price-asc", "price-desc"], index=0)
    with k4:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        fetch = st.button("Fetch latest ↗", disabled=not api_key)
    meta = st.session_state.get("api_meta", {})
    if n_items:
        st.caption(f"Source: {meta.get('fetched_at', 'n/a')} · API credits used this fetch: {meta.get('credits_used', '—')}")

if fetch:
    try:
        collected, credits, last_payload = [], 0, {}
        with st.spinner(f"Fetching {int(pages)} page(s) from Croma..."):
            for p in range(1, int(pages) + 1):
                last_payload = search_laptops(api_key, query=query, page=p, sort=sort)
                collected += normalize_products(last_payload)
                try:
                    credits += int(last_payload.get("credits_used", 0))
                except (TypeError, ValueError):
                    pass
        if not collected:
            st.info("No laptop listings were returned. Try a broader search such as 'laptop'.")
        else:
            save_products(collected)
            st.session_state["products"] = collected
            st.session_state["shortlist"] = []
            st.session_state["api_meta"] = {"fetched_at": last_payload.get("fetched_at", "just now"), "credits_used": credits or "Not provided"}
            st.rerun()
    except Exception as exc:
        st.error(f"Could not fetch listings: {exc}")
        st.caption("Check your API key, account credits, internet connection, and API.SH service status.")

# --------------------------------------------------------------------------
# Recommender
# --------------------------------------------------------------------------
if catalog.empty:
    st.info("No laptops loaded yet. Open the catalog panel above and fetch listings.")
else:
    use_case = st.radio("What will you use it for?", list(USE_CASES), horizontal=True)
    st.caption(USE_CASES[use_case]["blurb"])

    r1, r2, r3, r4 = st.columns([3, 1.2, 1.2, 2])
    budget = r1.slider("Budget (max)", min_value=20000, max_value=300000, value=100000, step=5000, format="₹%d")
    min_ram = r2.selectbox("Min RAM", [0, 8, 16, 32], format_func=lambda v: "Any" if v == 0 else f"{v}GB")
    min_storage = r3.selectbox("Min storage", [0, 256, 512, 1024], format_func=lambda v: "Any" if v == 0 else (f"{v}GB" if v < 1024 else "1TB"))
    all_brands = sorted(x for x in catalog["brand"].dropna().astype(str).unique() if x.strip())
    brands_sel = r4.multiselect("Brands", all_brands, placeholder="All brands")

    q1, q2, q3 = st.columns([2, 1, 1])
    keywords = q1.text_input("Anything specific? (optional)", placeholder="e.g. OLED, Ryzen 7, 1TB")
    need_gpu = q2.checkbox("Dedicated GPU only")
    need_touch = q3.checkbox("Touchscreen only")

    recs = recommend(catalog, use_case, budget, min_ram, min_storage, need_gpu, need_touch, brands_sel, keywords, top_n=9)

    if recs.empty:
        st.info("Nothing fits those requirements. Raise the budget or relax RAM, storage or the must-haves.")
    else:
        st.markdown(top_pick_html(recs.iloc[0]), unsafe_allow_html=True)
        if len(recs) > 1:
            st.markdown('<div class="mono lime" style="margin-top:34px;">Also worth a look</div>', unsafe_allow_html=True)
            st.markdown(grid_html([card_html(r, match=r["match"], reasons=r["reasons"]) for _, r in recs.iloc[1:].iterrows()]), unsafe_allow_html=True)

    # brand strip
    if all_brands:
        st.markdown('<div class="brands">' + "".join(f"<span>{esc(b)}</span>" for b in all_brands[:7]) + "</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------------------
    # Browse
    # ----------------------------------------------------------------------
    st.markdown(
        '<div class="sec" id="browse"><div class="mono eyebrow">The catalog / 002</div>'
        '<h2 class="display">Every laptop.<br>No misses.</h2>'
        '<p class="lead">Browse everything loaded, straight from the listings.</p></div>',
        unsafe_allow_html=True,
    )
    brand_pick = st.radio("Brand", ["All brands"] + all_brands, horizontal=True, label_visibility="collapsed")
    b1, b2 = st.columns([3, 2])
    find = b1.text_input("Find your laptop", placeholder="Search by name, e.g. M5, RTX, Ryzen")
    order = b2.selectbox("Order", ["Featured", "Price: low to high", "Price: high to low", "Biggest discount", "Top rated"])
    view = catalog.copy()
    if brand_pick != "All brands":
        view = view[view["brand"].astype(str) == brand_pick]
    if find.strip():
        view = view[view["name"].astype(str).str.contains(find.strip(), case=False, na=False)]
    if order == "Price: low to high":
        view = view.sort_values("price_inr")
    elif order == "Price: high to low":
        view = view.sort_values("price_inr", ascending=False)
    elif order == "Biggest discount":
        view = view.sort_values("discount_num", ascending=False)
    elif order == "Top rated":
        view = view.sort_values(["rating", "ratings_count"], ascending=False)
    st.markdown(f'<div class="mono" style="color:#9a9a9a;margin-top:10px;">{len(view)} laptops</div>', unsafe_allow_html=True)
    if view.empty:
        st.info("No laptops match these filters.")
    else:
        st.markdown(grid_html([card_html(r) for _, r in view.head(48).iterrows()]), unsafe_allow_html=True)
        if len(view) > 48:
            st.caption("Showing the first 48. Use the filters to narrow down.")
    csv_cols = [c for c in ["name", "brand", "price_inr", "mrp_inr", "discount", "rating", "ram_gb", "storage_gb", "screen_in", "processor", "product_url"] if c in view.columns]
    st.download_button("Download these listings (CSV)", view[csv_cols].to_csv(index=False).encode("utf-8-sig"), "lappick_listings.csv", "text/csv")

    # ----------------------------------------------------------------------
    # Compare + similar
    # ----------------------------------------------------------------------
    st.markdown(
        '<div class="sec" id="compare"><div class="mono eyebrow">Shortlist / 003</div>'
        '<h2 class="display">Side by side.<br><span class="lime">Or more like this.</span></h2>'
        '<p class="lead">Pick up to four laptops to compare, or find look-alikes for one you already like.</p></div>',
        unsafe_allow_html=True,
    )
    names = dict(zip(catalog["pid"], catalog["name"].astype(str).str.slice(0, 90)))
    chosen = st.multiselect("Shortlist (max 4)", list(names), key="shortlist", format_func=lambda p: names[p], max_selections=4, placeholder="Choose laptops to compare")
    if len(chosen) >= 2:
        st.markdown(compare_html(catalog[catalog["pid"].isin(chosen)].set_index("pid").loc[chosen].reset_index()), unsafe_allow_html=True)
    elif chosen:
        st.caption("Add at least one more laptop to compare.")

    base = st.selectbox("Find laptops similar to", ["—"] + list(names), format_func=lambda p: "Choose a laptop" if p == "—" else names[p])
    if base != "—":
        sim = similar_to(catalog, base, n=4)
        st.markdown(grid_html([card_html(r, match=r["match"], match_label="similar") for _, r in sim.iterrows()]), unsafe_allow_html=True)

# --------------------------------------------------------------------------
# How it works + footer
# --------------------------------------------------------------------------
st.markdown(
    """
<div class="how" id="how"><div class="inner">
  <div class="mono">How it works / 004</div>
  <h2 class="display" style="margin-top:14px;">Specs in.<br>Best fit out.</h2>
  <div class="steps">
    <div class="st"><div class="n">01</div><div class="t">Read the specs</div><p>RAM, storage, processor tier, GPU, screen size, price and rating are pulled from each live listing.</p></div>
    <div class="st"><div class="n">02</div><div class="t">Weigh by use</div><p>A gaming laptop is scored on GPU and CPU first. A travel laptop is scored on size and price first.</p></div>
    <div class="st"><div class="n">03</div><div class="t">Rank within budget</div><p>Anything over budget or missing your must-haves is dropped. The rest are ranked by match score, and "similar" uses cosine similarity on the spec vectors.</p></div>
  </div>
</div></div>
<div class="foot">Data source: public Croma product listings returned by API.SH. Specs are read from listing text and may be incomplete. Prices and availability change; verify on the retailer's product page.</div>
""",
    unsafe_allow_html=True,
)
