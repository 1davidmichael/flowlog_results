from flowlog_results import flowlog_results
import json
import boto3
import unittest
from moto import mock_s3
class TestFlowlogUploadMethods(unittest.TestCase):

    def test_extract_s3_info(self):
        upload = flowlog_results('test_file.txt', 's3://test.example.com/test_key')
        bucket, key = upload.extract_s3_info()
        assert bucket  == 'test.example.com'
        assert key == 'test_key'


    def test_count_rejected_ips(self):
        upload = flowlog_results('test_file.txt', 's3://test.example.com/test_key')

        valid_results = {
            '91.230.47.38': 1
        }

        assert upload.count_rejected_ips() == valid_results


    @mock_s3
    def test_upload_to_s3(self):


        upload = flowlog_results('test_file.txt', 's3://test.example.com/test_key')
        bucket, key = upload.extract_s3_info()
        count = upload.count_rejected_ips()

        conn = boto3.resource('s3')
        conn.create_bucket(Bucket=bucket)

        upload.upload_to_s3()
        body = conn.Object(bucket, key).get()['Body'].read().decode("utf-8")
        print(body, count)
        assert body == json.dumps(count)


if __name__ == '__main__':
    unittest.main()
