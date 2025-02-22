
from crewai.flow.flow import Flow, start, listen, or_
from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

class ParallelFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    api_key = os.getenv("GEMINI_API_KEY")

    @start()
    def llm_1(self):
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{"role": "user", "content": "Generate a creative blog topic variant #1."}]
        )
        variant = response["choices"][0]["message"]["content"].strip()
        print(f"Variant 1: {variant}")
        return variant

    @start()
    def llm_2(self):
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{"role": "user", "content": "Generate a creative blog topic variant #2."}]
        )
        variant = response["choices"][0]["message"]["content"].strip()
        print(f"Variant 2: {variant}")
        return variant
    
    @start()
    def llm_3(self):
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{"role": "user", "content": "Generate a creative blog topic variant #3."}]
        )
        variant = response["choices"][0]["message"]["content"].strip()
        print(f"Variant 3: {variant}")
        return variant

    @listen(or_(llm_1, llm_2))
    def aggregate_variants(self, variant):
        # For simplicity, print the first variant received.
        print("Aggregated Variant:")
        print(variant)
        return variant

def main():
    flow = ParallelFlow()
    final = flow.kickoff()
    print("Final Aggregated Output:")
    print(final)
    flow.plot()

if __name__ == "__main__":
    main()
