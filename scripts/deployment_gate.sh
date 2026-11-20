#!/usr/bin/env bash

# Stop deployment if the Ansible pre-check fails.
if ansible-playbook -i ansible/inventory.yml ansible/precheck.yml -k; then
    echo "PRE-CHECK PASSED: Deployment eligible"
else
    echo "PRE-CHECK FAILED: Deployment blocked"
    exit 1
fi

# No configuration deployment is performed yet.
echo "SAFETY GATE COMPLETE: No router changes made"
