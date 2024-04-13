import os
from PyPDF2 import PdfFileReader

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

    directory_path = 'trip_plans'
    output_directory = 'trip_plans_txt'

    # Debugging: Print the current working directory
    print(f"Current working directory: {os.getcwd()}")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created directory: {output_directory}")
        return None

    file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.pdf')]

    for file_path in file_paths:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file_path = os.path.join(output_directory, f"{file_name}.txt")

        # Debugging: Print the file paths being processed
        print(f"Processing file: {file_path}")
        print(f"Will save to: {output_file_path}")

        if not os.path.exists(output_file_path):
            try:
                with open(file_path, 'rb') as file:
                    pdf = PdfFileReader(file)
                    text_content = []
                    for page in range(pdf.getNumPages()):
                        text_content.append(pdf.getPage(page).extractText())

                    with open(output_file_path, 'w') as output_file:
                        output_file.write('\n'.join(text_content))
                        print(f"Content written to {output_file_path}")
            except Exception as e:
                print(f"Failed to process file {file_path} with error: {e}")
        else:
            print(f"File already processed: {output_file_path}")


    return input_string