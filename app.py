"""
VKG Capability-Tier Evaluation — Demo UI (Enhanced)
All data hardcoded as placeholders. No backend required.
"""
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import math

st.set_page_config(page_title="VKG Tier Evaluation Demo", page_icon="🧬", layout="wide")

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
.main { background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f1f5f9 100%); color: #1e293b; }
h1, h2, h3, h4 { color: #1e293b !important; }
p, span, label, .stMarkdown { color: #334155; }
.stTabs [data-baseweb="tab-list"] { gap: 6px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(100,116,139,0.08); border-radius: 8px; padding: 8px 16px;
    color: #475569; font-weight: 600; border: 1px solid rgba(100,116,139,0.15);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2); color: white;
    border: none; box-shadow: 0 4px 15px rgba(102,126,234,0.3);
}
.metric-card {
    background: white; border-radius: 12px; padding: 18px;
    border: 1px solid #e2e8f0; text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin: 4px 0;
}
.metric-card h3 { color: #4f46e5 !important; font-size: 1.8em; margin: 0; }
.metric-card p { color: #64748b; margin: 4px 0 0 0; font-size: 0.85em; }
.query-badge {
    display: inline-block; padding: 4px 12px; border-radius: 16px;
    font-size: 0.8em; font-weight: 600; margin: 2px;
}
.badge-volume { background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; }
.badge-coverage { background: #fef9c3; color: #ca8a04; border: 1px solid #fde047; }
.badge-proximity { background: #dcfce7; color: #16a34a; border: 1px solid #86efac; }
.badge-multiplicity { background: #ccfbf1; color: #0d9488; border: 1px solid #5eead4; }
.badge-containment { background: #f3e8ff; color: #7c3aed; border: 1px solid #c4b5fd; }
div[data-testid="stSidebar"] { background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%); }
div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] h2, div[data-testid="stSidebar"] h3 { color: #1e293b !important; }
div[data-testid="stSidebar"] p, div[data-testid="stSidebar"] span { color: #475569; }
.scan-card {
    background: white; border-radius: 10px; padding: 10px 14px;
    border: 1px solid #e2e8f0; margin: 4px 0; box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.scan-relevant { border-left: 4px solid #16a34a; }
.scan-irrelevant { border-left: 4px solid #dc2626; }
</style>
""", unsafe_allow_html=True)

# ── Placeholder Data ─────────────────────────────────────────────────────────
QUERIES = {
    "Q010 — Multiplicity [FLARE]": {
        "id": "Q010_multiplicity", "dataset": "FLARE",
        "text": "Find scans with multi-focal tumors or multi-organ involvement.",
        "constraints": ["multiplicity"], "min_tier": "T1", "t5_weight": "0%",
        "relevant_total": "22 / 85",
        "tiers": {
            "T1": {"count": 10, "scans": [("F1575",True,0,1.0),("F2100",True,1,0.98),("F0488",True,2,0.857),("F1115",True,3,0.857),("F1158",True,4,0.639),("F0689",True,5,0.596),("F0487",True,6,0.587),("F0955",True,7,0.54),("F2175",True,8,0.525),("F1474",True,9,0.44)]},
            "T2": {"count": 10, "scans": [("F2100",True,0,0.996),("F1575",True,1,0.971),("F1115",True,2,0.906),("F0488",True,3,0.855),("F0689",True,4,0.636),("F1158",True,5,0.625),("F0487",True,6,0.548),("F2175",True,7,0.525),("F0955",True,8,0.524),("F1474",True,9,0.503)]},
            "T3": {"count": 10, "scans": [("F2100",True,0,0.995),("F1575",True,1,0.969),("F1115",True,2,0.896),("F0488",True,3,0.862),("F0689",True,4,0.633),("F1158",True,5,0.62),("F1474",True,6,0.56),("F0487",True,7,0.551),("F0955",True,8,0.541),("F2175",True,9,0.534)]},
            "T4": {"count": 10, "scans": [("F1575",True,0,1.0),("F2100",True,1,0.991),("F0488",True,2,0.934),("F1115",True,3,0.886),("F0689",True,4,0.65),("F0487",True,5,0.578),("F2175",True,6,0.555),("F1158",True,7,0.522),("F1474",True,8,0.494),("F0083",True,9,0.477)]},
            "T5": {"count": 10, "scans": [("F2100",True,0,0.998),("F1575",True,1,0.975),("F0488",True,2,0.957),("F1115",True,3,0.921),("F0689",True,4,0.576),("F0487",True,5,0.537),("F2175",True,6,0.505),("F1158",True,7,0.502),("F1474",True,8,0.496),("F0083",True,9,0.487)]},
        },
        "takeaway": "All 5 tiers retrieve 10/10 relevant scans — a perfect hit rate. Multiplicity is captured directly by tabular tumor/organ count features.",
    },
    "Q028 — Coverage + Proximity [Pancreas]": {
        "id": "Q028_coverage_proximity", "dataset": "Pancreas",
        "text": "Find scans with high tumor coverage within the host organ AND close spatial proximity to adjacent structures.",
        "constraints": ["coverage", "proximity"], "min_tier": "T5", "t5_weight": "38.0%",
        "relevant_total": "14 / 57",
        "tiers": {
            "T1": {"count": 4, "scans": [("P094",False,0,0.978),("P088",False,1,0.956),("P414",True,2,0.928),("P391",False,3,0.909),("P041",True,4,0.895),("P012",True,5,0.781),("P071",False,6,0.704),("P131",True,7,0.618),("P086",False,8,0.595),("P405",False,9,0.534)]},
            "T2": {"count": 2, "scans": [("P074",False,0,0.949),("P310",False,1,0.869),("P071",False,2,0.859),("P398",True,3,0.847),("P391",False,4,0.8),("P157",False,5,0.789),("P350",False,6,0.736),("P012",True,7,0.691),("P094",False,8,0.684),("P231",False,9,0.664)]},
            "T3": {"count": 10, "scans": [("P098",True,0,0.978),("P041",True,1,0.974),("P274",True,2,0.92),("P012",True,3,0.919),("P395",True,4,0.872),("P398",True,5,0.852),("P107",True,6,0.845),("P122",True,7,0.841),("P125",True,8,0.826),("P414",True,9,0.816)]},
            "T4": {"count": 10, "scans": [("P041",True,0,0.999),("P098",True,1,0.978),("P274",True,2,0.931),("P012",True,3,0.897),("P107",True,4,0.893),("P395",True,5,0.882),("P125",True,6,0.856),("P122",True,7,0.823),("P414",True,8,0.818),("P398",True,9,0.806)]},
            "T5": {"count": 10, "scans": [("P041",True,0,0.978),("P098",True,1,0.96),("P274",True,2,0.924),("P107",True,3,0.882),("P012",True,4,0.86),("P125",True,5,0.857),("P395",True,6,0.85),("P122",True,7,0.839),("P398",True,8,0.812),("P414",True,9,0.81)]},
        },
        "takeaway": "Biggest T5 gain: 4→10 relevant (+6). Coverage+proximity needs visual understanding — CLIP is the key unlock.",
    },
    "Q009 — Coverage + Containment + Proximity [Pancreas]": {
        "id": "Q009_coverage_containment_proximity", "dataset": "Pancreas",
        "text": "Find scans with high tumor coverage AND complex organ topology AND close proximity to adjacent structures.",
        "constraints": ["coverage", "containment", "proximity"], "min_tier": "T5", "t5_weight": "63.3%",
        "relevant_total": "10 / 57",
        "tiers": {
            "T1": {"count": 2, "scans": [("P094",False,0,0.971),("P088",False,1,0.956),("P414",True,2,0.863),("P041",True,3,0.855),("P391",False,4,0.846),("P012",False,5,0.799),("P071",False,6,0.676),("P131",False,7,0.657),("P086",False,8,0.606),("P405",False,9,0.536)]},
            "T2": {"count": 1, "scans": [("P074",False,0,0.949),("P398",True,1,0.891),("P071",False,2,0.879),("P310",False,3,0.879),("P157",False,4,0.841),("P350",False,5,0.754),("P391",False,6,0.754),("P231",False,7,0.725),("P256",False,8,0.716),("P094",False,9,0.701)]},
            "T3": {"count": 8, "scans": [("P041",True,0,1.0),("P098",True,1,0.969),("P012",False,2,0.912),("P274",True,3,0.909),("P395",True,4,0.904),("P398",True,5,0.874),("P107",True,6,0.871),("P122",True,7,0.869),("P278",False,8,0.837),("P414",True,9,0.829)]},
            "T4": {"count": 8, "scans": [("P041",True,0,1.0),("P098",True,1,0.973),("P274",True,2,0.94),("P107",True,3,0.908),("P395",True,4,0.901),("P012",False,5,0.886),("P125",True,6,0.863),("P122",True,7,0.838),("P414",True,8,0.838),("P278",False,9,0.822)]},
            "T5": {"count": 9, "scans": [("P041",True,0,0.962),("P098",True,1,0.945),("P274",True,2,0.918),("P107",True,3,0.872),("P125",True,4,0.844),("P395",True,5,0.843),("P012",False,6,0.829),("P122",True,7,0.828),("P414",True,8,0.825),("P398",True,9,0.802)]},
        },
        "takeaway": "Progressive: 2→1→8→8→9. 3-constraint query needs all modalities. CLIP main unlock, VKG pushes to near-perfect 9/10.",
    },
    "Q138 — Volume + Containment [FLARE]": {
        "id": "Q138_volume_containment", "dataset": "FLARE",
        "text": "Find scans with high tumor volume AND complex organ topology (strong evidence paths).",
        "constraints": ["volume", "containment"], "min_tier": "T5", "t5_weight": "61.1%",
        "relevant_total": "20 / 85",
        "tiers": {
            "T1": {"count": 3, "scans": [("F1273",False,0,1.0),("F1074",True,1,0.926),("F0003",True,2,0.921),("F0281",False,3,0.904),("F1474",False,4,0.859),("F0487",False,5,0.786),("F1495",False,6,0.767),("F2017",False,7,0.763),("F1991",False,8,0.761),("F1654",True,9,0.758)]},
            "T2": {"count": 3, "scans": [("F1273",False,0,0.967),("F1074",True,1,0.947),("F0003",True,2,0.929),("F1474",False,3,0.874),("F0281",False,4,0.852),("F1495",False,5,0.808),("F1056",False,6,0.773),("F0802",False,7,0.77),("F1991",False,8,0.763),("F1107",True,9,0.762)]},
            "T3": {"count": 10, "scans": [("F0239",True,0,0.996),("F1314",True,1,0.991),("F1074",True,2,0.974),("F2123",True,3,0.973),("F0106",True,4,0.97),("F1115",True,5,0.966),("F0128",True,6,0.965),("F1225",True,7,0.961),("F0805",True,8,0.952),("F1107",True,9,0.916)]},
            "T4": {"count": 10, "scans": [("F0955",True,0,0.919),("F0239",True,1,0.886),("F1314",True,2,0.884),("F0128",True,3,0.874),("F0106",True,4,0.871),("F2123",True,5,0.864),("F1074",True,6,0.855),("F1225",True,7,0.852),("F1115",True,8,0.831),("F0805",True,9,0.826)]},
            "T5": {"count": 10, "scans": [("F0955",True,0,0.936),("F1314",True,1,0.908),("F1115",True,2,0.899),("F0239",True,3,0.89),("F2123",True,4,0.88),("F1225",True,5,0.871),("F1453",True,6,0.859),("F0128",True,7,0.855),("F1074",True,8,0.854),("F1107",True,9,0.849)]},
        },
        "takeaway": "Massive T3 jump (3→10). Containment requires organ topology — CLIP captures spatial patterns. Top-10 completely restructured.",
    },
    "Q059 — Volume + Proximity + Containment [LiTS]": {
        "id": "Q059_volume_proximity_containment", "dataset": "LiTS",
        "text": "Find scans with high tumor volume AND close proximity to adjacent structures AND complex organ topology.",
        "constraints": ["volume", "proximity", "containment"], "min_tier": "T5", "t5_weight": "61.7%",
        "relevant_total": "6 / 24",
        "tiers": {
            "T1": {"count": 3, "scans": [("9",False,0,0.873),("8",False,1,0.863),("21",False,2,0.862),("18",False,3,0.861),("78",False,4,0.852),("79",False,5,0.846),("103",True,6,0.836),("1",False,7,0.829),("113",True,8,0.826),("124",True,9,0.823)]},
            "T2": {"count": 2, "scans": [("8",False,0,0.968),("21",False,1,0.958),("69",False,2,0.915),("14",False,3,0.852),("9",False,4,0.817),("113",True,5,0.816),("0",False,6,0.804),("1",False,7,0.804),("18",False,8,0.785),("58",True,9,0.783)]},
            "T3": {"count": 3, "scans": [("103",True,0,0.988),("113",True,1,0.986),("74",False,2,0.96),("9",False,3,0.952),("78",False,4,0.95),("58",True,5,0.944),("71",False,6,0.918),("14",False,7,0.907),("69",False,8,0.897),("21",False,9,0.892)]},
            "T4": {"count": 3, "scans": [("103",True,0,0.983),("113",True,1,0.981),("74",False,2,0.953),("58",True,3,0.95),("9",False,4,0.94),("78",False,5,0.933),("71",False,6,0.92),("14",False,7,0.899),("21",False,8,0.887),("69",False,9,0.886)]},
            "T5": {"count": 6, "scans": [("113",True,0,0.96),("58",True,1,0.943),("103",True,2,0.939),("9",False,3,0.925),("78",False,4,0.916),("74",False,5,0.905),("71",False,6,0.905),("124",True,7,0.882),("97",True,8,0.877),("118",True,9,0.865)]},
        },
        "takeaway": "Most dramatic: T1–T4 plateau at 2–3/6, only T5 VKG reasoning achieves PERFECT 6/6.",
    },
}

TIER_COLORS = {"T1": "#607D8B", "T2": "#2196F3", "T3": "#FF9800", "T4": "#4CAF50", "T5": "#E91E63"}
TIER_LABELS = {"T1": "Attribute-only", "T2": "Semantic Emb.", "T3": "Multimodal (CLIP)", "T4": "GraphSAGE", "T5": "VKG (Ours)"}
NDCG_DATA = {"T1": [0.700, 0.545, 0.764], "T2": [0.696, 0.528, 0.767], "T3": [0.802, 0.860, 0.866], "T4": [0.802, 0.874, 0.865], "T5": [0.823, 0.890, 0.916]}
AUROC_DATA = {"T1": [0.663, 0.571, 0.662], "T2": [0.639, 0.543, 0.634], "T3": [0.749, 0.733, 0.788], "T4": [0.741, 0.742, 0.793], "T5": [0.762, 0.758, 0.859]}
DATASETS = ["LiTS", "Pancreas", "FLARE"]
PHENOTYPE_AUROC = {
    "LiTS": {"P1 Tumor Burden": [0.741,0.716,0.748,0.755,0.754], "P2 Visual Severity": [0.533,0.488,0.670,0.672,0.710], "P3 Structural Complexity": [0.775,0.789,0.826,0.803,0.812], "P4 Evidence Reasoning": [0.602,0.563,0.753,0.733,0.773]},
    "Pancreas": {"P1 Tumor Burden": [0.671,0.620,0.696,0.712,0.721], "P2 Visual Severity": [0.534,0.482,0.837,0.851,0.879], "P3 Structural Complexity": [0.582,0.638,0.625,0.623,0.626], "P4 Evidence Reasoning": [0.497,0.433,0.773,0.784,0.804]},
    "FLARE": {"P1 Tumor Burden": [0.657,0.602,0.695,0.704,0.709], "P2 Visual Severity": [0.622,0.585,0.881,0.884,0.896], "P3 Structural Complexity": [0.773,0.774,0.803,0.805,0.974], "P4 Evidence Reasoning": [0.596,0.576,0.774,0.780,0.858]},
}

# ── Placeholder 3D organ data per scan (generated procedurally) ──────────────
ORGAN_COLORS = {"Liver": "#1565C0", "Right Kidney": "#2E7D32", "Spleen": "#C62828",
                "Pancreas": "#F9A825", "Left Kidney": "#7B1FA2", "Tumor": "#212121"}

def _generate_organ_ellipsoid(cx, cy, cz, rx, ry, rz, n=300, rng=None):
    if rng is None: rng = np.random.RandomState(42)
    u = rng.uniform(0, 2*np.pi, n)
    v = rng.uniform(0, np.pi, n)
    x = cx + rx * np.cos(u) * np.sin(v) + rng.normal(0, rx*0.08, n)
    y = cy + ry * np.sin(u) * np.sin(v) + rng.normal(0, ry*0.08, n)
    z = cz + rz * np.cos(v) + rng.normal(0, rz*0.08, n)
    return x, y, z

def generate_3d_scan_data(scan_id, dataset, seed=42):
    rng = np.random.RandomState(hash(scan_id) % 2**31)
    structures = {}
    if dataset == "Pancreas":
        structures["Pancreas"] = _generate_organ_ellipsoid(40, 120, 80, 15, 40, 20, 400, rng)
        n_tumors = rng.randint(1, 3)
        for t in range(n_tumors):
            tx = 40 + rng.randint(-10, 10)
            ty = 120 + rng.randint(-30, 30)
            structures[f"Tumor {t+1}"] = _generate_organ_ellipsoid(tx, ty, 80+rng.randint(-10,10), 5+rng.randint(0,5), 5+rng.randint(0,5), 4+rng.randint(0,4), 200, rng)
    elif dataset == "LiTS":
        structures["Liver"] = _generate_organ_ellipsoid(120, 150, 120, 60, 50, 40, 600, rng)
        n_tumors = rng.randint(1, 5)
        for t in range(n_tumors):
            tx = 120 + rng.randint(-40, 40)
            ty = 150 + rng.randint(-30, 30)
            structures[f"Tumor {t+1}"] = _generate_organ_ellipsoid(tx, ty, 120+rng.randint(-20,20), 8+rng.randint(0,8), 6+rng.randint(0,6), 5+rng.randint(0,5), 150, rng)
    else:  # FLARE
        structures["Liver"] = _generate_organ_ellipsoid(150, 170, 130, 65, 55, 45, 500, rng)
        structures["Right Kidney"] = _generate_organ_ellipsoid(80, 120, 110, 15, 25, 20, 250, rng)
        structures["Spleen"] = _generate_organ_ellipsoid(220, 100, 100, 25, 30, 20, 300, rng)
        structures["Pancreas"] = _generate_organ_ellipsoid(140, 120, 100, 12, 35, 12, 250, rng)
        structures["Left Kidney"] = _generate_organ_ellipsoid(210, 130, 110, 15, 25, 20, 250, rng)
        n_tumors = rng.randint(1, 4)
        organs_list = ["Liver", "Spleen", "Pancreas"]
        for t in range(n_tumors):
            org = organs_list[t % len(organs_list)]
            base = structures[org]
            cx = float(np.mean(base[0])) + rng.randint(-10, 10)
            cy = float(np.mean(base[1])) + rng.randint(-10, 10)
            cz = float(np.mean(base[2])) + rng.randint(-5, 5)
            structures[f"Tumor {t+1}"] = _generate_organ_ellipsoid(cx, cy, cz, 6+rng.randint(0,8), 5+rng.randint(0,6), 4+rng.randint(0,5), 150, rng)
    return structures

# ── Detailed KG subgraph data with metadata per scan ──────────────────────
SCAN_KG_META = {}
def _build_scan_kg(scan_id, dataset, relevant, rank, score):
    rng = np.random.RandomState(hash(scan_id) % 2**31)
    organs = ["Pancreas"] if dataset == "Pancreas" else ["Liver"] if dataset == "LiTS" else ["Liver", "Spleen", "Pancreas", "Right Kidney", "Left Kidney"]
    n_tumors = rng.randint(1, 4) if dataset == "FLARE" else rng.randint(1, 3)
    tumors = []
    for t in range(n_tumors):
        vol = rng.randint(100, 15000)
        cov = round(rng.uniform(0.05, 30.0), 2)
        dist = round(rng.uniform(3.0, 80.0), 1)
        org = organs[t % len(organs)]
        tumors.append({"id": f"T{t+1}", "vol": vol, "cov": cov, "dist": dist, "organ": org})
    features = [("structural", round(rng.uniform(0.4, 0.99), 2)),
                ("spatial", round(rng.uniform(0.3, 0.98), 2)),
                ("morphology", round(rng.uniform(0.5, 0.95), 2))]
    if rng.random() > 0.3:
        features.append(("appearance", round(rng.uniform(0.4, 0.92), 2)))
    return {"scan_id": scan_id, "dataset": dataset, "relevant": relevant,
            "rank": rank, "score": score, "tumors": tumors,
            "organs": list(set(t["organ"] for t in tumors)),
            "features": features}

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 VKG Tier Evaluation")
    st.markdown("**Visual Knowledge Graph** capability-tier evaluation for medical scan retrieval.")
    st.markdown("---")
    st.markdown("### 🎨 Tier Legend")
    for tk, color in TIER_COLORS.items():
        st.markdown(f'<span style="background:{color}33;color:{color};padding:4px 12px;border-radius:10px;font-weight:600;border:1px solid {color}55">{tk} — {TIER_LABELS[tk]}</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📖 Constraints")
    for c, cls in [("Volume","volume"),("Coverage","coverage"),("Proximity","proximity"),("Multiplicity","multiplicity"),("Containment","containment")]:
        st.markdown(f'<span class="query-badge badge-{cls}">{c}</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🔬 3D Color Legend")
    for org, col in ORGAN_COLORS.items():
        st.markdown(f'<span style="color:{col};font-weight:600">● {org}</span>', unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 🧬 VKG Capability-Tier Evaluation — Interactive Demo")
st.markdown("*Progressive feature tiers (T1→T5) for medical scan retrieval across 3 datasets.*")

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Query Browser", "📊 Tier Viz", "🧠 KG Subgraphs", "🫀 3D Organs", "📋 Summary"])

# === TAB 1: Query Browser ====================================================
with tab1:
    selected_q = st.selectbox("**Select a Query Case:**", list(QUERIES.keys()))
    q = QUERIES[selected_q]
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card"><h3>{q["dataset"]}</h3><p>Dataset</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><h3>{q["min_tier"]}</h3><p>Min Tier</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><h3>{q["t5_weight"]}</h3><p>T5 Weight</p></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><h3>{q["relevant_total"]}</h3><p>Relevant</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.info(f'📝 *"{q["text"]}"*')
    st.markdown("**Constraints:** " + " ".join(f'<span class="query-badge badge-{c}">{c.title()}</span>' for c in q["constraints"]), unsafe_allow_html=True)

    # Show ALL top-10 scans for selected tier
    st.markdown("### 📋 Top-10 Retrieved Scans (All Visible)")
    tier_sel = st.select_slider("Tier:", ["T1","T2","T3","T4","T5"], value="T5", key="t1_slider")
    scans = q["tiers"][tier_sel]["scans"]

    # Display as scan cards in 2 columns
    col_l, col_r = st.columns(2)
    for idx, (sid, rel, rank, score) in enumerate(scans):
        card_class = "scan-relevant" if rel else "scan-irrelevant"
        icon = "✅" if rel else "❌"
        card_html = f'''<div class="scan-card {card_class}">
            <strong>#{rank+1}</strong> &nbsp; {icon} &nbsp; <code>{sid}</code>
            &emsp; Score: <strong>{score:.3f}</strong>
        </div>'''
        if idx < 5:
            with col_l: st.markdown(card_html, unsafe_allow_html=True)
        else:
            with col_r: st.markdown(card_html, unsafe_allow_html=True)

    st.success(f"**{tier_sel}:** {q['tiers'][tier_sel]['count']}/{q['relevant_total'].split('/')[0].strip()} relevant in top-10")

# === TAB 2: Tier Viz ==========================================================
with tab2:
    selected_q2 = st.selectbox("**Select Query:**", list(QUERIES.keys()), key="tab2_q")
    q2 = QUERIES[selected_q2]

    counts = [q2["tiers"][t]["count"] for t in ["T1","T2","T3","T4","T5"]]
    fig_bar = go.Figure()
    for i, tk in enumerate(["T1","T2","T3","T4","T5"]):
        fig_bar.add_trace(go.Bar(x=[tk], y=[counts[i]], marker_color=TIER_COLORS[tk], name=f"{tk}", text=[counts[i]], textposition="outside", textfont=dict(size=16, color="#1e293b")))
    total_rel = int(q2["relevant_total"].split("/")[0].strip())
    fig_bar.add_hline(y=total_rel, line_dash="dash", line_color="rgba(100,116,139,0.4)", annotation_text=f"Total: {total_rel}", annotation_font_color="#475569")
    fig_bar.update_layout(title=f"Relevant in Top-10 — {q2['id']}", template="plotly_white", paper_bgcolor="white", plot_bgcolor="#f8fafc", yaxis_title="# Relevant", showlegend=False, height=380, font=dict(family="Inter", color="#1e293b"))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Rank heatmap
    all_scan_ids = set()
    for tk in ["T1","T2","T3","T4","T5"]:
        for sid, rel, rank, score in q2["tiers"][tk]["scans"]:
            if rel: all_scan_ids.add(sid)
    all_scan_ids = sorted(all_scan_ids)[:10]
    heat_data = []
    for sid in all_scan_ids:
        row = []
        for tk in ["T1","T2","T3","T4","T5"]:
            found = None
            for s, rel, rank, score in q2["tiers"][tk]["scans"]:
                if s == sid and rel:
                    found = rank + 1
                    break
            row.append(found)
        heat_data.append(row)
    fig_heat = go.Figure(go.Heatmap(z=heat_data, x=["T1","T2","T3","T4","T5"], y=all_scan_ids, colorscale="RdYlGn_r", zmin=1, zmax=10, text=heat_data, texttemplate="%{text}", textfont=dict(size=13)))
    fig_heat.update_layout(title="Rank of Relevant Scans (1=best, blank=outside)", template="plotly_white", paper_bgcolor="white", plot_bgcolor="#f8fafc", height=max(250, 40*len(all_scan_ids)), font=dict(family="Inter", color="#1e293b"), yaxis=dict(dtick=1))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.warning(f"💡 **Takeaway:** {q2['takeaway']}")

# === TAB 3: KG Subgraphs (Show ALL top-10 scans) =============================
with tab3:
    selected_q3 = st.selectbox("**Select Query:**", list(QUERIES.keys()), key="tab3_q")
    q3 = QUERIES[selected_q3]
    tier_kg = st.select_slider("Tier:", ["T1","T2","T3","T4","T5"], value="T5", key="kg_tier")

    st.markdown("### 🕸️ Knowledge Graph Subgraphs — All Top-10 Scans")
    st.caption("Each scan shown with its KG structure: CT Scan → Tumors (vol, cov%, dist) → Organs → Image → Features")

    scans_kg = q3["tiers"][tier_kg]["scans"]

    # Let user pick which scan to view in detail
    scan_options = [f"#{r+1} {sid} ({'✅ Relevant' if rel else '❌ Irrelevant'}) — score {sc:.3f}" for sid, rel, r, sc in scans_kg]
    selected_scan_idx = st.selectbox("View scan KG:", range(len(scan_options)), format_func=lambda i: scan_options[i], key="scan_kg_sel")

    sid_sel, rel_sel, rank_sel, score_sel = scans_kg[selected_scan_idx]
    kg_data = _build_scan_kg(sid_sel, q3["dataset"], rel_sel, rank_sel, score_sel)

    # Build KG data for vis.js
    vis_nodes = []
    vis_edges = []
    node_id_counter = 0
    node_id_map = {}

    # CTScan node
    ct_id = f"CTScan_{sid_sel}"
    node_id_map[ct_id] = node_id_counter
    vis_nodes.append({"id": node_id_counter, "label": f"CT Scan\n{sid_sel}",
        "color": {"background": "#1565C0", "border": "#0D47A1", "highlight": {"background": "#1E88E5", "border": "#0D47A1"}},
        "shape": "box", "margin": 10, "font": {"color": "white", "size": 14, "face": "Inter", "multi": True}})
    node_id_counter += 1

    # Tumor nodes
    for t in kg_data["tumors"]:
        t_id = f"Tumor_{t['id']}"
        node_id_map[t_id] = node_id_counter
        vis_nodes.append({"id": node_id_counter, "label": f"{t['id']}\nvol={t['vol']}\ncov={t['cov']}%",
            "color": {"background": "#E53935", "border": "#B71C1C", "highlight": {"background": "#EF5350", "border": "#B71C1C"}},
            "shape": "box", "margin": 8, "font": {"color": "white", "size": 12, "face": "Inter", "multi": True}})
        vis_edges.append({"from": node_id_map[ct_id], "to": node_id_counter, "label": "hasTumor",
            "color": {"color": "#64748b"}, "font": {"color": "#1e293b", "size": 11, "strokeWidth": 0, "background": "#f1f5f9"}})
        # Organ node
        o_id = f"Organ_{t['organ']}"
        if o_id not in node_id_map:
            node_id_counter += 1
            node_id_map[o_id] = node_id_counter
            vis_nodes.append({"id": node_id_counter, "label": t["organ"],
                "color": {"background": "#43A047", "border": "#2E7D32", "highlight": {"background": "#66BB6A", "border": "#2E7D32"}},
                "shape": "box", "margin": 8, "font": {"color": "white", "size": 12, "face": "Inter"}})
        vis_edges.append({"from": node_id_map[t_id], "to": node_id_map[o_id], "label": f"connectedTo (dist={t['dist']})",
            "color": {"color": "#64748b"}, "font": {"color": "#1e293b", "size": 10, "strokeWidth": 0, "background": "#f1f5f9"}})
        node_id_counter += 1

    # Image node
    img_id = "Image_Viz"
    node_id_map[img_id] = node_id_counter
    vis_nodes.append({"id": node_id_counter, "label": "Image\n3D Viz",
        "color": {"background": "#AB47BC", "border": "#7B1FA2", "highlight": {"background": "#CE93D8", "border": "#7B1FA2"}},
        "shape": "box", "margin": 8, "font": {"color": "white", "size": 12, "face": "Inter", "multi": True}})
    first_tumor = [k for k in node_id_map if k.startswith("Tumor_")]
    if first_tumor:
        vis_edges.append({"from": node_id_map[first_tumor[0]], "to": node_id_counter, "label": "hasViz",
            "color": {"color": "#64748b"}, "font": {"color": "#1e293b", "size": 10, "strokeWidth": 0, "background": "#f1f5f9"}})
    node_id_counter += 1

    # Feature nodes
    for cat, conf in kg_data["features"]:
        f_id = f"Feat_{cat}"
        node_id_map[f_id] = node_id_counter
        vis_nodes.append({"id": node_id_counter, "label": f"{cat}\nconf={conf}",
            "color": {"background": "#FF9800", "border": "#E65100", "highlight": {"background": "#FFB74D", "border": "#E65100"}},
            "shape": "box", "margin": 6, "font": {"color": "white", "size": 11, "face": "Inter", "multi": True}})
        vis_edges.append({"from": node_id_map[img_id], "to": node_id_counter, "label": "hasFeature",
            "color": {"color": "#64748b"}, "font": {"color": "#1e293b", "size": 10, "strokeWidth": 0, "background": "#f1f5f9"}})
        node_id_counter += 1

    # Proximity edges between tumors
    tumor_keys = [k for k in node_id_map if k.startswith("Tumor_")]
    for i in range(len(tumor_keys)):
        for j in range(i+1, len(tumor_keys)):
            vis_edges.append({"from": node_id_map[tumor_keys[i]], "to": node_id_map[tumor_keys[j]],
                "label": "proximate", "dashes": True,
                "color": {"color": "#94a3b8"}, "font": {"color": "#475569", "size": 10, "strokeWidth": 0, "background": "#f1f5f9"}})

    # Adjacency between organs
    organ_keys = [k for k in node_id_map if k.startswith("Organ_")]
    for i in range(len(organ_keys)):
        for j in range(i+1, len(organ_keys)):
            vis_edges.append({"from": node_id_map[organ_keys[i]], "to": node_id_map[organ_keys[j]],
                "label": "adjacent", "dashes": True,
                "color": {"color": "#94a3b8"}, "font": {"color": "#475569", "size": 10, "strokeWidth": 0, "background": "#f1f5f9"}})

    rel_status = "✅ RELEVANT" if rel_sel else "❌ IRRELEVANT"
    title_html = f"KG: {sid_sel} [{q3['dataset']}] | {tier_kg} #{rank_sel+1} | {rel_status}"

    # Render vis.js interactive force-directed graph
    vis_html = f"""
    <html><head>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
      body {{ margin:0; background: transparent; font-family: Inter, sans-serif; }}
      #title {{ color: #1e293b; font-size: 14px; font-weight: 600; padding: 8px 12px; text-align: center; }}
      #kg-container {{ width: 100%; height: 520px; border: 1px solid #e2e8f0;
                       border-radius: 12px; background: #ffffff; }}
      #legend {{ display: flex; gap: 16px; justify-content: center; padding: 8px; color: #475569; font-size: 12px; }}
      .leg-item {{ display:flex; align-items:center; gap:4px; }}
      .leg-dot {{ width:12px; height:12px; border-radius:50%; display:inline-block; }}
    </style>
    </head><body>
    <div id="title">{title_html}</div>
    <div id="kg-container"></div>
    <div id="legend">
      <span class="leg-item"><span class="leg-dot" style="background:#1565C0"></span> CTScan</span>
      <span class="leg-item"><span class="leg-dot" style="background:#E53935"></span> Tumor</span>
      <span class="leg-item"><span class="leg-dot" style="background:#43A047"></span> Organ</span>
      <span class="leg-item"><span class="leg-dot" style="background:#AB47BC"></span> Image</span>
      <span class="leg-item"><span class="leg-dot" style="background:#FF9800"></span> Feature</span>
      <span style="color:#64748b; margin-left:12px">⟵ Drag nodes to rearrange ⟶</span>
    </div>
    <script>
      var nodes = new vis.DataSet({json.dumps(vis_nodes)});
      var edges = new vis.DataSet({json.dumps(vis_edges)});
      var container = document.getElementById('kg-container');
      var data = {{ nodes: nodes, edges: edges }};
      var options = {{
        physics: {{
          enabled: true,
          solver: 'forceAtlas2Based',
          forceAtlas2Based: {{
            gravitationalConstant: -60,
            centralGravity: 0.015,
            springLength: 160,
            springConstant: 0.06,
            damping: 0.4,
            avoidOverlap: 0.8
          }},
          stabilization: {{ iterations: 200, fit: true }}
        }},
        interaction: {{
          dragNodes: true,
          dragView: true,
          zoomView: true,
          hover: true,
          tooltipDelay: 100
        }},
        edges: {{
          smooth: {{ type: 'continuous', roundness: 0.3 }},
          width: 2,
          arrows: {{ to: {{ enabled: true, scaleFactor: 0.6 }} }}
        }},
        nodes: {{
          borderWidth: 2,
          shadow: {{ enabled: true, color: 'rgba(0,0,0,0.15)', size: 6 }}
        }}
      }};
      var network = new vis.Network(container, data, options);
      network.once('stabilized', function() {{
        network.fit({{ animation: {{ duration: 500, easingFunction: 'easeInOutQuad' }} }});
      }});
    </script>
    </body></html>
    """
    components.html(vis_html, height=600, scrolling=False)

    st.markdown("**Node Types:** 🔵 CTScan &nbsp; 🔴 Tumor (vol, cov%) &nbsp; 🟢 Organ &nbsp; 🟣 Image &nbsp; 🟠 Feature (category, confidence)")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Nodes", len(vis_nodes))
    with c2: st.metric("Edges", len(vis_edges))
    with c3: st.metric("Tumors", len(kg_data["tumors"]))
    with c4: st.metric("Organs", len(kg_data["organs"]))

    # Scan gallery: show mini-cards for all 10
    st.markdown("### 📋 All Top-10 Scan KG Overview")
    rows_overview = []
    for sid, rel, rank, score in scans_kg:
        kg_info = _build_scan_kg(sid, q3["dataset"], rel, rank, score)
        rows_overview.append({
            "Rank": f"#{rank+1}",
            "Scan": sid,
            "Relevant": "✅" if rel else "❌",
            "Score": f"{score:.3f}",
            "Tumors": len(kg_info["tumors"]),
            "Organs": ", ".join(kg_info["organs"]),
            "Features": len(kg_info["features"]),
            "Total Vol": sum(t["vol"] for t in kg_info["tumors"]),
            "Max Cov%": max(t["cov"] for t in kg_info["tumors"]),
            "Min Dist": min(t["dist"] for t in kg_info["tumors"]),
        })
    st.dataframe(pd.DataFrame(rows_overview), use_container_width=True, hide_index=True)

# === TAB 4: 3D Organ Visualization ============================================
with tab4:
    selected_q4 = st.selectbox("**Select Query:**", list(QUERIES.keys()), key="tab4_q")
    q4 = QUERIES[selected_q4]
    tier_3d = st.select_slider("Tier:", ["T1","T2","T3","T4","T5"], value="T5", key="3d_tier")

    st.markdown("### 🫀 3D Organ & Tumor Visualizations — Top Retrieved Scans")
    st.caption("Interactive 3D scatter plots showing organ structures and tumor positions in voxel space. Rotate, zoom, and pan to explore.")

    scans_3d = q4["tiers"][tier_3d]["scans"]

    # Let user view 1 or compare 2 scans
    view_mode = st.radio("View mode:", ["Single scan detail", "Compare 2 scans side-by-side"], horizontal=True)

    def render_3d_scan(scan_id, dataset, relevant, rank, score, container):
        structs = generate_3d_scan_data(scan_id, dataset)
        fig = go.Figure()
        for name, (x, y, z) in structs.items():
            is_tumor = "Tumor" in name
            color = ORGAN_COLORS.get(name, ORGAN_COLORS.get("Tumor", "#666"))
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z, mode="markers",
                marker=dict(size=3 if not is_tumor else 4, color=color, opacity=0.6 if not is_tumor else 0.85),
                name=name,
                hovertemplate=f"{name}<br>x=%{{x:.0f}}<br>y=%{{y:.0f}}<br>z=%{{z:.0f}}<extra></extra>"
            ))
        rel_txt = "✅ RELEVANT" if relevant else "❌ IRRELEVANT"
        fig.update_layout(
            title=dict(text=f"3D Viz: {scan_id} [{dataset}] | Rank #{rank+1} | {rel_txt}", font=dict(size=13, color="#1e293b")),
            template="plotly_white", paper_bgcolor="white",
            scene=dict(
                xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
                xaxis=dict(backgroundcolor="white", gridcolor="rgba(100,116,139,0.15)", color="#475569"),
                yaxis=dict(backgroundcolor="white", gridcolor="rgba(100,116,139,0.15)", color="#475569"),
                zaxis=dict(backgroundcolor="#f1f5f9", gridcolor="rgba(100,116,139,0.15)", color="#475569"),
                aspectmode="data"
            ),
            height=500, margin=dict(l=0,r=0,t=40,b=0),
            legend=dict(orientation="h", y=-0.05, font=dict(size=10, color="#1e293b")),
            font=dict(family="Inter", color="#1e293b")
        )
        container.plotly_chart(fig, use_container_width=True)

    if view_mode == "Single scan detail":
        scan_opts_3d = [f"#{r+1} {sid} ({'✅' if rel else '❌'}) — {sc:.3f}" for sid, rel, r, sc in scans_3d]
        sel_idx = st.selectbox("Select scan:", range(len(scan_opts_3d)), format_func=lambda i: scan_opts_3d[i], key="3d_scan_sel")
        sid, rel, rank, score = scans_3d[sel_idx]
        render_3d_scan(sid, q4["dataset"], rel, rank, score, st)
    else:
        scan_opts_3d = [f"#{r+1} {sid} ({'✅' if rel else '❌'})" for sid, rel, r, sc in scans_3d]
        col_a, col_b = st.columns(2)
        with col_a:
            idx_a = st.selectbox("Scan A:", range(len(scan_opts_3d)), format_func=lambda i: scan_opts_3d[i], index=0, key="3d_a")
        with col_b:
            idx_b = st.selectbox("Scan B:", range(len(scan_opts_3d)), format_func=lambda i: scan_opts_3d[i], index=min(1, len(scan_opts_3d)-1), key="3d_b")
        col_3a, col_3b = st.columns(2)
        sid_a, rel_a, r_a, sc_a = scans_3d[idx_a]
        sid_b, rel_b, r_b, sc_b = scans_3d[idx_b]
        render_3d_scan(sid_a, q4["dataset"], rel_a, r_a, sc_a, col_3a)
        render_3d_scan(sid_b, q4["dataset"], rel_b, r_b, sc_b, col_3b)

    # Mini gallery: show all 10 scans as a summary table
    st.markdown("### 📋 All Top-10 Scans — Structural Summary")
    rows_3d = []
    for sid, rel, rank, score in scans_3d:
        structs = generate_3d_scan_data(sid, q4["dataset"])
        organ_names = [k for k in structs if "Tumor" not in k]
        tumor_names = [k for k in structs if "Tumor" in k]
        rows_3d.append({
            "Rank": f"#{rank+1}", "Scan": sid, "Relevant": "✅" if rel else "❌",
            "Score": f"{score:.3f}", "Organs": ", ".join(organ_names),
            "# Tumors": len(tumor_names),
        })
    st.dataframe(pd.DataFrame(rows_3d), use_container_width=True, hide_index=True)

# === TAB 5: Summary Dashboard ================================================
with tab5:
    st.markdown("### 📊 Results Overview — All Datasets Side by Side")
    mc1, mc2, mc3 = st.columns(3)
    with mc1: st.markdown('<div class="metric-card"><h3>0.916</h3><p>Best nDCG@10 (FLARE T5)</p></div>', unsafe_allow_html=True)
    with mc2: st.markdown('<div class="metric-card"><h3>0.859</h3><p>Best Avg AUROC (FLARE T5)</p></div>', unsafe_allow_html=True)
    with mc3: st.markdown('<div class="metric-card"><h3>+19.8%</h3><p>Avg T5 vs T1 nDCG Gain</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Table 1: nDCG@10")
        rows = [{"Method": f"{tk} {TIER_LABELS[tk]}", "LiTS": NDCG_DATA[tk][0], "Pancreas": NDCG_DATA[tk][1], "FLARE": NDCG_DATA[tk][2]} for tk in ["T1","T2","T3","T4","T5"]]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    with col_b:
        st.markdown("#### Table 2: AUROC")
        rows = [{"Method": f"{tk} {TIER_LABELS[tk]}", "LiTS": AUROC_DATA[tk][0], "Pancreas": AUROC_DATA[tk][1], "FLARE": AUROC_DATA[tk][2]} for tk in ["T1","T2","T3","T4","T5"]]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.markdown("---")
    st.markdown("#### 📈 nDCG@10 Across Datasets")
    fig_ndcg = go.Figure()
    for i, ds in enumerate(DATASETS):
        fig_ndcg.add_trace(go.Bar(name=ds, x=["T1","T2","T3","T4","T5"], y=[NDCG_DATA[tk][i] for tk in ["T1","T2","T3","T4","T5"]], text=[f"{NDCG_DATA[tk][i]:.3f}" for tk in ["T1","T2","T3","T4","T5"]], textposition="outside"))
    fig_ndcg.update_layout(barmode="group", template="plotly_white", paper_bgcolor="white", plot_bgcolor="#f8fafc", height=380, yaxis_title="nDCG@10", font=dict(family="Inter", color="#1e293b"), legend=dict(orientation="h", y=1.15))
    st.plotly_chart(fig_ndcg, use_container_width=True)
    st.markdown("#### 🧬 Per-Phenotype AUROC")
    ds_sel = st.selectbox("Dataset:", DATASETS, key="pheno_ds")
    pheno = PHENOTYPE_AUROC[ds_sel]
    fig_pheno = go.Figure()
    for pname, vals in pheno.items():
        fig_pheno.add_trace(go.Scatter(x=["T1","T2","T3","T4","T5"], y=vals, mode="lines+markers", name=pname, line=dict(width=3), marker=dict(size=10)))
    fig_pheno.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="#f8fafc", height=380, yaxis_title="AUROC", yaxis_range=[0.35,1.0], font=dict(family="Inter", color="#1e293b"), legend=dict(orientation="h", y=1.15))
    st.plotly_chart(fig_pheno, use_container_width=True)
    st.markdown("#### 🏆 Case Summary")
    summary_rows = [
        {"Case": 1, "Dataset": "FLARE", "Query": "Q010", "Constraints": "multiplicity", "Min Tier": "T1", "Hits T1→T5": "10→10→10→10→10", "Insight": "All tiers equivalent"},
        {"Case": 2, "Dataset": "Pancreas", "Query": "Q028", "Constraints": "coverage+proximity", "Min Tier": "T5", "Hits T1→T5": "4→2→10→10→10", "Insight": "CLIP key unlock +8 at T3"},
        {"Case": 3, "Dataset": "Pancreas", "Query": "Q009", "Constraints": "cov+cont+prox", "Min Tier": "T5", "Hits T1→T5": "2→1→8→8→9", "Insight": "Progressive improvement"},
        {"Case": 4, "Dataset": "FLARE", "Query": "Q138", "Constraints": "volume+containment", "Min Tier": "T5", "Hits T1→T5": "3→3→10→10→10", "Insight": "CLIP reshuffles top-10"},
        {"Case": 5, "Dataset": "LiTS", "Query": "Q059", "Constraints": "vol+prox+cont", "Min Tier": "T5", "Hits T1→T5": "3→2→3→3→6", "Insight": "Only VKG perfect retrieval"},
    ]
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)
