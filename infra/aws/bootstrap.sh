#!/usr/bin/env bash
# One-time setup for the AWS Terraform state backend. Run once, locally, with
# your AWS credentials already configured (aws sso login / aws configure).
# Not part of any CI pipeline - this bucket must exist before `terraform init`
# in infra/aws or infra/aws/oidc can succeed.
set -euo pipefail

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET="mortcal-tfstate-${ACCOUNT_ID}"
REGION="us-east-1"

aws s3api create-bucket \
  --bucket "$BUCKET" \
  --region "$REGION"

aws s3api put-bucket-versioning \
  --bucket "$BUCKET" \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-encryption \
  --bucket "$BUCKET" \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

aws s3api put-public-access-block \
  --bucket "$BUCKET" \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

echo "Terraform state bucket ready: $BUCKET"
