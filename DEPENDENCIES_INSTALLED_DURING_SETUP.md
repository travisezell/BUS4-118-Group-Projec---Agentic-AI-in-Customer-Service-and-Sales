## Dependencies installed during this setup (local / Anaconda)

This file records the extra packages installed while fixing notebook execution issues and migrating off deprecated APIs.

### Environment observed

- **Notebook kernel Python**: `/opt/anaconda3/bin/python`

### Installed (via pip into `/opt/anaconda3`)

- **`langchain==1.2.13`**
  - Needed for `from langchain.agents import create_agent`
- **`langchain-openai==1.0.1`**
  - Provides `langchain_openai` (`ChatOpenAI`, embeddings)
- **`openai==2.30.0`**
  - Installed as a dependency of `langchain-openai`
- **`tiktoken==0.12.0`**
  - Installed as a dependency of `langchain-openai`
- **`jiter==0.13.0`**
  - Installed as a dependency of `openai`

### Recorded in repo files

- `requirements.txt`
  - Added `langchain==1.2.13`
  - Added `nbconvert>=7.0` (for exporting notebooks to HTML for screenshots)
- `llm_provider_setup.py`
  - Updated to raise a clearer error message when `provider="openai"` but `langchain-openai` is missing.

