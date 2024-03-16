from flask import Flask, render_template

import llm_generate
app = Flask(__name__)

@app.route("/")
def index():

    llm_response = llm_generate.generate_content()
    if llm_response:
      print(llm_response)
      return render_template('home.html', car_models=llm_response)
    return "Sever response is not available."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)