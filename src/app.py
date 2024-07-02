""" Streamlit UI for interaction """
import streamlit as st
from typing import Dict
from pipeline import get_house


def display_page() -> Dict:
    """" Streamlit website for UI interaction """

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
        ! Make mobile friendly
        @media (max-width: 600px) {
            .main {
                padding: 1rem;
            }
            .css-18e3th9 {
                flex-direction: column;
            }
        }

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
    with col2:
        data['min_bathroom'] = st.text_input("Minimum Number of Bathrooms: ",
                                             placeholder=2)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        data['min_school_rating'] = st.text_input("Minimum school rating",
                                                  placeholder=7)
    data['school_name'] = st.text_input(
        "Please indicate a school you must have around the house",
        placeholder="Thomas Jefferson High School for Science & Technology")

    st.write("(Please wait for at least 20 seconds after pressing the button. "
             "Will be longer depending on the number of results.) ")

    # Create a button and call the function when the button is pressed
    if st.button("Get House"):
        st.write("Getting Resultes...")
        houses = get_house(zipcode=data['zipcode'],
                           bedroom_min_size=int(data['min_bedroom']),
                           bathroom_min_size=int(data['min_bathroom']),
                           price_min=int(data['min_price']),
                           price_max=int(data['max_price']),
                           min_school_rating=int(data['min_school_rating']),
                           desired_school=data['school_name'])

        if not houses:
            st.write("We did not find any house that fit the criteria. "
                     "Please make a wider search.")

        for house in houses:
            st.markdown(f"[{house}]({house})")
    return data


def main():

    data = display_page()
    print(data)


if __name__ == "__main__":
    main()
