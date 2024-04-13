import openai

openai.api_key = 'api-key-here'

def generate_plan(preprocessed_data):
    """
    Generate a trip plan based on user input using OpenAI's chat model.

    Parameters:
    - preprocessed_data: A preprocessed string containing user input data.

    Returns:
    - A string containing the generated trip plan.
    """
    try:
        # Using the Chat API for chat-based models
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the chat model here
            messages=[{"role": "system", "content": "Generate a trip plan."},
                      {"role": "user", "content": preprocessed_data}]
        )
        
        # Extracting the generated text from the chat response
        if response['choices']:
            trip_plan = response['choices'][0]['message']['content']
        else:
            trip_plan = "No plan could be generated."
            
    except openai.error.InvalidRequestError as e:
        print(f"Encountered an error: {e}")
        trip_plan = "An error occurred while generating the plan."

    return trip_plan