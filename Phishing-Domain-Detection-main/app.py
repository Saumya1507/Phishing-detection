from flask import Flask, request, render_template
import urlFeatures
import jsFeatures
import domainFeatures
import pickle
import numpy as np

app = Flask(__name__, static_url_path="/static")


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST" and "url" in request.form:
        url = request.form.get("url")
        features = []
        features.extend(urlFeatures.fetchURLFeatures(url))
        features.extend(jsFeatures.fetchJSFeatures(url))
        features.extend(domainFeatures.fetchDomainFeatures(url))

        # print(features)

        features = np.array(features)
        features = features.reshape(1, -1)

        filename = 'model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        result = loaded_model.predict(features)

        if result[0] == -1:
            msg = "warning"
        else:
            msg = "safe"
        return render_template('index.html', msg=msg)

    else:
        return render_template("index.html", msg="")


if __name__ == '__main__':
    app.run(debug=False)
