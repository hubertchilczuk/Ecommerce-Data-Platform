#!/usr/bin/env bash
# Deploy infrastructure with Terraform.
set -euo pipefail

ENV="${1:-dev}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT/terraform"
terraform init -upgrade
terraform workspace select "$ENV" 2>/dev/null || terraform workspace new "$ENV"
terraform plan -var "env=$ENV" -out=tfplan
terraform apply -auto-approve tfplan
