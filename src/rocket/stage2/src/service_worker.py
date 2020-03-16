"""
Service worker to run offline.
"""
import pandas as pd

# @TODO(aaronhma, rohan): Step 1. Load service_worker.json
service_worker = pd.read_json('./service_worker.json')
# @TODO(aaronhma, rohan): Step 2. Make stage2 offline.
service_workerx = service_worker.loc[service_worker.short_name == f'atlas_stage2']
print(service_workerx)
print("\n\ns")
print(service_worker.head())