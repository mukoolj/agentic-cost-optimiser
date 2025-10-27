terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# This module expects that target EC2 instances are already imported into the state
# using resource names derived from instance IDs (see examples/imports.sh).
# The module then updates instance types safely.
#
# For truly production-grade flows, prefer Launch Templates + ASGs and roll nodes,
# or use SSM Automation for in-place stop/modify/start with health checks.

locals {
  ids = keys(var.desired_instance_types)
}

# Represent each managed instance as a separate resource by ID label
resource "aws_instance" "managed" {
  for_each               = var.desired_instance_types
  ami                    = "ami-placeholder"      # ignored after import
  instance_type          = each.value
  subnet_id              = "subnet-placeholder"   # ignored after import
  vpc_security_group_ids = ["sg-placeholder"]     # ignored after import
  tags = {
    ManagedBy = "AgenticCostOptimiser"
  }
  # IMPORTANT: All attributes except instance_type are placeholders post-import.
  # Terraform will only update instance_type on change.
  lifecycle {
    ignore_changes = [
      ami,
      subnet_id,
      vpc_security_group_ids,
      tags,
      # ignore other fields; we only want to drift on type
    ]
  }
}
