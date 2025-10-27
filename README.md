# Agentic AI Cost Optimiser (Template)

End-to-end template for an Agent-driven Cloud Cost Optimiser built with **Python + Terraform + an LLM**.

## What it does (template)
- Pulls utilisation metrics for compute (stubbed for EC2).
- Uses an LLM + policy guardrails to propose **safe** right-sizing plans.
- Generates Terraform changes and opens a PR.
- Runs **plan in PR**, **apply on merge** with approvals & environment protections.
- Rolls out progressively and auto-rolls back if SLOs degrade.

> This is a **starter**. Wire it to your real metrics, CMDB/graph, and production Terraform state/workflows.

## Quick start

```bash
# 1) Python env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Configure env
cp .env.example .env
# fill in: AWS creds (if not using OIDC), LLM key, repo info, SLO thresholds, etc.

# 3) Dry run analysis
python agent/main.py --mode analyse --lookback-days 14 --min-util 0.15

# 4) Create a PR with a right-sizing plan (plan only; no apply)
python agent/main.py --mode propose --branch feature/rightsize-2025-10-27

# 5) After PR review & merge, GitHub Actions will run `terraform apply` with approval gates.
```

## Design
- **Data**: `agent/cloud_metrics.py` (stubs) → replace with real CloudWatch/Azure Monitor/Stackdriver readers.
- **Reasoning**: `agent/llm.py` + `agent/optimiser.py` → prompts, policy, and plan synthesis.
- **Guardrails**: `agent/guardrails.py` → freeze windows, error budgets, dependency checks (wire to your systems).
- **Actuation**: `agent/terraform_runner.py` → writes tfvars, runs terraform; opens PR via GitPython.
- **Infra**: Terraform module under `infra/modules/rightsize-ec2` updates instance types for provided IDs.

## Safety
- Plan-only on PRs.
- Apply requires merge + environment protection + manual approval.
- Progressive rollout & automatic rollback if health breaches SLOs.

## Notes
- The EC2 right-size module expects instances are importable to Terraform (see `examples/imports.sh`). Adapt for your infra (ASGs/Launch Templates, AKS/EKS nodes, DB tiers, etc.).
