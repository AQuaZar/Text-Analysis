from flask import Flask, request, jsonify
import spacy

from models import Concept, Property, Aspect, Characteristic, NaturalLanguageTransformer


app = Flask(__name__)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    nlp = spacy.load("en_core_web_md")
    try:
        doc = nlp(data["input"])
        noun = data["noun"]
        verb = data["verb"]
    except KeyError:
        return jsonify({"error": "Wrong data parameters"})
    except TypeError:
        return jsonify({"error": "Wrong data format"})

    elements = []

    for w in doc:
        if "nsubj" in w.dep_:
            concept = Concept(w.text)
            elements.append(concept)
        if "ROOT" == w.dep_:
            property_ = Property(w.text)
            elements.append(property_)
            for w1 in doc:
                # searching for branch verb and auxiliary verb
                if "cc" == w1.dep_ and w1.head.text == property_.name:
                    property_.particle = w1.text
                if "conj" == w1.dep_ and w1.head.text == property_.name:
                    property_.branch = w1.text
                # check if concept exist
                if "nsubj" in w.dep_:
                    property_.concept = w1.text
        if "aux" == w.dep_:
            aspect = Aspect(w.text)
            elements.append(aspect)
        if "auxpass" == w.dep_:
            aspect.particle = w.text
        if "adv" in w.dep_:
            characteristic = Characteristic(w.text)
            elements.append(characteristic)

    visitor = NaturalLanguageTransformer(f"To {verb} {noun},")
    for element in elements:
        element.accept(visitor)

    return jsonify({"result": visitor.body})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
