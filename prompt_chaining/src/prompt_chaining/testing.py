# from crewai.flow.flow import Flow, start, listen
# from litellm import completion
# import os
# from dotenv import load_dotenv
# import networkx as nx
# import matplotlib.pyplot as plt

# load_dotenv()

# class TopicOutlineFlow(Flow):
#     model = "gemini/gemini-1.5-flash"
#     api_key = os.getenv("GEMINI_API_KEY")
#     execution_path = []  # Track the actual execution path

#     @start()
#     def llm_call_1(self):
#         self.execution_path = ['LLM Call 1']  # Start tracking
#         response = completion(
#             model=self.model,
#             api_key=self.api_key,
#             messages=[{
#                 "role": "user",
#                 "content": "Generate a creative blog topic for 2025."
#             }]
#         )
#         output_1 = response["choices"][0]["message"]["content"].strip()
#         print(f"LLM Call 1 Output: {output_1}")
#         return output_1

#     @listen(llm_call_1)
#     def gate_check(self, output_1):
#         self.execution_path.append('Gate')
#         words = output_1.split()
#         passed = len(words) < 10
        
#         if not passed:
#             print("Gate check failed. Exiting...")
#             self.execution_path.append('Exit')
#             return {"status": "fail", "data": output_1}
        
#         print("Gate check passed. Proceeding...")
#         return {"status": "pass", "data": output_1}

#     @listen(gate_check)
#     def llm_call_2(self, gate_result):
#         if gate_result["status"] == "fail":
#             return None
            
#         self.execution_path.append('LLM Call 2')
#         response = completion(
#             model=self.model,
#             api_key=self.api_key,
#             messages=[{
#                 "role": "user",
#                 "content": f"Based on '{gate_result['data']}', create a detailed outline."
#             }]
#         )
#         output_2 = response["choices"][0]["message"]["content"].strip()
#         print(f"LLM Call 2 Output: {output_2}")
#         return output_2

#     @listen(llm_call_2)
#     def llm_call_3(self, output_2):
#         if output_2 is None:
#             return None
            
#         self.execution_path.append('LLM Call 3')
#         response = completion(
#             model=self.model,
#             api_key=self.api_key,
#             messages=[{
#                 "role": "user",
#                 "content": f"Enhance and polish this outline: {output_2}"
#             }]
#         )
#         output_3 = response["choices"][0]["message"]["content"].strip()
#         print(f"LLM Call 3 Output: {output_3}")
        
#         self.execution_path.append('Out')
#         with open("outline.md", "w") as f:
#             f.write(output_3)
#         print("Final output saved to outline.md")
#         return output_3

#     def custom_plot(self):
#         G = nx.DiGraph()
        
#         # Add all possible nodes
#         nodes = ['In', 'LLM Call 1', 'Gate', 'LLM Call 2', 'LLM Call 3', 'Out', 'Exit']
#         G.add_nodes_from(nodes)
        
#         # Add edges based on actual execution path
#         path = ['In'] + self.execution_path
        
#         # Add edges between consecutive nodes in the path
#         for i in range(len(path) - 1):
#             G.add_edge(path[i], path[i + 1])
        
#         # Create the plot
#         plt.figure(figsize=(12, 6))
#         pos = nx.spring_layout(G)
        
#         # Draw nodes
#         nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)
#         nx.draw_networkx_labels(G, pos)
        
#         # Draw edges
#         nx.draw_networkx_edges(G, pos)
        
#         plt.title("Flow Execution Path")
#         plt.axis('off')
#         plt.savefig('flow_visualization.png')
#         plt.close()

# def main():
#     flow = TopicOutlineFlow()
#     final_output = flow.kickoff()
#     flow.custom_plot()  # Use our custom plotting instead of the default

# if __name__ == "__main__":
#     main()