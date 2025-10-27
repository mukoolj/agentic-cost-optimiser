from typing import List
from .llm import LLMClient, OptimisationCandidate
from .config import settings

class Optimiser:
    def __init__(self):
        self.llm = LLMClient()

    def propose_rightsizing(self, metrics_summary) -> List[OptimisationCandidate]:
        return self.llm.reason_about_rightsizing(metrics_summary)

    def batch(self, candidates: List[OptimisationCandidate]):
        """Break into rollout batches."""
        for i in range(0, len(candidates), settings.batch_size):
            yield candidates[i:i+settings.batch_size]
