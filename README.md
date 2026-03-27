# ⚖️ Nyay Saar — Making Court Orders Understandable

> Ever tried reading a court order and felt completely lost? You're not alone. Nyay Saar fixes that.

---

## 📑 Table of Contents

- [What Is This?](#-what-is-this-for-everyone)
- [The Problem](#-the-problem)
- [How It Solves It](#-how-nyay-saar-solves-it)
- [RAG Pipeline](#-how-the-ai-works--rag-pipeline)
- [Personas](#-persona-based-responses)
- [Tech Stack](#-tech-stack-deep-dive)
- [Folder Structure](#-folder-structure)
- [Installation & Setup](#-installation--setup)
- [Quick Test](#-quick-test)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🤔 What Is This? (For Everyone)

**Nyay Saar** (meaning _"Essence of Justice"_ in Hindi) is a web application that takes complex, jargon-heavy court orders and turns them into plain English summaries that anyone can understand.

Think of it like this: Imagine you receive a 40-page court document full of legal terms you've never heard of. Instead of hiring a lawyer just to _understand_ what it says, you upload it to Nyay Saar — and within seconds, you get a clear, simple summary of what the order means, what actions are required, and who it affects.

You can also **chat with the document** — ask questions like _"What are my deadlines?"_ or _"What does Section 3 mean?"_ and get human-like answers instantly.

---

## 🚨 The Problem

Court orders are written for lawyers, not people. They're filled with Latin phrases, legal citations, and dense paragraphs that make it nearly impossible for a common person to understand their own legal situation without paying for professional help.

This creates a huge gap in access to justice — especially for people who can't afford legal consultations just to _read_ a document.

---

## 💡 How Nyay Saar Solves It

| Feature                        | What It Does                                                                 |
| ------------------------------ | ---------------------------------------------------------------------------- |
| 📄 **Upload PDFs**             | Upload any court order document directly                                     |
| 🧠 **AI Summarization**        | Automatically generates a clear, structured summary                          |
| 💬 **Chat with Document**      | Ask questions about the document in plain language                           |
| 🎭 **Persona-Based Responses** | Get explanations tailored to your background (student, business owner, etc.) |
| 👁️ **Document Viewer**         | Read the original document alongside its explanation                         |

---

## 🧠 How the AI Works — RAG Pipeline

Nyay Saar uses a technique called **RAG (Retrieval-Augmented Generation)**. In simple terms: instead of the AI trying to "remember" everything, it first _finds_ the relevant parts of your document and then _generates_ an answer based only on those parts. This makes answers accurate and grounded in your actual document.

Here's the full flow, step by step:

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER UPLOADS PDF                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TEXT EXTRACTION                            │
│           PDF is parsed and raw text is extracted               │
│                    [ PyMuPDF / pdfplumber ]                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       TEXT CHUNKING                             │
│     Long text is split into smaller overlapping chunks          │
│       (e.g. 500 tokens each with 50 token overlap)              │
│                    [ LangChain TextSplitter ]                   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  EMBEDDING GENERATION                           │
│   Each chunk is converted into a vector (a list of numbers      │
│   that captures the meaning of the text)                        │
│                  [ HuggingFace Embeddings ]                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PINECONE VECTOR DB                           │
│        All vectors are stored in Pinecone for fast              │
│        similarity search later                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
   ┌──────────────────────┐        ┌────────────────────────┐
   │    AUTO SUMMARY      │        │    USER ASKS A Q       │
   │                      │        │                        │
   │  Top-ranked chunks   │        │  Query is embedded     │
   │  sent to LLM to      │        │  → most similar chunks │
   │  build structured    │        │  fetched from Pinecone │
   │  plain-English       │        │  via vector search     │
   │  summary             │        │                        │
   └──────────┬───────────┘        └───────────┬────────────┘
              │                                │
              └──────────────┬─────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PROMPT CONSTRUCTION                           │
│   Retrieved chunks + user query + selected persona             │
│   are combined into a structured prompt for the LLM            │
│                      [ LangChain ]                             │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GROQ LLM INFERENCE                            │
│   The complete prompt is sent to Groq's hosted LLM             │
│   (Llama 3 / Mixtral) for ultra-fast generation                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSE TO USER                             │
│   Plain-language answer shown in the chat / summary panel      │
│   Styled according to selected persona                         │
└─────────────────────────────────────────────────────────────────┘
```

**Why RAG instead of just sending the whole document to an AI?**

- Court orders can be very long (50–200+ pages) — too big to send all at once
- RAG finds only the _relevant_ sections, making answers faster and more accurate
- It keeps the AI grounded in your actual document, reducing hallucinations

---

## 🎭 Persona-Based Responses

One of Nyay Saar's unique features is **Persona Mode** — the AI adjusts _how_ it explains things based on who you are. The same court order can mean very different things to different people.

---

### 👨‍⚖️ Common Citizen

**Best for:** Anyone with no legal background

The default mode. Explanations avoid legal terms entirely. Deadlines and key actions are highlighted. Language is conversational and empathetic.

> _Example: "The court has ordered that you must vacate the property by March 31st. This means you need to move out before that date or you may face penalties."_

---

### 🎓 Law Student

**Best for:** Students studying law or legal professionals in training

Uses proper legal terminology but also explains the reasoning and relevant precedents. Good for understanding how to read and interpret orders analytically.

> _Example: "The court issued an ex-parte injunction under Section 94 CPC, restraining the respondent from alienating the disputed property pendente lite."_

---

### 💼 Business Owner / Litigant

**Best for:** Companies or individuals directly named in the case

Focuses on business impact, financial obligations, compliance deadlines, and what actions need to be taken immediately to avoid further legal consequences.

> _Example: "You are required to pay ₹2,40,000 in damages within 30 days. Failure to comply may result in attachment of your business assets."_

---

### 📰 Journalist / Researcher

**Best for:** Media professionals, academics, policy researchers

Provides a neutral, factual breakdown suitable for reporting or analysis. Highlights public interest dimensions and broader legal implications of the order.

> _Example: "In a landmark ruling, the court upheld the petitioner's right to information, setting a significant precedent for future RTI-related disputes in the jurisdiction."_

---

### 👵 Senior Citizen / Low Literacy

**Best for:** Elderly users or those with limited reading experience

Very short sentences. No jargon at all. Uses simple everyday analogies. Large conceptual ideas are broken into tiny, digestible steps.

> _Example: "The judge said you win. The other person must pay you money. You will get ₹50,000. They must pay within one month."_

---

## 🛠️ Tech Stack Deep Dive

### Frontend

| Technology           | Version | Why We Use It                             |
| -------------------- | ------- | ----------------------------------------- |
| **React**            | 18+     | Component-based UI, fast re-renders       |
| **Tailwind CSS**     | 3+      | Utility-first styling, no custom CSS mess |
| **Axios**            | Latest  | Clean HTTP requests to the backend API    |
| **React Router**     | 6+      | Client-side multi-page navigation         |
| **React PDF Viewer** | Latest  | Renders PDF documents in the browser      |

### Backend

| Technology               | Version | Why We Use It                               |
| ------------------------ | ------- | ------------------------------------------- |
| **FastAPI**              | 0.100+  | High-performance async Python API framework |
| **Python**               | 3.10+   | Core backend language                       |
| **Uvicorn**              | Latest  | ASGI server to run FastAPI                  |
| **PyMuPDF / pdfplumber** | Latest  | Extracts text from uploaded PDFs            |
| **python-dotenv**        | Latest  | Manages API keys via `.env` file            |

### AI / ML Layer

| Technology                 | Role                                                                |
| -------------------------- | ------------------------------------------------------------------- |
| **Groq**                   | Ultra-fast LLM inference — runs Llama 3 / Mixtral models            |
| **LangChain**              | Orchestrates the full RAG pipeline (chunking, retrieval, prompting) |
| **Pinecone**               | Cloud vector database for storing and searching embeddings          |
| **HuggingFace Embeddings** | Converts text chunks into dense numerical vectors                   |

### Why These Specific Tools?

- **Groq over OpenAI** — Groq's inference speed is 10–20x faster, which is critical for a real-time chat experience. No one wants to wait 10 seconds for a reply.
- **Pinecone over local vector stores (FAISS, Chroma)** — Fully managed, production-ready, no infra to maintain. Scales automatically.
- **FastAPI over Flask/Django** — Native async support, automatic interactive API docs at `/docs`, and Pydantic validation built in.
- **LangChain** — Handles the complex plumbing of RAG (text splitters, retrievers, prompt templates) so we build features, not boilerplate.

---

## 📁 Folder Structure

<<<<<<< HEAD

```
nyay-saar/
├── frontend/               ← React app (the UI)
│   └── src/
│       ├── components/     ← Reusable UI pieces (chat, PDF viewer, etc.)
│       ├── pages/          ← Full pages (Home, Document view)
│       └── services/       ← API calls to the backend
│
├── backend/                ← FastAPI app (the AI engine)
│   └── app/
│       ├── routes/         ← API endpoints (upload, summarize, chat)
│       ├── services/       ← Core logic (PDF parsing, RAG, LLM calls)
│       └── models/         ← Request/response data shapes
│
├── .gitignore
└── README.md
```

=======
NYAY_SAAR/
├── backend/
│ └── app/
│ ├── api/
│ ├── rag/
│ ├── services/
│ ├── config/
│ ├── models/
│ ├── utils/
│ └── main.py
│
├── frontend/
│ ├── app/
│ ├── public/
│ └── package.json
│
├── .gitignore
├── .env.example
└── README.md

> > > > > > > 9722531836c32c8b6c0d9bfa2d23ba07fff55ee6

---

## 🚀 Installation & Setup

> **Prerequisites — make sure these are installed before you begin:**
>
> - [Node.js](https://nodejs.org/) (v18 or above) — for the frontend
> - [Python](https://www.python.org/) (v3.10 or above) — for the backend
> - [Git](https://git-scm.com/) — to clone the project

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/nyay-saar.git
cd nyay-saar
```

---

### Step 2 — Configure Environment Variables

```bash
cd backend
cp .env.example .env    # Creates your .env from the template
```

Open `.env` and fill in your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=your_pinecone_environment       # e.g. us-east-1-aws
PINECONE_INDEX=nyay-saar                     # name of your Pinecone index
```

> **Where to get keys:**
>
> - Groq → [console.groq.com](https://console.groq.com) (free tier available)
> - Pinecone → [app.pinecone.io](https://app.pinecone.io) (free tier available)

---

### Step 3 — Set Up the Backend

```bash
# Make sure you're inside the backend/ folder
cd backend

# Create a virtual environment (keeps dependencies isolated)
python -m venv .venv

# Activate it:
# Windows (Command Prompt / PowerShell):
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# Install all Python dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn app.main:app --reload
```

✅ Backend running at: `http://localhost:8000`  
📖 Interactive API docs at: `http://localhost:8000/docs`

---

### Step 4 — Set Up the Frontend

Open a **new terminal window** (keep the backend running in the other one):

```bash
cd frontend

# Install Node packages
npm install

# Start the dev server
npm run dev
```

✅ Frontend running at: `http://localhost:5173`

Open that URL in your browser — you're good to go! 🎉

---

## 🧪 Quick Test

Once both servers are running:

1. Open `http://localhost:5173` in your browser
2. Upload a PDF court order (or any legal document)
3. Select a **persona** that matches your background
4. Wait a few seconds for the AI to process it
5. Read the plain-English summary on the right
6. Use the chat box to ask questions like _"What are my deadlines?"_ or _"Who filed this case?"_

---

## 🛠️ Troubleshooting

| Issue                                | Fix                                                                   |
| ------------------------------------ | --------------------------------------------------------------------- |
| `pip` not found                      | Use `pip3` instead                                                    |
| `npm` not found                      | Install Node.js from [nodejs.org](https://nodejs.org)                 |
| Backend fails to start               | Verify all keys in `.env` are correct and not empty                   |
| Pinecone connection error            | Check `PINECONE_ENV` and index name match your Pinecone dashboard     |
| Port already in use                  | Run backend on a different port: `uvicorn app.main:app --port 8001`   |
| Virtual env won't activate (Windows) | Run `Set-ExecutionPolicy RemoteSigned` in PowerShell as Administrator |
| PDF upload fails                     | Ensure the PDF is not password-protected or corrupted                 |
| Chat gives wrong answers             | Re-upload the document — it may not have been indexed correctly       |

---

## 🤝 Contributing

Pull requests are welcome! If you find a bug or have a feature idea, open an issue first to discuss it.

1. Fork the repository
2. Create your branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature"`
4. Push to your fork and open a Pull Request
