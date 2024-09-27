import os
import tempfile
import requests
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import TextSplitter

from .utils import download_pdf_from_url, prompt_func, openaiAPI

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
    
    class ParagraphTextSplitter(TextSplitter):
        def split_text(self, text):
            return text.split('\n\n')
        
    def initialize_assistant(self):
        try:
            downloaded_pdf_path = download_pdf_from_url(self.pdf_url)
            loader = PyPDFLoader(downloaded_pdf_path)
            documents = loader.load()
            
            # Instantiate the custom ParagraphTextSplitter
            text_splitter = self.ParagraphTextSplitter()
            
            self.index = VectorstoreIndexCreator(
                vectorstore_cls=Chroma, 
                embedding=OpenAIEmbeddings(chunk_size=20),
                text_splitter=text_splitter  # Use instantiated splitter
            ).from_documents(documents)
            
            os.remove(downloaded_pdf_path)
            print("Assistant initialized successfully")
        except Exception as e:
            print(f"Error initializing Assistant: {str(e)}")
            self.index = None
    
    def get_response(self, query):
        if self.index is None:
            raise ValueError("Assistant is not initialized.")
        
        # Log the input query
        print(f"Received query: {query}")

        # Construct the classification prompt
        prompt = prompt_func(query, 1, self.role, self.classes)
        print(f"Constructed classification prompt: {prompt}")

        # Call the OpenAI API for classification
        category = openaiAPI(prompt, 0.5, self.openai_key)
        print(f"Classified category: {category}")

        # Check if the category is in the predefined classes
        if category in self.classes:
            print(f"Category '{category}' is in the predefined classes.")
            
            if self.replies.get(category) == "RAG":
                print("Category requires RAG. Attempting to retrieve relevant documents...")

                # Perform RetrievalQA
                retriever = self.index.vectorstore.as_retriever()
                qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=retriever)
                result = qa_chain.run(query)
                print(f"RAG result: {result}")

                if result in ("I don't know", "I don't know."):
                    print("RAG result was 'I don't know'. Trying to rephrase the query.")
                    prompt = prompt_func(query, 2, self.role, self.classes)
                    result = openaiAPI(prompt, 0.9, self.openai_key)
                    print(f"Rephrased query result: {result}")
            else:
                # Use the predefined automatic reply
                reply = self.replies.get(category, "I'm not sure how to respond to that.")
                print(f"Using automatic reply: {reply}")
                result = openaiAPI(f"Rephrase this: {reply}", 0.9, self.openai_key)
                print(f"Rephrased automatic reply result: {result}")
        else:
            print(f"Category '{category}' is not recognized.")
            result = "Unfortunately, I am unable to help you with that."
        
        # Log the final result
        print(f"Final result: {result}")
        
        return result

