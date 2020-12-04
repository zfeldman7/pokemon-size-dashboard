#!/usr/bin/env python
# coding: utf-8

# Visualizing Pokemon
# This is a small 

# First, we load the dataset we're familiar with, and remember what it contains.
import streamlit as st
import pandas as pd
import numpy as np
import math

pokemon_data = pd.read_csv( 'pokemon_data.csv' )

st.title('Which Pokemon are closest to you in size?')

# user input fields on sidebar
st.sidebar.write('Enter your Height and Weight')

user_height_ft = st.sidebar.number_input('Height (ft):', value=0, min_value=0)

user_height_in = st.sidebar.number_input('Height (in):', value=0, min_value=0, max_value=11)

user_weight_lbs = st.sidebar.number_input('Weight (lbs):', value=0, min_value=0)

# need to convert imperial values to metric system to compare against our pokemon data
user_height_meters = round(((user_height_ft * 12) + user_height_in) * 0.0254, 2)
user_weight_kg = round(user_weight_lbs * 0.453592, 2)

# to get the pokemon with the closest size to the users, we are going to use the 
# Euclidean distance formula: 
# sqrt( (height_user - height_pokemon)^2 + (weight_user - weight_pokemon)^2)

min_distance = 1000000 # start the min distance at an impossibly high number
min_pokedex_entry = 0
for pokedex_entry in range(1, pokemon_data.shape[0]):

	# tally the euclidian distance for all potential pokemon and find the minimum value
	height_diff = ( user_height_meters - pokemon_data.loc[pokedex_entry -1, 'height_m']) ** 2
	weight_diff = ( user_weight_kg - pokemon_data.loc[pokedex_entry -1, 'weight_kg']) ** 2
	distance = math.sqrt(height_diff + weight_diff)

	# append the distance to the entry of the pokemon
	pokemon_data.loc[pokedex_entry -1, 'eu_distance'] = round(distance, 4)

# grab the three pokemon with smallest distance
three_closest_pokemon = pokemon_data.nsmallest(n=3, columns='eu_distance')

st.write(f'User input converted to: {user_height_meters} meters and {user_weight_kg} kg')

# create three streamlit columns and package them up in a list
poke_1, poke_2, poke_3 = st.beta_columns(3)
columns = [poke_1, poke_2, poke_3]

# loop through the columns and the three pokemon to display their information & images
for index, column in enumerate(columns):
	image_url = three_closest_pokemon.iloc[index]['image_url']
	name = three_closest_pokemon.iloc[index]['name']

	
	poke_info = three_closest_pokemon[['pokedex_number', 'height_m', 'weight_kg', 'type1', 'type2', 'eu_distance']]
	poke_info.set_index('pokedex_number', inplace=True)
	columns_map = {'pokdex_number': 'Pokedex Number', 
		'height_m': 'Height (m)',
		'weight_kg': 'Weight (kg)',
		'type1': 'Type 1',
		'type2': 'Type 2',
		'eu_distance': 'Euclidean Dist'
	}

	poke_info = poke_info.rename(columns=columns_map)

	poke_info = poke_info.astype(object).replace(np.nan, 'None')
	
	column.image(image_url, width=300, caption=name)
	column.write(poke_info.iloc[index])