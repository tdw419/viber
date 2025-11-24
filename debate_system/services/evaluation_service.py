
from ..models import debate

class EvaluationService:
    def evaluate_debate(self, debate: debate.Debate) -> float:
        """
        Evaluates a debate and returns a score.
        This is a placeholder for the actual evaluation logic.
        """
        # For now, we'll just return a dummy score based on the number of messages.
        return len(debate.messages) * 0.1
