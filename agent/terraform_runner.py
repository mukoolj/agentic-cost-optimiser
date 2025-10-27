import subprocess, json, pathlib, os, shutil
from typing import List
from dataclasses import asdict
from git import Repo
from .config import settings
from .llm import OptimisationCandidate

INFRA_DIR = pathlib.Path("infra/modules/rightsize-ec2")

def write_tfvars(candidates: List[OptimisationCandidate], path: pathlib.Path):
    desired = {c.resource_id: c.proposed_type for c in candidates}
    out = {
        "desired_instance_types": desired
    }
    (path / "desired.auto.tfvars.json").write_text(json.dumps(out, indent=2))

def ensure_repo_identity(repo: Repo):
    with repo.config_writer() as cw:
        cw.set_value("user", "name", settings.git_user_name)
        cw.set_value("user", "email", settings.git_user_email)

def run_cmd(cmd: list, cwd: pathlib.Path):
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.stdout

def create_branch_and_commit(branch: str, message: str):
    repo = Repo(".")
    ensure_repo_identity(repo)
    git = repo.git
    git.checkout(settings.git_main_branch)
    git.pull(settings.git_remote, settings.git_main_branch)
    try:
        git.checkout("-b", branch)
    except Exception:
        git.checkout(branch)
    repo.index.add([str(p) for p in INFRA_DIR.rglob("*")])
    repo.index.commit(message)
    git.push(settings.git_remote, branch)

def terraform_plan(cwd: pathlib.Path):
    run_cmd(["terraform", "init", "-upgrade"], cwd)
    return run_cmd(["terraform", "plan"], cwd)

def terraform_apply(cwd: pathlib.Path):
    # Usually only in CI on protected envs.
    return run_cmd(["terraform", "apply", "-auto-approve"], cwd)
