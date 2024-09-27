import os
import tempfile
import requests
import warnings  # Import to suppress any remaining warnings
from langchain_community.chat_models import ChatOpenAI  # Updated import
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader  # Updated import
from langchain_community.vectorstores import Chroma  # Chroma import
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Updated import

from .utils import download_pdf_from_url, prompt_func, openaiAPI

# Suppress all warnings
warnings.filterwarnings("ignore")

class VoiAssistant:
    def __init__(self, openai_key, pdf_url, role, classes, replies, segment_assignments):
        # Initialize API key and other configurations
        self.openai_key = openai_key
        os.environ['OPENAI_API_KEY'] = self.openai_key
        self.pdf_url = pdf_url
        self.role = role
        self.classes = classes
        self.replies = replies
        self.segment_assignments = segment_assignments
        self.index = None
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
    
    class ParagraphTextSplitter(RecursiveCharacterTextSplitter):
        def split_text(self, text):
            return text.split('\n\n')
        
    def initialize_assistant(self):
        try:
            # Download the PDF
            downloaded_pdf_path = download_pdf_from_url(self.pdf_url)
            loader = PyPDFLoader(downloaded_pdf_path)
            documents = loader.load()

            # Split the document text
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.split_documents(documents)

            # Create the embeddings
            embeddings = OpenAIEmbeddings()

            # Create Chroma vectorstore from documents
            self.index = Chroma.from_documents(docs, embeddings)

            os.remove(downloaded_pdf_path)
        except Exception as e:
            print(f"Error initializing assistant: {str(e)}")
            self.index = None
    
    def get_response(self, query):
        if self.index is None:
            raise ValueError("Assistant is not initialized.")

        # Construct the classification prompt
        prompt = prompt_func(query, 1, self.role, self.classes)

        # Call the OpenAI API for classification
        category = openaiAPI(prompt, 0.5, self.openai_key)

        # Check if the category is in the predefined classes
        if category in self.classes:
            if self.replies.get(category) == "RAG":
                # Perform RetrievalQA
                retriever = self.index.as_retriever()
                qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=retriever)
                result = qa_chain.run(query)

                if result in ("I don't know", "I don't know."):
                    result = prompt_func(query, 2, self.role, self.classes)
            else:
                # Use the predefined automatic reply
                result = self.replies.get(category, "I'm not sure how to respond to that.")
        else:
            result = "Unfortunately, I am unable to help you with that."
        
        return result
