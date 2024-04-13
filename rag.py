from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from PyPDF2 import PdfReader
import os

from langchain.chains import RetrievalQA
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain.agents.agent_types import AgentType
import tiktoken


api_key = "api-key"
# Set the API key as an environment variable
os.environ["OPENAI_API_KEY"] = api_key

llm_model = "gpt-3.5-turbo"

# Define the path to your PDF file
#change so that it uses a relative path
pdf_file_path = "/Users/mariana/Desktop/stats/trip_plans/italia.pdf"

#TODO: check if the pdf is already processed (in txt)
#If already in txt... use that one. If not, preprocess it.
#TODO: find a way to index documents and chunk info 
# Extract text from the PDF
pdf_text = ""
with open(pdf_file_path, 'rb') as f:
    pdf_reader = PdfReader(f)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()

# Save the extracted text to a temporary text file
temp_txt_filename = pdf_file_path.replace('.pdf', '.txt')
with open(temp_txt_filename, 'w', encoding='utf-8') as f:
    f.write(pdf_text)

# Use the extracted text file for further processing
loader = TextLoader(file_path=temp_txt_filename, encoding="utf-8")
data = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
data = text_splitter.split_documents(data)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(data, embedding=embeddings)

# Create conversation chain
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
memory = ConversationBufferMemory(
memory_key='chat_history', return_messages=True)
conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        memory=memory
        )

query = "Que plan hay en el dia 6 para el viaje de italia?"
result = conversation_chain({"question": query})
answer = result["answer"]
print(answer)