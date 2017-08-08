Flowlog Upload
==============

This is a simple script to upload an example flowlog to a precreated S3 bucket.

[![CircleCI](https://circleci.com/gh/1davidmichael/flowlog_upload/tree/master.svg?style=svg)](https://circleci.com/gh/1davidmichael/flowlog_upload/tree/master)

Requirements
------------

* python 3
* virtualenv
* Pre-created S3 bucket
* AWS access and secret key with permission to write S3 object

Running
-------

Create virtualenv
```
make venv
```

Install dependencies
```
make reqs
```

Test
```
make test
```

Run
```
flowlog_results.py --file=flowlog.log--s3url=s3://dm-testbucket/results.json
```
