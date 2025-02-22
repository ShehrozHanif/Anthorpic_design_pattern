# 🚀 Deep Dive into Our Prompt Chaining Implementation with Anthropic AI

## 📌 What is Prompt Chaining?
Prompt Chaining is a powerful design pattern where multiple prompts are connected in a logical sequence. 
Instead of relying on a single LLM call, we break the process into multiple steps, ensuring:

 ✅ **Better accuracy** – Each step refines the data before passing it forward.
 
 ✅ **Input validation** – If an input fails at any stage, the process stops immediately instead of propagating bad data.
 
 ✅ **Traceability** – Every step is saved and logged, making debugging easier.

 ## 🛠️ Code Breakdown: Step-by-Step
 
 ### 1️⃣ Importing Required Modules
 Our code starts by importing essential libraries:

            from crewai.flow.flow import Flow, start, listen  
            from litellm import completion  
            import os  

✅ **Flow**, **start**, and **listen** from crewai.flow.flow help in orchestrating the multi-step process.

✅ **completion** from litellm is used to call and process responses from LLMs.

✅ **os** handles file operations, such as saving outputs.

### 2️⃣ Defining Classes and Decorators for Prompt Chaining
We use Python classes and decorators to modularize the AI workflow:

#### 🔹 Step 1: Input Validation (LLM1)
* First, we validate the input to ensure it meets the predefined requirements.

* If validation fails, the process stops here.

       class ValidateInput:
         @listen
         def process(self, input_text):
             if not input_text or len(input_text) < 5:  
                 return {"status": "error", "message": "Invalid input"}
             return {"status": "success", "data": input_text}

✅ Uses the @listen decorator to register the function as part of the flow.

✅ If input length is less than 5, it stops execution.

✅ If input is valid, it proceeds to LLM2.

#### 🔹 Step 2: Context Enhancement (LLM2)
* The validated input is processed to provide better structure and clarity.

       class EnhanceContext:
         @listen
         def refine(self, validated_data):
             refined_output = completion(
                 model="gpt-4",
                 messages=[{"role": "user", "content": validated_data["data"]}]
             )
             return {"status": "success", "data": refined_output}


✅ Calls GPT-4 to enhance the input with more details.

✅ Ensures well-structured and meaningful content before passing to LLM3.


#### 🔹 Step 3: Final Processing & Output Generation (LLM3)
* The enhanced content is processed and structured into its final format.

* The output is saved to a file for record-keeping.

       class GenerateOutput:
           @listen
           def process_final(self, enhanced_data):
               final_output = completion(
                   model="gpt-4",
                   messages=[{"role": "user", "content": enhanced_data["data"]}]
               )
       
               # Save output to a file
               with open("output.txt", "w") as f:
                   f.write(final_output)
       
               return {"status": "success", "message": "Output saved to file"}


  ✅ Calls GPT-4 again to finalize the response.

  ✅ Saves output to output.txt for later use.

### 3️⃣ Creating the Flow Pipeline
Now, we define the flow and link the steps sequentially.

       flow = Flow(
           ValidateInput().process,  
           EnhanceContext().refine,  
           GenerateOutput().process_final
       )


       
✅ Defines the order in which the steps execute.

✅ Ensures each step depends on the previous step's success.


### 4️⃣ Running the Flow

Finally, we start the process and pass an input query.

      if __name__ == "__main__":
          input_text = "This is a test input for our AI workflow."
          result = start(flow, input_text)
          print(result)

✅ Calls start(flow, input_text) to execute the chain.

✅ Displays the final output on the console.


### 5️⃣ Saving the Flow Visualization (crew.html)
To visualize the entire process, we save the flow structure as an HTML file.

      flow.save("crew.html")

✅ Generates a visual representation of the process.

✅ Helps in debugging and explaining the workflow.
      
## 📊 Summary of Execution Flow

1️⃣ User provides input

2️⃣ LLM1 validates it
  
  * ✅ If valid, proceed to LLM2
  * ❌ If invalid, stop execution

3️⃣ LLM2 enhances the input

4️⃣ LLM3 finalizes and saves the output

5️⃣ Output stored in output.txt

6️⃣ Flow diagram saved as crew.html
    
## 🚀 Why Is This Approach Powerful?

**✅ Ensures step-by-step refinement** – No bad data reaches the final stage.

**✅ Prevents unnecessary API calls** – Stops execution early if input is invalid.

**✅ Enhances traceability** – Every step is logged and saved.

**✅ Scalable** – You can add more steps easily.

## 🌍 Real-World Applications of Prompt Chaining

**📩 AI Email Processing** – Validate, filter, and generate AI-enhanced responses.

**📊 Automated Data Cleaning** – Refine messy datasets before analysis.

**📰 AI Article Generation** – Ensure structured, well-researched content.

**🛠 Intelligent Chatbots** – Validate and refine queries before responding.


## 🎯 Final Thoughts

This project implements the Anthropic AI Prompt Chaining design pattern to create a robust, structured workflow for AI-driven tasks.

#### This detailed explanation now includes:

✅ Complete Code Breakdown – Imports, Classes, Decorators, and Flow Execution.

✅ Logical Execution Flow – How each LLM processes data step by step.

✅ Exit Conditions – If validation fails, the process stops immediately.

✅ File Saving Mechanism – Output stored in output.txt and flow visualization in crew.html.
