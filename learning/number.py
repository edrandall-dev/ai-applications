from typing import TypedDict
from langgraph.graph import StateGraph, END

# 1. Define the state — this is the "briefcase" passed between nodes
class AppState(TypedDict):
    number: int

# 2. Define functions. These function will become nodes when we register them with the graph.
def add_two(state: AppState) -> AppState:
    return {"number": state["number"] + 2}
    
def times_ten(state: AppState) -> AppState:
    return {"number": state["number"] * 10}

# 3. Build the graph

# a. Create a graph builder, telling it what our state dictionary looks like
graph_builder = StateGraph(AppState)

# b. Register the functions with the graph — this is the moment they becomes nodes
graph_builder.add_node("add_two_first", add_two)
graph_builder.add_node("add_two_second", add_two)
graph_builder.add_node("times_ten", times_ten)

# c. Tell the graph which node to run first
graph_builder.set_entry_point("add_two_first")

#d.  Define the edges
graph_builder.add_edge("add_two_first", "times_ten")
graph_builder.add_edge("times_ten", "add_two_second")
graph_builder.add_edge("add_two_second", END)

# f. Finalise the graph — after this line it is ready to run
graph = graph_builder.compile()
#print(graph.get_graph().draw_ascii())

# 4. Run it
result1 = graph.invoke({"number": 5})
print(result1["number"])

# 5. Run it again
result2 = graph.invoke({"number": 4})
print(result2["number"])
