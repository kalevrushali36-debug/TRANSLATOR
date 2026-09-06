from googletrans import Translator

# Create a translator object
translator = Translator()

# Take text from the user
text = input("Enter text: ")

# Ask the user for the destination language
language = input("Enter language code (hi, mr, en, ur, jp): ")

# Translate the text
translated = translator.translate(text, dest=language)

# Display original and translated text
print("\nOriginal:", text)
print("Translated:", translated.text)