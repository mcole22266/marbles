#!/bin/bash
# Creates backup of database

AWS_CONFIG_FILE="/root/.aws/credentials"

touch ./backup.sql
pg_dump -U mcole22266 marbles > ./backup.sql
aws s3 cp ./backup.sql s3://themarblerace-website/postgres-backups/backup_$(date +"%Y-%m-%d").sql
rm ./backup.sql