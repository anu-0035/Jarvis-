# main.py - FastAPI app that exposes /chat endpoint
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


from rag_pipeline import rag_answer, get_engine


load_dotenv()


app = FastAPI(title="Jarvis RAG API")


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


class Question(BaseModel):
    query: str


@app.on_event("startup")
async def startup_event():
# initialize the engine once on startup (builds or loads the vector DB)
    try:
        get_engine()
    except Exception as e:
        print("Warning: engine failed to initialize on startup:", e)


@app.get("/")
async def root():
    return {"message": "Jarvis RAG API is running"}


@app.post("/chat")
async def chat(q: Question):
    try:
        res = rag_answer(q.query)
        return {"response": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))