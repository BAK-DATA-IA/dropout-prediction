"""
Composants réutilisables sur toutes les pages.

But : que chaque page ait 3 lignes identiques en haut (set_page_config,
apply_theme, render_sidebar) et un page_header() pour le titre, au lieu
de recoder le HTML/CSS partout.
"""

import streamlit as st
from assets.styles.color import Colors
from assets.styles.typography import Typography

# Badges de couleur partagés par kpi_card() et feature_card()
BADGE_MAP = {
    "blue": Colors.BADGE_BLUE,
    "purple": Colors.BADGE_PURPLE,
    "green": Colors.BADGE_GREEN,
    "amber": Colors.BADGE_AMBER,
    "sky": Colors.BADGE_SKY,
    "rose": Colors.BADGE_ROSE,
}


# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
def render_sidebar() -> None:
    """En-tête + pied de page de la sidebar. A appeler sur CHAQUE page,
    juste après apply_theme()."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-logo">🎓</div>
                <p class="sidebar-brand-title">Student Dropout AI</p>
                <p class="sidebar-brand-caption">Machine Learning Dashboard</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

    # Le pied de page est injecté à la fin du script de la page (voir
    # render_sidebar_footer) pour rester en bas visuellement.


def render_sidebar_footer(extra_line: str | None = None) -> None:
    """A appeler en toute fin de script, pour un pied de sidebar cohérent."""
    with st.sidebar:
        st.divider()
        lines = "Student Dropout Prediction<br/>Version 1.0 • Juillet 2026"
        if extra_line:
            lines += f"<br/>{extra_line}"
        st.markdown(f'<div class="sidebar-footer">{lines}</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------
# En-têtes de page
# ----------------------------------------------------------------------
def page_header(title: str, subtitle: str = "", eyebrow: str = "") -> None:
    """En-tête standard : eyebrow (optionnel) + titre + sous-titre.
    Remplace st.title() + st.write() pour un rendu plus soigné."""
    if eyebrow:
        st.markdown(f'<span class="app-eyebrow">{eyebrow}</span>', unsafe_allow_html=True)
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f'<p class="app-subtitle">{subtitle}</p>', unsafe_allow_html=True)
    st.write("")


def section_title(icon: str, title: str, tag: str | None = None, tag_kind: str = "neutral") -> None:
    """Titre de section à mettre en haut d'une carte (st.container(border=True)),
    façon "📊 Vue d'ensemble" sur la maquette.

    tag: étiquette courte optionnelle affichée à droite du titre, pour
        distinguer par exemple des données figées ("Données fixes") d'un
        suivi qui évolue à chaque prédiction ("Temps réel").
    tag_kind: "neutral" (gris) | "success" (vert) | "error" (rouge) —
        couleur du tag, réutilise les pilules de statut existantes.
    """
    tag_html = ""
    if tag:
        css_class = {
            "success": "status-pill-success",
            "error": "status-pill-error",
        }.get(tag_kind, "status-pill-neutral")
        tag_html = f'<span class="status-pill {css_class}" style="margin-left:0.6rem;vertical-align:middle;">{tag}</span>'

    st.markdown(
        f'<p class="section-title">{icon} {title}{tag_html}</p>',
        unsafe_allow_html=True,
    )


def chart_title(title: str) -> None:
    """Titre discret au-dessus d'un graphique (remplace le titre intégré à
    Plotly, pour garder la même typographie que le reste de l'app)."""
    st.markdown(f'<p class="chart-title">{title}</p>', unsafe_allow_html=True)


def resolve_status_colors(categories) -> dict:
    """Construit un color_discrete_map pour px.pie/px.bar en détectant les
    catégories de type succès/abandon (peu importe la casse ou la langue),
    afin d'avoir toujours bleu = succès, rouge = abandon, comme sur la
    maquette — sans dépendre de l'orthographe exacte des libellés.

    Les catégories non reconnues ne sont pas ajoutées au mapping (Plotly
    leur applique alors sa palette par défaut)."""
    mapping = {}
    for cat in categories:
        low = str(cat).lower()
        if any(k in low for k in ("abandon", "dropout", "échec", "echec")):
            mapping[cat] = Colors.CHART_BINARY[1]  # rouge
        elif any(k in low for k in ("succ", "graduate", "réussite", "reussite", "diplôm", "diplom")):
            mapping[cat] = Colors.CHART_BINARY[0]  # bleu
    return mapping


def result_card(text: str, positive: bool = True) -> None:
    """Carte de résultat colorée pour la prédiction (remplace st.error/st.success
    quand on veut un rendu plus intégré au design)."""
    css_class = "result-card-success" if positive else "result-card-error"
    icon = "✅" if positive else "⚠️"
    st.markdown(
        f'<div class="result-card {css_class}">'
        f'<strong>{icon} {text}</strong></div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# Cartes KPI à badge icône (remplace st.metric quand on veut ce look)
# ----------------------------------------------------------------------
def kpi_card(icon: str, value, label: str, caption: str = "", badge: str = "blue") -> None:
    """Carte KPI façon maquette : icône dans un badge coloré, valeur en
    gros, label, puis caption grise. A appeler DANS une colonne st.columns.

    badge: "blue" | "purple" | "green" | "amber" | "sky" | "rose"

    Usage:
        col1, col2 = st.columns(2)
        with col1:
            kpi_card("👨‍🎓", 4424, "Étudiants", "Total dans la base", badge="blue")
    """
    bg, fg = BADGE_MAP.get(badge, Colors.BADGE_BLUE)

    caption_html = f'<div class="kpi-caption">{caption}</div>' if caption else ""

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-value">
                <div class="kpi-icon" style="background-color:{bg};color:{fg};">{icon}</div>
                <div class="kpi-value">{value}</div>
            </div>
            <div class="kpi-label">{label}</div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# Carte "feature" (icône + titre + description) — page About
# ----------------------------------------------------------------------
def feature_card(icon: str, title: str, description: str, badge: str = "blue") -> None:
    """Carte présentant une fonctionnalité : icône dans un badge coloré,
    titre, puis paragraphe descriptif. Réutilise le style visuel de
    kpi_card (mêmes classes CSS) mais pour du texte plutôt qu'un chiffre.
    A appeler DANS une colonne st.columns.

    Usage:
        col1, col2, col3 = st.columns(3)
        with col1:
            feature_card("🔮", "Prediction", "Description...", badge="blue")
    """
    bg, fg = BADGE_MAP.get(badge, Colors.BADGE_BLUE)

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-value">
                <div class="kpi-icon" style="background-color:{bg};color:{fg};">{icon}</div>
                <div class="kpi-label" style="font-size:1.05rem;">{title}</div>
            </div>
            <div class="kpi-caption" style="line-height:1.55;">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# Carte auteur / profil — page About
# ----------------------------------------------------------------------
def render_author_card(name: str, role: str, details: dict, icon: str = "👨‍💻") -> None:
    """Carte profil : avatar circulaire, nom, rôle, puis une liste de
    détails clé/valeur (Formation, Projet, Année...).

    Usage:
        render_author_card(
            name="Bakary Dembele",
            role="Ingénierie Science des Données et Intelligence Artificielle (ISDIA)",
            details={"Projet": "Student Dropout Prediction", "Année": "2025-2026"},
        )
    """
    rows_html = "".join(
        f'<div class="profile-detail-row">'
        f'<span class="profile-detail-label">{key}</span><span>{value}</span></div>'
        for key, value in details.items()
    )
    st.markdown(
        f"""
        <div class="profile-avatar">{icon}</div>
        <div class="profile-name">{name}</div>
        <div class="profile-role">{role}</div>
        {rows_html}
        """,
        unsafe_allow_html=True,
    )


def status_pill(label: str, positive: bool = True) -> str:
    """Retourne le HTML d'une pilule de statut colorée (à utiliser dans un
    st.markdown ou une colonne de dataframe transformée en HTML)."""
    css_class = "status-pill-success" if positive else "status-pill-error"
    return f'<span class="status-pill {css_class}">{label}</span>'


# ----------------------------------------------------------------------
# Tableau custom façon maquette (carte blanche, header discret, pilules)
# ----------------------------------------------------------------------
def render_data_table(
    df,
    pill_column: str | None = None,
    pill_rules: dict | None = None,
    formatters: dict | None = None,
) -> None:
    """Affiche un DataFrame sous forme de tableau HTML façon maquette :
    carte blanche arrondie, header discret en majuscules, lignes avec
    hover, et une colonne optionnelle rendue en pilules colorées
    (comme la colonne "Prédiction" du tableau "Dernières prédictions").

    Args:
        df: le DataFrame à afficher.
        pill_column: nom de la colonne à transformer en pilules (optionnel).
        pill_rules: dict {mot-clé: "success"|"error"|"neutral"} — le
            premier mot-clé trouvé (recherche insensible à la casse, par
            sous-chaîne) dans la valeur de la cellule détermine la couleur.
            Ex: {"augmente": "error", "diminue": "success", "abandon": "error",
            "succès": "success"}. Si aucun mot-clé ne correspond, la pilule
            est grise (neutre).
        formatters: dict {colonne: fonction} pour formater des valeurs
            avant affichage. Ex: {"Impact sur la prédiction": lambda v: f"{v:.3f}"}

    Usage:
        render_data_table(
            shap_df,
            pill_column="Effet",
            pill_rules={"augmente": "error", "diminue": "success"},
        )
    """
    pill_rules = pill_rules or {}
    formatters = formatters or {}

    headers_html = "".join(f"<th>{col}</th>" for col in df.columns)

    rows_html = ""
    for _, row in df.iterrows():
        cells_html = ""
        for col in df.columns:
            value = row[col]
            if col in formatters:
                value = formatters[col](value)

            if col == pill_column:
                value_str = str(value)
                css_class = "status-pill-neutral"
                lowered = value_str.lower()
                for keyword, kind in pill_rules.items():
                    if keyword.lower() in lowered:
                        css_class = f"status-pill-{kind}"
                        break
                cells_html += (
                    f'<td><span class="status-pill {css_class}">{value_str}</span></td>'
                )
            else:
                cells_html += f"<td>{value}</td>"

        rows_html += f"<tr>{cells_html}</tr>"

    st.markdown(
        f"""
        <div class="app-table-wrapper">
            <table class="app-table">
                <thead><tr>{headers_html}</tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# Graphiques Plotly
# ----------------------------------------------------------------------
def style_chart(fig, height: int = 320, show_legend: bool = True, legend_position: str = "bottom"):
    """A appliquer à CHAQUE figure Plotly avant st.plotly_chart(), pour un
    rendu cohérent (police, fond transparent, couleurs, marges).

    Le titre Plotly natif n'est jamais défini : on affiche plutôt un titre
    HTML via chart_title() au-dessus du graphique, pour garder la même
    typographie (Inter) que le reste de l'app.

    legend_position: "bottom" (sous le graphique, comme les donuts de la
        maquette) ou "top" (au-dessus du tracé, à utiliser quand l'axe X a
        des catégories longues/pivotées qui chevaucheraient une légende
        placée en bas).

    Usage:
        chart_title("Répartition des prédictions")
        fig = px.pie(...)
        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    """
    if legend_position == "top":
        legend = dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        )
        margin = dict(l=10, r=10, t=36, b=10)
    else:
        legend = dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        )
        margin = dict(l=10, r=10, t=10, b=60)

    fig.update_layout(
        font_family=Typography.FONT_FAMILY,
        font_color=Colors.TEXT_PRIMARY,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        colorway=Colors.CHART_CATEGORICAL,
        height=height,
        margin=margin,
        showlegend=show_legend,
        legend=legend,
        hoverlabel=dict(
            bgcolor=Colors.BG_CARD,
            font_family=Typography.FONT_FAMILY,
            bordercolor=Colors.BORDER,
        ),
    )
    fig.update_xaxes(gridcolor=Colors.BORDER, zerolinecolor=Colors.BORDER)
    fig.update_yaxes(gridcolor=Colors.BORDER, zerolinecolor=Colors.BORDER)
    return fig
