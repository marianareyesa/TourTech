import streamlit as st
from travel_generator import generate_and_save_travel_plan, check_existing_travel_plan
from rag import generate_conversation, conversation_chain

def display_rag_conversation():
    # Custom CSS for chat bubble styling
    st.markdown("""
        <style>
            .chat-message {
                padding: 0.3rem 1rem;
                margin: 0.3rem 0;
                border-radius: 25px;
                position: relative;
            }
            .chat-message.you {
                margin-left: auto;
                background-color: #0b93f6;
                color: white;
            }
            .chat-message.rag {
                background-color: #e5e5ea;
                color: black;
            }
            .chat-container {
                max-width: 80%;
                margin: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("RAG Model Conversation")
    conversation_history = st.session_state.get('conversation_history', [])

    # Display the conversation history
    for exchange in conversation_history:
        message_type = "you" if exchange['sender'] == "You:" else "rag"
        st.markdown(
            f'<div class="chat-container"><div class="chat-message {message_type}">{exchange["content"]}</div></div>',
            unsafe_allow_html=True
        )

    # Text input for the user's message
    user_message = st.text_input("", placeholder="Type a message...", key='user_message')

    # When the 'Ask' button is pressed, update the conversation history and clear the message input
    if st.button("Ask"):
        if user_message:
            # Append user question to conversation history
            conversation_history.append({
                'sender': 'You:',
                'content': user_message,
            })

            # Get the response from RAG
            response = generate_conversation(user_message, conversation_chain)

            # Append RAG response to conversation history
            conversation_history.append({
                'sender': 'RAG:',
                'content': response,
            })

            # Update the conversation history in the state
            st.session_state.conversation_history = conversation_history
            

def main():
    st.title("Travel Planning Helper")
    col1, col2 = st.columns(2)

    with col1:
        if st.button('Plan a New Trip'):
            st.session_state.check_country = True
            st.session_state.previous_countries = False

    with col2:
        if st.button('Previous Countries'):
            st.session_state.previous_countries = True
            st.session_state.check_country = False

    if 'previous_countries' in st.session_state and st.session_state.previous_countries:
        display_rag_conversation()

    elif 'check_country' in st.session_state and st.session_state.check_country:
        country = st.text_input("Enter the country you plan to visit:", key="country").lower()
        num_days = st.number_input("Enter the number of days you are planning to travel:", min_value=1, key="num_days")
        if st.button("Generate Travel Plan"):
            if check_existing_travel_plan(country):
                st.warning(f"{country.title()} is already in the dataset. Please use the RAG feature to retrieve the plan.")
                st.session_state.check_country = False
            else:
                filename = generate_and_save_travel_plan(country, int(num_days))
                st.success(f"Travel plan generated and saved! Filename: {filename}")
                with open(filename, 'r', encoding='utf-8') as file:
                    travel_plan = file.read()
                    st.text_area("Your travel plan:", travel_plan, height=250)

# Run the main function when the script is executed
if __name__ == "__main__":
    if 'check_country' not in st.session_state:
        st.session_state.check_country = False
    if 'previous_countries' not in st.session_state:
        st.session_state.previous_countries = False
    main()