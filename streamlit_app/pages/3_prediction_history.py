import streamlit as st
import sys
from pathlib import Path
from theme import apply_theme

root = Path(__file__).resolve().parents[2]  
sys.path.insert(0, str(root))

from src.Database.database import load_history


history = load_history()

history["probability"] = (
    history["probability"] * 100
).round(2).astype(str) + " %"



st.dataframe(history)
