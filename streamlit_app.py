import streamlit as st
import pandas as pd
import requests as rq
import snowflake.connector
from urllib.error import URLError

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

st.header('Fruityvice Fruit Advice')

fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
st.write('The user entered', fruit_choice)

### Pull in FruityVice API response
fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)

### Normalize the FV json data
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

### Output as a table
st.dataframe(fruityvice_normalized)

st.stop()

### Connect to snowflake and add fruit load list
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

### Add second text entry box
my_add_fruit = st.text_input('What fruit would you like information about?')
st.write('Thanks for adding', my_add_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
