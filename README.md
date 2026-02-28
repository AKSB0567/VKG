# 🧬 VKG — Visual Knowledge Graph Capability-Tier Evaluation

> **Interactive demo** showcasing how progressive feature tiers (T1→T5) improve medical CT scan retrieval using Visual Knowledge Graphs.

🔗 **Live Demo:** [https://vkg-cvpr.streamlit.app/](https://vkg-cvpr.streamlit.app/)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vkg-cvpr.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?logo=plotly)
![vis.js](https://img.shields.io/badge/vis.js-Network-orange)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features & Tabs](#features--tabs)
- [Installation & Setup](#installation--setup)
- [Running Locally](#running-locally)
- [Deployment to Streamlit Cloud](#deployment-to-streamlit-cloud)
- [Project Structure](#project-structure)
- [Technologies](#technologies)

---

## Overview

The **VKG (Visual Knowledge Graph)** system enables capability-tier evaluation for medical scan retrieval across three abdominal CT datasets:

| Dataset | Organ Focus | # Scans |
|---------|------------|---------|
| **FLARE** | Multi-organ (Liver, Spleen, Kidneys, Pancreas) | 85 |
| **Pancreas** | Pancreas | 57 |
| **LiTS** | Liver | 24 |

### The 5 Feature Tiers

| Tier | Name | Description |
|------|------|-------------|
| **T1** | Attribute-only | Tabular metadata (tumor count, volume, etc.) |
| **T2** | Semantic Embedding | Dense vector embeddings of scan features |
| **T3** | Multimodal (CLIP) | Vision-language model features for spatial understanding |
| **T4** | GraphSAGE | Graph neural network embeddings over the KG |
| **T5** | **VKG (Ours)** | Full visual knowledge graph with all modalities combined |

### Query Constraints

Queries test retrieval under different phenotypic constraints:
- 🔴 **Volume** — Tumor size metrics
- 🟡 **Coverage** — Tumor coverage within host organ
- 🟢 **Proximity** — Distance to adjacent anatomical structures
- 🔵 **Multiplicity** — Multi-focal tumors or multi-organ involvement
- 🟣 **Containment** — Complex organ topology and spatial relationships

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │  Query   │ │  Tier    │ │   KG     │ │  3D      │   │
│  │ Browser  │ │  Viz     │ │Subgraphs │ │ Organs   │   │
│  │ (Tab 1)  │ │ (Tab 2)  │ │ (Tab 3)  │ │ (Tab 4)  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Summary Dashboard (Tab 5)             │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│ Components:                                              │
│  • Plotly (Charts, 3D Scatter)                          │
│  • vis.js (Force-directed KG)                           │
│  • Custom CSS (Light medical theme)                     │
├─────────────────────────────────────────────────────────┤
│ Data Layer:                                              │
│  • Hardcoded query results (5 representative cases)     │
│  • Procedural 3D organ/tumor generation via NumPy       │
│  • Per-scan KG metadata (tumors, organs, features)      │
└─────────────────────────────────────────────────────────┘
```

---

## Features & Tabs

### Tab 1: 🔍 Query Browser

Browse individual query cases and inspect retrieval results per tier.

- **Metric cards** showing dataset, minimum tier, T5 weight, and relevance count
- **Natural language query** with constraint badges
- **Top-10 retrieved scans** displayed as cards with rank, scan ID, relevance status (✅/❌), and similarity score
- **Tier slider** to compare retrieval results across T1→T5

### Tab 2: 📊 Tier Visualization

Compare tier performance through interactive charts.

- **Bar chart** — Number of relevant scans retrieved per tier for the selected query
- **Rank heatmap** — Where each relevant scan appears in the top-10 across all tiers (color-coded, 1=best)
- **Takeaway insight** highlighting the key finding for each query

### Tab 3: 🧠 KG Subgraphs

Explore the Knowledge Graph structure for each retrieved scan using an **interactive vis.js force-directed graph**.

- **Box-shaped nodes** with metadata written directly on them:
  - 🔵 **CT Scan** — Scan identifier
  - 🔴 **Tumor** — Volume, coverage %, distance to nearest organ
  - 🟢 **Organ** — Organ name (Liver, Pancreas, etc.)
  - 🟣 **Image** — 3D visualization reference
  - 🟠 **Feature** — Category and confidence score
- **Labeled directed edges** showing relationships: `hasTumor`, `connectedTo`, `hasViz`, `hasFeature`, `proximate`, `adjacent`
- **Physics simulation** — Drag nodes to rearrange; the graph adjusts dynamically
- **Auto-centered** — Graph fits all nodes in view after stabilization
- **Scan overview table** — Metadata summary for all 10 retrieved scans

### Tab 4: 🫀 3D Organs

Interactive 3D scatter plots visualizing organ structures and tumor positions in voxel space.

- **Point-cloud rendering** — Each organ rendered as a cluster of colored dots
- **Tumor visualization** — Tumors shown as darker, denser point clusters positioned within the organs
- **Interactive 3D rotation** — Rotate, zoom, and pan to explore spatial relationships
- **Single scan detail** or **side-by-side comparison** mode
- **Structural summary table** — All 10 scans with organ lists and tumor counts

### Tab 5: 📈 Summary Dashboard

Aggregate performance metrics across all datasets.

- **nDCG@10 grouped bar chart** — Normalized Discounted Cumulative Gain comparing tiers across FLARE, LiTS, and Pancreas
- **Per-phenotype AUROC line chart** — Classification performance for individual phenotypes (volume, coverage, proximity, etc.)
- **Case summary table** — Key observations and T5 impact for each query

### Sidebar

Persistent sidebar with:
- 🎯 **Tier Legend** — Color-coded tier labels (T1–T5)
- 📋 **Constraint Legend** — All 5 phenotypic constraints with colored badges

---

## Installation & Setup

### Prerequisites

- **Python 3.9+** installed
- **pip** package manager
- **Git** installed

### Step 1: Clone the Repository

```bash
git clone https://github.com/AKSB0567/VKG.git
cd VKG
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — Web framework
- `plotly` — Interactive charts and 3D visualizations
- `pandas` — Data manipulation
- `numpy` — Numerical computation (used for procedural 3D organ generation)

---

## Running Locally

### Start the Streamlit Server

```bash
streamlit run app.py
```

The app will automatically open in your browser at **http://localhost:8501**.

### Run with Custom Port

```bash
streamlit run app.py --server.port 8502
```

### Run in Headless Mode (No Browser Auto-Open)

```bash
streamlit run app.py --server.headless true
```

### Full Command with All Options

```bash
streamlit run app.py --server.headless true --server.port 8501 --server.address 0.0.0.0
```

---

## Deployment to Streamlit Cloud

### Step 1: Push Code to GitHub

Make sure all files are committed and pushed:

```bash
git add .
git commit -m "VKG Demo UI with interactive KG and 3D organs"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select:
   - **Repository**: `AKSB0567/VKG`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Deploy"**

### Step 3: Access Your App

Once deployed, the app will be available at:

🔗 **https://vkg-cvpr.streamlit.app/**

---

## Project Structure

```
VKG/
├── app.py                  # Main Streamlit application (all 5 tabs)
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── kgFlare23.ttl           # Knowledge Graph - FLARE dataset (Turtle format)
├── kgLiTS.ttl              # Knowledge Graph - LiTS dataset (Turtle format)
├── kg_nii.ttl              # Knowledge Graph - Pancreas dataset (Turtle format)
├── make_subgraphs.py       # KG subgraph extraction utility
├── query_report.md         # Query analysis report (Markdown)
├── query_report.pptx       # Query analysis report (PowerPoint)
├── pptx_images/            # Images used in the PowerPoint report
└── Exp5.ipynb              # Experiment notebook
```

---

## Technologies

| Technology | Purpose |
|-----------|---------|
| [Streamlit](https://streamlit.io) | Web application framework |
| [Plotly](https://plotly.com) | Interactive charts, 3D scatter plots |
| [vis.js](https://visjs.org) | Force-directed knowledge graph visualization |
| [Pandas](https://pandas.pydata.org) | Data manipulation and table rendering |
| [NumPy](https://numpy.org) | Procedural 3D organ/tumor geometry generation |
| Custom CSS | Light medical-themed UI with Inter font |

---

## License

This project is part of ongoing research. Please contact the repository owner for usage permissions.

---

<p align="center">
  Built with ❤️ using Streamlit • VKG Tier Evaluation Demo
</p>
