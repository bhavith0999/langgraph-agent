from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage
from src.agent.graph import build_graph

app = build_graph()

print("Agent is ready to type")

while True:
    question = input("YOU: ").strip()
    if question.lower()=="quit":
        break
    if not question:
        continue
    print("Thinking...", flush=True)
    result = app.invoke({"messages": [HumanMessage(content=question)]},config={"configurable": {"thread_id": "main-thread"}})
    print(f"Agent: {result['messages'][-1].content}\n", flush=True)