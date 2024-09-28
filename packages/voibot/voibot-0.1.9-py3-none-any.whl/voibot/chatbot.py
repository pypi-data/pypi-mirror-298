import os
import tempfile
import requests
import warnings  # Import to suppress any remaining warnings
from langchain_community.chat_models import ChatOpenAI  # Updated import
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader  # Updated import
from langchain_community.vectorstores import Chroma  # Chroma import
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain.memory import ConversationBufferMemory  # Import memory
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Use CharacterTextSplitter instead of RecursiveCharacterTextSplitter
from langchain.schema import AIMessage, HumanMessage  # Import AIMessage and HumanMessage


from .utils import download_pdf_from_url, prompt_func, openaiAPI, openaiReply

# Suppress all warnings
warnings.filterwarnings("ignore")

class VoiAssistant:
    def __init__(self, openai_key, pdf_url, role, intents, replies, segment_assignments, dont_know_response=None):
        # Initialize API key and other configurations
        self.openai_key = openai_key
        os.environ['OPENAI_API_KEY'] = self.openai_key
        self.pdf_url = pdf_url
        self.role = role
        self.intents = intents
        self.replies = replies
        self.segment_assignments = segment_assignments
        self.dont_know_response = dont_know_response if dont_know_response else {}  # Custom responses from the user
        self.index = None
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)  # Use ConversationBufferMemory

    def get_most_recent_response(self):
        """
        Returns the most recent response from the conversation history.
        """
        chat_history = self.memory.load_memory_variables({})

        # Ensure the chat_history is not empty
        if chat_history and chat_history.get("chat_history"):
            # Loop through the chat history in reverse to find the most recent assistant response
            for message in reversed(chat_history["chat_history"]):
                if isinstance(message, AIMessage):  # Check if it's an AIMessage
                    return message.content  # AIMessage has a 'content' attribute
        return "Error: Most recent response could not be retrieved"
    
    def get_most_recent_query(self):
        """
        Returns the most recent query from the conversation history.
        """
        chat_history = self.memory.load_memory_variables({})

        # Ensure the chat_history is not empty
        if chat_history and chat_history.get("chat_history"):
            # Loop through the chat history in reverse to find the most recent assistant response
            for message in reversed(chat_history["chat_history"]):
                if isinstance(message, HumanMessage):  # Check if it's a HumanMessage
                    return message.content  # HumanMessage has a 'content' attribute
        return "Error: Most recent query could not be retrieved"

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
        prompt = prompt_func(query, 1, self.role, self.intents)

        # Call the OpenAI API for classification
        category = openaiAPI(prompt, 0.5, self.openai_key)

        # Check if the category is in the predefined classes
        if category in self.intents:
            if self.replies.get(category) == "RAG":
                # Perform ConversationalRetrieval with memory
                retriever = self.index.as_retriever()
                conversational_chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=retriever,
                    memory=self.memory  # Use memory here
                )
                result = conversational_chain.run({"question": query, "chat_history": self.memory.load_memory_variables({})})

                if result in ("I don't know", "I don't know."):
                    # Use custom response for n == 2, if provided, else default
                    result = self.dont_know_response
            elif self.replies.get(category) == "role_based_llm_reply":
                # Use LLM to provide an appropriate role-based reply
                result = openaiReply(query, 0.9, category, self.openai_key, self.role)
            else:
                # Replace {context_from_previous_response} with the previous response
                result = self.replies.get(category, "I'm not sure how to respond to that.")
                if "{most_recent_response}" in result:
                    previous_response = self.get_most_recent_response()
                    result = result.replace("{most_recent_response}", previous_response)
                elif "{most_recent_query}" in result:
                    previous_query = self.get_most_recent_query()
                    result = result.replace("{most_recent_query}", previous_query)
        else:
            result = "Unfortunately, I am unable to help you with that."

        # Save the chat history for context in future queries
        # Save the chat history for context in future queries
        self.memory.save_context({"question": query}, {"response": result})

        return result

