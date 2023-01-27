import streamlit as st
import pandas as pd
import requests as rq

st.title('My Mom\'s New Healthy Diner')
st.subheader('Mon-Sat 7am - 9pm')
st.subheader('Sun 9am - 2:30pm')
st.header('Breakfast Favorites')

st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')
st.header('🍌🥭 Build your Own Fruit Smoothie 🥝🍇')


fruit_csv = 'https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt'

my_fruit_list = pd.read_csv(fruit_csv)
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

### Pull in FruityVice API response
st.header('Fruityvice Fruit Advice')
fruityvice_response = rq.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json()) #removed in favor of the tabular output below

### Normalize the FV json data
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

### Output as a table
st.dataframe(fruityvice_normalized)

