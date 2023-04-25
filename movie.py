import pandas as pd
import streamlit as st
import openpyxl


st.set_page_config(page_title='Find your movie')
logo = "logo.png"
st.image(logo, width=150, caption="", use_column_width=False)
st.header('Helping you focus more on the chill then the Netflix')
st.subheader('Please select your criterias')

# Define the year ranges
year_ranges = {
    '1901 to 1990': (1901, 1990),
    '1990 to 2000': (1990, 2000),
    '2000 to 2010': (2000, 2010),
    '2010 to 2023': (2010, 2023)
}

# Multiselect for type
type_options = ['MOVIE','SHOW']
type_selection = st.multiselect('Type of content:',
                                    type_options)

#Slidebar for runtime
runtime_selection = st.slider('Runtime in minutes:',
                        min_value= 15,
                        max_value= 200,
                        value=(15,200))

#Slidebar for imdb score
imdb_score_selection = st.slider('IMDB score:',
                        min_value= 1.0,
                        max_value= 10.0,
                        value=(1.0,10.0),
                        step=0.1)

# Multiselect for genres
genres_options = ['drama', 'comedy', 'thriller', 'action', 'documentation','romance', 'family','animation','scifi','fantasy','horror','european','music','reality','sport','war','western']
genres_selection = st.multiselect('Movie Genres:',
                                    genres_options)

# Allow the user to select a year range
year_selection = st.multiselect('Release Year Range', list(year_ranges.keys()))

# Multiselect for platforms
platforms_options = ['netflix','hbomax','amazonprime','paramount','appletv','disney']
platforms_selection = st.multiselect('Platforms:',
                                    platforms_options)


df = pd.read_excel('titles_expanded_platforms.xlsx',
                   'Titles',
                   usecols='A:AP')

# --- FILTER DATAFRAME BASED ON SELECTION
genre_masks = []
for genre in genres_selection:
    genre_masks.append((df['genre_1'] == genre) | (df['genre_2'] == genre) | (df['genre_3'] == genre) |
                       (df['genre_4'] == genre) | (df['genre_5'] == genre) | (df['genre_6'] == genre) |
                       (df['genre_7'] == genre) | (df['genre_8'] == genre) | (df['genre_9'] == genre) |
                       (df['genre_10'] == genre) | (df['genre_11'] == genre) | (df['genre_12'] == genre))

if genre_masks:
    mask = genre_masks[0]
    for genre_mask in genre_masks[1:]:
        mask |= genre_mask
    mask &= (df['runtime'].between(*runtime_selection)) & (df['imdb_score'].between(*imdb_score_selection))
else:
    mask = (df['runtime'].between(*runtime_selection)) & (df['imdb_score'].between(*imdb_score_selection))

# --- FILTER DATAFRAME BASED ON SELECTED TYPE
if 'MOVIE' in type_selection:
    mask &= (df['type'] == 'MOVIE')
if 'SHOW' in type_selection:
    mask &= (df['type'] == 'SHOW')

# --- FILTER DATAFRAME BASED ON SELECTED SELECTED YEAR RANGE
if '1901 to 1990' in year_selection:
    mask &= (df['release_year'].between(1901,1990))
if '1990 to 2000' in year_selection:
    mask &= (df['release_year'].between(1990,2000))
if '2000 to 2010' in year_selection:
    mask &= (df['release_year'].between(2000,2010))
if '2010 to 2023' in year_selection:
    mask &= (df['release_year'].between(2010,2023))

number_of_result = df[mask].shape[0]
number_of_result

## --- GROUP DATAFRAME AFTER SELECTION
st.subheader('Our selection !')
df_grouped = df[mask].groupby(by=['title','type','platforms']).count().reset_index()
df_grouped.head(15).reset_index()[['title','type','platforms']]
