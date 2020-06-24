
BE_VERBS = ("AM", "ARE", "DO", "WILL", "WON'T", "DID", "DIDN'T", "DON'T")
NOM_PRONOUNS = ("I", "YOU", "HE", "SHE", "THEY", "WE")
POSESSIVES = ("MY", "YOUR", "HER", "HIS", "THEIR", "OUR")
QUESTIONS = ("WHY","WHEN","WHERE","HOW","WHAT")
replacements = {
    "YOU" : "I",
    "YOU'RE" : "I'M",
    "YOUR" : "MY",
    "I" : "YOU",
    "WE" : "YOU",
    "I'M" : "YOU'RE",
    "MY" : "YOUR",
    "OUR" : "YOUR",
    "AM" : "ARE",
    "ARE" : "ARE.CHECK", #Dealt with later
}

def split_sentence(sentence):
    return [word.strip(".,?!") for word in user_says.upper().split(" ")]

def create_statement(sentence):
    response = []

    for word in sentence:
        if word in replacements.keys():
            response.append(replacements[word])
        else:
            response.append(word)

    if response[0] in QUESTIONS:
        response = response[1:]

    #Deal with "are"s
    while "ARE.CHECK" in response:
        position = response.index("ARE.CHECK")
        if position > 0 and response[position - 1] == "I":
            response[position] = "AM"
        elif position < len(response) - 1 and response[position + 1] == "I":
            response[position] = "AM"
        else:
            response[position] = "ARE"

    for position in range(len(response) - 1):
        if response[position] in BE_VERBS and response[position + 1] in NOM_PRONOUNS:
            response[position], response[position + 1] = response[position + 1], response[position]

    for pronoun in NOM_PRONOUNS:
        if pronoun in response:
            response = response[response.index(pronoun):]

    return " ".join(response)

print("ELIZA> HELLO.")

running = True
while running:
    user_says = input("YOU> ")
    sentence = split_sentence(user_says)
    response = ""

    if "ALWAYS" in sentence or "EVERY" in sentence or "ALL" in sentence:
        response = "COULD YOU GIVE ME AN EXAMPLE?"
    elif "WANT" in sentence and "BECAUSE" not in sentence:
        response = "WHY DO YOU THINK " + create_statement(sentence)
    elif "YES" in sentence or "NO" in sentence:
        response = "I SEE. WHAT ELSE CAN YOU TELL ME?"
    elif "CAN'T" in sentence or "WON'T" in sentence or "WOULDN'T" in sentence and "BECAUSE" not in sentence:
        response = "WHY NOT?"
    elif "BECAUSE" in sentence:
        response = "DOES THAT SEEM LIKE A GOOD REASON?"

    #Check for question
    if len(response) == 0:
        for question in QUESTIONS:
            if question in sentence:
                response = question + " DO YOU THINK " + create_statement(sentence) +"?"

    #Check for possessives at the end
    if len(response) == 0:
        for possessive in POSESSIVES:
            if possessive in sentence and sentence.index(possessive) == len(sentence) - 2:
                if possessive in replacements.keys():
                    response = "TELL ME MORE ABOUT " + replacements[possessive] + " " + sentence[sentence.index(possessive) + 1]
                else:
                    response = "TELL ME MORE ABOUT " + possessive + " " + sentence[sentence.index(possessive) + 1]

    statement = create_statement(sentence)
    if len(response) == 0 and statement != " ".join(sentence):
        response = "WHY DO YOU THINK " + statement + "?"

    if len(response) == 0:
        response = "IS THERE ANYTHING ELSE YOU CAN TELL ME?"

    if "GOODBYE" in sentence:
        response = "GOODBYE."
        running = False

    print("ELIZA> " + response)