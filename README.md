# AI Notes - Intelligent Document Processing & Q&A System

AI Notes is a comprehensive document processing and question-answering system that combines document upload, text extraction, semantic search, and AI-powered responses. The application allows users to upload PDF documents, process them into searchable sections, and ask questions that are answered using context from the uploaded documents.

## 🚀 Features

- **Document Upload & Processing**: Upload PDF documents with automatic text extraction and chunking
- **Semantic Search**: Advanced vector search using Qdrant for finding relevant document sections
- **AI-Powered Q&A**: Get intelligent answers based on document content using OpenAI GPT models
- **Conversation Threads**: Maintain conversation history and context for follow-up questions
- **Document-Specific Queries**: Ask questions about specific documents or across all documents
- **Real-time Chat Interface**: Modern chat interface with real-time responses
- **Document Workspace**: View and edit documents with integrated text editor
- **Tag Management**: Organize documents with custom tags

## 🏗️ Architecture

The application consists of two main components:

### Backend (FastAPI)
- **FastAPI** server with RESTful APIs
- **Qdrant** vector database for semantic search
- **CouchDB** for document and metadata storage
- **OpenAI** integration for AI responses
- **PyMuPDF** for PDF text extraction
- **Sentence Transformers** for embeddings

### Frontend (Next.js)
- **Next.js 15** with React 18
- **Tailwind CSS** for styling
- **TipTap** rich text editor
- **React PDF** for document viewing
- **Axios** for API communication

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- Qdrant database
- CouchDB database
- OpenAI API key

## 🛠️ Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (create a `.env` file):
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=http://localhost:6333
COUCHDB_URL=http://localhost:5984
```

4. Start the backend server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🚀 Usage

1. **Upload Documents**: Use the dashboard to upload PDF documents
2. **Process Documents**: Documents are automatically processed and indexed
3. **Ask Questions**: Use the chat interface to ask questions about your documents
4. **View Documents**: Access the workspace to view and edit documents
5. **Manage Conversations**: Maintain conversation threads for context-aware responses

## 📁 Project Structure

```
AI-Notes/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes and endpoints
│   ├── app/                # Application logic
│   ├── core/               # Core utilities and configurations
│   └── uploads/            # Document storage
└── frontend/               # Next.js frontend
    ├── app/                # Next.js app directory
    ├── components/         # Reusable UI components
    └── lib/                # Utility functions
```

## 🔧 API Endpoints

- `POST /api/documents/upload` - Upload and process documents
- `POST /api/bot/query` - Ask questions to the AI bot
- `GET /api/documents` - Retrieve document list
- `POST /api/threads` - Manage conversation threads

## 📚 API Details

### Documents API (`/api/documents`)

- **POST `/upload`**
  - **Description:** Upload a PDF document for processing and indexing.
  - **Parameters:**
    - `document` (form-data, file): The PDF file to upload (must be .pdf)
    - `tags` (form-data, string): Comma-separated tags for the document
  - **Response:**
    - Success: DocumentUploadResponse (document_id, status, message, created_at)
    - Error: 400 if not PDF, 500 on server error

- **GET `/get/{document_id}`**
  - **Description:** Retrieve metadata and information about a specific document by its ID.
  - **Parameters:**
    - `document_id` (path, string): The unique document identifier
  - **Response:**
    - Document details or error message

- **DELETE `/delete/{document_id}`**
  - **Description:** Delete a document by its ID.
  - **Parameters:**
    - `document_id` (path, string): The unique document identifier
  - **Response:**
    - DocumentDeleteResponse (status, message)

---

### Bot API (`/api/bot`)

- **POST `/response`**
  - **Description:** Ask a question to the AI bot across all documents.
  - **Body:**
    - `query` (string): The user's question
    - Additional fields as per `BotQueryRequest`
  - **Response:**
    - BotQueryResponse (query, response, document_ids, tags, date_time)

- **POST `/document/response`**
  - **Description:** Ask a question to the AI bot about a specific document.
  - **Body:**
    - `query` (string): The user's question
    - `document_id` (string): The document to query
    - Additional fields as per `BotDocumentsQueryRequest`
  - **Response:**
    - BotQueryResponse (query, response, document_ids, tags, date_time)

- **POST `/thread/response`**
  - **Description:** Continue a conversation thread with the AI bot (context-aware Q&A).
  - **Body:**
    - As per `BotRequest` (includes thread context)
  - **Response:**
    - BotQueryResponse (query, response, document_ids, tags, date_time)

---

### Questions API (`/api/question`)

- **POST `/create/response`**
  - **Description:** Save a question and its answer to the database.
  - **Body:**
    - As per `QuestionAnswerRequest` (question, answer, metadata)
  - **Response:**
    - SaveQuestionResponse (status, message, question_id, etc.)

---

### Miscellaneous

- **GET `/testroute`**
  - **Description:** Test endpoint to verify the API is running.
  - **Response:** `{ "message": "Hello World" }`

---

Each endpoint returns structured JSON responses. For detailed request/response models, see the backend `api/*/request/` and `api/*/response/` modules.

## 🤖 Advanced Bot Services & HyDE

### HyDE (Hypothetical Document Embeddings)
- **Purpose:**
  - HyDE is an advanced retrieval-augmented generation technique. Instead of searching the database with the user's raw query, HyDE first generates a hypothetical answer to the query using the language model. This hypothetical answer is then embedded and used as the search query in the vector database (Qdrant), often resulting in more relevant context retrieval for ambiguous or open-ended questions.
- **How it works:**
  1. User submits a question.
  2. The system generates a hypothetical answer using the LLM (OpenAI).
  3. The hypothetical answer is embedded into a vector.
  4. This vector is used to search Qdrant for the most relevant document sections.
  5. The retrieved context is used to generate the final answer.
- **Benefits:**
  - Improves retrieval for vague or complex queries.
  - Reduces the risk of missing relevant context.

### Thread-based Q&A
- **Purpose:**
  - Maintains conversation history and context, allowing the bot to answer follow-up questions with awareness of previous exchanges.
- **How it works:**
  1. Each conversation is tracked as a thread.
  2. When a user asks a follow-up, the system combines previous Q&A pairs into a context string.
  3. The context and new question are used to generate a prompt for the LLM.
  4. The LLM generates a context-aware answer.
- **Benefits:**
  - Enables multi-turn, context-rich conversations.
  - Supports follow-up and clarification questions.

### Follow-up/Contextual Q&A
- **Purpose:**
  - Allows users to ask follow-up questions that reference previous answers, with the system maintaining and leveraging context.
- **How it works:**
  1. The system stores previous Q&A pairs.
  2. For a follow-up, it generates a prompt that includes the conversation history and the new question.
  3. The LLM uses this prompt to generate a contextually relevant answer.
- **Benefits:**
  - Delivers more accurate and relevant answers in ongoing conversations.

---

These advanced services are implemented in the backend (`app/bot/bot.py`) and are accessible via the `/api/bot` endpoints. HyDE is used internally to improve retrieval, while thread and follow-up Q&A are exposed via dedicated endpoints for context-aware interactions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue in the repository.
