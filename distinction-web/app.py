import math
import os

from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f2f5fb; color: #18243b; }
    header { background: #253f79; color: white; padding: 30px 8%; }
    main { max-width: 700px; margin: 35px auto; padding: 0 18px; }
    .card { background: white; padding: 28px; border-radius: 14px; box-shadow: 0 5px 20px #dce3f0; }
    label { display: block; margin: 18px 0 6px; font-weight: bold; }
    input { width: 100%; box-sizing: border-box; padding: 12px; font-size: 16px; }
    button { margin-top: 20px; padding: 12px 20px; background: #253f79; color: white; border: 0; border-radius: 7px; cursor: pointer; }
    .result { margin-top: 25px; padding: 18px; background: #e9f1ff; border-radius: 9px; }
    .error { color: #a32424; }
  </style>
</head>
<body>
  <header>
    <h1>{{ title }}</h1>
    <p>Plan your project milestones with a simple progress estimate.</p>
  </header>
  <main>
    <div class="card">
      <form method="post">
        <label for="total">Total project tasks</label>
        <input id="total" name="total" type="number" min="1" required value="{{ total }}">
        <label for="completed">Completed tasks</label>
        <input id="completed" name="completed" type="number" min="0" required value="{{ completed }}">
        <button type="submit">Calculate progress</button>
      </form>

      {% if error %}<p class="error">{{ error }}</p>{% endif %}
      {% if result %}
      <div class="result">
        <h2>Your progress</h2>
        <p><strong>Completed:</strong> {{ result.percent }}%</p>
        <p><strong>Remaining tasks:</strong> {{ result.remaining }}</p>
        <p><strong>Estimated days remaining:</strong> {{ result.days }}</p>
        <p>Estimate based on {{ daily_target }} tasks per day.</p>
      </div>
      {% endif %}
    </div>
  </main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    title = os.getenv("APP_TITLE", "Milestone Progress Tracker")
    daily_target = max(1, int(os.getenv("DAILY_TARGET", "2")))
    total = ""
    completed = ""
    result = None
    error = None

    if request.method == "POST":
        total = request.form.get("total", "")
        completed = request.form.get("completed", "")
        try:
            total_number = int(total)
            completed_number = int(completed)
            if total_number < 1 or completed_number < 0 or completed_number > total_number:
                raise ValueError()
            remaining = total_number - completed_number
            result = {
                "percent": round(completed_number * 100 / total_number, 1),
                "remaining": remaining,
                "days": math.ceil(remaining / daily_target),
            }
        except ValueError:
            error = "Enter a positive total and a completed count between 0 and the total."

    return render_template_string(
        PAGE, title=title, daily_target=daily_target, total=total,
        completed=completed, result=result, error=error
    )


@app.get("/health")
def health():
    return {"application": "milestone-progress-tracker", "status": "healthy"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
