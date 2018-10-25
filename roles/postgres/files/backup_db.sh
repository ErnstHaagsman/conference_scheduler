#!/bin/bash

pg_dump "$1" --format=custom -f "/var/backups/database/$1-latest"
aws s3 cp "/var/backups/database/$1-latest" "s3://$2/$1-$(date -Iminutes)"
