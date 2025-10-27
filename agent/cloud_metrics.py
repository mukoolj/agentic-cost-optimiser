from typing import List, Dict, Any
import random
from .config import settings

def fetch_ec2_utilisation_stub(lookback_days: int) -> List[Dict[str, Any]]:
    """
    Stub: Replace with real CloudWatch calls. Returns a list of instance metrics.
    """
    # pretend we discovered these instances
    sample = []
    for i in range(1, 11):
        cpu = random.uniform(0.03, 0.7)
        mem = random.uniform(0.1, 0.8)
        itype = random.choice(["t3.large","m5.xlarge","m5.large","c6i.xlarge"])
        sample.append({
            "instance_id": f"i-0demo{i:03d}",
            "instance_type": itype,
            "avg_cpu": cpu,
            "avg_mem": mem,
            "monthly_cost": random.uniform(50, 300),
        })
    return sample
