import openai
import os
from datetime import datetime
import glob


# Ensure you replace this with your actual OpenAI API key
# It's recommended to use an environment variable for this.
openai.api_key = os.getenv('OPENAI_API_KEY', 'api-key-here')

def generate_travel_plan(country, num_days):
    # Define the conversation prompt using country and num_days
    conversation_prompt = (
        f"Create a detailed travel plan for a {num_days}-day trip to {country}.\n\n"
        "The travel plan should include a daily itinerary with activities, places to visit, "
        "and food recommendations."
    )
    try:
        # Send request to the OpenAI API using the ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a travel assistant."},
                {"role": "user", "content": conversation_prompt},
            ]
        )
        # Extract the travel plan from the response
        plan = response['choices'][0]['message']['content']
        return plan
    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")

def save_travel_plan_to_txt(country, plan):
    # Generate a unique filename using country name and current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"trip_plans/{country.replace(' ', '_')}_{timestamp}.txt"
    # Ensure the travel_plans directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # Open a .txt file in write mode with the generated filename
    with open(filename, 'w', encoding='utf-8') as file:
        # Write the plan to the file
        file.write(plan)
    return filename

def generate_and_save_travel_plan(country, num_days):
    plan = generate_travel_plan(country, num_days)
    filename = save_travel_plan_to_txt(country, plan)
    return filename

def check_existing_travel_plan(country):
    # Normalize the country name to match the filename pattern
    country_pattern = country.replace(' ', '_').lower()
    # Search for existing plans in the travel_plans directory
    existing_files = glob.glob(f'trip_plans/{country_pattern}_*.txt')
    return len(existing_files) > 0

