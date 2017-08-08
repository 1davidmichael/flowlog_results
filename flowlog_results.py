#!/usr/bin/env python3
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


class flowlog_results(object):

    def __init__(self, flowlog_file, s3_url):
        self.flowlog_file = flowlog_file
        self.s3_url = s3_url

    def extract_s3_info(self):
        # This regex is not complete and could accept incorrect values
        regexp = re.compile(r's3:\/\/(.*)\/(.*)')
        match = regexp.match(self.s3_url)
        self.bucket = match.group(1)
        self.key = match.group(2)
        return(self.bucket, self.key)

    def upload_to_s3(self):
        # Upload file to s3
        s3 = boto3.client('s3')
        try:
            s3.put_object(
                Bucket=self.bucket,
                Key=self.key,
                Body=json.dumps(self.count)
            )
            return(True)
        except:
            print('Upload to S3 failed!')

    def count_rejected_ips(self):
        # Create empty dict
        count = {}

        # Iterate over log entries
        with open(self.flowlog_file) as f:
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

        self.count = count
        return(self.count)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='FlowLog Upload')

    flowlog_file = arguments['--file']
    s3_url = arguments['--s3url']

    upload = flowlog_results(flowlog_file, s3_url)

    upload.extract_s3_info()
    upload.count_rejected_ips()
    if upload.upload_to_s3():
        print("S3 PUT Successful!")
    print(upload.s3_url)
