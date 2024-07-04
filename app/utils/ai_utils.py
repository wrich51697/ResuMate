from transformers import BertTokenizer, BertForTokenClassification
from transformers import pipeline

# Load pre-trained model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Create a pipeline for named entity recognition (NER)
nlp = pipeline("ner", model=model, tokenizer=tokenizer)


def extract_keywords(text):
    ner_results = nlp(text)
    keywords = [result['word'] for result in ner_results if result['entity'] == 'LABEL_1']
    return keywords
