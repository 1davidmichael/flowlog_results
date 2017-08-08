Flowlog Results
===============

This is a simple script to upload an example flowlog to a precreated S3 bucket.

[![CircleCI](https://circleci.com/gh/1davidmichael/flowlog_results/tree/master.svg?style=svg)](https://circleci.com/gh/1davidmichael/flowlog_results/tree/master)

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
flowlog_results.py --file=flowlog.log --s3url=s3://dm-testbucket/results.json
```

TODO
----

* Add error handling
* [Verify s3 bucket and key](http://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html)
* Pre-create S3 bucket if IAM permissions allow and does not exist

Renaming Repo
-------------

Renaming a repo after setting up CircleCI breaks integration. See [here](https://discuss.circleci.com/t/build-not-triggered-after-github-repo-was-renamed/10774/3) for more details.
