"""FlowLog Upload
Usage:
  flowlog_upload.py --file=<file> --s3url=<s3_url>
  flowlog_upload.py -h | --help 


"""

import boto3
import json
import os
import re
import tempfile

from docopt import docopt
from moto import mock_s3


def extract_s3_info(s3_url):
    # This regex is not complete and could accept incorrect values
    regexp = re.compile(r's3:\/\/(.*)\/(.*)')
    match = regexp.match(s3_url)
    bucket = match.group(1)
    key = match.group(2)
    return(bucket, key)


def upload_to_s3(bucket, key, ip_data):
    # Upload file to s3
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(ip_data))

    return()


def count_rejected_ips(flow_log):
    # Create empty dict
    count = {}

    # Iterate over log entries
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

    return(count)


def test_extract_s3_info():
    bucket, key = extract_s3_info('s3://test.example.com/test_key')
    assert bucket == 'test.example.com'
    assert key == 'test_key'


def test_count_rejected_ips():
    flow_log = (
        '2 765419780228 eni-c7efca9b 91.230.47.38 172.31.7.225 51363 5332 6 1 40 1501906710 1501906742 REJECT OK'
        '2 765419780228 eni-c7efca9b 45.33.48.4 172.31.7.225 123 123 17 3 228 1501907170 1501907342 ACCEPT OK'
    )

    valid_results = {
        '91.230.47.38': 1
    }

    assert count_rejected_ips(flow_log) == valud_results


@mock_s3
def test_upload_to_s3():
    bucket = 'test'
    key = 'test'
    ip_data = {
        '192.168.1.1': 1
    }

    conn = boto3.resource('s3')
    conn.create_bucket(Bucket=bucket)
    upload_to_s3(bucket, key, ip_data)

    body = conn.Object(bucket, key).get()['Body'].read().decode("utf-8")
    assert body == ip_data.json()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='FlowLog Upload')

    flowlog_file = arguments['--file']
    s3_url = arguments['--s3url']

    rejected_entries = count_rejected_ips(flowlog_file)
    print(rejected_entries)

    bucket, key = extract_s3_info(s3_url)
    upload_to_s3(bucket, key, rejected_entries)
