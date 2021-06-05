
# -----------------------------------------------------
# Import required classes from Azureml
# -----------------------------------------------------
from azureml.core import Workspace, Datastore, Dataset, Experiment


# -----------------------------------------------------
# Access the Workspace, Datastore and Datasets
# -----------------------------------------------------
ws                = Workspace.from_config("./config")
az_store          = Datastore.get(ws, 'azure_sdk_blob01')
az_dataset        = Dataset.get_by_name(ws, 'Loan Applications Using SDK')
az_default_store  = ws.get_default_datastore()

# -----------------------------------------------------
# Create/Access an experiment object
# -----------------------------------------------------
experiment = Experiment(workspace=ws,
                        name="Loan-SDK-Exp01")


# -----------------------------------------------------
# Run an experiment using start_logging method
# -----------------------------------------------------
new_run = experiment.start_logging()


# -----------------------------------------------------
# Do your stuff here
# -----------------------------------------------------
df = az_dataset.to_pandas_dataframe()

# Count the observations
total_observations = len(df)

# Get the null/missing values
nulldf = df.isnull().sum()


# -----------------------------------------------------
# Log metrics and Complete an experiment run
# -----------------------------------------------------

# Log the metrics to the workspace
new_run.log("Total Observations", total_observations)

# Log the missing data values
for columns in df.columns:
    new_run.log(columns, nulldf[columns])

new_run.complete()


# ------------------------------------------------------------
# Run a script in an Azureml environment
# ------------------------------------------------------------
# This code will submit the script provided in ScriptRunConfig
# and create an Azureml environment on the local machine
# including the docker for Azureml
# ------------------------------------------------------------

# Import the Azure ML classes
from azureml.core import Workspace, Experiment, ScriptRunConfig

# Access the workspace using config.json
ws = Workspace.from_config("./config")


# Create/access the experiment from workspace 
new_experiment = Experiment(workspace=ws,
                            name="Loan_Script")


# Create a script configuration
script_config = ScriptRunConfig(source_directory=".",
                                script="180 - Script To Run.py")


# Submit a new run using the ScriptRunConfig
new_run = new_experiment.submit(config=script_config)


# Create a wait for completion of the script
new_run.wait_for_completion()

# -----------------------------------------------------
#  Create a compute cluster using AzureML SDK
# -----------------------------------------------------

# Import the Workspace class
from azureml.core import Workspace


# Access the workspace from the config.json 
ws = Workspace.from_config(path="./config")


# Specify the cluster name
cluster_name = "my-cluster-001"


# Provisioning configuration using AmlCompute
from azureml.core.compute import AmlCompute

# Configuration of the compute cluster
compute_config = AmlCompute.provisioning_configuration(
                                 vm_size="STANDARD_D11_V2",
                                 max_nodes=2)


# Create the cluster
cluster = AmlCompute.create(ws, cluster_name, compute_config)































