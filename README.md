# Minutes: Hybrid Text Summarizer for Online Meetings

This project implements a hybrid text summarization system that combines extractive and abstractive summarization techniques for generating concise meeting summaries from audio, video, or text inputs.

## 🔍 Project Overview

- **Objective**: Automatically generate coherent, human-like summaries of online meetings.
- **Approach**:
  - **Extractive Summarization** using centroid-based TF-IDF and Word2Vec embeddings.
  - **Abstractive Summarization** using fine-tuned BART and T5 models.
  - **ASR Integration** for handling audio and video inputs using AssemblyAI API.

## 🧠 Core Components

- **ASR Module**: Converts audio/video to transcribed text.
- **Extractive Module**: Selects most relevant sentences using TF-IDF + Word2Vec + cosine similarity.
- **Abstractive Module**: Generates fluent summaries using BART and one-line titles using T5.
- **Web Interface**: Built using Django backend and Chrome extension for inline summarization.

## 📦 Tech Stack

- Python, Django
- PyTorch, HuggingFace Transformers
- Word2Vec (Gensim), NLTK, Scikit-learn
- AssemblyAI API (ASR)
- Twilio API (OTP Login)
- HTML/CSS/JavaScript (Frontend)

## 🧪 Evaluation

- **Datasets**: CNN/DailyMail, BBC Articles
- **Metrics**: ROUGE-1, ROUGE-2, ROUGE-L, BLEU
- **Result**: BLEU-4 score of 18.7, with strong qualitative human evaluation

## 🚀 Deployment

- Model inference hosted through Django.
- Input options: text files, URLs, YouTube videos, audio.
- Outputs downloadable in `.txt` or `.pdf` format.

## 📄 Publication

This project was published in the **2023 IEEE 14th International Conference on Computing Communication and Networking Technologies (ICCCNT)**.

**Citation**:  
*A Mahadevan, A Pillai, J Lamba - Minutes: Hybrid Text Summarizer for Online Meetings*

**Paper link**: [https://ieeexplore.ieee.org/document/10254909](https://ieeexplore.ieee.org/document/10254909)

---
