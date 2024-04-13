import streamlit as st
from travel_generator import generate_and_save_travel_plan, check_existing_travel_plan
from rag import generate_conversation, query, conversation_chain

def main():
    st.title("Travel Planning Helper")

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Plan a New Trip'):
            st.session_state.check_country = True

    with col2:
        if st.button('Previous Countries'):
            st.session_state.previous_countries = True  # Maintain state for RAG section

    if 'previous_countries' in st.session_state and st.session_state.previous_countries:
        st.title("RAG Model Conversation")
        user_input = st.text_input("You:", key="user_input")

        if st.button("Ask", key="ask_button"):
            # Call to RAG generate_conversation function and store result directly in session state
            st.session_state.answer = generate_conversation(user_input, conversation_chain)

        # Check if an answer is stored in the session state and display it
        if 'answer' in st.session_state:
            st.text_area("RAG:", value=st.session_state.answer, height=200)

    if st.session_state.get('check_country', False):
        country = st.text_input("Enter the country you plan to visit:", key="country").lower()
        num_days = st.number_input("Enter the number of days you are planning to travel:", min_value=1, key="num_days")
        if st.button("Generate Travel Plan"):
            if check_existing_travel_plan(country):
                st.warning(f"{country.title()} is already in the dataset. Please use the RAG feature to retrieve the plan.")
                st.session_state.check_country = False  # Optionally reset state
            else:
                filename = generate_and_save_travel_plan(country, int(num_days))
                st.success(f"Travel plan generated and saved! Filename: {filename}")

                # Display the travel plan
                with open(filename, 'r', encoding='utf-8') as file:
                    travel_plan = file.read()
                    st.text_area("Your travel plan:", travel_plan, height=250)

if __name__ == "__main__":
    if 'check_country' not in st.session_state:
        st.session_state.check_country = False
    main()