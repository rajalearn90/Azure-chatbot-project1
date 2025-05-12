import streamlit as st
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import AzureChatOpenAI
from langchain_community.retrievers import AzureAISearchRetriever

# Step 1: Set the environment variables for Azure AI Search and OpenAI API Key securely
azure_search_service = os.getenv("AZURE_SEARCH_SERVICE_NAME", "azurelibaisearch")
azure_search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
azure_search_index = os.getenv("AZURE_SEARCH_INDEX_NAME", "azuretable-indexer")
azure_content_field = os.getenv("AZURE_CONTENT_KEY", "Answer")

openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://rajaa-makza3il-eastus2.openai.azure.com/")
openai_model = "gpt-4"  # Ensure this is the correct model for your requirements

# Initialize the Azure AI Search Retriever
retriever = AzureAISearchRetriever(
    service_name=azure_search_service,
    api_key=azure_search_api_key,
    index_name=azure_search_index,
    content_key=azure_content_field,
    top_k=3
)

# Define the prompt template for the language model
prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}

Question: {question}"""
)

# Initialize the Azure Chat OpenAI model
llm = AzureChatOpenAI(
    api_version="2025-01-01-preview",  # Specify the API version
    azure_endpoint=openai_endpoint,
    api_key=openai_api_key,
    model=openai_model
)

# Create a processing chain
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
    try:
        with st.chat_message("assistant"):
            # Pass the correct inputs to the chain
            response = chain.invoke({"context": retriever, "question": user_question})
            st.markdown(response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
