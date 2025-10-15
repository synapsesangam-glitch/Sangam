# Sangam Synapse – AI Innovation Sprint Starter Code (V2)

Welcome, innovators! This repository contains an expanded set of starter code for the Sangam Synapse event. Your objective is to enhance, optimize, integrate, and expand these AI programs within the given timeframe.

This version includes:
- **Two Chatbots**: `mixtral_chat.py` and `gemini_chat.py`.
- **Live Transcription**: `live_speech_to_text.py` captures audio from your microphone.
- **High-Quality TTS**: `text_to_speech_deepgram.py` uses Deepgram's Aura for voice synthesis.
- **Wake Word Detection**: `wake_word_detector.py` listens for a keyword like "Hey Google".

---

## 📜 Competition Rules & Guidelines

Please read all rules carefully. Failure to comply may lead to disqualification.

### **Core Rules (from the official circular)**
* **Time Limit**: You have exactly **2 hours and 30 minutes** to complete all modifications, testing, and submission.
* **Team Size**: Teams must consist of **exactly two members**.
* **Internet Use**: Internet use is allowed for reference, research, and accessing documentation. However, **plagiarism is strictly forbidden** and will result in immediate disqualification.
* **Integrity**: Any form of malpractice or unfair means is prohibited.
* **Final Decision**: The judges' decision will be final and binding.

### **Technical & Submission Rules**
* **Use of AI Tools**: You are encouraged to use AI assistants (like Gemini, GitHub Copilot, etc.) for coding, debugging, and generating ideas. This is an AI Innovation Sprint, so leverage the tools!
* **Submission Format**: Your final submission **must be a GitHub repository**. At the end of the event, you will provide the public URL to your repository for evaluation.
* **Final Commit**: All code modifications must be committed and pushed to your GitHub repository before the 2.5-hour time limit expires. Commits made after the deadline will not be considered.
* **API Keys**: Do **not** commit your `.env` file or any API keys directly into your code. Use the provided `.env` setup. Teams are responsible for managing their own API keys.
* **Dependencies**: If you add any new Python libraries, you **must** update the `requirements.txt` file accordingly. This is crucial for the judges to run your code.

### **Presentation & Demonstration**
* **Mandatory Presentation**: Each team must present their work for 5 minutes.
* **Content**: Your presentation should clearly explain the improvements you made, showcase the new functionality with a live demonstration, and highlight the most creative or innovative aspects of your approach.

---

## 🚀 Getting Started

Follow these steps to set up your project environment.

### 1. Install Dependencies
This project has dependencies that may require extra steps.

**a. Install PortAudio**
The `pyaudio` library (for microphone access) needs `portaudio`.
- **Windows**: `pyaudio` often comes with the necessary files.
- **macOS**: Use Homebrew: `brew install portaudio`
- **Linux (Debian/Ubuntu)**: `sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0`

**b. Install Python Libraries**
Open your terminal in this project folder and run:
```bash
pip install -r requirements.txt"# Sangam-Synapse" 
