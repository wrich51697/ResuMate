import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a test sentence.")
print([(token.text, token.pos_) for token in doc])
