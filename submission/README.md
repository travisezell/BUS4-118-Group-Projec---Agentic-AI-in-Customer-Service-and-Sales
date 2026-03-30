# Submission Materials – Customer Service Chatbot Project

This folder contains all materials submitted for the BUS4-118 Group Project.

## Contents

- **`chatbot_presentation(1).html`** – 3-slide HTML presentation explaining:
  - How the chatbot works (architecture, agents, routing)
  - Example multi-turn conversation
  - Memory and state handling (LangGraph MemorySaver)
  
  *Open this file in a browser to view the interactive slide deck. The slides require minor scrolling.*

- **`code_03_XX Product QnA Agentic chatbot (1).pdf`** – Notebook output showing the Product Q&A agent with tools (`getproductprice`, `GetProductFeatures`) answering golf product questions.

- **`code_04_XX Orders Chatbot with custom agent (1).pdf`** – Notebook output showing the Orders and Refund agents with custom tools (`getorderdetails`, `updateorderstatus`, `getrefundpolicy`).

- **`code_06_XX Multi-agent chatbots with routing.pdf`** – Notebook output showing the LangGraph RouterAgent and AgenticSupervisor orchestrating multi-agent conversations (PRODUCT / ORDER / REFUND / SMALLTALK).

## How to Run the Code

All code is in the root of this repository on the `ollama-defaults` branch. See the main [README](../README.md) for setup instructions using Ollama (recommended to avoid API costs).

## Notes

This project was developed and tested locally using Ollama (`llama3.1:8b`) to avoid the high token costs associated with cloud LLM APIs given the multi-agent, multi-turn nature of the chatbot.
