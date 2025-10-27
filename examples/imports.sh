#!/usr/bin/env bash
set -euo pipefail

# Example of importing existing EC2 instances into the module state.
# Replace instance IDs and state addresses accordingly.
# Run from infra/modules/rightsize-ec2

terraform init

# For each target instance, import to the address:
# aws_instance.managed["<instance-id>"]
# e.g.:
# terraform import 'aws_instance.managed["i-0123456789abcdef0"]' i-0123456789abcdef0

echo "Edit this script with your instance IDs and run imports before planning."
