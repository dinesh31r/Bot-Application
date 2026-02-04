import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import RAG components
from RAG.vector_store import knowledge_base
from RAG.llm_engine import llm_engine

app = FastAPI(title="JARVIS Backend")

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    query = request.query
    
    # 1. Retrieve Context from Vector DB
    context = knowledge_base.search(query)
    
    # 2. Generate Response using LLM
    if context:
        print(f"Context found: {context[:100]}...") # Debug log
    
    response_text = llm_engine.generate_response(query, context)
    
    return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
