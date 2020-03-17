"""
Service worker to run offline.
"""
import pandas as pd

# complete - @TODO(aaronhma, rohan): Step 1. Load service_worker.json
service_worker = pd.read_json('./service_worker.json') # load the json file

service_workerx = service_worker.loc[service_worker.short_name == f'atlas_stage2'] # select only stage2 data
print(service_workerx) # print filtered data
print("\n\n") # sep
print(service_worker.head()) # show all data
# todo - @TODO(aaronhma, rohan): Make stage 2 offline