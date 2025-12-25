from flask import Flask, render_template, Response, jsonify
from camera import generate_frames, set_alert_state

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# 🔔 Alert toggle API
@app.route('/toggle_alert', methods=['POST'])
def toggle_alert():
    state = set_alert_state()
    return jsonify({"alert": state})

if __name__ == "__main__":
    app.run(debug=True)
