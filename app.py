from cypher_system import CaesarCipher, PoemCipher, TrithemiusCipher
from flask import Flask, flash, request, render_template

app = Flask(__name__)


@app.route("/ceasar/", methods=["GET", "POST"])
def index():
    result = ""
    bruteforce_results = []
    text_value = ""
    lang_value = "EN"

    if request.method == "POST":
        text_value = request.form.get("text", "")
        shift = int(request.form.get("shift", 3))
        lang_value = request.form.get("lang", "EN")
        action = request.form.get("action", "encrypt")

        cipher = CaesarCipher(shift)

        if action == "encrypt":
            result = cipher.encrypt(text_value)
        elif action == "decrypt":
            result = cipher.decrypt(text_value)

            alphabet_length = 26 if lang_value == "EN" else 33
            for s in range(1, alphabet_length):
                brute_cipher = CaesarCipher(s)
                decoded = brute_cipher.decrypt(text_value)
                bruteforce_results.append((s, decoded))

    return render_template(
        "CeasarCipher.html",
        result=result,
        bruteforce_results=bruteforce_results,
        text_value=text_value,
        lang_value=lang_value
    )



@app.route("/trithemius/", methods=["GET", "POST"])
def trithemius():
    result = ""
    text_value = ""
    key_value = ""
    key_type = "linear"

    if request.method == "POST":
        text_value = request.form.get("text", "")
        key_input = request.form.get("key", "")
        key_type = request.form.get("key_type", "linear")
        action = request.form.get("action", "encrypt")

        cipher = TrithemiusCipher()


        try:
            if key_type in ["linear", "quadratic"]:

                key_parts = [int(x.strip()) for x in key_input.split(",")]
                key = key_parts
            else:
                key = key_input
        except Exception as e:
            return render_template("TrithemiusCipher.html",
                                   result="Помилка ключа: " + str(e),
                                   text_value=text_value,
                                   key_value=key_input,
                                   key_type=key_type)

        if action == "encrypt":
            result = cipher.encrypt(text_value, key)
        elif action == "decrypt":
            result = cipher.decrypt(text_value, key)

    return render_template("TrithemiusCipher.html",
                           result=result,
                           text_value=text_value,
                           key_value=key_value,
                           key_type=key_type)


@app.route("/poem/", methods=["GET", "POST"])
def poem():
    result = None
    error = None
    formdata = {}

    if request.method == "POST":
        formdata = request.form.to_dict()
        action = request.form.get("action")
        text = request.form.get("text", "")
        poem_key = request.form.get("poem", "")

        try:
            cipher = PoemCipher(poem_key)
            if action == "encrypt":
                result = cipher.encrypt(text)
            elif action == "decrypt":
                result = cipher.decrypt(text)
            else:
                raise ValueError("Невідома дія.")
        except Exception as e:
            error = str(e)
            flash(error, "danger")

    return render_template("PoemCipher.html", result=result, formdata=formdata)




if __name__ == "__main__":
    app.run(debug=True)
