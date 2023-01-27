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

### Connect to fruityvice api for fruit info
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())   
    return fruityvice_normalized

st.header('Fruityvice Fruit Advice')
try:
    fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
    if not fruit_choice:
        st.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        st.dataframe(back_from_function)
except URLError as e:
    st.error()

### Connect to snowflake and add fruit load list
st.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

if st.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    st.dataframe(my_data_rows)

#st.stop()

### Fruit Name Submissions
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlit')")
        return "Thanks for adding " + new_fruit

add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    st.text(back_from_function)




### Add second text entry box
#my_add_fruit = st.text_input('What fruit would you like information about?')
#st.write('Thanks for adding', my_add_fruit)


m#y_cur.execute("insert into fruit_load_list values ('from streamlit')")
