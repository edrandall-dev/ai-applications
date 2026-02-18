from typing import TypedDict
from langgraph.graph import StateGraph, END


# 1. Define the state — this is the "briefcase" passed between nodes
class AppState(TypedDict):
    message1: str
    message2: str

# 2. Define a function. This function will become a node when we register it with the graph.
def say_hello(state: AppState) -> AppState:
    return {"message1": "Hello, World!"}

def say_bye(state: AppState) -> AppState:
    return {"message2": "Goodbye, World!"}

# 3. Build the graph

# a. Create a graph builder, telling it what our state dictionary looks like
graph_builder = StateGraph(AppState)

# b. Register say_hello with the graph — this is the moment it becomes a node
graph_builder.add_node("say_hello", say_hello)
graph_builder.add_node("say_bye", say_bye)



# c. Tell the graph which node to run first
graph_builder.set_entry_point("say_hello")

# d. Tell the graphy to run say_bye after say_hello
graph_builder.add_edge("say_hello", "say_bye")

# e. Tell the graph that after say_bye runs, execution should stop
graph_builder.add_edge("say_bye", END)

# f. Finalise the graph — after this line it is ready to run
graph = graph_builder.compile()


# 4. Run it
result = graph.invoke({"message1": "", "message2": ""})
print(result["message1"])
print(result["message2"])