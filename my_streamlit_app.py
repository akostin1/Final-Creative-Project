# This Python file is used to organize the Streamlit app into pages, and serves 
# as the main file for the app

import streamlit as st
import pandas as pd
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide")

nav = get_nav_from_toml(".streamlit/pages.toml")

pg = st.navigation(nav)

add_page_title(pg)

pg.run()