import speech_recognition as sr
from gtts import gTTS
import requests
import os
import urllib.parse


# ============================================================
# VOICE TO TEXT
# ============================================================

def voice_to_text():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\n🎤 Speak now...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text

        except sr.UnknownValueError:
            print("❌ Sorry, I could not understand your voice.")
            return ""

        except sr.RequestError:
            print("❌ Could not connect to speech recognition service.")
            return ""

    except Exception as e:
        print("❌ Microphone error:", e)
        return ""


# ============================================================
# TRANSLATION
# ============================================================

def translate_text(text, target_language):

    try:
        # MyMemory translation service
        encoded_text = urllib.parse.quote(text)

        url = (
            "https://api.mymemory.translated.net/get"
            "?q=" + encoded_text +
            "&langpair=autodetect|" + target_language
        )

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("❌ Translation server error.")
            return ""

        data = response.json()

        translated = data["responseData"]["translatedText"]

        if translated:
            return translated

        print("❌ No translation received.")
        return ""

    except requests.exceptions.Timeout:
        print("❌ Translation request timed out.")
        return ""

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to translation service.")
        return ""

    except Exception as e:
        print("❌ Translation error:", e)
        return ""


# ============================================================
# TEXT TO VOICE
# ============================================================

def text_to_voice(text, language):

    if not text:
        print("❌ There is no translated text to speak.")
        return

    try:

        speech = gTTS(
            text=text,
            lang=language
        )

        filename = "translation.mp3"

        speech.save(filename)

        print("\n🔊 Playing translated voice...")

        os.startfile(filename)

    except Exception as e:
        print("❌ Voice output error:", e)


# ============================================================
# MAIN PROGRAM
# ============================================================

print("========================================")
print("        LANGUAGE TRANSLATOR")
print("========================================")


# ============================================================
# INPUT METHOD
# ============================================================

print("\nChoose input method:")
print("1. Enter text")
print("2. Speak")

input_choice = input("Choose 1 or 2: ").strip()


if input_choice == "1":

    text = input("\nEnter your text: ").strip()

elif input_choice == "2":

    text = voice_to_text()

else:

    print("❌ Invalid choice.")
    exit()


# ============================================================
# CHECK INPUT
# ============================================================

if not text:

    print("❌ No input received.")
    exit()


print("\nYour input:", text)


# ============================================================
# TARGET LANGUAGE
# ============================================================

print("\nChoose target language:")
print("1. English")
print("2. Hindi")
print("3. Marathi")
print("4. French")
print("5. Spanish")
print("6. German")
print("7. Japanese")

language_choice = input(
    "Choose language (number or name): "
).strip().lower()


languages = {

    "1": "en",
    "2": "hi",
    "3": "mr",
    "4": "fr",
    "5": "es",
    "6": "de",
    "7": "ja",

    "english": "en",
    "hindi": "hi",
    "marathi": "mr",
    "french": "fr",
    "spanish": "es",
    "german": "de",
    "japanese": "ja"
}


if language_choice not in languages:

    print("❌ Invalid language.")
    exit()


target_language = languages[language_choice]


# ============================================================
# TRANSLATE
# ============================================================

print("\nTranslating...")

translated_text = translate_text(
    text,
    target_language
)


# ============================================================
# CHECK TRANSLATION
# ============================================================

if not translated_text:

    print("\n========================================")
    print("❌ Translation could not be completed.")
    print("========================================")

    exit()


# ============================================================
# DISPLAY TRANSLATION
# ============================================================

print("\n========================================")
print("Translated Text:")
print(translated_text)
print("========================================")


# ============================================================
# OUTPUT METHOD
# ============================================================

print("\nChoose output:")
print("1. Text only")
print("2. Voice only")
print("3. Text + Voice")

output_choice = input(
    "Choose 1, 2 or 3: "
).strip()


if output_choice == "1":

    print("\n📄 Translation:")
    print(translated_text)


elif output_choice == "2":

    text_to_voice(
        translated_text,
        target_language
    )


elif output_choice == "3":

    print("\n📄 Translation:")
    print(translated_text)

    text_to_voice(
        translated_text,
        target_language
    )


else:

    print("❌ Invalid output choice.")


print("\n========================================")
print("        PROGRAM FINISHED")
print("========================================")
