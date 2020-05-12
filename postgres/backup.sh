#!/bin/bash
# Creates backup of database

AWS_CONFIG_FILE="/root/.aws/credentials"

touch ./backup.bak
pg_dump -U mcole22266 marbles > ./backup.bak
aws s3 cp ./backup.bak s3://themarblerace-website/postgres-backups/backup_$(date +"%Y-%m_%d").bak
rm ./backup.bak