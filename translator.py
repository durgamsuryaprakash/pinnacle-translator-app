from typing import TypedDict

from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound, TooManyRequests
from requests.exceptions import ConnectionError, RequestException, Timeout


LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
}
LANGUAGES = list(LANGUAGE_CODES)
MAX_TEXT_LENGTH = 5000


class TranslationResult(TypedDict):
    success: bool
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    error: str | None


def translation_result(
    success: bool,
    text: str,
    source_language: str,
    target_language: str,
    translated_text: str = "",
    error: str | None = None,
) -> TranslationResult:
    return {
        "success": success,
        "original_text": text,
        "translated_text": translated_text,
        "source_language": source_language,
        "target_language": target_language,
        "error": error,
    }


def translate_text(
    text: str,
    source_language: str,
    target_language: str,
) -> TranslationResult:
    cleaned_text = (text or "").strip()

    if not cleaned_text:
        return translation_result(
            False,
            cleaned_text,
            source_language,
            target_language,
            error="Please enter some text to translate.",
        )
    if len(cleaned_text) > MAX_TEXT_LENGTH:
        return translation_result(
            False,
            cleaned_text,
            source_language,
            target_language,
            error=f"Please limit the text to {MAX_TEXT_LENGTH:,} characters.",
        )
    if source_language not in LANGUAGE_CODES or target_language not in LANGUAGE_CODES:
        return translation_result(
            False,
            cleaned_text,
            source_language,
            target_language,
            error="Please choose a supported source and target language.",
        )
    if source_language == target_language:
        return translation_result(
            False,
            cleaned_text,
            source_language,
            target_language,
            error="Please choose two different languages.",
        )

    try:
        translated_text = GoogleTranslator(
            source=LANGUAGE_CODES[source_language],
            target=LANGUAGE_CODES[target_language],
        ).translate(cleaned_text)
    except (ConnectionError, Timeout):
        error = "The translation service is unavailable. Check your internet connection and try again."
    except TooManyRequests:
        error = "The translation service is busy right now. Please wait a moment and try again."
    except TranslationNotFound:
        error = "A translation could not be found for this text. Please try different wording."
    except RequestException:
        error = "The translation request could not be completed. Please try again shortly."
    except Exception:
        error = "Translation failed unexpectedly. Please try again."
    else:
        if translated_text:
            return translation_result(
                True,
                cleaned_text,
                source_language,
                target_language,
                translated_text=translated_text.strip(),
            )
        error = "The translation service returned no result. Please try again."

    return translation_result(
        False,
        cleaned_text,
        source_language,
        target_language,
        error=error,
    )