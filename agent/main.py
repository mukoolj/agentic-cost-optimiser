import argparse, datetime as dt, pathlib, sys
from .config import settings
from .cloud_metrics import fetch_ec2_utilisation_stub
from .optimiser import Optimiser
from .guardrails import in_freeze_window, passes_slo_checks, validate_batch, should_rollback
from .terraform_runner import write_tfvars, create_branch_and_commit, terraform_plan, INFRA_DIR

def analyse(args):
    metrics = fetch_ec2_utilisation_stub(lookback_days=args.lookback_days or settings.lookback_days)
    print(f"Discovered {len(metrics)} instances")
    low = [m for m in metrics if m["avg_cpu"] < args.min_util or m["avg_cpu"] < settings.min_util]
    print(f"Candidates (low util): {len(low)}")
    for m in low[:10]:
        print(m)

def propose(args):
    now = dt.datetime.utcnow()
    if in_freeze_window(now):
        print("Currently in freeze window. Exiting.")
        sys.exit(1)
    if not passes_slo_checks():
        print("Baseline SLOs are not green. Exiting.")
        sys.exit(1)

    metrics = fetch_ec2_utilisation_stub(lookback_days=settings.lookback_days)
    opt = Optimiser()
    candidates = opt.propose_rightsizing(metrics)
    if not candidates:
        print("No safe candidates found.")
        return
    print(f"Proposed {len(candidates)} candidates")

    # Progressive rollout in batches
    branch = args.branch or f"feature/rightsize-{now.date()}"
    batch_id = 0
    for batch in opt.batch(candidates):
        batch_id += 1
        if not validate_batch(batch):
            print(f"Batch {batch_id} failed guardrails. Skipping.")
            continue
        # Write tfvars for this batch
        write_tfvars(batch, INFRA_DIR)
        # Plan locally (optional); CI will also plan in PR
        out = terraform_plan(INFRA_DIR)
        print(out[:5000])
        # Create a PR branch
        create_branch_and_commit(branch=f"{branch}-b{batch_id}", message=f"Rightsize batch {batch_id} via agent")

    print("Batches proposed. Review PRs and merge to apply via CI.")

def main():
    p = argparse.ArgumentParser(description="Agentic Cost Optimiser")
    p.add_argument("--mode", choices=["analyse","propose"], required=True)
    p.add_argument("--lookback-days", type=int)
    p.add_argument("--min-util", type=float)
    p.add_argument("--branch", type=str)
    args = p.parse_args()

    if args.mode == "analyse":
        analyse(args)
    elif args.mode == "propose":
        propose(args)

if __name__ == "__main__":
    main()
