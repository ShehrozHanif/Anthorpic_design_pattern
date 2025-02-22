from crewai.flow.flow import Flow, start, listen, or_
from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

class ParallelFlow(Flow):
    
    
    model = "gemini/gemini-1.5-flash"
    model2 = "gemini/gemini-2.0-flash-exp"
    api_key = os.getenv("GEMINI_API_KEY")


    @start()
    def llm_call_1(self):
        response = completion(
            model=self.model2,
            api_key=self.api_key,
            messages=[{"role": "user", "content": "Generate a creative blog topic."}]
        )
        result = response["choices"][0]["message"]["content"].strip()
        print(f"LLM Call 1 Result: {result}")
        return ("LLM 1", result)

    @start()
    def llm_call_2(self):
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{"role": "user", "content": "Generate a creative blog topic."}]
        )
        result = response["choices"][0]["message"]["content"].strip()
        print(f"LLM Call 2 Result: {result}")
        return ("LLM 2", result)

    @start()
    def llm_call_3(self):
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{"role": "user", "content": "Generate a creative blog topic."}]
        )
        result = response["choices"][0]["message"]["content"].strip()
        print(f"LLM Call 3 Result: {result}")
        return ("LLM 3", result)

    @listen(or_(llm_call_1, llm_call_2, llm_call_3))
    def aggregator(self, result_tuple):
        # Take the first result that arrives
        llm_source, result = result_tuple
        print(f"Aggregator received first complete result from {llm_source}: {result}")
        return result_tuple

    @listen(aggregator)
    def output(self, selected_tuple):
        if selected_tuple:
            llm_source, result = selected_tuple
            print("\nFinal Output Processing:")
            print(f"Using first complete result from: {llm_source}")
            return f"Final Processed Output:\n{result}"
        return None

def main():
    flow = ParallelFlow()
    final = flow.kickoff()
    print("\nFlow Completed!")
    flow.plot()

if __name__ == "__main__":
    main()
    
