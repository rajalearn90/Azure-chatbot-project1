import streamlit as st
#from openai import OpenAI
import os
st.title("Azurelib Chatbot")

# Step 2: Set the environment variables for Azure AI Search
# These variables configure the search service and index for retrieving documents

# Import necessary libraries and modules from Langchain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import AzureChatOpenAI
from langchain_community.retrievers import AzureAISearchRetriever

# Step 1: Initialize the AzureAI Search Retriever
# This retrieves relevant documents based on the user query from the Azure Search index
retriever = AzureAISearchRetriever(
    service_name="azurelibaisearch",  # Ensure this matches your service name
    api_key="",  # Ensure this is a valid API key
    index_name="azuretable-indexer",  # Ensure this matches your index name
    content_key="Answer",  # Ensure this matches the field in your index
    top_k=3
)

# Step 2: Define the prompt template for the language model
# This sets up how the context and question will be formatted for the model
prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}

Question: {question}"""
)

# Step 3: Initialize the Azure Chat OpenAI model
# This sets up the model to be used for generating responses
llm = AzureChatOpenAI(
    api_version="2025-01-01-preview",  # Specify the API version to use
    azure_endpoint="https://rajaa-makza3il-eastus2.openai.azure.com/" ,
    api_key="", # Fetch the API key for Azure OpenAI from environment variables
    model="gpt-4o" # Specify the model to use
)

# Step 4: Create a processing chain
# This chain will process the retrieved context and the user question
#chain = (
#    {"context": retriever , "question": RunnablePassthrough()}  # Set context using the retriever and format it
#    | prompt       # Pass the formatted context and question to the prompt
#    | llm          # Generate a response using the language model
#    | StrOutputParser() # Parse the output to a string format
#)

chain = (
    {"context": lambda x: retriever.get_relevant_documents(x["question"]), "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_question := st.chat_input("How Can I help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_question})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_question)

   # Retrieve context and generate assistant response
    with st.chat_message("assistant"):
        # Pass the correct inputs to the chain
        response = chain.invoke({"context": retriever, "question": user_question})
        st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})