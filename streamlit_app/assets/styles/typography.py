"""
Système typographique de l'application.

Police : Inter (importée depuis Google Fonts dans theme.py).
Une seule famille, mais une échelle de tailles/graisses claire pour
créer de la hiérarchie visuelle sans multiplier les polices.
"""


class Typography:
    FONT_FAMILY = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    GOOGLE_FONT_IMPORT = (
        "https://fonts.googleapis.com/css2?"
        "family=Inter:wght@400;500;600;700;800&display=swap"
    )

    # Échelle de tailles
    SIZE_PAGE_TITLE = "1.9rem"
    SIZE_H2 = "1.35rem"
    SIZE_H3 = "1.1rem"
    SIZE_BODY = "0.95rem"
    SIZE_SMALL = "0.82rem"
    SIZE_CAPTION = "0.75rem"

    # Graisses
    WEIGHT_REGULAR = 400
    WEIGHT_MEDIUM = 500
    WEIGHT_SEMIBOLD = 600
    WEIGHT_BOLD = 700
    WEIGHT_EXTRABOLD = 800

    LETTER_SPACING_TIGHT = "-0.02em"
    LETTER_SPACING_WIDE = "0.04em"
