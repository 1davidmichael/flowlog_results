"""FlowLog Upload
Usage:
  flowlog_upload.py --file=<file> --s3url=<s3_url>
  flowlog_upload.py -h | --help | --version


"""

import boto3
import json
import re
import tempfile


from docopt import docopt


flow_log = 'example.txt'
s3_url = 's3://dwolla-technical-exercise/problem1'
count = {}

regexp = re.compile(r's3:\/\/(.*)\/(.*)')
match = regexp.match(s3_url)
bucket = match.group(1)
key = match.group(2)
print('%s:%s' % (bucket, key))

with open(flow_log) as f:
    log_entries = f.readlines()

for log_entry in log_entries:
    # Filter out non-REJECT entries
    if "REJECT" in log_entry:
        fields = log_entry.split()
        source_ip = fields[3]

        # Add IP address if it isn't present, else increment by 1
        if source_ip not in count:
            count[source_ip] = 1
        else:
            count[source_ip] += 1

# Create temporary file for json data
json_file = tempfile.NamedTemporaryFile()

print(json_file.name)
with open('/tmp/output.json', 'w') as f:
    json.dump(count, f, sort_keys=True, indent=4)

# Upload file to s3
s3 = boto3.resource('s3')
#s3.Bucket(bucket).put_object(Key=key, Body=json_file.name)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='FlowLog Upload')
    print(arguments)
