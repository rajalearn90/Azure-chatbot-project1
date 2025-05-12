#Create an Azure Table based on the File / Private Knowledge Base

import csv
from azure.data.tables import TableServiceClient, TableEntity

# Set up your Azure Table Storage connection
connection_string ="DefaultEndpointsProtocol=https;AccountName=aimodelstorageproj1;AccountKey=6XVQztdZbxBemxCp/Hl/ry//VWxeIZQhFNMM2WwmMfgdolsaZrbMPJts+Z6vg+Pn3vSK0YOGKi0o+ASt7boBAA==;EndpointSuffix=core.windows.net"
table_name = "AzureChatQA"

# Create a TableServiceClient
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)

# Create a table if it doesn't exist
try:
    table_service.create_table(table_name)
except Exception as e:
    print(f"Table already exists: {e}")

# Read the CSV file and upload the data
csv_file_path = "azurelib2.csv"

with open(csv_file_path) as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)
        # Create a new entity
        entity = TableEntity()
        entity['PartitionKey'] = "AZURELIB"  # You can set this to whatever makes sense
        entity['RowKey'] = row['id']  # Use ID as RowKey
        entity['Question'] = row['question']
        entity['Answer'] = row['answer']

        # Upload the entity to the table
        try:
            table_service.get_table_client(table_name).create_entity(entity=entity)
            print(f"Uploaded: {entity['RowKey']} - {entity['Question']}")
        except Exception as e:
            print(e)
print("Data upload complete.")