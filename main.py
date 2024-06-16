#import gradio as gr

def greet(name):
    return "Hello " + name + "!"

import spacy
import re
from natasha import Segmenter, NewsEmbedding, NewsNERTagger, Doc
from deeppavlov import build_model


from flask import Flask, request, jsonify



app = Flask(__name__)



nlp_spacy = spacy.load("ru_core_news_sm")

segmenter_natasha = Segmenter()
emb_natasha = NewsEmbedding()
ner_tagger_natasha = NewsNERTagger(emb_natasha)

model_deeppavlov = build_model('./ner_ontonotes_bert_mult.json', install=True, download=True)

print("lets start!")

def hide_confidential_data(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_patterns = [
        r'\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}',
        r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2}',
        r'\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}'
    ]
    passport_pattern = r'\b\d{4}\s\d{6}\b'
    date_pattern = r'\b\d{2}\.\d{2}\.\d{4}\b'  
    credit_card_pattern = r'\b\d{4} \d{4} \d{4} \d{4}\b' 


    doc_spacy = nlp_spacy(text)
    for ent in doc_spacy.ents:
        if ent.label_ in ["PER", "GPE", "LOC", "ORG", "DATE"]:
            text = text.replace(ent.text, "###")

    doc_natasha = Doc(text)
    doc_natasha.segment(segmenter_natasha)
    doc_natasha.tag_ner(ner_tagger_natasha)
    for span in doc_natasha.spans:
        if span.type in {"PER", "LOC", "ORG", "DATE"}:
            text = text.replace(span.text, "###")
    
    results_deeppavlov = model_deeppavlov([text])
    for tag, word in zip(results_deeppavlov[1][0], results_deeppavlov[0][0]):
        if tag in ['PER', 'LOC', 'ORG', 'DATE', 'PHONE', 'EMAIL', 'PASSPORT']:
            text = text.replace(word, "###", 1)
            
    text = re.sub(email_pattern, '###', text)
    for pattern in phone_patterns:
        text = re.sub(pattern, '###', text)
    text = re.sub(passport_pattern, '###', text)
    text = re.sub(date_pattern, '###', text)
    text = re.sub(credit_card_pattern, '###', text)

    return text



@app.route('/', methods=['POST'])
def assist():
    data = request.json
    print(data)
#    if "text" not in data.keys():
#        return jsonify({"error": "Give param 'text'"}), 400
    return jsonify({"result": hide_confidential_data(data["text"])}), 200

@app.route('/', methods=['GET'])
def assist_get():
    return jsonify({"result": "all works"}), 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')



#demo = gr.Interface(fn=hide_confidential_data, inputs="text", outputs="text")

#if __name__ == "__main__":
#    demo.launch()
