# Jarvis RAG - FastAPI + LangChain + Chroma + Simple Frontend


Small demo project showing Retrieval-Augmented Generation using LangChain.


## Features
- FastAPI backend exposing `/chat` endpoint
- LangChain RAG pipeline using OpenAI embeddings + ChatOpenAI for answer generation
- Chroma vectorstore persisted locally
- Simple HTML/CSS frontend to ask questions


## Setup (local)


1. Clone repository (or copy files into a folder)


2. Create a Python virtual environment and install dependencies


```bash
cd backend
python -m venv venv
source venv/bin/activate # mac/linux
venv\Scripts\activate # windows
pip install -r requirements.txt







Great — here is your **complete README** with steps 1–7 formatted cleanly and professionally. You can copy-paste directly into your `README.md`:

---

````md
# Jarvis RAG - FastAPI + LangChain + Chroma + Simple Frontend

Small demo project showing Retrieval-Augmented Generation (RAG) using LangChain, FastAPI, Chroma, and OpenAI.

---

## 🚀 Features
- FastAPI backend exposing `/chat` endpoint
- LangChain RAG pipeline using **OpenAI Embeddings + ChatOpenAI**
- **ChromaDB** vector store with local persistence
- Simple **HTML/CSS frontend** for querying your documents
- Supports **PDF / TXT knowledge files**

---

## 🛠️ Setup (Local)

### **1. Clone the repository**
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
````

### **2. Create a Python virtual environment and install dependencies**

```bash
cd backend
python -m venv venv
source venv/bin/activate   # mac/linux
venv\Scripts\activate      # windows
pip install -r requirements.txt
```

### **3. Create `.env`**

Inside the `backend/` folder, create a `.env` file based on `.env.example` and add:

```env
OPENAI_API_KEY=your_api_key_here
```

### **4. Add your documents**

Place your PDF or TXT files inside the `data/` folder at the repo root, e.g.:

```
./data/mydoc.pdf
```

### **5. Run the backend**

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

### **6. First run will build the vector store**

When the API runs for the first time, it will:

* Load files from `./data`
* Split and embed the text
* Store embeddings in **ChromaDB**
* Persist it to `CHROMA_PERSIST_DIR`

This avoids rebuilding on every startup.

### **7. Open the frontend**

Open:

```
frontend/index.html
```

(or serve it with any static server)

The frontend will POST requests to:

```
http://127.0.0.1:8000/chat
```

---

## 📌 Tech Stack

* **Backend:** FastAPI, LangChain, OpenAI, ChromaDB
* **Frontend:** HTML, CSS, JavaScript
* **Language:** Python 3.10+

---

## ✅ RAG Flow

```
User Question → Retriever → ChromaDB → LangChain → OpenAI → Final Answer
```

---

## 📮 API Endpoint

| Method | Endpoint | Description                    |
| ------ | -------- | ------------------------------ |
| POST   | `/chat`  | Ask a question to your RAG bot |

---

If you want, I can also add:

✅ Screenshots section
✅ Demo GIF
✅ Folder structure
✅ Future enhancements

Would you like me to add these too?



User Question → Retriever → ChromaDB → LangChain → OpenAI → Final Answer


