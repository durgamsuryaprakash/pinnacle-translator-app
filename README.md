# Pinnacle Translator App

Pinnacle Translator App is a Streamlit web application that translates text between seven languages. It is built as Task 3 of the Pinnacle Labs Artificial Intelligence Internship and runs on the free Google translation endpoint provided by the `deep-translator` library, so no API key is required.

## Project Overview

The application provides a clean, card-based interface where users enter text, choose a source and target language, and translate between them. Every translation is validated before it is sent to the service, network problems are reported with friendly messages, and the most recent translations are kept in a session history so users can look back at what they translated. The interface has four pages: Translate, History, Languages, and About.

## Features

- Text translation between seven languages
- Source and target language selection
- One-click language swap
- English to Telugu translation (the default language pair)
- Session translation history with a clear-history action
- Popular language pairs that can be set with one click
- Input validation: empty text, identical languages, unsupported languages, and a 5,000 character limit
- Friendly error messages for connectivity and service problems
- Large text input area with a clear original and translated result section

## Tech Stack

- Python 3
- Streamlit (user interface and session state)
- deep-translator (Google translation service)
- unittest (standard library, used for the test suite)

## How It Works

1. `app.py` renders the Streamlit interface, manages navigation, and stores application state (selected languages, input text, latest translation, history) in `st.session_state`.
2. When the Translate button is pressed, `run_translation` calls `translate_text` from `translator.py`.
3. `translate_text` validates the input (non-empty, within 5,000 characters, supported and distinct languages) and then sends the request through `deep_translator.GoogleTranslator` using the language code map defined in `LANGUAGE_CODES`.
4. Network, rate-limit, and empty-result errors are caught and converted into readable messages instead of exceptions.
5. Successful translations are stored in a session history capped at the 8 most recent entries.

## Project Structure

```
Pinnacle_Translator_App/
├── app.py                  # Streamlit interface and session state handling
├── translator.py           # Translation logic, language map, and validation
├── requirements.txt        # Runtime dependencies
├── tests/
│   └── test_translator.py  # Unit tests for input validation
├── README.md
└── .gitignore
```

## Installation

1. Clone the repository and open a terminal in the project folder.
2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

An internet connection is required for translations. No paid API or API key is needed.

## How to Run

```bash
python -m streamlit run app.py
```

Streamlit will start a local server and open the app in your browser, by default at `http://localhost:8501`.

## Example Usage

1. Select **English** as the source language and **Telugu** as the target language (this is the default pair).
2. Enter `Good morning` in the text area.
3. Select **Translate**. The translated text appears in the result section and the entry is added to the session history.
4. Use the swap button to reverse the selected languages, or **Clear** to reset the text and result.
5. Open the **History** page to review the translations from the current session.

Supported languages: English, Hindi, Telugu, Spanish, French, German, Japanese.

## Limitations

- Translation quality depends on the free Google translation endpoint; it occasionally returns transient failures or rate limits, which the app reports as friendly messages.
- An active internet connection is required.
- Input is limited to 5,000 characters per translation.
- History is stored only for the current browser session and is capped at 8 entries; it is lost when the session ends.
- The source language must be chosen manually; there is no automatic language detection.
- The app is a learning project and has not been prepared for production deployment.

## Future Improvements

- Automatic source-language detection
- Speech input and pronunciation playback
- Document and file translation
- Exporting translation history
- Support for additional languages

## Internship Context

This project is Task 3 of the Artificial Intelligence Internship at Pinnacle Labs. The goal of the task was to build a working translator application with a clean interface, sound input validation, and readable, maintainable code.

## Author

Durgam Surya Prakash - [GitHub](https://github.com/durgamsuryaprakash)
