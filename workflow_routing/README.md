# Step-by-Step Explanation of the Routing-Based AI Workflow Using CrewAI & LiteLLM

This project is a practical implementation of Anthropic AI's Routing Design Pattern using CrewAI and LiteLLM. 
The workflow dynamically generates a blog topic and routes it to different processing paths based on its category (Tech, Business, or Lifestyle). Finally, it saves the generated content into different files. 
Let's break down the code step by step.

## 1. Importing Required Libraries

          from crewai.flow.flow import Flow, start, listen, router
          from litellm import completion

* **CrewAI:** This is a library for defining AI-driven workflows.

  * Flow: The base class for defining a workflow.

  * start: A decorator that marks the starting function of the workflow.

  * listen: A decorator that listens for specific events to trigger functions.

  * router: A decorator used to route the flow to different functions based on conditions.

* **LiteLLM:** This library provides a unified API for multiple LLMs, including Gemini, OpenAI, and others.

   * completion: A function that sends a prompt to an LLM and retrieves a response.


  ## 2. Defining the AI Workflow Class
  
        class RoutedFlow(Flow):
          model = "gemini/gemini-1.5-flash"

* RoutedFlow extends Flow, meaning it follows CrewAI's workflow structure.

* The model is set to "gemini/gemini-1.5-flash", a high-speed model from Google's Gemini series.


## 3. Step 1: Generating a Blog Topic

          @start()
          def generate_topic(self):
              response = completion(
                  model=self.model,
                  messages=[{"role": "user", "content": "Generate a blog topic for 2025."}]
              )
              topic = response["choices"][0]["message"]["content"].strip()


* The first function in the flow is generate_topic(), marked with @start().

* It sends a request to Gemini to generate a blog topic for 2025.

* The response is extracted from response["choices"][0]["message"]["content"].


## 4. Step 2: Classifying the Topic
        
        self.state["is_tech"] = any(word in topic.lower() for word in ["tech", "technology", "software", "programming", "ai", "artificial intelligence", "machine learning", "data", "digital"])
        self.state["is_lifestyle"] = any(word in topic.lower() for word in ["lifestyle", "life", "living", "wellness", "health"])
        self.state["is_business"] = any(word in topic.lower() for word in ["business", "finance", "economy", "market"])

* The topic is checked for specific keywords to classify it into Tech, Lifestyle, or Business.

* Flags (is_tech, is_lifestyle, is_business) are stored in self.state, which is a persistent state storage in CrewAI.


## 5. Step 3: Routing Based on Category

          @router(generate_topic)
          def route_LLM(self):
              if self.state.get("is_tech"):
                  return "tech_route"
              elif self.state.get("is_business"):
                  return "business_route"
              else:
                  return "lifestyle_route"


* This function is decorated with @router(generate_topic), meaning it runs after generate_topic().

* Based on the topic classification, it routes the flow to one of three paths:

  * "tech_route" → Tech-related topics

  * "business_route" → Business-related topics

  * "lifestyle_route" → Lifestyle-related topics


## 6. Step 4: Generating Blog Outlines

Each route calls a specific function to generate a blog outline.

### Tech Blog Outline

        @listen("tech_route")
        def tech_LLM(self, topic):
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": f"Create a detailed tech blog outline for: {topic}"}]
            )
            outline = response["choices"][0]["message"]["content"].strip()
            print("Tech Outline:")
            print(outline)
            return outline

* If the topic is tech-related, this function listens for "tech_route".

* It generates a detailed tech blog outline using the LLM.                 

### Business Blog Outline
        
        @listen("business_route")
        def business_LLM(self, topic):
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": f"Create a detailed business blog outline for: {topic}"}]
            )

* Listens for "business_route" and generates a business blog outline.

 ### Lifestyle Blog Outline
 
         @listen("lifestyle_route")
        def lifestyle_LLM(self, topic):
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": f"Create a detailed lifestyle blog outline for: {topic}"}]
            )
            outline = response["choices"][0]["message"]["content"].strip()
            print("Lifestyle Outline:")
            print(outline)
            return outline

  * Listens for "lifestyle_route" and generates a lifestyle blog outline.


    ## 7. Step 5: Saving the Generated Outline

    Each blog outline is saved to a file based on its category.

    ### Saving Tech Outline

            @router(tech_LLM)
        def tech_save(self, outline):
            with open("tech_outline.md", "w") as f:
                f.write(outline)
            return "tech_outline_saved"

  * After tech_LLM() generates the outline, it is saved to tech_outline.md.

### Saving Business Outline

      @router(business_LLM)
      def business_save(self, outline):
          with open("business_outline.md", "w") as f:
              f.write(outline)
          return "business_outline_saved"
          
* Saves business content to business_outline.md.

 ### Saving Lifestyle Outline

       @router(lifestyle_LLM)
      def lifestyle_save(self, outline):
          with open("lifestyle_outline.md", "w") as f:
              f.write(outline)
          return "lifestyle_outline_saved"

    * Saves lifestyle content to lifestyle_outline.md.


 ## 8. Step 6: Running the Workflow
       
        def main():
            flow = RoutedFlow()
            final_output = flow.kickoff()
            print("Final Output:")
            print(final_output)
            flow.plot()

* kickoff() starts the AI workflow.

* The final output is printed.

* flow.plot() visualizes the flow structure


## 9. Executing the Code

      if __name__ == "__main__":
          main()
 * Runs the main() function when the script is executed.

## Final Summary
1. **Topic Generation** → LLM generates a blog topic.

2. **Routing** → Classifies the topic into Tech, Business, or Lifestyle.

3. **Content Generation** → LLM generates a detailed blog outline.

4. **Saving** → The outline is saved to a Markdown file.

5. **Execution** → The entire flow is run and visualized.

## Conclusion

This project showcases AI-driven routing in content generation workflows, dynamically adapting to input and automating decisions. 
It follows Anthropic’s Routing Design Pattern, allowing AI-powered workflows to become more intelligent and context-aware.

