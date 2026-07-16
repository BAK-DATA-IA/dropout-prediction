"""
Palette de couleurs de l'application.

Direction : sidebar bleu plein (marque) + contenu clair, badges d'icônes
pastel sur les cartes KPI, rouge/vert réservés au sens (abandon/succès).
Toute couleur utilisée dans l'app doit venir d'ici : on change une valeur
ici et elle se répercute partout (theme.py, components.py, graphiques).
"""


class Colors:
    # ---- Accent principal (boutons, liens actifs, highlights) ----
    PRIMARY = "#2563EB"          # Blue 600
    PRIMARY_HOVER = "#1D4ED8"    # Blue 700
    PRIMARY_SOFT = "#EFF6FF"     # Blue 50 (fonds légers, badges)
    PRIMARY_SOFT_BORDER = "#BFDBFE"  # Blue 200

    # ---- Sidebar (bleu plein, comme sur la maquette) ----
    SIDEBAR_BG = "#1D4ED8"            # Blue 700
    SIDEBAR_BG_ELEVATED = "#1E40AF"   # Blue 800 (hover / actif)
    SIDEBAR_BORDER = "#3B82F6"
    SIDEBAR_TEXT = "#DBEAFE"          # Blue 100
    SIDEBAR_TEXT_MUTED = "#93C5FD"    # Blue 300
    SIDEBAR_ACTIVE_BG = "#FFFFFF"
    SIDEBAR_ACTIVE_TEXT = "#1D4ED8"

    # ---- Badges d'icônes des cartes KPI (fond pastel + icône saturée) ----
    BADGE_BLUE = ("#DBEAFE", "#2563EB")
    BADGE_PURPLE = ("#EDE9FE", "#7C3AED")
    BADGE_GREEN = ("#DCFCE7", "#16A34A")
    BADGE_AMBER = ("#FEF3C7", "#D97706")
    BADGE_SKY = ("#E0F2FE", "#0284C7")
    BADGE_ROSE = ("#FFE4E6", "#E11D48")

    # ---- Zone de contenu (thème clair) ----
    BG_APP = "#F8FAFC"       # Slate 50
    BG_CARD = "#FFFFFF"
    BORDER = "#E2E8F0"       # Slate 200
    BORDER_STRONG = "#CBD5E1"  # Slate 300

    TEXT_PRIMARY = "#0F172A"    # Slate 900
    TEXT_SECONDARY = "#64748B"  # Slate 500
    TEXT_MUTED = "#94A3B8"      # Slate 400

    # ---- Champs de formulaire (inputs, select, textarea) ----
    # Un fond légèrement teinté pour se détacher du blanc des cartes/expanders
    INPUT_BG = "#F1F5F9"          # Slate 100
    INPUT_BORDER = "#CBD5E1"      # Slate 300
    INPUT_BORDER_FOCUS = "#2563EB"  # = PRIMARY

    # ---- États sémantiques ----
    SUCCESS = "#16A34A"
    SUCCESS_SOFT = "#F0FDF4"
    SUCCESS_BORDER = "#BBF7D0"

    ERROR = "#DC2626"
    ERROR_SOFT = "#FEF2F2"
    ERROR_BORDER = "#FECACA"

    WARNING = "#D97706"
    WARNING_SOFT = "#FFFBEB"
    WARNING_BORDER = "#FDE68A"

    INFO = "#0284C7"
    INFO_SOFT = "#F0F9FF"
    INFO_BORDER = "#BAE6FD"

    # ---- Palette graphiques (Plotly) ----
    # Catégorielle : bleu en tête, puis teintes distinguables pour le reste
    CHART_CATEGORICAL = [
        "#2563EB",  # blue
        "#0EA5E9",  # sky
        "#14B8A6",  # teal
        "#F59E0B",  # amber
        "#F43F5E",  # rose
        "#7C3AED",  # violet
        "#84CC16",  # lime
        "#64748B",  # slate (valeur "autre / non renseigné")
    ]

    # Séquentielle : pour les histogrammes / heatmaps à une seule variable
    CHART_SEQUENTIAL = [
        "#EFF6FF", "#BFDBFE", "#93C5FD", "#60A5FA",
        "#3B82F6", "#2563EB", "#1D4ED8", "#1E40AF",
    ]

    # Binaire (utilisé pour dropout / no dropout, boursier / non boursier, etc.)
    # Bleu = succès, rouge = abandon — comme sur la maquette (donut, barres empilées)
    CHART_BINARY = ["#2563EB", "#DC2626"]
    CHART_BINARY_STATUS = {"Dropout": "#DC2626", "No dropout": "#2563EB"}

    # Pilules de statut dans les tableaux (History, dernières prédictions)
    STATUS_SUCCESS_BG = "#DCFCE7"
    STATUS_SUCCESS_TEXT = "#15803D"
    STATUS_ERROR_BG = "#FEE2E2"
    STATUS_ERROR_TEXT = "#B91C1C"
