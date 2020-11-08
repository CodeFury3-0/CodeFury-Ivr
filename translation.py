from googletrans import Translator
import json
translator = Translator()

translations  = {
        'message1':'Welcome to the Workers Helpline.',
        'message2':'This helpline is your one stop solution to daily work.',
        'message3':'Press 1 for english, Press 2 for Hindi, Press 3 for Kannada',
        'message4':'Thank you for choosing the language',
        'message5':'What is your Age ?',
        'message6':'Press 1 if you are male and Press 2 if you are female',
        'message7':'Press 1 if you are a Plumber, Press 2 if you are a Carpenter, Press 3 if you are a Daily wage worker, Press 4 if you are a House Worker',
        'message8':'What is your expected per day salary ?',
        'message9':'Please tell your Name and City separated by from',
        'message10':"Thank you for providing the age",
        "message11":"Thank you for providing the gender",
        "message12":"Thank you for selecting the occupation",
        "message13":"Thank you for telling the expected salary",
        "message14":"Thank you for telling the name and the city",
        'message15':'We wil start recording after the beep',
        "message16":"You are now successfully registered. You will receive all the daily wage notification directly on your mobile phone. Goodbye"
    }  


def saveTranslation(language):
    translated = dict()
    translationKeys = list(translations.keys())
    translationValues = list(translations.values())
    translationsToLanguage = translator.translate(translationValues, dest=language)
    print(translationsToLanguage,type(translationsToLanguage))
    for trans in range(0,len(translationKeys)):
        translated[translationKeys[trans]] = translationsToLanguage[trans].text
    print(translated)
    json_object = json.dumps(translated, indent = 4) 
    filename = language + '.json'
    with open(filename, "w") as outfile: 
        outfile.write(json_object) 
    return

saveTranslation('hi')
saveTranslation('kn')