# Parallelization WorkFlow

## Step-by-Step Explanation of the Code

This code is a Parallelization_or Workflow using CrewAI Flow and LiteLLM, designed to generate a creative blog topic using multiple AI models in parallel and selecting the first available result.

## 📌 Step 1: Import Required Libraries

        from crewai.flow.flow import Flow, start, listen, or_
        from litellm import completion
        import os
        from dotenv import load_dotenv
        
* CrewAI Flow (Flow, start, listen, or_) → Helps structure the workflow.

* LiteLLM (completion) → Allows calling different AI models.

* os & dotenv (load_dotenv()) → Used to load the API key securely from the .env file.

## 📌 Step 2: Load Environment Variables

        load_dotenv()

* Loads the .env file, which contains API keys (like GEMINI_API_KEY), so they are not hardcoded in the script.

## 📌 Step 3: Define the ParallelFlow Class

The ParallelFlow class inherits from Flow, which helps in defining an AI-driven process.

      class ParallelFlow(Flow):

* This class represents our workflow where different AI models work in parallel.

## 📌 Step 4: Define Class-Level Variables

        model = "gemini/gemini-1.5-flash"
        model2 = "gemini/gemini-2.0-flash-exp"
        api_key = os.getenv("GEMINI_API_KEY")

* model & model2 → These specify which AI models will generate the blog topic.
 
* api_key → Gets the API key from the environment variables (.env file).

## 📌 Step 5: Define LLM Calls (Parallel Execution)

These methods call different AI models simultaneously to generate a creative blog topic.

### 1️⃣ LLM Call 1

          @start()
          def llm_call_1(self):
              response = completion(
                  model=self.model2,  # Using model2 (Gemini 2.0)
                  api_key=self.api_key,
                  messages=[{"role": "user", "content": "Generate a creative blog topic."}]
              )
              result = response["choices"][0]["message"]["content"].strip()
              print(f"LLM Call 1 Result: {result}")
              return ("LLM 1", result)

* Sends a request to gemini-2.0 to generate a blog topic.

* Extracts the AI-generated content.

* Prints the result and returns ("LLM 1", result) (tuple containing model name & output).            

### 1️⃣ LLM Call 2

            @start()
            def llm_call_2(self):
                response = completion(
                    model=self.model,  # Using model (Gemini 1.5)
                    api_key=self.api_key,
                    messages=[{"role": "user", "content": "Generate a creative blog topic."}]
                )
                result = response["choices"][0]["message"]["content"].strip()
                print(f"LLM Call 2 Result: {result}")
                return ("LLM 2", result)

* Same as LLM Call 1, but uses gemini-1.5.


### 1️⃣ LLM Call 3

        @start()
        def llm_call_3(self):
            response = completion(
                model=self.model,  # Using the same Gemini 1.5 model
                api_key=self.api_key,
                messages=[{"role": "user", "content": "Generate a creative blog topic."}]
            )
            result = response["choices"][0]["message"]["content"].strip()
            print(f"LLM Call 3 Result: {result}")
            return ("LLM 3", result)

* **Same as LLM Call 2**

## 📌 Step 6: Aggregator (Selects First Available Result)

        @listen(or_(llm_call_1, llm_call_2, llm_call_3))
        def aggregator(self, result_tuple):
            llm_source, result = result_tuple
            print(f"Aggregator received first complete result from {llm_source}: {result}")
            return result_tuple

* or_(llm_call_1, llm_call_2, llm_call_3) → This means the aggregator function will listen for whichever LLM call finishes first.

* Takes the first available result, prints it, and returns the tuple (model_name, result).


  ## 📌 Step 7: Output Function (Final Processing)

        @listen(aggregator)
        def output(self, selected_tuple):
            if selected_tuple:
                llm_source, result = selected_tuple
                print("\nFinal Output Processing:")
                print(f"Using first complete result from: {llm_source}")
                return f"Final Processed Output:\n{result}"
            return None
* Receives the result from the aggregator function.

* Prints which AI model’s result was chosen.


## 📌 Step 8: Running the Flow

          def main():
            flow = ParallelFlow()  # Creates an instance of the flow
            final = flow.kickoff()  # Starts execution
            print("\nFlow Completed!")
            flow.plot()  # (Optional) Visualizes the flow
        
        if __name__ == "__main__":
            main()


* Creates a ParallelFlow instance.

* Runs the workflow using kickoff(), which executes all functions in the defined sequence.

* Prints "Flow Completed!" when done.

* flow.plot() (optional) → Generates a graphical representation of the workflow.


##   🔍 Summary of Execution Flow
1. Multiple AI models run in parallel (llm_call_1, llm_call_2, llm_call_3).

2. The first AI model to finish is selected (using or_() in the aggregator).

3. The chosen response is processed and printed (output function).



## 🎯 Real-World Analogy

💡 Imagine you are in a company where three writers are working on the same task.

   * Three writers (LLM calls) start writing a blog topic simultaneously.

   * The first writer to complete the task submits it.

   * The editor (aggregator) picks the first completed article and finalizes it.

   * The final blog post is published (output function).

## 📌 Why is this Code Useful?

✅ Faster Execution – Uses the first result available.

✅ Parallel Processing – Calls multiple models at the same time.

✅ Efficient Decision Making – Selects the best response dynamically.













   
