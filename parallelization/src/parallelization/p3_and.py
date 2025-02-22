from crewai.flow.flow import Flow, start, listen, and_
from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()




class AndAggregationFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    model2 = "gemini/gemini-2.0-flash-exp"
    api_key = os.getenv("GEMINI_API_KEY")

    @start()
    def generate_slogan(self):
        # This task generates a creative slogan.
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{
                "role": "user",
                "content": "Generate a creative slogan for a futuristic brand."
            }]
        )
        slogan = response["choices"][0]["message"]["content"].strip()
        print("\033[92mSlogan generated:\033[0m", slogan)  # Parrot green
        return slogan

    @start()
    def generate_tagline(self):
        # This task generates a creative tagline.
        response = completion(
            model=self.model2,
            api_key=self.api_key,
            messages=[{
                "role": "user",
                "content": "Generate a creative tagline for a futuristic brand."
            }]
        )
        tagline = response["choices"][0]["message"]["content"].strip()
        print("\033[93mTagline generated:\033[0m", tagline)  # Bright yellow
        return tagline

    @listen(and_(generate_slogan, generate_tagline))
    def combine_outputs(self, outputs):
        # The `and_` decorator ensures this method is called only when both tasks complete.
        # Get the last output from each task since we might receive multiple outputs
        slogan = outputs[0][-1] if isinstance(outputs[0], (list, tuple)) else outputs[0]
        tagline = outputs[1][-1] if isinstance(outputs[1], (list, tuple)) else outputs[1]
        
        combined = f"Combined Output: Slogan - '{slogan}' | Tagline - '{tagline}'"
        print("\033[94mAggregated Combined Output:\033[0m", combined)  # Blue
        return combined

def main():
    flow = AndAggregationFlow()
    final_output = flow.kickoff()
    print("Final Output of the Flow:")
    print(final_output)
    flow.plot()

if __name__ == "__main__":
    main()
