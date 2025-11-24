
from ..models import debate, agent

class DebateService:
    def __init__(self):
        self.debates = {}
        self.next_debate_id = 1

    def create_debate(self, topic: str, participants: list[agent.Agent]) -> debate.Debate:
        """
        Creates a new debate.
        """
        new_debate = debate.Debate(id=self.next_debate_id, topic=topic, participants=participants)
        self.debates[self.next_debate_id] = new_debate
        self.next_debate_id += 1
        return new_debate

    def get_debate(self, debate_id: int) -> debate.Debate:
        """
        Gets a debate by its ID.
        """
        return self.debates.get(debate_id)

    def post_message(self, debate_id: int, agent_id: int, message: str):
        """
        Posts a message to a debate.
        """
        debate = self.get_debate(debate_id)
        if debate:
            # In a real system, we would verify that the agent is a participant.
            debate.messages.append(f"Agent {agent_id}: {message}")

    def get_messages(self, debate_id: int) -> list[str]:
        """
        Gets all the messages in a debate.
        """
        debate = self.get_debate(debate_id)
        if debate:
            return debate.messages
        return []
