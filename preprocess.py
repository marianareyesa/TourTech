def preprocess_data(user_data):
    """
    Preprocess user input data for the AI model.

    Parameters:
    - user_data: A dictionary containing the user's input data.

    Returns:
    - A string formatted for the AI model input.
    """
    # Example preprocessing, converting user_data dict to a formatted string
    # Adjust the preprocessing logic based on the AI model's requirements
    input_string = f"Age: {user_data['age']}, Gender: {user_data['gender']}, " \
                   f"Destination: {user_data['destination']}, Duration: {user_data['duration']} days, " \
                   f"People: {user_data['companions']}, Budget: {user_data['budget']}"
    return input_string