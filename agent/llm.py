from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from .config import settings

# Minimal pluggable LLM interface; extend to other providers if needed.
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

@dataclass
class OptimisationCandidate:
    resource_id: str
    current_type: str
    proposed_type: str
    avg_cpu: float
    avg_mem: float
    monthly_savings_estimate: float

class LLMClient:
    def __init__(self):
        provider = settings.llm_provider.lower()
        if provider == "openai" and OpenAI:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.llm_model
        else:
            self.client = None
            self.model = None

    def reason_about_rightsizing(self, metrics_summary: List[Dict[str, Any]]) -> List[OptimisationCandidate]:
        """
        Use an LLM to propose safe instance-type downgrades based on utilisation and constraints.
        For demo, we do a deterministic heuristic + LLM justification (optional).
        """
        # Deterministic heuristic (safe baseline)
        results: List[OptimisationCandidate] = []
        for m in metrics_summary:
            cpu, mem = m["avg_cpu"], m.get("avg_mem", 0.2)
            if cpu < 0.15 and mem < 0.5:  # example threshold
                # naive map: large -> medium, xlarge -> large, etc.
                mapping = {"nano":"nano","micro":"micro","small":"small","medium":"small","large":"medium",
                           "xlarge":"large","2xlarge":"xlarge","3xlarge":"2xlarge","4xlarge":"3xlarge"}
                current = m["instance_type"]
                base = current.split(".")[-1]
                fam = current.split(".")[0]
                new_size = mapping.get(base, base)
                proposed = f"{fam}.{new_size}"
                if proposed != current:
                    results.append(OptimisationCandidate(
                        resource_id=m["instance_id"],
                        current_type=current,
                        proposed_type=proposed,
                        avg_cpu=cpu,
                        avg_mem=mem,
                        monthly_savings_estimate= m.get("monthly_cost", 100.0) * 0.35 # dummy
                    ))
        # Optionally ask LLM to review or annotate (omitted to keep template key-free).
        return results
