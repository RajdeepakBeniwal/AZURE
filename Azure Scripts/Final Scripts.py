
# -----------------------------------------------------
# Import Workspace class 
# -----------------------------------------------------
from azureml.core import Workspace


# -----------------------------------------------------
#  Create the workspace
# -----------------------------------------------------
ws = Workspace.create(name='<Your Workspace Name>',
                      subscription_id='<Your Subscription ID>',
                      resource_group='<Resource group Name',
                      create_resource_group=True,                    # True if it does not exist
                      location='<Nearest Azure region>')


# -----------------------------------------------------
# Write the config.json file to local directory
# -----------------------------------------------------

ws.write_config(path="./config")

# -----------------------------------------------------
# Import the Workspace and Datastore class
# -----------------------------------------------------
from azureml.core import Workspace, Datastore


# -----------------------------------------------------
# Access the workspace from the config.json 
# -----------------------------------------------------
ws = Workspace.from_config(path="./config")


# -----------------------------------------------------
# Create a datastore 
# -----------------------------------------------------
az_store = Datastore.register_azure_blob_container(
            workspace=ws,
            datastore_name="azure_sdk_blob01",
            account_name="azuremlstb01",
            container_name="azuremlstb01blob",
            account_key="mQ6meDug7SdlFXu0/tBu7pKcNerxxYtO6X1V13M4sSohBAv2/i2KxdYe3ueiQXKrw+alPU1ou4NBuYBtuBVsig==")


# -----------------------------------------------------
# Access datastore by its name
# -----------------------------------------------------
az_store = Datastore.get(ws, "azure_sdk_blob01")


# -----------------------------------------------------
# Create and register the dataset
# -----------------------------------------------------

# Create the path of the csv file
csv_path = [(az_store, "Loan Data/Loan Approval Prediction.csv")]

# Create the dataset
loan_dataset = Dataset.Tabular.from_delimited_files(path=csv_path)

# Register the dataset
loan_dataset = loan_dataset.register(workspace=ws,
                                     name="Loan Applications Using SDK",
                                     create_new_version=True)


# -----------------------------------------------------
# List all the workspaces within a subscription
# -----------------------------------------------------

ws_list = Workspace.list(subscription_id="77819c59-5764-4995-8596-d09cdc661078")
ws_list = list(ws_list)


# -----------------------------------------------------
# Access the default datastore from workspace
# -----------------------------------------------------
az_default_store = ws.get_default_datastore()


# -----------------------------------------------------
# List all the datastores
# -----------------------------------------------------
store_list = list(ws.datastores)


# -----------------------------------------------------
# Get the dataset by name from a workspace
# -----------------------------------------------------
az_dataset = Dataset.get_by_name(ws, "Loan Applications Using SDK")


# -----------------------------------------------------
# List datasets from a workspace
# -----------------------------------------------------

ds_list = list(ws.datasets.keys())

for items in ds_list:
    print(items)



# -----------------------------------------------------
# Access the Workspace, Datastore and Datasets
# -----------------------------------------------------
ws                = Workspace.from_config("./config")
az_store          = Datastore.get(ws, 'azure_sdk_blob01')
az_dataset        = Dataset.get_by_name(ws, 'Loan Applications Using SDK')
az_default_store  = ws.get_default_datastore()


# -----------------------------------------------------
# Load the Azureml Dataset into the pandas dataframe
# -----------------------------------------------------
df = az_dataset.to_pandas_dataframe()


# -----------------------------------------------------
# Upload the dataframe to the azureml dataset
# -----------------------------------------------------
df_sub = df[["Married", "Gender", "Loan_Status"]]

az_ds_from_df = Dataset.Tabular.register_pandas_dataframe(
                dataframe=df_sub,
                target=az_store,
                name="Loan Dataset From Dataframe")

# -----------------------------------------------------
# Upload local files to storage account using datastore 
# -----------------------------------------------------
files_list = ["./data/test.csv", "./data/test1.csv"]

az_store.upload_files(files=files_list,
                      target_path="Loan Data/",
                      relative_root="./data/",
                      overwrite=True)


# -----------------------------------------------------
# Upload folder or directory to the storage account
# -----------------------------------------------------
az_store.upload(src_dir="./data",
                target_path="Loan Data/data",
                overwrite=True)


































