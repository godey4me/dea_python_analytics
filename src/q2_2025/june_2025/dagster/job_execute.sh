#!/bin/bash

echo $DAGSTER_POSTGRES_URL

dagster job execute -f pipeline.py -c config.yaml