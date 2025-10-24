# Sangam Synapse – AI Innovation Sprint Starter Code

Welcome, innovators! This repository contains the official starter code for the **Sangam Synapse – AI Innovation Sprint**. Your objective is to enhance, optimize, and integrate these AI programs within the given timeframe, inspired by the event's theme: **"AI Innovation: Bridging Uttar Pradesh's Astronomical Legacy with Modern Computing."**

---

## 🧰 Your AI Toolkit

You have a variety of Python scripts to build upon. Explore what each one does:

* **`gemini_chat.py`**: A creative chatbot powered by Google's Gemini Pro model that can answer questions and hold a conversation.
* **`mixtral_chat.py`**: Another powerful conversational chatbot that uses a Mixtral model for dialogue.
* **`image_classifier.py`**: A tool that uses the Gemini Vision model to look at an image (`sample_image.jpg`) and describe what it sees.
* **`text_summarize.py`**: A script that can take a long piece of text and use Gemini to generate a concise summary.
* **`text_to_speech.py`**: A real-time text-to-speech engine that streams audio directly from the Deepgram API.
* **`data_analyser.py`**: A script that reads data from a CSV file (`sample_data.csv`), performs a basic statistical analysis, and creates a visual bar chart from the data.
* **`information_finder.py`**: A utility that connects to the Wikipedia API to fetch and display a summary of any topic you search for.
* **`web_search.py`**: An interface to the Groq API, giving you access to fast, web-indexed information and search capabilities.

---

## 📜 Competition Rules & Guidelines

Please read all rules carefully. Failure to comply may lead to disqualification.

### **Core Rules**
* **Time Limit**: You have exactly **2 hours and 30 minutes** for the coding sprint to complete all modifications, testing, and submission.
* **Team Size**: Teams must consist of **exactly two members** from Grades 9-12.
* **Internet Use**: Internet access is allowed for research and documentation. However, **plagiarism is strictly forbidden** and will result in immediate disqualification.
* **Integrity**: Any form of malpractice or unfair means is prohibited.
* **Final Decision**: The judges' decision will be final and binding.

### **Technical & Submission Rules**
* **Use of AI Tools**: You are encouraged to use AI assistants (like Gemini, GitHub Copilot, etc.) for coding and debugging. This is an AI Innovation Sprint—leverage the tools!
* **Submission Format**: Your final submission **must be a public GitHub repository**. You will provide the URL for evaluation at the end of the event.
* **Final Commit**: All code must be committed and pushed to your GitHub repository before the time limit expires. Commits made after the deadline will not be considered.
* **API Keys**: Do **not** commit your `.env` file or any API keys directly into your code. Use the provided `.env` setup. Teams are responsible for managing their own keys.
* **Dependencies**: If you add new Python libraries, you **must** update the `requirements.txt` file. This is crucial for the judges to run your code.

### **Presentation & Demonstration**
* **Mandatory Presentation**: Each team must present their work for 5 minutes.
* **Content**: Your presentation should clearly explain the improvements you made, showcase the new functionality with a live demonstration, and highlight the creative aspects of your solution.

---

## 🚀 Setup & Getting Started

Follow these steps to get your project running:

1.  **Install Libraries**: Open your terminal and run the following command to install all the necessary Python packages from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set Up API Keys**: Create a file named `.env` in the main project folder. Copy the contents of the `.env.example` file into it and add your unique API keys:
    ```
    # For mixtral_chat.py
    MIXTRAL_API_KEY="YOUR_MIXTRAL_API_KEY_HERE"

    # For gemini_chat.py, image_classifier.py, text_summarize.py
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"

    # For web_search.py
    GROQ_API_KEY="YOUR_GROQ_API_KEY_HERE"
    
    # For text_to_speech.py
    DEEPGRAM_API_KEY="YOUR_DEEPGRAM_API_KEY"
    ```
3.  **Add Sample Files**: Make sure you have the `sample_image.jpg` and `sample_data.csv` files in the same folder so you can test the `image_classifier.py` and `data_analyser.py` scripts.

---

> "Innovation is born when tradition sparks curiosity and technology fuels creation."

**Good luck, and build something amazing!**