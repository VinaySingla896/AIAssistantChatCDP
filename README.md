# CDP Support Chatbot

A powerful chatbot designed to assist users with questions about popular Customer Data Platforms (CDPs) including Segment, mParticle, Lytics, and Zeotap.

## Features

- 💬 Interactive chat interface with streaming responses
- 📚 Access to comprehensive CDP documentation
- 🔍 Intelligent context-aware answers
- 🎯 Focused on "how-to" questions and practical guidance
- 🔄 Natural conversation flow with chat history

## Technical Stack

- Frontend: Streamlit
- Backend: FastAPI
- Natural Language Processing: LangChain
- Vector Storage: FAISS
- Embeddings: OpenAI

## Setup

1. Clone the repository
2. Navigate to backend
```bash
cd backend
```
3. create and activate a virtual env
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set up environment variables:
```bash
export OPENAI_API_KEY='your-api-key'
```
5. Start the backend server:
```bash
python backend/main.py
```
6. Open another termial and navigate to frontend
```bash
cd frontend
```
7. create and activate a virtual env
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
8. Install dependencies:
```bash
pip install -r requirements.txt
```
9. Start the frontend server:
```bash
streamlit run app.py
```

The application will be available at http://localhost:5000

## Usage Examples

Ask questions about various CDP functionalities:

- "How do I set up a new source in Segment?"
- "What's the process for creating user profiles in mParticle?"
- "How can I build audience segments in Lytics?"
- "What are the steps for data integration with Zeotap?"

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI server
│   ├── chat_processor.py    # Chat handling logic
│   └── document_processor.py # Documentation processing
├── frontend/
│   ├── app.py              # Streamlit interface
│   └── styles.css          # Custom styling
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - feel free to use this project for your own purposes.
