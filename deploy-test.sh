#!/bin/bash

terraform apply ./terraform
ANSIBLE_CONFIG=./ansible.cfg ansible-playbook deploy-test.yml -e 'ansible_python_interpreter=/usr/bin/python3'
