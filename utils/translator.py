from deep_translator import GoogleTranslator

def translate_text(text, language):

    try:

        translated = GoogleTranslator(
            source="auto",
            target=language
        ).translate(text)

        return translated

    except Exception as e:

        return f"Translation Error: {str(e)}"