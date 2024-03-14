import streamlit as st
import seaborn as sns
import pandas as pd
import requests

pokemon_colours = {
    'normal': '#A8A77A',
    'fire': '#EE8130',
    'water': '#6390F0',
    'electric': '#F7D02C',
    'grass': '#7AC74C',
    'ice': '#96D9D6',
    'fighting': '#C22E28',
    'poison': '#A33EA1',
    'ground': '#E2BF65',
    'flying': '#A98FF3',
    'psychic': '#F95587',
    'bug': '#A6B91A',
    'rock': '#B6A136',
    'ghost': '#735797',
    'dragon': '#6F35FC',
    'dark': '#705746',
    'steel': '#B7B7CE',
    'fairy': '#D685AD'
}

st.title("Pokemon Explorer")

def get_details(poke_number):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        return pokemon['name'], pokemon['height'], pokemon['weight'], len(pokemon['moves']), pokemon['sprites']['other']['official-artwork']['front_default'], pokemon['types'][0]['type']['name'], pokemon['cries']['latest']
    except:
        return 'Error', None, None, None, None, None, None

def fetch_and_plot_details(pokemon_number, prev_height):
    
    name, height, weight, moves, sprite_url, pokemon_type, cry_url = get_details(pokemon_number)

    st.write(f'Name: {name}')
    st.write(f'Height: {height}')
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

    colour = pokemon_colours.get(pokemon_type)

    height_data = {'Pokemon': ['Previous', 'Current'],
                   'Heights': [prev_height, height]}

    graph = sns.barplot(data=height_data,
                        x='Pokemon',
                        y='Heights',
                        palette=[pokemon_colours.get('normal'), colour])

    st.pyplot(graph.figure)

    return height

prev_pokemon_number = st.session_state.get('prev_pokemon_number', 1)
prev_height = st.session_state.get('prev_height', None)

pokemon_number = st.slider("Pick a pokemon",
                          min_value=1,
                          max_value=1025,
                          value=prev_pokemon_number)

if st.button("Fetch and Compare"):
    prev_height = fetch_and_plot_details(pokemon_number, prev_height)
    st.session_state.prev_height = prev_height
    st.session_state.prev_pokemon_number = pokemon_number

