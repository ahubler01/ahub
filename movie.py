import pandas as pd
import streamlit as st

  
st.set_page_config(page_title='Find your movie')
logo = "logo.png"
st.image(logo, width=150, caption="", use_column_width=False)
st.header('Helping you focus more on the chill then the Netflix')
st.subheader('Please select your criterias')


### --- LOAD DATAFRAME
excel_file = 'titles_expanded_platforms.xlsx'
sheet_name = 'Titles'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='A:AP')

# Remove films where the imdb votes is lower than 204
df = df.sort_values('imdb_votes')
df = df[df['imdb_votes'] >= 204]

# --- STREAMLIT SELECTION

#Streming platforms
netflix = df['netflix'].unique().tolist()
hbomax = df['hbomax'].unique().tolist()
amazonprime = df['amazonprime'].unique().tolist()
disney = df['disney'].unique().tolist()
paramount = df['paramount'].unique().tolist()
appletv = df['appletv'].unique().tolist()

#Runtime
runtime = df['runtime'].unique().tolist()

#IMDB score
imdb_score = df['imdb_score'].unique().tolist()

#Genres
genre_1 = df['genre_1'].unique().tolist()
genre_2 = df['genre_2'].unique().tolist()
genre_3 = df['genre_3'].unique().tolist()
genre_4 = df['genre_4'].unique().tolist()
genre_5 = df['genre_5'].unique().tolist()
genre_6 = df['genre_6'].unique().tolist()
genre_7 = df['genre_7'].unique().tolist()
genre_8 = df['genre_8'].unique().tolist()
genre_9 = df['genre_9'].unique().tolist()
genre_10 = df['genre_10'].unique().tolist()
genre_11 = df['genre_11'].unique().tolist()
genre_12 = df['genre_12'].unique().tolist()

# Define the year ranges
year_ranges = {
    '1901 to 1990': (1901, 1990),
    '1990 to 2000': (1990, 2000),
    '2000 to 2010': (2000, 2010),
    '2010 to 2023': (2010, 2023)
}

#Type
type_options = df['type'].unique().tolist()

# Multiselect for type
type_selection = st.multiselect('Type of content:',
                                    type_options)

#Slidebar for runtime
runtime_selection = st.slider('Runtime in minutes:',
                        min_value= min(runtime),
                        max_value= 240,
                        value=(min(runtime),240))

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
st.markdown(f'Available Results: {number_of_result}')


## --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['title','type','platforms','release_year','all_genres','imdb_score','runtime']).count().reset_index()
st.subheader('Our selection !')
df_grouped.sample(n=15).reset_index()[['title','type','platforms','release_year','all_genres','imdb_score','runtime']]








