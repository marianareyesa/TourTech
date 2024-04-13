from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from PyPDF2 import PdfReader
import os

def extract_and_process_pdf(pdf_file_paths):
    all_data = []
    for pdf_file_path in pdf_file_paths:
        # Extract text from the PDF
        pdf_text = ""
        with open(pdf_file_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()

        # Create a temporary text file
        temp_txt_filename = pdf_file_path.replace('.pdf', '.txt')
        with open(temp_txt_filename, 'w', encoding='utf-8') as f:
            f.write(pdf_text)

        # Use the extracted text file for further processing
        loader = TextLoader(file_path=temp_txt_filename, encoding="utf-8")
        data = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        data = text_splitter.split_documents(data)
        all_data.extend(data)
    
    return all_data

def create_conversation_chain(processed_texts, api_key):
    # Set the API key as an environment variable
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Create vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(processed_texts, embedding=embeddings)

    # Create conversation chain
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Input your OpenAI API key here
api_key = "api-key"

# Define the list of PDF files
pdf_files = [
    "/Users/mariana/Desktop/stats/TourTech/trip_plans/italia.pdf",
    "/Users/mariana/Desktop/stats/TourTech/trip_plans/coracia_bosnia.pdf",
    "/Users/mariana/Desktop/stats/TourTech/trip_plans/grecia.pdf"
]

# Define the query
query = "Que paises estan siendo mencionados?"

# Extract and process PDF text for all documents
processed_texts = extract_and_process_pdf(pdf_files)

# Create conversation chain with combined processed text
conversation_chain = create_conversation_chain(processed_texts, api_key)

# Query the conversation chain
result = conversation_chain({"question": query})
answer = result["answer"]

# Print the answer
print("Answer:", answer)