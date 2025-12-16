# This Python file is used to organize the "Euclidean Distance" page, including its
# introductory text and all code required for the recommendation system

# Import statements
import streamlit as st
import pandas as pd
import ast

# Introductory text
st.header("What's this about?")
st.text("As described in the Cosine Similarity webpage, we can assign each song’s spotify values to a unique vector in multidimensional space. Whereas cosine similarity computed the angle between vectors, Euclidean distance calculates (as one would expect) the distance between two vectors’ endpoints. As such, the lower this distance, the more similar one would expect two songs to be.")
st.image("Euc_Dist.png", caption="Example of the Euclidean distance between 2-dimensional vectors, with attributes 'valence' and 'energy.' Figure was created by Owen Yaggy and Dr. Richard Freedman, at Haverford College.")
st.text("To remain consistent, we’ve normalized this value to express similarity on an identical scale from 0 to 1, where songs with a similarity closer to 1 are more similar. As such, we created a DataFrame of “ranked pairs” similar to that of our cosine similarity model, displaying songs similar to a degree of 0.95 or higher. By entering a proposed song and filtering to narrow down the list, one can create and download a similar DataFrame of recommendations. Give it a try for yourself!")
st.header("Recommendation Station")


# ___________________________________________________________________________________________


# Loading our "songs" df and "euclidean_ranked_pairs" df, using st.cache_data to save the 
# resulting DataFrame, lowering the amount of time it takes results to load

#function to load songs_CSV as a workable dataframe "songs"
@st.cache_data
def load_songs_csv(file_path: str):
    """Load CSV file and cache the result."""
    return pd.read_csv(file_path)
songs = load_songs_csv("songs.csv")

#function to load euc_ranked_pairs CSV as a workable dataframe "ranked_pairs"
@st.cache_data
def load_euc_csv(file_path: str):
    """Load CSV file and cache the result."""
    return pd.read_csv(file_path)
ranked_pairs = load_euc_csv("euc_ranked_pairs.csv")


# ___________________________________________________________________________________________


# Making our interactive song selection system

# List of titles with at least one match
song_titles = ranked_pairs['source_song'].unique() 

# Song select menu
st.write("Please enter the first few letters of a song or artist you enjoy to select a song from the list below:")
selected_song = st.multiselect(
    "Type a song or artist name",
    (song_titles),
    max_selections=3,
    placeholder="Select song..."
)

# Create a df of songs that match the user's selection
my_song_matches = ranked_pairs[ranked_pairs['source_song'].isin(selected_song)]
recommended_songs = list(my_song_matches['matched_song'].unique()) # creates a unique list of recommended songs, if two inputs give the same output
recommended_songs_df=songs[songs['song'].isin(recommended_songs)] # filters the original "songs" dataframe for data on recommended songs
recommended_songs_df=recommended_songs_df.drop(columns=['index']) # drops the index column

# Merge this recommended songs df with the similarity data
recommended_songs_df = pd.merge(right=my_song_matches, 
         left=recommended_songs_df, 
         right_on="matched_song", 
         left_on="song", 
         how="inner")


# ___________________________________________________________________________________________


# Filtering results

# Create a unique list of years from selected songs, for use in filtering
year_list=list(recommended_songs_df['year'].unique())

# If year_list only contains 1 year, there is no need for a slider, and we continue to filtering genre
if len(year_list) == 1:
    filtered_year=recommended_songs_df[recommended_songs_df['year']==year_list[0]]

    # Converting genres from strings to objects, to properly separate them for our genre_list
    filtered_year['tags'] = filtered_year['tags'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # Filling NaN tags and exploding filtered_year df by genre, then creating a list of unique genres from this exploded df
    filtered_year['tags'] = filtered_year['tags'].fillna('none specified')
    filtered_year_explode = filtered_year.explode('tags')
    genre_list=sorted(filtered_year_explode['tags'].unique())

    # Genre filtering menu
    if len(genre_list) > 0: 
        selected_genres = st.multiselect(
        "Select a genre",
        (genre_list),
        max_selections=3,
        placeholder="Select genre...")

        # Searching filtered_year df for instances where songs have genres in selected_genres list
        if len(selected_genres) > 0:
            filtered_genre = filtered_year[
                filtered_year['tags'].apply(
                lambda tags: any(tag in selected_genres for tag in tags))]
            filtered_genre = filtered_genre.sort_values(by='similarity',ascending=False) # sort by similarity, high to low

            # Rename select columns we wish to display
            filtered_genre['Source Song']=filtered_genre['source_song']
            filtered_genre['Matched Song']=filtered_genre['matched_song']
            filtered_genre['Year']=filtered_genre['year']
            filtered_genre['Genre Tags']=filtered_genre['tags']
            filtered_genre['Similarity']=filtered_genre['similarity']
            filtered_genre['Spotify URL']=filtered_genre['spotify_preview_url']

            # Update to only show desired columns
            final_recs = filtered_genre[['Source Song','Matched Song','Year','Genre Tags','Similarity','Spotify URL']].reset_index() # select only the columns we want to display in our final product
            final_recs = final_recs.drop(columns=['index'])
            st.dataframe(final_recs) # display final df

            # Allowing for resulting df "final_recs" to be downloaded as a CSV
            csv_data = final_recs.to_csv(index=False)
            st.download_button(
                    label="Download Recommendations as CSV",
                    data=csv_data,
                    file_name = 'final_recommendations.csv',
                    mime='text/csv')
            
        # Prevent empty df from displaying if no genre selected    
        else:
            st.write('Please select a genre to view results')


# ___________________________________________________________________________________________


# If year_list contains more than 1 year, we create a year filtering menu
if len(year_list) > 1:
    start_year, end_year = st.select_slider(
    "Select a range of years",
    options=year_list,
    value=(min(year_list), max(year_list)))
    filtered_year=recommended_songs_df[(recommended_songs_df['year']>=start_year) & (recommended_songs_df['year']<=end_year)]

    # Converting genres from strings to objects, to properly separate them for our genre_list
    filtered_year['tags'] = filtered_year['tags'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # Filling NaN tags and exploding filtered_year df by genre, then creating a list of unique genres from this exploded df
    filtered_year['tags'] = filtered_year['tags'].fillna('none specified')
    filtered_year_explode = filtered_year.explode('tags')
    genre_list=sorted(filtered_year_explode['tags'].unique())

    # Genre filtering menu
    if len(genre_list) > 0: 
        selected_genres = st.multiselect(
        "Select a preferred genre from the list below:",
        (genre_list),
        max_selections=3,
        placeholder="Select genre...")

        # Searching filtered_year df for instances where songs have genres in selected_genres list
        if len(selected_genres) > 0:
            filtered_genre = filtered_year[
                filtered_year['tags'].apply(
                lambda tags: any(tag in selected_genres for tag in tags))]
            filtered_genre = filtered_genre.sort_values(by='similarity',ascending=False) # sort by similarity, high to low

            # Rename select columns we wish to display
            filtered_genre['Source Song']=filtered_genre['source_song']
            filtered_genre['Matched Song']=filtered_genre['matched_song']
            filtered_genre['Year']=filtered_genre['year']
            filtered_genre['Genre Tags']=filtered_genre['tags']
            filtered_genre['Similarity']=filtered_genre['similarity']
            filtered_genre['Spotify URL']=filtered_genre['spotify_preview_url']

            # update to only show desired columns
            final_recs = filtered_genre[['Source Song','Matched Song','Year','Genre Tags','Similarity','Spotify URL']].reset_index() # select only the columns we want to display in our final product
            final_recs = final_recs.drop(columns=['index'])
            st.dataframe(final_recs)

            # Allowing for resulting df "final_recs" to be downloaded as a CSV
            csv_data = final_recs.to_csv(index=False)
            st.download_button(
                    label="Download Recommendations as CSV",
                    data=csv_data,
                    file_name = 'final_recommendations.csv',
                    mime='text/csv')
            
        # Prevent empty df from displaying if no genre selected  
        else:
            st.write('Please select a genre to view results')


# ___________________________________________________________________________________________


# Prevent empty df from displaying if no song selected  
else:
    st.write('Please select a song to view results')
