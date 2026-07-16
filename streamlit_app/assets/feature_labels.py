"""
Traduction des noms de variables bruts (issus du pipeline de preprocessing/
ColumnTransformer) vers des libellés naturels en français, pour l'affichage
dans le tableau et le graphique SHAP de la page Prediction.

Pourquoi ce module existe :
Le pipeline encode les variables catégorielles (one-hot), ce qui multiplie
les colonnes (ex: "Course" devient "Course_Tourisme", "Course_Droit", ...).
On ne peut donc pas se contenter d'un simple dict {ancien_nom: nouveau_nom} :
il faut détecter la variable d'origine en préfixe, puis afficher
"Formation : Tourisme" plutôt que le nom brut encodé.

Usage:
    from assets.feature_labels import humanize_feature_name
    shap_df["Facteur"] = shap_df["Facteur"].apply(humanize_feature_name)
    # et pour le waterfall SHAP (shap.Explanation) :
    shap_values.feature_names = [humanize_feature_name(f) for f in shap_values.feature_names]
"""

import re

# ----------------------------------------------------------------------
# Dictionnaire des 36 variables d'origine du dataset (UCI "Predict
# Students' Dropout and Academic Success") vers un libellé naturel.
#
# Les clés sont normalisées (espaces/underscores/apostrophes uniformisés,
# minuscules) par _normalize() avant la recherche, donc l'orthographe
# exacte utilisée par le pipeline (espace vs underscore, casse, avec ou
# sans parenthèses) importe peu.
# ----------------------------------------------------------------------
FEATURE_LABELS = {
    "marital status": "Situation matrimoniale",
    "application mode": "Mode de candidature",
    "application order": "Ordre de préférence",
    "course": "Formation",
    "daytime evening attendance": "Régime (jour/soir)",
    "previous qualification": "Qualification précédente",
    "previous qualification grade": "Note de la qualification précédente",
    "nacionality": "Nationalité",
    "nationality": "Nationalité",
    "mothers qualification": "Qualification de la mère",
    "fathers qualification": "Qualification du père",
    "mothers occupation": "Profession de la mère",
    "fathers occupation": "Profession du père",
    "admission grade": "Note d'admission",
    "displaced": "Etudiant déplacé",
    "educational special needs": "Bésoins particuliers educatifs",
    "debtor": "Etudiant débiteur",
    "tuition fees up to date": "Frais de scolarité à jour",
    "gender": "Genre",
    "scholarship holder": "Boursier",
    "age at enrollment": "Âge à l'inscription",
    "international": "Etudiant international",
    "curricular units 1st sem credited": "Crédits validés avant le 1er semestre",
    "curricular units 1st sem enrolled": "Matières inscrites au 1er semestre",
    "curricular units 1st sem evaluations": "Évaluations passées au 1er semestre",
    "curricular units 1st sem approved": "Matières validées au 1er semestre",
    "curricular units 1st sem grade": "Moyenne au 1er semestre",
    "curricular units 1st sem without evaluations": "Matières sans évaluation au 1er semestre",
    "curricular units 2nd sem credited": "Crédits validés avant le 2e semestre",
    "curricular units 2nd sem enrolled": "Matières inscrites au 2e semestre",
    "curricular units 2nd sem evaluations": "Évaluations passées au 2e semestre",
    "curricular units 2nd sem approved": "Matières validées au 2e semestre",
    "curricular units 2nd sem grade": "Moyenne au 2e semestre",
    "curricular units 2nd sem without evaluations": "Matières sans évaluation au 2e semestre",
    "unemployment rate": "Taux de chômage",
    "inflation rate": "Taux d'inflation",
    "gdp": "PIB",

    # ------------------------------------------------------------------
    # Colonnes "_grouped" : remplacent les colonnes brutes supprimées après
    # regroupement des modalités (data.drop(columns=[...])). Comme elles
    # sont plus longues que leur équivalent brut, elles sont testées en
    # priorité par le matching en préfixe (_SORTED_BASES trie par longueur
    # décroissante) — donc les entrées brutes ci-dessus (ex: "marital
    # status") ne posent pas de conflit même si elles restent dans le dict.
    # ------------------------------------------------------------------
    "marital status grouped": "Situation matrimoniale (regroupée)",
    "application mode grouped": "Mode de candidature (regroupé)",
    "mothers qualification grouped": "Qualification de la mère (regroupée)",
    "fathers qualification grouped": "Qualification du père (regroupée)",
    "mothers occupation grouped": "Profession de la mère (regroupée)",
    "fathers occupation grouped": "Profession du père (regroupée)",
    "previous qualification grouped": "Qualification précédente (regroupée)",

    # ------------------------------------------------------------------
    # Variables créées par feature engineering. Libellés déduits du nom de
    # la colonne — à vérifier/ajuster si le sens exact diffère de ce que
    # j'ai supposé ici.
    # ------------------------------------------------------------------
    "no academic activity": "Aucune activité académique",
    "no assessment taken": "Aucune évaluation passée",
    "low performance": "Performance académique faible",
    "grade2 echec": "Échec au 2e semestre",
}

# Tri par longueur de clé décroissante : indispensable pour le matching en
# préfixe des colonnes one-hot (ex: il faut tester "curricular units 1st
# sem grade" avant "curricular units 1st sem" pour ne pas couper au
# mauvais endroit).
_SORTED_BASES = sorted(FEATURE_LABELS.keys(), key=len, reverse=True)


def _normalize(text: str) -> str:
    """Uniformise un nom de variable pour la recherche dans le dictionnaire :
    minuscules, apostrophes retirées (mother's -> mothers, pas "mother s"),
    parenthèses/underscores/tirets remplacés par des espaces, espaces
    multiples réduits."""
    text = text.lower()
    text = text.replace("cat__", "").replace("num__", "").replace("remainder__", "")
    text = re.sub(r"['’]", "", text)       # mother's -> mothers (pas d'espace inséré)
    text = re.sub(r"[()]", " ", text)      # "(grade)" -> " grade "
    text = re.sub(r"[_\-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def humanize_feature_name(raw_name: str) -> str:
    """Traduit un nom de variable brut (avant ou après one-hot encoding)
    en libellé naturel français.

    - Variable numérique connue -> libellé direct ("Age at enrollment" ->
      "Âge à l'inscription").
    - Variable catégorielle encodée (one-hot) -> "{Libellé de base} : {valeur}"
      (ex: "Course_Tourisme" -> "Formation : Tourisme").
    - Variable inconnue -> nettoyage générique (underscores -> espaces,
      première lettre en majuscule) pour ne jamais afficher un nom brut
      illisible, même si le dictionnaire n'a pas cette entrée.
    """
    if not isinstance(raw_name, str) or not raw_name:
        return raw_name

    normalized = _normalize(raw_name)

    # 1. Correspondance exacte (variable numérique ou catégorielle non encodée)
    if normalized in FEATURE_LABELS:
        return FEATURE_LABELS[normalized]

    # 2. Correspondance en préfixe (variable catégorielle one-hot : la partie
    # restante après le préfixe est la valeur de la catégorie, ex: "tourisme",
    # "2nd phase"...). On ne capitalise que la 1ère lettre de la valeur (pas
    # de .title() par mot, qui casserait des valeurs comme "2nd phase").
    for base in _SORTED_BASES:
        if normalized.startswith(base + " "):
            remainder = normalized[len(base):].strip()
            label = FEATURE_LABELS[base]
            value_display = remainder[:1].upper() + remainder[1:] if remainder else remainder
            return f"{label} : {value_display}"

    # 3. Repli générique : jamais de nom brut illisible affiché
    fallback = re.sub(r"['’()_\-]", " ", raw_name)
    fallback = re.sub(r"\s+", " ", fallback).strip()
    return fallback[:1].upper() + fallback[1:] if fallback else raw_name
