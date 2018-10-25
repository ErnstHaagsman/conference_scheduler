#!/bin/bash

aws s3 cp "/var/backups/database/$1-latest" "s3://$2/$1-$(date -Iminutes)"
