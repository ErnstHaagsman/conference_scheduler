#!/bin/bash

terraform apply ./terraform
ANSIBLE_CONFIG=./ansible.cfg ansible-playbook main.yml -e 'ansible_python_interpreter=/usr/bin/python3'
