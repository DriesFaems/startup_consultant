import streamlit as st
import asyncio
from agents import Agent, Runner
from openai import OpenAI

import os


# get OpenAI api key by reading the first line of the text file Open AI coding.txt with encoding utf-8

with open(r'C:\Users\dries.faems\Biografie\Open AI coding.txt', 'r', encoding = 'utf-8') as file:
    api_key = str(file.readline())[1:-1]

# set the api key

os.environ["OPENAI_API_KEY"] = api_key

# Define our specialized agents
technical_expert = Agent(
    name="Technical Expert",
    instructions="You are a technical expert specializing in technology, engineering, and scientific matters. Provide detailed technical analysis and solutions.",
    handoff_description="Specialist for technical and engineering questions"
)

legal_expert = Agent(
    name="Legal Expert",
    instructions="You are a legal expert specializing in law, regulations, and compliance. Provide legal analysis and guidance.",
    handoff_description="Specialist for legal and regulatory questions"
)

commercial_expert = Agent(
    name="Commercial Expert",
    instructions="You are a commercial expert specializing in business, marketing, and sales. Provide business insights and recommendations.",
    handoff_description="Specialist for business and commercial questions"
)

hr_expert = Agent(
    name="HR Expert",
    instructions="You are an HR expert specializing in human resources, employee relations, and workplace matters. Provide HR guidance and best practices.",
    handoff_description="Specialist for HR and workplace questions"
)

# Define the triage agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are a triage agent responsible for determining which specialized agents should handle the user's question.
    Analyze the question and determine which experts should be involved. You can select multiple experts if needed.
    Respond with a JSON containing the names of the experts who should handle the question and a brief explanation of why.""",
    handoffs=[technical_expert, legal_expert, commercial_expert, hr_expert]
)

async def process_question(api_key: str, question: str):
    # First, let the triage agent determine which experts should handle the question
    triage_result = await Runner.run(triage_agent, question, {"api_key": api_key})
    
    # Parse the triage result to determine which experts to use
    selected_experts = []
    if "technical" in triage_result.answer.lower():
        selected_experts.append(technical_expert)
    if "legal" in triage_result.answer.lower():
        selected_experts.append(legal_expert)
    if "commercial" in triage_result.answer.lower():
        selected_experts.append(commercial_expert)
    if "hr" in triage_result.answer.lower():
        selected_experts.append(hr_expert)
    
    # Get responses from all selected experts
    expert_responses = []
    for expert in selected_experts:
        response = await Runner.run(expert, question, {"api_key": api_key})
        expert_responses.append({
            "expert": expert.name,
            "response": response.answer
        })
    
    return expert_responses

def main():
    st.title("Synthetic Startup Consultation Team")
    st.write("Ask your question and our team of experts will help you!")

    # API Key input
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    
    # Question input
    question = st.text_area("Enter your question:")
    
    if st.button("Get Expert Advice"):
        if not api_key:
            st.error("Please enter your OpenAI API Key")
            return
        if not question:
            st.error("Please enter your question")
            return
            
        with st.spinner("Consulting our team of experts..."):
            # Run the async function
            responses = asyncio.run(process_question(api_key, question))
            
            # Display responses
            for response in responses:
                with st.expander(f"Response from {response['expert']}"):
                    st.write(response['response'])

if __name__ == "__main__":
    main() 