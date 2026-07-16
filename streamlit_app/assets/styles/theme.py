"""
Thème visuel de l'application.

config.toml gère la base (couleurs natives des widgets, sidebar sombre).
Ce module affine : typographie, cartes de métriques, nav de la sidebar,
expanders, dataframes, boutons — tout ce que config.toml ne couvre pas.

Usage : appeler apply_theme() une seule fois, juste après st.set_page_config(),
en haut de chaque page.
"""

import streamlit as st
from assets.styles.color import Colors
from assets.styles.typography import Typography


def _build_css() -> str:
    return f"""
<style>
@import url('{Typography.GOOGLE_FONT_IMPORT}');

/* ---------- Base ---------- */
html, body, [class*="css"] {{
    font-family: {Typography.FONT_FAMILY};
}}

.stApp {{
    background-color: {Colors.BG_APP};
}}

h1, h2, h3, h4 {{
    font-family: {Typography.FONT_FAMILY};
    color: {Colors.TEXT_PRIMARY};
    letter-spacing: {Typography.LETTER_SPACING_TIGHT};
}}

/* Titre principal de page (st.title) */
h1 {{
    font-weight: {Typography.WEIGHT_EXTRABOLD};
    font-size: {Typography.SIZE_PAGE_TITLE} !important;
}}

h2 {{
    font-weight: {Typography.WEIGHT_BOLD};
}}

h3 {{
    font-weight: {Typography.WEIGHT_SEMIBOLD};
}}

p, li, span, label {{
    color: {Colors.TEXT_PRIMARY};
}}

/* Masquer le footer "Made with Streamlit" */
footer {{ visibility: hidden; }}
#MainMenu {{ visibility: hidden; }}

/* ---------- Layout général ---------- */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
    border-right: 1px solid {Colors.SIDEBAR_BORDER};
}}

section[data-testid="stSidebar"] * {{
    font-family: {Typography.FONT_FAMILY};
}}

section[data-testid="stSidebar"] hr {{
    border-color: {Colors.SIDEBAR_BORDER};
}}

/* Navigation auto-générée (liste des pages) */
[data-testid="stSidebarNav"] {{
    padding-top: 0.5rem;
}}

[data-testid="stSidebarNav"] a {{
    border-radius: 8px;
    margin: 2px 8px;
    padding: 0.5rem 0.75rem !important;
    color: {Colors.SIDEBAR_TEXT_MUTED} !important;
    font-weight: {Typography.WEIGHT_MEDIUM};
    font-size: {Typography.SIZE_BODY};
    transition: background-color 0.15s ease, color 0.15s ease;
}}

[data-testid="stSidebarNav"] a:hover {{
    background-color: {Colors.SIDEBAR_BG_ELEVATED};
    color: {Colors.SIDEBAR_TEXT} !important;
}}

[data-testid="stSidebarNav"] a[aria-current="page"] {{
    background-color: {Colors.SIDEBAR_ACTIVE_BG};
    color: {Colors.SIDEBAR_ACTIVE_TEXT} !important;
    font-weight: {Typography.WEIGHT_SEMIBOLD};
}}

/* Bloc d'entête custom qu'on injecte en haut de la sidebar */
.sidebar-brand {{
    padding: 0.25rem 0.5rem 1rem 0.5rem;
}}
.sidebar-brand-title {{
    color: #FFFFFF;
    font-size: 1.15rem;
    font-weight: {Typography.WEIGHT_BOLD};
    margin: 0;
    line-height: 1.3;
}}
.sidebar-brand-caption {{
    color: {Colors.SIDEBAR_TEXT_MUTED};
    font-size: {Typography.SIZE_SMALL};
    margin-top: 0.15rem;
}}

.sidebar-footer {{
    color: {Colors.SIDEBAR_TEXT_MUTED};
    font-size: {Typography.SIZE_CAPTION};
    line-height: 1.5;
}}

/* ---------- Cartes de métriques (st.metric) ---------- */
[data-testid="stMetric"] {{
    background-color: {Colors.BG_CARD};
    border: 1px solid {Colors.BORDER};
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    transition: box-shadow 0.15s ease, border-color 0.15s ease;
}}

[data-testid="stMetric"]:hover {{
    border-color: {Colors.PRIMARY_SOFT_BORDER};
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.08);
}}

[data-testid="stMetricLabel"] {{
    font-weight: {Typography.WEIGHT_MEDIUM};
    color: {Colors.TEXT_SECONDARY};
}}

[data-testid="stMetricValue"] {{
    color: {Colors.TEXT_PRIMARY};
    font-weight: {Typography.WEIGHT_BOLD};
}}

/* ---------- Boutons ---------- */
.stButton > button {{
    border-radius: 8px;
    font-weight: {Typography.WEIGHT_SEMIBOLD};
    border: 1px solid {Colors.PRIMARY};
    transition: transform 0.1s ease, box-shadow 0.15s ease;
}}

.stButton > button[kind="primary"] {{
    background-color: {Colors.PRIMARY};
}}

.stButton > button:hover {{
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
    transform: translateY(-1px);
}}

/* ---------- Expanders (formulaire de prédiction) ---------- */
[data-testid="stExpander"] {{
    background-color: {Colors.PRIMARY_SOFT};
    border: 1px solid {Colors.PRIMARY_SOFT_BORDER};
    border-radius: 12px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
}}

[data-testid="stExpander"] summary {{
    font-weight: {Typography.WEIGHT_SEMIBOLD};
    font-size: {Typography.SIZE_H3};
}}

/* Champs blancs à l'intérieur de l'expander pour contraster sur le fond bleu clair */
[data-testid="stExpander"] [data-testid="stTextInput"] input,
[data-testid="stExpander"] [data-testid="stNumberInput"] input,
[data-testid="stExpander"] [data-testid="stTextArea"] textarea,
[data-testid="stExpander"] [data-testid="stDateInput"] input,
[data-testid="stExpander"] div[data-baseweb="select"] > div,
[data-testid="stExpander"] div[data-baseweb="input"] {{
    background-color: #FFFFFF !important;
}}

[data-testid="stExpander"] [data-testid="stBaseButton-secondary"],
[data-testid="stExpander"] [data-testid="stBaseButton-secondaryFormSubmit"] {{
    background-color: #FFFFFF !important;
}}

/* ---------- Dataframes / tables ---------- */
[data-testid="stDataFrame"] {{
    border: 1px solid {Colors.BORDER};
    border-radius: 10px;
    overflow: hidden;
}}

/* ---------- Champs de formulaire (inputs, select, textarea, slider) ---------- */
/* Sans ça, les champs sont blancs sur fond de carte blanc = invisibles */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input,
div[data-baseweb="select"] > div,
div[data-baseweb="input"] {{
    background-color: {Colors.INPUT_BG} !important;
    border: 1px solid {Colors.INPUT_BORDER} !important;
    border-radius: 8px !important;
    color: {Colors.TEXT_PRIMARY} !important;
}}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
div[data-baseweb="select"]:focus-within > div {{
    background-color: {Colors.BG_CARD} !important;
    border-color: {Colors.INPUT_BORDER_FOCUS} !important;
    box-shadow: 0 0 0 1px {Colors.INPUT_BORDER_FOCUS} !important;
}}

/* Menu déroulant du selectbox */
div[data-baseweb="popover"] ul[role="listbox"] {{
    background-color: {Colors.BG_CARD} !important;
    border: 1px solid {Colors.BORDER};
    border-radius: 8px;
}}

/* Slider : piste au repos visible sur fond blanc */
[data-testid="stSlider"] > div > div > div {{
    background-color: {Colors.INPUT_BG};
}}

/* Radio / boutons segmentés horizontaux : petit fond de groupe */
[data-testid="stRadio"] > div[role="radiogroup"] {{
    background-color: {Colors.INPUT_BG};
    border: 1px solid {Colors.INPUT_BORDER};
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
}}

[data-testid="stExpander"] [data-testid="stRadio"] > div[role="radiogroup"] {{
    background-color: #FFFFFF;
}}

/* ---------- Dividers ---------- */
hr {{
    border-color: {Colors.BORDER} !important;
    margin: 1.5rem 0 !important;
}}

/* ---------- Cartes custom (page_header, kpi, etc.) ---------- */
.app-eyebrow {{
    display: inline-block;
    background-color: {Colors.PRIMARY_SOFT};
    color: {Colors.PRIMARY};
    border: 1px solid {Colors.PRIMARY_SOFT_BORDER};
    border-radius: 999px;
    padding: 0.2rem 0.75rem;
    font-size: {Typography.SIZE_CAPTION};
    font-weight: {Typography.WEIGHT_SEMIBOLD};
    letter-spacing: {Typography.LETTER_SPACING_WIDE};
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}}

.app-subtitle {{
    color: {Colors.TEXT_SECONDARY};
    font-size: {Typography.SIZE_BODY};
    max-width: 760px;
    margin-top: -0.4rem;
}}

.result-card {{
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    border: 1px solid;
    margin-bottom: 1rem;
}}
.result-card-success {{
    background-color: {Colors.SUCCESS_SOFT};
    border-color: {Colors.SUCCESS_BORDER};
}}
.result-card-error {{
    background-color: {Colors.ERROR_SOFT};
    border-color: {Colors.ERROR_BORDER};
}}

/* ---------- Cartes KPI à badge icône ---------- */
.kpi-card {{
    background-color: {Colors.BG_CARD};
    border: 1px solid {Colors.BORDER};
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    height: 100%;
    transition: box-shadow 0.15s ease, transform 0.15s ease;
}}
.kpi-card:hover {{
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.10);
    transform: translateY(-1px);
}}
.kpi-icon-value {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}}
.kpi-icon {{
    width: 42px;
    height: 42px;
    min-width: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
}}
.kpi-value {{
    font-size: 1.55rem;
    font-weight: {Typography.WEIGHT_EXTRABOLD};
    color: {Colors.TEXT_PRIMARY};
    line-height: 1.15;
}}
.kpi-label {{
    font-size: {Typography.SIZE_BODY};
    font-weight: {Typography.WEIGHT_SEMIBOLD};
    color: {Colors.TEXT_PRIMARY};
    margin-bottom: 0.15rem;
}}
.kpi-caption {{
    font-size: {Typography.SIZE_SMALL};
    color: {Colors.TEXT_SECONDARY};
}}

/* ---------- Pilules de statut (tableaux) ---------- */
.status-pill {{
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    font-size: {Typography.SIZE_SMALL};
    font-weight: {Typography.WEIGHT_SEMIBOLD};
}}
.status-pill-success {{
    background-color: {Colors.STATUS_SUCCESS_BG};
    color: {Colors.STATUS_SUCCESS_TEXT};
}}
.status-pill-error {{
    background-color: {Colors.STATUS_ERROR_BG};
    color: {Colors.STATUS_ERROR_TEXT};
}}
.status-pill-neutral {{
    background-color: {Colors.INPUT_BG};
    color: {Colors.TEXT_SECONDARY};
}}

/* ---------- Tableau custom façon maquette (carte + pilules) ---------- */
.app-table-wrapper {{
    background-color: {Colors.BG_CARD};
    border: 1px solid {Colors.BORDER};
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}}

.app-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: {Typography.SIZE_BODY};
}}

.app-table thead th {{
    text-align: left;
    background-color: {Colors.BG_APP};
    color: {Colors.TEXT_SECONDARY};
    font-weight: {Typography.WEIGHT_SEMIBOLD};
    font-size: {Typography.SIZE_SMALL};
    text-transform: uppercase;
    letter-spacing: {Typography.LETTER_SPACING_WIDE};
    padding: 0.75rem 1.1rem;
    border-bottom: 1px solid {Colors.BORDER};
    white-space: nowrap;
}}

.app-table tbody td {{
    padding: 0.75rem 1.1rem;
    border-bottom: 1px solid {Colors.BORDER};
    color: {Colors.TEXT_PRIMARY};
    font-weight: {Typography.WEIGHT_MEDIUM};
    vertical-align: middle;
}}

.app-table tbody tr:last-child td {{
    border-bottom: none;
}}

.app-table tbody tr:hover td {{
    background-color: {Colors.BG_APP};
}}

/* ---------- Médaillon logo de la sidebar ---------- */
.sidebar-logo {{
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background-color: rgba(255,255,255,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 0.6rem;
}}

/* ---------- Titres de section (cartes "Vue d'ensemble", etc.) ---------- */
.section-title {{
    font-size: {Typography.SIZE_H3};
    font-weight: {Typography.WEIGHT_BOLD};
    color: {Colors.TEXT_PRIMARY};
    margin: 0 0 1rem 0;
}}

/* ---------- Titres de mini-graphique (au-dessus de chaque chart) ---------- */
.chart-title {{
    font-size: {Typography.SIZE_BODY};
    font-weight: {Typography.WEIGHT_SEMIBOLD};
    color: {Colors.TEXT_PRIMARY};
    margin: 0 0 0.35rem 0;
}}

/* ---------- Conteneurs bordés (st.container(border=True)) façon carte ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: {Colors.BG_CARD};
    border-radius: 16px !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}}
[data-testid="stVerticalBlockBorderWrapper"] > div {{
    border-radius: 16px !important;
}}
/* ---------- Carte auteur / profil (page About) ---------- */
.profile-avatar {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background-color: {Colors.PRIMARY_SOFT};
    color: {Colors.PRIMARY};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin-bottom: 0.75rem;
}}
.profile-name {{
    font-size: 1.15rem;
    font-weight: {Typography.WEIGHT_BOLD};
    color: {Colors.TEXT_PRIMARY};
    margin-bottom: 0.15rem;
}}
.profile-role {{
    color: {Colors.TEXT_SECONDARY};
    font-size: {Typography.SIZE_SMALL};
    margin-bottom: 0.9rem;
}}
.profile-detail-row {{
    display: flex;
    gap: 0.6rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid {Colors.BORDER};
    font-size: {Typography.SIZE_BODY};
}}
.profile-detail-row:last-child {{
    border-bottom: none;
}}
.profile-detail-label {{
    color: {Colors.TEXT_SECONDARY};
    min-width: 110px;
    font-weight: {Typography.WEIGHT_SEMIBOLD};
}}
/* ---------- CTA bouton plein (st.page_link stylé en bouton) ---------- */
.st-key-home-cta-prediction [data-testid="stPageLink"] {{
    background-color: {Colors.PRIMARY} !important;
    border-radius: 10px !important;
    padding: 0.15rem 0.9rem !important;
    justify-content: center !important;
    border: none !important;
}}
.st-key-home-cta-prediction [data-testid="stPageLink"] p,
.st-key-home-cta-prediction [data-testid="stPageLink"] span,
.st-key-home-cta-prediction [data-testid="stPageLink"] svg {{
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    font-weight: {Typography.WEIGHT_SEMIBOLD};
}}
.st-key-home-cta-prediction [data-testid="stPageLink"]:hover {{
    background-color: {Colors.PRIMARY_HOVER} !important;
}}
</style>
"""


def apply_theme() -> None:
    """A appeler juste après st.set_page_config() sur CHAQUE page."""
    st.markdown(_build_css(), unsafe_allow_html=True)
