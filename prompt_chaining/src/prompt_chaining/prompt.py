from crewai.flow.flow import Flow, start, listen
from litellm import completion
import os
from dotenv import load_dotenv
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

load_dotenv()

class TopicOutlineFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    api_key = os.getenv("GEMINI_API_KEY")
    execution_path = []  # Track the actual execution path

    @start()
    def llm_call_1(self):
        self.execution_path = ['LLM Call 1']  # Start tracking
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{
                "role": "user",
                "content": "Generate a creative blog topic for AI and the future."
            }]
        )
        output_1 = response["choices"][0]["message"]["content"].strip()
        print(f"LLM Call 1 Output: {output_1}")
        return output_1

    @listen(llm_call_1)
    def gate_check(self, output_1):
        self.execution_path.append('Gate')
        words = output_1.split()
        passed = len(words) > 10
        
        if not passed:
            print("Gate check failed. Exiting...")
            self.execution_path.append('Exit')
            return {"status": "fail", "data": output_1}
        
        print("Gate check passed. Proceeding...")
        return {"status": "pass", "data": output_1}

    @listen(gate_check)
    def llm_call_2(self, gate_result):
        if gate_result["status"] == "fail":
            return None
            
        self.execution_path.append('LLM Call 2')
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{
                "role": "user",
                "content": f"Based on '{gate_result['data']}', create a detailed outline."
            }]
        )
        output_2 = response["choices"][0]["message"]["content"].strip()
        print(f"LLM Call 2 Output: {output_2}")
        return output_2

    @listen(llm_call_2)
    def llm_call_3(self, output_2):
        if output_2 is None:
            return None
            
        self.execution_path.append('LLM Call 3')
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{
                "role": "user",
                "content": f"Enhance and polish this outline: {output_2}"
            }]
        )
        output_3 = response["choices"][0]["message"]["content"].strip()
        print(f"LLM Call 3 Output: {output_3}")
        
        self.execution_path.append('Out')
        with open("outline.md", "w") as f:
            f.write(output_3)
        print("Final output saved to outline.md")
        return output_3

    def custom_plot(self):
        # Create an interactive network
        net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")
        
        # Define node positions for both success and failure paths
        positions = {
            'In': {'x': -400, 'y': 0},
            'LLM Call 1': {'x': -200, 'y': 0},
            'Gate': {'x': 0, 'y': 0},
            'LLM Call 2': {'x': 200, 'y': 0},
            'LLM Call 3': {'x': 400, 'y': 0},
            'Out': {'x': 600, 'y': 0},
            'Exit': {'x': 200, 'y': 200}
        }
        
        # Add all nodes with fixed positions
        for node, pos in positions.items():
            if node in ['In'] + self.execution_path:
                net.add_node(node, x=pos['x'], y=pos['y'], physics=False)
        
        # Add edges based on actual execution path
        path = ['In'] + self.execution_path
        for i in range(len(path) - 1):
            net.add_edge(path[i], path[i + 1])
        
        # Customize the appearance
        net.set_options("""
        var options = {
            "nodes": {
                "shape": "box",
                "font": {
                    "size": 20
                }
            },
            "edges": {
                "arrows": {
                    "to": {
                        "enabled": true
                    }
                },
                "smooth": {
                    "type": "curvedCW",
                    "roundness": 0.2
                }
            },
            "physics": {
                "enabled": false
            }
        }
        """)
        
        # Save to HTML file
        net.save_graph("crewai_flow.html")
        
        # Also create a static matplotlib visualization
        G = nx.DiGraph()
        G.add_nodes_from(['In'] + self.execution_path)
        
        # Add edges between consecutive nodes in the path
        for i in range(len(path) - 1):
            G.add_edge(path[i], path[i + 1])
        
        # Create the plot with a larger figure size
        plt.figure(figsize=(12, 6))
        
        # Use the same positions for matplotlib
        pos = {node: [positions[node]['x']/100, positions[node]['y']/100] for node in G.nodes()}
        
        # Draw the graph
        nx.draw(G, pos,
                node_color='lightblue',
                node_size=3000,
                with_labels=True,
                font_size=10,
                font_weight='bold',
                arrows=True,
                edge_color='gray',
                arrowsize=20)
        
        plt.title("Flow Execution Path")
        plt.axis('off')
        plt.savefig('flow_visualization.png', bbox_inches='tight', dpi=300)
        plt.close()
        print("Flow visualization saved to flow_visualization.png")
        print("Flow visualization saved to crewai_flow.html")

def main():
    flow = TopicOutlineFlow()
    final_output = flow.kickoff()
    flow.custom_plot()  # Use our custom plotting instead of the default

if __name__ == "__main__":
    main()
