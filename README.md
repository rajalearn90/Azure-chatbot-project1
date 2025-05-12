# Azure-chatbot-project1
Azure-chatbot-project1

1) Data Storage: Create storage account -> Import csv Data to storage table using the python code using storage the connection string.
2) AI Search Service: Create AI search service -> import the data from the azure table created above using the storage Connection string.
   Here we can schedule the data refresh daily, monthly, custom etc.
   * Search service key is required later.
3) Azure AI model: create HUb -> Project -> Launch studio and then  choose the AI MODEL (gpt-35-turbo) deploy -> 
   * AI Model key is required later.
    
4) APP UX - Streamlit 
5) Langchain Framework is used.

pip install azure - is depricated, Install specific service package.
* pip install azure-data-tables
* pip install streamlit
* pip install langchain_core
* pip install langchain_openai
* pip install langchain_community
*************************************************************
pip install --upgrade pip setuptools wheel
pip install azure-identity azure-mgmt-resource


Blob Storage	pip install azure-storage-blob
Key Vault (Secrets)	pip install azure-keyvault-secrets
Identity (Auth)	pip install azure-identity
Resource Management	pip install azure-mgmt-resource
Compute (VMs, etc.)	pip install azure-mgmt-compute
Cosmos DB	pip install azure-cosmos
*************************************************************