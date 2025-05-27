from flask import Flask, render_template_string, request, redirect, url_for, session
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")

USER = os.getenv("LOGIN_USER")
PASS = os.getenv("LOGIN_PASS")

if USER is None or PASS is None:
    raise RuntimeError("LOGIN_USER and LOGIN_PASS must be set in the .env file.")

LOGIN_FORM = """
<form method="post">
  <input name="username" placeholder="Username" required>
  <input name="password" type="password" placeholder="Password" required>
  <button type="submit">Login</button>
</form>
{% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
"""

HELLO_SCREEN = """
<h1>Hello, World!</h1>
<p>Welcome, {{ user }}!</p>
<a href="{{ url_for('logout') }}">Logout</a>
"""

WELCOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Welcome</title>
  <style>
    html, body { height: 100%; margin: 0; padding: 0; overflow: hidden; }
    body { background: #111; color: #fff; display: flex; align-items: center; justify-content: center; height: 100vh; flex-direction: column;}
    h1 { font-size: 5em; z-index: 1; position: relative; margin-bottom: 40px;}
    #particles-js { position: fixed; width: 100vw; height: 100vh; top: 0; left: 0; z-index: 0; }
    .btn-pong {
      z-index: 1;
      font-size: 2em;
      padding: 20px 60px;
      background: #fff;
      color: #111;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 30px;
      transition: background 0.2s, color 0.2s;
      display: block;
      text-align: center;
      text-decoration: none;
    }
    .btn-pong:hover {
      background: #222;
      color: #fff;
    }
  </style>
</head>
<body>
  <div id="particles-js"></div>
  <h1>Welcome</h1>
  <a href="{{ url_for('pong') }}"><button class="btn-pong">Ping Pong</button></a>
  <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
        "color": { "value": "#ffffff" },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.5 },
        "size": { "value": 3 },
        "line_linked": { "enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.4, "width": 1 },
        "move": { "enable": true, "speed": 2 }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": { "enable": true, "mode": "repulse" },
          "onclick": { "enable": true, "mode": "push" }
        },
        "modes": {
          "repulse": { "distance": 100, "duration": 0.4 },
          "push": { "particles_nb": 4 }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""

PONG_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Ping Pong</title>
  <style>
    body { background: #222; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0;}
    #pongCanvas { background: #111; display: block; margin: 30px auto; border: 2px solid #fff; }
    .scoreboard { font-size: 2em; margin-top: 10px; }
    .back-btn { margin-top: 20px; font-size: 1.2em; padding: 10px 30px; border-radius: 8px; border: none; background: #fff; color: #111; cursor: pointer;}
    .back-btn:hover { background: #444; color: #fff; }
  </style>
</head>
<body>
  <h2>Ping Pong</h2>
  <div class="scoreboard">Skóre: <span id="score">0</span> | Životy: <span id="lives">3</span></div>
  <canvas id="pongCanvas" width="600" height="400"></canvas>
  <a href="{{ url_for('welcome') }}"><button class="back-btn">Späť</button></a>
  <script>
    const canvas = document.getElementById("pongCanvas");
    const ctx = canvas.getContext("2d");
    let paddleHeight = 10, paddleWidth = 100, paddleX = (canvas.width-paddleWidth)/2;
    let rightPressed = false, leftPressed = false;
    let ballRadius = 8, x = canvas.width/2, y = canvas.height-30, dx = 3, dy = -3;
    let score = 0, lives = 3;

    document.addEventListener("keydown", keyDownHandler, false);
    document.addEventListener("keyup", keyUpHandler, false);

    function keyDownHandler(e) {
      if(e.key == "Right" || e.key == "ArrowRight") rightPressed = true;
      else if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = true;
    }
    function keyUpHandler(e) {
      if(e.key == "Right" || e.key == "ArrowRight") rightPressed = false;
      else if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = false;
    }

    function drawPaddle() {
      ctx.beginPath();
      ctx.rect(paddleX, canvas.height-paddleHeight-2, paddleWidth, paddleHeight);
      ctx.fillStyle = "#fff";
      ctx.fill();
      ctx.closePath();
    }

    function drawBall() {
      ctx.beginPath();
      ctx.arc(x, y, ballRadius, 0, Math.PI*2);
      ctx.fillStyle = "#fff";
      ctx.fill();
      ctx.closePath();
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawPaddle();
      drawBall();
      document.getElementById("score").textContent = score;
      document.getElementById("lives").textContent = lives;

      // Ball movement
      if(x + dx > canvas.width-ballRadius || x + dx < ballRadius) dx = -dx;
      if(y + dy < ballRadius) dy = -dy;
      else if(y + dy > canvas.height-ballRadius-paddleHeight-2) {
        if(x > paddleX && x < paddleX + paddleWidth) {
          dy = -dy;
          score++;
        } else if(y + dy > canvas.height-ballRadius) {
          lives--;
          if(!lives) {
            alert("Koniec hry! Skóre: " + score);
            document.location.reload();
          } else {
            x = canvas.width/2; y = canvas.height-30; dx = 3; dy = -3;
            paddleX = (canvas.width-paddleWidth)/2;
          }
        }
      }

      x += dx; y += dy;

      if(rightPressed && paddleX < canvas.width-paddleWidth) paddleX += 7;
      else if(leftPressed && paddleX > 0) paddleX -= 7;

      requestAnimationFrame(draw);
    }
    draw();
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] == USER and request.form["password"] == PASS:
            session["user"] = USER
            return redirect(url_for("welcome"))
        else:
            error = "Invalid credentials"
    return render_template_string(LOGIN_FORM, error=error)

@app.route("/welcome")
def welcome():
    if "user" in session:
        return render_template_string(WELCOME_PAGE)
    return redirect(url_for("login"))

@app.route("/app")
def app_page():
    if "user" in session:
        return render_template_string(APP_PAGE)
    return redirect(url_for("login"))

@app.route("/hello")
def hello():
    if "user" in session:
        return render_template_string(HELLO_SCREEN, user=session["user"])
    return redirect(url_for("login"))

@app.route("/pong")
def pong():
    if "user" in session:
        return render_template_string(PONG_PAGE)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)