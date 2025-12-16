# This Python file is used to organize the "Fingerprint" page, including its
# introductory text and all code required for the recommendation system

# Import statement
import streamlit as st
import pandas as pd

# Introductory text
st.header("What's this about?")
st.text("This final recommendation method relies on the same spotify values as before, though it does not involve vectors. Rather, each song’s individual values (still normalized from 0 to 1) are sorted into evenly-spaced bins of low (l), medium-low (ml), medium (m), medium-high (mh), and high (h) magnitude. A fingerprint is then assigned to each song, resulting from its values categorizations. As a simplified example, if “Lovesong” by The Cure has medium-low danceability, high valence, and low danceability, it would be assigned a fingerprint of ml_h_l. ")
st.image("Fingerprint_DF.png", caption="Example DataFrame of songs with their associated Spotify values binned into categories of low (l), medium-low (ml), medium (m), medium-high (mh), and high (h). Each song's resulting fingerprint is displayed in the final 'fingerprint' column.")
st.text("Songs with identical fingerprints are then compiled into a DataFrame of recommended songs, excluding the inputted song itself. Give it a try for yourself!")
st.header("Recommendation Station")


# ______________________________________________________________________________________


# Loading our "songs" df, using st.cache_data to save the resulting DataFrame, lowering the amount of time it takes results to load

#function to load songs_CSV as a workable dataframe "songs"
@st.cache_data
def load_songs_csv(file_path: str):
    """Load CSV file and cache the result."""
    return pd.read_csv(file_path)
songs = load_songs_csv("songs.csv")


# ______________________________________________________________________________________


# Creating the songs_binned DF, obtaining the fingerprint of each song

# Creating a copy of the original songs df in case it is needed for later use, and cleaning tags
songs_binned=songs.copy()
songs_binned['tags'] = songs_binned['tags'].fillna('none specified') # filling NaNs in 'tags' column

# Binning data into five categories: low (l), medium low (ml), medium (m), medium high (mh), and high (h)
songs_binned['danceability'] = pd.cut(songs['danceability'], bins=5, labels=['l', 'ml','m','mh', 'h'])
songs_binned['energy'] = pd.cut(songs['energy'], bins=5, labels=['l', 'ml','m','mh', 'h'])
songs_binned['loudness'] = pd.cut(songs['loudness'], bins=5, labels=['l', 'ml','m','mh', 'h'])
songs_binned['speechiness'] = pd.cut(songs['speechiness'], bins=5, labels=['l', 'ml','m','mh', 'h'])
songs_binned['acousticness'] = pd.cut(songs['acousticness'], bins=5, labels=['l', 'ml','m','mh', 'h'])
songs_binned['instrumentalness'] = pd.cut(songs['instrumentalness'], bins=5, labels=['l', 'ml','m','mh', 'h'])
songs_binned['liveness'] = pd.cut(songs['liveness'], bins=5, labels=['l', 'ml','m','mh', 'h'])
songs_binned['valence'] = pd.cut(songs['valence'], bins=5, labels=['l', 'ml','m','mh', 'h'])
songs_binned['speed'] = pd.cut(songs['speed'], bins=5, labels=['l', 'ml','m','mh', 'h'])

# Converting data types (which are now categorical) to strings, then creating a fingerprint for each song by combining these strings
songs_binned[['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','speed']]=songs_binned[['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','speed']].astype('str')
songs_binned['fingerprint']=songs_binned['danceability']+'_'+songs_binned['energy']+'_'+songs_binned['loudness']+'_'+songs_binned['speechiness']+'_'+songs_binned['acousticness']+'_'+songs_binned['instrumentalness']+'_'+songs_binned['liveness']+'_'+songs_binned['valence']+'_'+songs_binned['speed']


# ______________________________________________________________________________________


# Creating the output recommended DF from a selected song input

# Find counts of each fingerprint
fingerprint_counts = pd.DataFrame(songs_binned['fingerprint'].value_counts().reset_index())
# Find the ones that only occur once
singular_fingerprints=fingerprint_counts[fingerprint_counts['count']==1]
# Make a list of those unique fingerprints
singular_fingerprint_list=singular_fingerprints['fingerprint'].to_list()

# Filter out songs that have a unique fingerprint (note use of tilde to reverse Boolean)
filtered_binned_songs = songs_binned[~(songs_binned['fingerprint'].isin(singular_fingerprint_list))].reset_index()

# Now, get ONLY song titles that have matches to other songs
song_titles = filtered_binned_songs['song'].unique()

# Song select menu
st.write("Please enter the first few letters of a song or artist you enjoy to select a song from the list below:")
selected_song = st.selectbox(
    "Type a song or artist name",
    (song_titles),
    placeholder="Select song...")

# getting the fingerprint of a selected song
fingerprint = songs_binned[songs_binned['song']==selected_song]['fingerprint'].iloc[0] # for whatever reason, fingerprint is giving index numbr bc it's printing in a df series. Here, there's only one argument we care about (our value), so we onlyh car about printing that first value!!

# Now dropping the selected song from the DataFrame, since we don't need it anymore to locate the fingerprint,
# and we want to be sure the input song is not recommended as an output
songs_binned_clean=songs_binned[~songs_binned['song'].str.contains(selected_song, regex=False)]

# Creating a DF of all songs that match the proposed fingerprint, renaming desired columns
my_song_matches = songs_binned_clean[songs_binned_clean['fingerprint'] == fingerprint].reset_index()
my_song_matches['Song and Artist']=my_song_matches['song']
my_song_matches['Year']=my_song_matches['year']
my_song_matches['Genre Tags']=my_song_matches['tags']
my_song_matches['Spotify URL']=my_song_matches['spotify_preview_url']
my_song_matches = my_song_matches[['Song and Artist','Year','Genre Tags','Spotify URL']] # update to only show desired columns

# Informing the user when the song_matches DF is empty
if my_song_matches.empty:
    st.text('No matches found. Please select another song.')
else:
    st.dataframe(my_song_matches)

    # Allowing for resulting df "my_song_matches" to be downloaded as a CSV  
    csv_data = my_song_matches.to_csv(index=False)
    st.download_button(
        label="Download Recommendations as CSV",
        data=csv_data,
        file_name = 'final_recommendations.csv',
        mime='text/csv')
