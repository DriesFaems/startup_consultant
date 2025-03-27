import streamlit as st
import asyncio
from agents import Agent, Runner
from openai import OpenAI

import os


st.title("Synthetic Startup Consultation Team")
st.write("Ask your question and our team of experts will help you!")


# API Key input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Question input
question = st.text_area("Enter your question:")

# set the api key

os.environ["OPENAI_API_KEY"] = api_key

if st.button("Get Expert Advice"):


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

    triage_result = Runner.run(triage_agent, question)

    response = triage_result.final_output
    
    st.expander(f"Response")
    st.write(response)

else:
    st.write("Please enter your OpenAI API Key and question to get expert advice.")