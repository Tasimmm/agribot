🌾 AgriBot 
An AI-powered chatbot for agriculture-related queries, built with **Streamlit** and **Gemini-Pro**. AgriBot provides text and voice-based responses in multiple languages, including English, Hindi, Malayalam, and Kannada.

 **Features**
✅ Handles agriculture-related queries using Google Gemini-Pro  
✅ Supports text and voice-based inputs  
✅ Provides real-time text and audio responses  
✅ Multi-language support: English, Hindi, Malayalam, and Kannada  
✅ Interactive chat history display  

---
🛠️ **Tech Stack**
- **Python**  
- **Streamlit** – For building the interactive UI  
- **Google Generative AI (Gemini-Pro)** – For AI-based responses  
- **SpeechRecognition** – For processing voice input  
- **gTTS (Google Text-to-Speech)** – For generating audio responses  
- **pydub** – For playing audio responses  

---
 📥 **Setup and Installation**
### 1. **Clone the Repository**
```bash
git clone https://github.com/USERNAME/agribot.git
cd agribot
```

### 2. **Create a Virtual Environment (Optional)**
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# .\venv\Scripts\activate  # Windows
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Set Google API Key**
- Open the project folder.  
- Create a `.env` file or set the API key directly in the code:
```python
GOOGLE_API_KEY = "your-google-api-key"
```

### 5. **Run the Application**
```bash
streamlit run app.py
```

---

 🗣️ **How to Use**
1. Open the app in your browser.
2. Type your agriculture-related query in the input field OR click **"Speak"** to ask via voice input.
3. The AI will process your query and provide a text and audio response.  
4. You can choose to receive responses in **English, Hindi, Malayalam, or Kannada**.  

---
 🎯 **Project Structure**
```plaintext
agribot/
├── app.py                  # Main Streamlit app file
├── requirements.txt        # List of dependencies
├── .env                    # API key (ignored in Git)
├── README.md               # Project documentation
└── C:/Temp                 # Directory for temporary audio files
```

---
🔑 **Environment Variables**
Create a `.env` file and add:
```env
GOOGLE_API_KEY=your-google-api-key
```

---
📦 **Dependencies**
Install dependencies using:
```bash
pip install -r requirements.txt
```

**requirements.txt**:
```plaintext
streamlit
google-generativeai
speechrecognition
gtts
pydub
```

---
🛡️ **License**
This project is licensed under the [MIT License](LICENSE).

---

🤝 **Contributing**
1. Fork the repository.  
2. Create a new branch (`git checkout -b feature/branch-name`).  
3. Commit changes (`git commit -m 'Add some feature'`).  
4. Push to the branch (`git push origin feature/branch-name`).  
5. Open a pull request.  

---

⭐ **Acknowledgments**
- [Streamlit](https://streamlit.io/)  
- [Google Generative AI](https://ai.google.dev/)  
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)  
- [gTTS](https://pypi.org/project/gTTS/)  
- [pydub](https://pypi.org/project/pydub/)  

---

This should cover everything you need to make the repository look professional! 😎
