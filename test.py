import boto3

flow_log = 'example.txt'

with open(flow_log) as f:
    log_entries = f.readlines()

for log_entry in log_entries:
    if "REJECT" in log_entry:
        fields = log_entry.split()
        print(fields)

