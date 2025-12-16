# This Python file codes all text and images shown on the "Homepage" tab

import streamlit as st

st.text('Have you ever found yourself wondering how Spotify sets up its recommendation system? How it suggests new songs in your “Discover Weekly” playlist? Or how it knows which curated playlists to direct you towards?')

st.image('Discover_Weekly.png',caption="Spotify's Discover Weekly interface, with recommended songs based on users' listening patterns.")

st.text('To understand how music companies attempt to quantify music “taste” for its listeners, we’ve created a simplified song recommendation system of our own, in the form of this interactive web application. Our goal is to enlighten our users on how python, pandas, and other coding libraries are used as tools to sift through large tables of Spotify data. In working with some of the company’s assigned values of “danceability,” “instrumentalness,” and “valence” (among others), we can attempt to sort songs by similarity using three different methods: cosine similarity, Euclidean distance, and binning as “fingerprints.”')

st.text('Each webpage includes background information on how each measure of “similarity” is computed, before providing you with an interactive space to select songs of your choosing and find recommendations of your own. Feel free to play around with filtering by year and genre, and don’t forget to download your results as a CSV (easily read by Microsoft Excel) for times when you’re looking for new music!')