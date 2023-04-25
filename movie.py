import pandas as pd
import streamlit as st
import openpyxl

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

df





