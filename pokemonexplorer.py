import streamlit as st
import matplotlib as plt
import seaborn as sns
import pandas as pd
import requests

st.title("Pokemon Explorer")

### Display image of pokemon
### Stretch version --> display the many sprites from the api
### make it look better
### add the audio file of the latest battle cry
### use whole pokedex
### pokemon type to change the color of bar chart

###def get_total_pokemon_count():
   ### try:
      ###  url = 'https://pokeapi.co/api/v2/pokemon/'
        ###reponse = requests.get(url)
        ###if response.status_code == 200:
           ### data = response.json()
            ###total_count = data['count']
            ###return total_count
        ###else:
           ### print('Failed to fetch total pokemon count from API')
            ###return None

def get_details(poke_number):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        return pokemon['name'], pokemon['height'], pokemon['weight'], len(pokemon['moves']), pokemon['sprites']['other']['official-artwork']['front_default'], pokemon['cries']['latest']
    except:
        return 'Error', None, None, None, None, None
    

###if get_total_pokemon_count:
   ###                        pokemon_number = st.slider('Pick a pokemon',
      ###                                                min_value = 1,
         ###                                             max_value = get_total_pokemon_count
            ###                                          )

    
pokemon_number = st.slider("Pick a pokemon",
                          min_value=1,
                          max_value=150)

name, height, weight, moves, sprite_url, cry_url = get_details(pokemon_number)

height_data = {'Pokemon': ['Weedle', name, 'Clefable'],
               'Heights': [3, height, 13]}

st.write(f'Name: {name}')
st.write(f'Height: {height}cm')
st.write(f'Weight: {weight}')
st.write(f'Move Count: {moves}')

if sprite_url:
    image = requests.get(sprite_url)
    
    st.image(image.content)
else:
    st.write('Image not available')

if cry_url:
    cry_audio = requests.get(cry_url)
    st.audio(cry_audio.content, format ='audio/mp3, start_time=0')
else:
    st.write('Battle cry audio not available')

###colors = sns.color_palette('husl', n_colors = len(types))

