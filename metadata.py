from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from PyPDF2 import PdfReader
import os
import re

def extract_and_process_pdf(pdf_file_paths):
    all_data = []
    document_metadata = {}
    for pdf_file_path in pdf_file_paths:
        # Extract text from the PDF
        pdf_text = ""
        with open(pdf_file_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                # Extract text from each page
                page_text = page.extract_text()
                # Remove special characters
                page_text = re.sub(r'[^\w\s]|\\n', '', page_text)
                # Append the text of the current page to the overall PDF text
                pdf_text += page_text

        # Create a temporary text file
        temp_txt_filename = pdf_file_path.replace('.pdf', '.txt')
        with open(temp_txt_filename, 'w', encoding='utf-8') as f:
            f.write(pdf_text)

        # Extract intention from the file path
        intention = extract_intention_from_filepath(pdf_file_path)

        # Store metadata (intention) for the document
        document_metadata[temp_txt_filename] = intention

        # Use the extracted text file for further processing
        loader = TextLoader(file_path=temp_txt_filename, encoding="utf-8")
        data = loader.load()
        all_data.extend(data)

    return all_data, document_metadata


def extract_intention_from_filepath(file_path):
    # Extract intention from the file path
    # For example, extract "italy" from "trip_plans/italy.pdf"
    intention = os.path.splitext(os.path.basename(file_path))[0]
    return intention

def create_conversation_chain(processed_texts, api_key):
    # Set the API key as an environment variable
    os.environ["OPENAI_API_KEY"] = api_key

    # Create vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(processed_texts, embedding=embeddings)

    # Create conversation chain
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def extract_intention_from_query(query):
    # Define a mapping of keywords to intentions
    keyword_intention_map = {
        "italia": "italia",
        "croacia": "croacia_bosnia",
        "grecia": "grecia",
        "condiciones": "condiciones_comerciales",
        "españa": "spain",
        "praga": "praga"
    }
    
    # Check if any of the keywords are present in the query
    for keyword, intention in keyword_intention_map.items():
        if keyword in query.lower():
            return intention
    
    # If no specific keyword is found, return a default intention
    return "general"

# Input your OpenAI API key here
api_key = "api-key"

pdf_files = [
    "trip_plans/italia.pdf",
    "trip_plans/croacia_bosnia.pdf",
    "trip_plans/grecia.pdf",
    "trip_plans/condiciones_comerciales.pdf",
    "trip_plans/spain.pdf",
    "trip_plans/praga.pdf"
]

# Define the query
query = "Cual es el plan de praga?"

# Extract and process PDF text for all documents
processed_texts, document_metadata = extract_and_process_pdf(pdf_files)

# Extract intention from the query
query_intention = extract_intention_from_query(query)

def filter_relevant_information(processed_texts, document_metadata, query_intention):
    relevant_texts = []
    for text, intention in zip(processed_texts, document_metadata.values()):
        if intention == query_intention:
            relevant_texts.append(text)
    return relevant_texts

# Extract and process PDF text for relevant documents
relevant_texts = filter_relevant_information(processed_texts, document_metadata, query_intention)

# Create conversation chain with relevant processed text
conversation_chain = create_conversation_chain(relevant_texts, api_key)

# Query the conversation chain
result = conversation_chain({"question": query})
answer = result["answer"]

# Print the answer
print("Answer:", answer)