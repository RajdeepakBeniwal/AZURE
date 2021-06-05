# --------------------------------------------------------------
# Model DataDrift Detection step of the pipeline run
# --------------------------------------------------------------

# Import required classes from Azureml
from azureml.core import Run
import argparse


# Get the context of the experiment run
new_run = Run.get_context()


# Access the Workspace
ws = new_run.experiment.workspace


################################################ Get parameters
parser = argparse.ArgumentParser()
parser.add_argument("--datafolder", type=str)
args = parser.parse_args()
#################################################


# -----------------------------------------------------
# Do your stuff here
# -----------------------------------------------------
# Upload/Access the Target data(this should be with timestamp)

default_ds = ws.get_default_datastore()
default_ds.upload_files(files=['./data/target_data_file.csv'],
                       target_path='target_data',
                       overwrite=True, 
                       show_progress=True)

# -----------------------------------------------------
# Create and register the target dataset
# -----------------------------------------------------

print('Registering target dataset...')
target_data_set = Dataset.Tabular.from_delimited_files(path=(default_ds, 'target_data/*.csv'))
target_data_set = target_data_set.register(workspace=ws, 
                           name='target data',
                           description='target data for comparison',
                           tags = {'format':'CSV'},
                           create_new_version=True)

print('Target dataset registered!')

# -----------------------------------------------------
#Checking/creating compute cluster
# -----------------------------------------------------

from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException

cluster_name = "your-compute-cluster-name"

try:
    # Check for existing compute target
    training_cluster = ComputeTarget(workspace=ws, name=cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    # If it doesn't already exist, create it
    try:
        compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS11_V2', max_nodes=2)
        training_cluster = ComputeTarget.create(ws, cluster_name, compute_config)
        training_cluster.wait_for_completion(show_output=True)
    except Exception as ex:
        print(ex)

# -----------------------------------------------------
#Creating DataDrift Monitor
# -----------------------------------------------------

from azureml.datadrift import DataDriftDetector, AlertConfiguration

# set up feature list
features = ['Pregnancies', 'Age', 'BMI']   # Provide your features of interest

# set up data drift detector

alert_config = AlertConfiguration(['rajdeepak.beniwal@tcs.com'])  # to get alert over e-mail

monitor = DataDriftDetector.create_from_datasets(ws, 'diabetes-drift-detector', baseline_data_set, target_data_set,
                                                      compute_target=cluster_name, 
                                                      frequency='Week', 
                                                      feature_list=features, 
                                                      drift_threshold=.3, 
                                                      latency=24,alert_config=alert_config)

# -----------------------------------------------------
#Backfill the Monitor
# -----------------------------------------------------

from azureml.widgets import RunDetails

backfill = monitor.backfill( dt.datetime.now() - dt.timedelta(weeks=6), dt.datetime.now())    

RunDetails(backfill).show()
backfill.wait_for_completion()

# -----------------------------------------------------
#Analysing Backfill Metrics
# -----------------------------------------------------

drift_metrics = backfill.get_metrics()
for metric in drift_metrics:
    print(metric, drift_metrics[metric])







