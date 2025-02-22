
from crewai.flow.flow import Flow, start, listen, router
from litellm import completion

class RoutedFlow(Flow):
    model = "gemini/gemini-1.5-flash"

    @start()
    def generate_topic(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a blog topic for 2025."}]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        # Add flags to the state for different topic categories
        self.state["is_tech"] = any(word in topic.lower() for word in ["tech", "technology", "software", "programming", "ai", "artificial intelligence", "machine learning", "data", "digital"])
        self.state["is_lifestyle"] = any(word in topic.lower() for word in ["lifestyle", "life", "living", "wellness", "health"])
        self.state["is_business"] = any(word in topic.lower() for word in ["business", "finance", "economy", "market"])
        print(f"Topic: {topic}")
        return topic

    @router(generate_topic)
    def route_LLM(self):
        # Route based on the is_tech flag.
        if self.state.get("is_tech"):
            return "tech_route"
        elif self.state.get("is_business"):
            return "business_route"
        else:
            return "lifestyle_route"

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
    
    @listen("business_route")
    def business_LLM(self, topic):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Create a detailed business blog outline for: {topic}"}]
        )

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
    
    @router(tech_LLM)
    def tech_save(self, outline):
        with open("tech_outline.md", "w") as f:
            f.write(outline)
        return "tech_outline_saved"
    
    @router(business_LLM)
    def business_save(self, outline):
        with open("business_outline.md", "w") as f:
            f.write(outline)
        return "business_outline_saved"
    

    @router(lifestyle_LLM)
    def lifestyle_save(self, outline):
        with open("lifestyle_outline.md", "w") as f:
            f.write(outline)
        return "lifestyle_outline_saved"
    
    
    
 
    
            
def main():
    flow = RoutedFlow()
    final_output = flow.kickoff()
    print("Final Output:")
    print(final_output)
    flow.plot()

if __name__ == "__main__":
    main()

