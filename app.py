
import streamlit as st
from model import generate_plan
from preprocess import preprocess_data
from firebase_config import init_firebase
from db_utils import save_user_input, fetch_plan

def main():
    # Initialize Firebase
    db = init_firebase()

    st.title("Tour Tech: Your Personalized Travel Planner")

    # Collect user inputs
    age = st.number_input("Age", min_value=18, max_value=100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    destination = st.text_input("Destination")
    duration = st.number_input("Duration (in days)", min_value=1, max_value=30)
    companions = st.number_input("How many people are you traveling with?", min_value=1, max_value=10)
    budget = st.number_input("Budget ($)", min_value=100, max_value=10000)

    # Button to generate travel plan
    if st.button("Generate My Travel Plan"):
        user_data = {
            "age": age,
            "gender": gender,
            "destination": destination,
            "duration": duration,
            "companions": companions,
            "budget": budget
        }

        # Preprocess the input data
        preprocessed_input = preprocess_data(user_data)

        # Generate the travel plan
        travel_plan = generate_plan(preprocessed_input)

        # Save user input to Firebase
        user_id = save_user_input(db, user_data)

        # Display the generated travel plan
        st.subheader("Your Travel Plan")
        st.write(travel_plan)

        # Optionally, save the generated plan to Firebase (not implemented in this snippet)
        # This could be an extension to store generated plans for user retrieval or analysis

if __name__ == "__main__":
    main()