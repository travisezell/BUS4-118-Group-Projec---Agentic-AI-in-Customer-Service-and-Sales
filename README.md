# BUS4-118 Group Project: Agentic AI in Customer Service and Sales

## Overview
A multi-agent AI chatbot built with LangChain, LangGraph, and Google Gemini that simulates a customer service assistant. The system routes user inquiries to specialized agents based on the type of question.

## Agents
- **Product Q&A Agent** (`code_03`) — Answers questions about product features and pricing using a vector store and pricing tool
- **Orders Agent** (`code_04`) — Handles order lookups and quantity updates
- **Router Agent** (`code_06`) — Receives all user input and routes it to the correct specialist agent

## Setup Instructions

### 1. Open in GitHub Codespaces (recommended)
1. Click the green **Code** button at the top of this repo
2. Click the **Codespaces** tab
3. Click **Create codespace on main**
4. Wait ~1 minute for the environment to load
5. You're ready — no installs or API keys needed (already configured)

### 2. Add your Google API key
- Go to [Google AI Studio](https://aistudio.google.com/app/apikeys) and create a free API key
- In GitHub, go to **Settings → Codespaces → Secrets** and add a secret named `GOOGLE_API_KEY`
- Make sure to give it access to this repository

## Running the Notebooks
Open each notebook and click **Run All**. Run them in order:
1. `code_03_XX Product QnA Agentic chatbot.ipynb`
2. `code_04_XX Orders Chatbot with custom agent.ipynb`
3. `code_06_XX Multi-agent chatbots with routing.ipynb`

## Project Structure
