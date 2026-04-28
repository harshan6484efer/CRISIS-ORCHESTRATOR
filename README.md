# CRISIS ORCHESTRATOR - Hospitality Crisis Management System

CRISIS ORCHESTRATOR is an adaptive, explainable AI-driven emergency management platform specifically designed for the hospitality sector. It transforms traditional disaster response into a real-time command-and-control dashboard.

## 🚀 Overview

The system uses advanced Large Language Models (LLMs) and computer vision to provide structured, decision-first protocols for various hospitality emergencies, including:
- **Fire Safety**: Immediate evacuation and suppression protocols.
- **Medical Emergencies**: Rapid responder dispatch and guest safety.
- **Security Threats**: Lockdown and perimeter security management.

## ✨ Key Features

- **Decision-First AI**: Provides clear, actionable commands (Decision, Who, Where) with XAI (Explainable AI) reasoning.
- **Image Analysis**: Uses computer vision to classify disaster scenes and suggest precautions.
- **Multilingual Support**: Supports English, Urdu, Hindi, and Japanese.
- **Hospitality Specialized**: Tailored locations and rescue contacts for hotel environments.

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **AI/LLM**: Groq (Llama 3.3 70B)
- **Computer Vision**: Hugging Face Transformers (Vit for Image Classification)
- **Frontend**: HTML5, Vanilla CSS

## 📋 Prerequisites

- Python 3.8+
- Groq API Key

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/harshan6484efer/CRISIS-ORCHESTRATOR.git
   cd CRISIS-ORCHESTRATOR
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## 📄 License

This project is licensed under the MIT License.
