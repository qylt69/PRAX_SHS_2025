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
<!DOCTYPE html>
<html>
<head>
  <title>Prihlásenie</title>
  <style>
    body {
      background: linear-gradient(135deg, #232526 0%, #414345 100%);
      min-height: 100vh;
      margin: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Segoe UI', Arial, sans-serif;
    }
    .login-container {
      background: rgba(30,30,30,0.97);
      border-radius: 16px;
      box-shadow: 0 8px 32px 0 rgba(31,38,135,0.37);
      padding: 48px 36px 36px 36px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 340px;
    }
    .login-logo {
      width: 64px;
      height: 64px;
      margin-bottom: 18px;
      border-radius: 50%;
      background: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2.2em;
      color: #232526;
      font-weight: bold;
      box-shadow: 0 2px 12px #0004;
    }
    .login-title {
      color: #fff;
      font-size: 2em;
      margin-bottom: 18px;
      font-weight: 500;
      letter-spacing: 1px;
    }
    form {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    input[type="text"], input[type="password"] {
      padding: 12px 16px;
      border-radius: 8px;
      border: none;
      font-size: 1.1em;
      background: #222;
      color: #fff;
      outline: none;
      transition: box-shadow 0.2s;
      box-shadow: 0 1px 4px #0002;
    }
    input[type="text"]:focus, input[type="password"]:focus {
      box-shadow: 0 0 0 2px #4e54c8;
    }
    button[type="submit"] {
      background: linear-gradient(90deg, #4e54c8 0%, #8f94fb 100%);
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 12px 0;
      font-size: 1.2em;
      font-weight: 500;
      cursor: pointer;
      margin-top: 8px;
      transition: background 0.2s, transform 0.1s;
      box-shadow: 0 2px 8px #0003;
    }
    button[type="submit"]:hover {
      background: linear-gradient(90deg, #232526 0%, #4e54c8 100%);
      transform: translateY(-2px) scale(1.03);
    }
    .login-error {
      color: #ff6b6b;
      margin-top: 10px;
      font-size: 1.05em;
      text-align: center;
      min-height: 1.2em;
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="login-logo">🎮</div>
    <div class="login-title">Prihlásenie</div>
    <form method="post">
      <input name="username" type="text" placeholder="Používateľské meno" required autocomplete="username">
      <input name="password" type="password" placeholder="Heslo" required autocomplete="current-password">
      <button type="submit">Prihlásiť sa</button>
    </form>
    <div class="login-error">{% if error %}{{ error }}{% endif %}</div>
  </div>
</body>
</html>
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
    .btn-pong, .btn-poker, .btn-blackjack {
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
    .btn-pong:hover, .btn-poker:hover, .btn-blackjack:hover {
      background: #222;
      color: #fff;
    }
  </style>
</head>
<body>
  <div id="particles-js"></div>
  <h1>Welcome</h1>
  <button class="btn-pong" onclick="window.location.href='{{ url_for('pong') }}'">Ping Pong</button>
  <button class="btn-poker" onclick="window.location.href='{{ url_for('poker') }}'">Poker</button>
  <button class="btn-blackjack" onclick="window.location.href='{{ url_for('blackjack') }}'">Black Jack</button>
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

POKER_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Poker</title>
  <style>
    body { background: #222; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0;}
    .cards { margin: 10px 0; }
    .card { display: inline-block; background: #fff; color: #111; border-radius: 6px; padding: 10px 16px; margin: 0 4px; font-size: 1.3em; min-width: 32px; text-align: center;}
    .btn { margin: 10px 8px 0 8px; font-size: 1.1em; padding: 10px 30px; border-radius: 8px; border: none; background: #fff; color: #111; cursor: pointer;}
    .btn:hover { background: #444; color: #fff; }
    .back-btn { margin-top: 20px; font-size: 1.2em; padding: 10px 30px; border-radius: 8px; border: none; background: #fff; color: #111; cursor: pointer;}
    .back-btn:hover { background: #444; color: #fff; }
    .status { margin: 12px 0 0 0; font-size: 1.2em; min-height: 1.5em;}
  </style>
</head>
<body>
  <h2>Poker (jednoduchá hra)</h2>
  <div>
    <div><b>Dealer:</b></div>
    <div class="cards" id="dealer-cards"></div>
  </div>
  <div style="margin-top:20px;">
    <div><b>Hráč:</b></div>
    <div class="cards" id="player-cards"></div>
  </div>
  <div class="status" id="status"></div>
  <div>
    <button class="btn" id="deal-btn">Rozdať</button>
    <button class="btn" id="restart-btn" style="display:none;">Reštart</button>
  </div>
  <a href="{{ url_for('welcome') }}"><button class="back-btn">Späť</button></a>
  <script>
    const suits = ['♠','♥','♦','♣'];
    const values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A'];
    let deck = [];
    let playerCards = [];
    let dealerCards = [];
    let dealt = false;

    function createDeck() {
      let d = [];
      for (let s of suits) {
        for (let v of values) {
          d.push({suit:s, value:v});
        }
      }
      for (let i = d.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [d[i], d[j]] = [d[j], d[i]];
      }
      return d;
    }

    function renderCards(elemId, cards) {
      const el = document.getElementById(elemId);
      el.innerHTML = '';
      cards.forEach((c) => {
        el.innerHTML += `<span class="card">${c.value}${c.suit}</span>`;
      });
    }

    function handRank(hand) {
      // Vracia jednoduchý popis kombinácie (len pár, dvojpár, trojica, postupka, farba, full house, poker, straight flush, high card)
      let vals = hand.map(c => values.indexOf(c.value)).sort((a,b)=>a-b);
      let suitsArr = hand.map(c => c.suit);
      let counts = {};
      for (let v of vals) counts[v] = (counts[v]||0)+1;
      let countVals = Object.values(counts).sort((a,b)=>b-a);
      let isFlush = suitsArr.every(s=>s===suitsArr[0]);
      let isStraight = vals.every((v,i,arr)=>i===0||v-arr[i-1]===1) || (JSON.stringify(vals)==JSON.stringify([0,1,2,3,12])); // A2345
      if (isStraight && isFlush) return "Straight Flush";
      if (countVals[0]===4) return "Poker";
      if (countVals[0]===3 && countVals[1]===2) return "Full House";
      if (isFlush) return "Flush";
      if (isStraight) return "Straight";
      if (countVals[0]===3) return "Trojica";
      if (countVals[0]===2 && countVals[1]===2) return "Dvojpár";
      if (countVals[0]===2) return "Pár";
      return "Najvyššia karta";
    }

    function compareHands(player, dealer) {
      // Jednoduché porovnanie podľa poradia kombinácií
      const ranks = ["Najvyššia karta","Pár","Dvojpár","Trojica","Straight","Flush","Full House","Poker","Straight Flush"];
      let pr = handRank(player), dr = handRank(dealer);
      let pi = ranks.indexOf(pr), di = ranks.indexOf(dr);
      if (pi > di) return "Vyhral hráč ("+pr+" > "+dr+")";
      if (pi < di) return "Vyhral dealer ("+dr+" > "+pr+")";
      // Ak rovnaká kombinácia, rozhoduje najvyššia karta
      let pvals = player.map(c=>values.indexOf(c.value)).sort((a,b)=>b-a);
      let dvals = dealer.map(c=>values.indexOf(c.value)).sort((a,b)=>b-a);
      for (let i=0;i<5;i++) {
        if (pvals[i]>dvals[i]) return "Vyhral hráč ("+pr+")";
        if (pvals[i]<dvals[i]) return "Vyhral dealer ("+dr+")";
      }
      return "Remíza";
    }

    function deal() {
      deck = createDeck();
      playerCards = [deck.pop(),deck.pop(),deck.pop(),deck.pop(),deck.pop()];
      dealerCards = [deck.pop(),deck.pop(),deck.pop(),deck.pop(),deck.pop()];
      renderCards('player-cards', playerCards);
      renderCards('dealer-cards', dealerCards);
      let result = compareHands(playerCards, dealerCards);
      document.getElementById('status').textContent = result;
      document.getElementById('deal-btn').disabled = true;
      document.getElementById('restart-btn').style.display = '';
      dealt = true;
    }

    function restart() {
      playerCards = [];
      dealerCards = [];
      renderCards('player-cards', []);
      renderCards('dealer-cards', []);
      document.getElementById('status').textContent = '';
      document.getElementById('deal-btn').disabled = false;
      document.getElementById('restart-btn').style.display = 'none';
      dealt = false;
    }

    document.getElementById('deal-btn').onclick = deal;
    document.getElementById('restart-btn').onclick = restart;
    restart();
  </script>
</body>
</html>
"""

BLACKJACK_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Black Jack</title>
  <style>
    body { background: #222; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0;}
    .cards { margin: 10px 0; }
    .card { display: inline-block; background: #fff; color: #111; border-radius: 6px; padding: 10px 16px; margin: 0 4px; font-size: 1.3em; min-width: 32px; text-align: center;}
    .btn { margin: 10px 8px 0 8px; font-size: 1.1em; padding: 10px 30px; border-radius: 8px; border: none; background: #fff; color: #111; cursor: pointer;}
    .btn:hover { background: #444; color: #fff; }
    .back-btn { margin-top: 20px; font-size: 1.2em; padding: 10px 30px; border-radius: 8px; border: none; background: #fff; color: #111; cursor: pointer;}
    .back-btn:hover { background: #444; color: #fff; }
    .status { margin: 12px 0 0 0; font-size: 1.2em; min-height: 1.5em;}
  </style>
</head>
<body>
  <h2>Black Jack</h2>
  <div>
    <div><b>Dealer:</b></div>
    <div class="cards" id="dealer-cards"></div>
    <div id="dealer-score"></div>
  </div>
  <div style="margin-top:20px;">
    <div><b>Vy:</b></div>
    <div class="cards" id="player-cards"></div>
    <div id="player-score"></div>
  </div>
  <div class="status" id="status"></div>
  <div>
    <button class="btn" id="hit-btn">Hit</button>
    <button class="btn" id="stand-btn">Stand</button>
    <button class="btn" id="restart-btn" style="display:none;">Restart</button>
  </div>
  <a href="{{ url_for('welcome') }}"><button class="back-btn">Späť</button></a>
  <script>
    const suits = ['♠','♥','♦','♣'];
    const values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
    let deck = [];
    let playerCards = [];
    let dealerCards = [];
    let gameOver = false;

    function createDeck() {
      let d = [];
      for (let s of suits) {
        for (let v of values) {
          d.push({suit:s, value:v});
        }
      }
      for (let i = d.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [d[i], d[j]] = [d[j], d[i]];
      }
      return d;
    }

    function cardValue(card) {
      if (card.value === 'A') return 11;
      if (['K','Q','J'].includes(card.value)) return 10;
      return parseInt(card.value);
    }

    function handValue(hand) {
      let val = 0, aces = 0;
      for (let c of hand) {
        val += cardValue(c);
        if (c.value === 'A') aces++;
      }
      while (val > 21 && aces > 0) {
        val -= 10;
        aces--;
      }
      return val;
    }

    function renderCards(elemId, cards, hideFirst=false) {
      const el = document.getElementById(elemId);
      el.innerHTML = '';
      cards.forEach((c, i) => {
        let cardHtml = hideFirst && i === 0 ? '<span class="card">?</span>' :
          `<span class="card">${c.value}${c.suit}</span>`;
        el.innerHTML += cardHtml;
      });
    }

    function renderScores() {
      document.getElementById('player-score').textContent = 'Skóre: ' + handValue(playerCards);
      let dealerScore = gameOver ? handValue(dealerCards) : (dealerCards.length > 1 ? 'Skóre: ?' : '');
      document.getElementById('dealer-score').textContent = dealerScore;
    }

    function updateUI() {
      renderCards('player-cards', playerCards);
      renderCards('dealer-cards', dealerCards, !gameOver);
      renderScores();
      document.getElementById('hit-btn').disabled = gameOver;
      document.getElementById('stand-btn').disabled = gameOver;
      document.getElementById('restart-btn').style.display = gameOver ? '' : 'none';
    }

    function checkGameEnd() {
      let playerVal = handValue(playerCards);
      if (playerVal > 21) {
        document.getElementById('status').textContent = 'Prehrali ste! (BUST)';
        gameOver = true;
      } else if (playerVal === 21) {
        stand();
      }
    }

    function dealerTurn() {
      while (handValue(dealerCards) < 17) {
        dealerCards.push(deck.pop());
      }
      let dealerVal = handValue(dealerCards);
      let playerVal = handValue(playerCards);
      let status = '';
      if (dealerVal > 21) status = 'Dealer busts! Vyhrali ste!';
      else if (dealerVal > playerVal) status = 'Dealer vyhráva!';
      else if (dealerVal < playerVal) status = 'Vyhrali ste!';
      else status = 'Remíza!';
      document.getElementById('status').textContent = status;
      gameOver = true;
      updateUI();
    }

    function hit() {
      if (gameOver) return;
      playerCards.push(deck.pop());
      updateUI();
      checkGameEnd();
    }

    function stand() {
      if (gameOver) return;
      gameOver = true;
      updateUI();
      setTimeout(() => {
        dealerTurn();
      }, 700);
    }

    function restart() {
      deck = createDeck();
      playerCards = [deck.pop(), deck.pop()];
      dealerCards = [deck.pop(), deck.pop()];
      gameOver = false;
      document.getElementById('status').textContent = '';
      updateUI();
      checkGameEnd();
    }

    document.getElementById('hit-btn').onclick = hit;
    document.getElementById('stand-btn').onclick = stand;
    document.getElementById('restart-btn').onclick = restart;

    restart();
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

@app.route("/poker")
def poker():
    if "user" in session:
        return render_template_string(POKER_PAGE)
    return redirect(url_for("login"))

@app.route("/blackjack")
def blackjack():
    if "user" in session:
        return render_template_string(BLACKJACK_PAGE)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)