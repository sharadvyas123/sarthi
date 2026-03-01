from app.agent.graph import agent
from app.agent.state import SarthiState

initial_state = SarthiState(
    question="What is Karma Yoga?"
)

final_state = agent.invoke(initial_state)
print(final_state["answer"])
print(final_state)