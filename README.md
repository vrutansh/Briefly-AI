# BrieflyAI 🔥

AI-powered video intelligence platform that transcribes, summarizes, extracts insights, and lets you chat with any video using RAG.

Built with **Streamlit + LLMs + Retrieval-Augmented Generation (RAG)**.

---

## ✨ Features

* 🎙 **Video Transcription**

  * Transcribes YouTube videos or local media files
  * Supports multiple languages (`English`, `Hinglish`)

* 📋 **AI Summarization**

  * Generates concise summaries from long-form video content

* 🏷 **Automatic Title Generation**

  * Detects and generates meaningful titles from transcripts

* ✅ **Action Item Extraction**

  * Identifies tasks, responsibilities, and next steps

* 🔑 **Key Decision Detection**

  * Extracts important decisions discussed in meetings/videos

* ❓ **Open Question Detection**

  * Finds unresolved questions and discussion points

* 🧠 **RAG-powered Chat**

  * Ask questions directly about the video content
  * Context-aware conversational retrieval system

* 🎨 **Modern UI**

  * Fully custom-designed Streamlit interface
  * Cyberpunk-inspired visual theme
  * Interactive pipeline tracker

---

# 🚀 Demo Flow

1. Paste a YouTube URL or local video path
2. Click **Analyse Video**
3. BrieflyAI:

   * extracts audio
   * transcribes speech
   * summarizes content
   * extracts insights
   * builds a RAG knowledge base
4. Chat with the video instantly

---

# 🏗 Project Structure

```bash
Briefly-AI/
│
├── app.py
├── core/
│   ├── transcriber.py
│   ├── summarize.py
│   ├── extractor.py
│   └── rag_engine.py
│
├── utils/
│   └── audio_processor.py
│
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Tech Stack

* **Frontend**

  * Streamlit

* **AI / NLP**

  * LLMs
  * RAG Pipeline
  * Embeddings
  * Semantic Retrieval

* **Audio Processing**

  * FFmpeg
  * Whisper / Speech-to-Text

* **Backend Utilities**

  * Python
  * dotenv

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/vrutansh/Briefly-AI.git
cd Briefly-AI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

Add any additional provider/API keys your pipeline uses.

---

# ▶️ Run the App

```bash
streamlit run app.py
```

---

# 💬 Example Use Cases

* Meeting summarization
* Podcast analysis
* Lecture note generation
* YouTube content intelligence
* Team standup tracking
* Interview analysis
* Research/video indexing

---

# 🧠 RAG Chat Examples

Ask questions like:

```text
What were the main takeaways?
Who owns what action items?
What deadlines were discussed?
Summarize the discussion in 5 bullet points.
What concerns were raised?
```

---

# 🎨 UI Highlights

* Custom CSS-powered Streamlit experience
* Animated pipeline tracker
* Interactive chat interface
* Minimal dark-mode aesthetic
* Responsive card-based layout

---

# 📌 Pipeline Overview

```text
Input Video
   ↓
Audio Extraction
   ↓
Speech Transcription
   ↓
Title Generation
   ↓
Summarization
   ↓
Insight Extraction
   ↓
RAG Knowledge Base
   ↓
Conversational Q&A
```

---

# 🔥 Future Improvements

* Multi-language support
* Speaker diarization
* Timestamped summaries
* Export to PDF/Notion
* Real-time live meeting mode
* Video highlights generation
* Team collaboration

---

# 🤝 Contributing

Pull requests are welcome.

If you'd like to improve BrieflyAI, feel free to fork the repo and submit a PR.

---

# 📄 License

MIT License

---


