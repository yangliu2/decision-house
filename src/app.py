import streamlit as st
from typing import Dict
from pipeline import get_house


def display_page() -> Dict:

    data = {}

    st.set_page_config(page_title="House Finder",
                       layout="centered",
                       initial_sidebar_state="auto")

    # Title of the app
    st.title("House finder")

    # Custom CSS to set the width of the textbox to 25% of the screen size
    st.markdown(
        """
        <style>
        .textbox input {
            width: 100% !important;
        }
        .css-1d391kg {
        background-color: lightgray !important;
        }   
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Use columns for formatting
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        data['zipcode'] = st.text_input("Zipcode: ",
                                        placeholder=78750,
                                        key=1)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        data['min_price'] = st.text_input("Minimum Price: ",
                                          placeholder=800_000,
                                          key=2)
    with col2:
        data['max_price'] = st.text_input("Maximum Price: ",
                                          placeholder=1_000_000,
                                          key=3)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        data['min_bedroom'] = st.text_input("Minimum Number of Bedrooms: ",
                                            placeholder=4)
        data['min_bathroom'] = st.text_input("Minimum Number of Bathrooms: ",
                                             placeholder=2)


    # Create a button and call the function when the button is pressed
    if st.button("Get House"):
        st.write("Getting Resultes...")
        houses = get_house(zipcode=data['zipcode'],
                           bedroom_min_size=int(data['min_bedroom']),
                           bathroom_min_size=int(data['min_bathroom']),
                           price_min=int(data['min_price']),
                           price_max=int(data['max_price']))

        for house in houses:
            st.markdown(f"[{house}]({house})")
    return data


def main():

    data = display_page()
    print(data)


if __name__ == "__main__":
    main()
