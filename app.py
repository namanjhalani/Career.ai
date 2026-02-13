from career_data import career_data
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    stream = request.form.get("stream")
    percentile = int(request.form.get("percentile"))
    interest = request.form.get("interest")

    scores = {}

    for index, (career, career_interest) in enumerate(career_data[stream]):

        score = 40  # base score (not same for all logic)

        # Interest match (most important)
        if career_interest == interest:
            score += 35
        else:
            score += 10

        # Percentile impact
        if percentile >= 90:
            score += 20
        elif percentile >= 80:
            score += 15
        elif percentile >= 70:
            score += 10
        else:
            score += 5

        # Priority bias (first careers are more suitable generally)
        score -= index * 5

        # Safety cap
        if score > 98:
            score = 98

        scores[career] = score

    # Sort & pick top 3
    top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

    return render_template("result.html", results=top_3)



if __name__ == "__main__":
    app.run(debug=True)
