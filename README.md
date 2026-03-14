# NLP Chatbot with Voice and Sentiment Analysis

This project is a Python-based chatbot that combines **Natural Language Processing (NLP)**, **voice interaction**, and **sentiment analysis**.
It provides a graphical interface where users can type or speak messages and receive spoken responses from the chatbot.

The system also performs sentiment analysis on each message and stores the conversation history locally.

## Features

* Rule-based chatbot using **NLTK**
* **Graphical user interface** built with Tkinter
* **Speech recognition** for voice input
* **Text-to-speech** responses
* **Sentiment analysis** using TextBlob
* **Conversation history logging**
* Support for **Portuguese and basic English interactions**

## Technologies Used

* Python
* NLTK (Natural Language Toolkit)
* TextBlob
* Tkinter
* SpeechRecognition
* pyttsx3

## Installation

1. Clone the repository

git clone https://github.com/emanodev/chatbot-pln-python.git

2. Navigate to the project folder

cd chatbot_pln

3. Install the required dependencies

pip install -r requirements.txt

## Running the Application

Run the chatbot with:

python chatbot_pln.py

The graphical interface will open and you can start interacting with the chatbot.

## Usage

* Type a message and press **Enter** or click **Send**
* Click the **microphone button** to speak with the chatbot
* The chatbot will respond with text and voice
* Each message will also be analyzed for sentiment
* Conversations are automatically saved in `historico_chat.txt`

## Future Improvements

* More advanced NLP techniques
* Intent classification using machine learning
* Integration with modern language models
* Web interface
* Context-aware conversation handling

## License

This project is open source and available for educational and research purposes.

## Author

Emanoel Victor  
Data Science Student  
Brazil

