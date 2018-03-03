from flask import Flask, request, jsonify
import json
import os
from activate_functions import activate_function_hardly, activate_function_simple
from neural import BooleanNeural
from z2 import Z2

app = Flask(__name__)


@app.route("/lazy_magic", methods=["POST"])
def magic_simple():
    data = json.loads(request.data)
    result = neural_simple.test(data["vars"])

    y = result["out"]
    reality = result["reality"]

    return jsonify({
        "result": 1 if y > 0.8 else 0,
        "probability": y,
        "reality": reality,
        "vars": data["vars"],
        "error": y - reality
    })


@app.route("/real_magic", methods=["POST"])
def magic():
    data = json.loads(request.data)
    result = neural.test(data["vars"])

    y = result["out"]
    reality = result["reality"]

    return jsonify({
        "result": 1 if y > 0.8 else 0,
        "probability": y,
        "reality": reality,
        "vars": data["vars"],
        "error": y - reality
    })


def model(vars, AND, OR, NOT):
    return AND(OR(NOT(vars[0]), OR(NOT(vars[1]), NOT(vars[2]))), OR(NOT(vars[1]), OR(NOT(vars[2]), vars[3])))


if __name__ == "__main__":
    neural_simple = BooleanNeural(4, Z2(4).truth_table(model), activate_function_simple, 0.3, 100000)
    neural_simple.training()

    neural = BooleanNeural(4, Z2(4).truth_table(model), activate_function_hardly, 0.3, 100000)
    neural.training()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
