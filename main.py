import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="지렁이 게임", page_icon="🐍")

st.title("🐍 지렁이 게임 (Snake Game)")
st.caption("키보드 **화살표 키(↑, ↓, ←, →)**로 조종하세요!")

# 웹 브라우저에서 동작하는 HTML5 Canvas 기반 지렁이 게임
snake_game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: #0e1117;
            color: #ffffff;
            font-family: sans-serif;
            margin: 0;
            padding: 10px;
        }
        #score-board {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        canvas {
            border: 3px solid #ff4b4b;
            border-radius: 8px;
            background-color: #1a1c23;
        }
        .btn {
            margin-top: 15px;
            padding: 8px 16px;
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .btn:hover {
            background-color: #d43b3b;
        }
    </style>
</head>
<body>

    <div id="score-board">점수: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <button class="btn" onclick="resetGame()">다시 시작</button>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;

        let snake = [{ x: 10, y: 10 }];
        let food = { x: 15, y: 15 };
        let dx = 0;
        let dy = 0;
        let score = 0;
        let gameStarted = false;

        document.addEventListener("keydown", changeDirection);

        function gameLoop() {
            if (!gameStarted) return;
            moveSnake();
            if (checkGameOver()) {
                alert("게임 오버! 최종 점수: " + score);
                resetGame();
                return;
            }
            clearCanvas();
            drawFood();
            drawSnake();
        }

        function clearCanvas() {
            ctx.fillStyle = "#1a1c23";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        function drawSnake() {
            snake.forEach((part, index) => {
                ctx.fillStyle = index === 0 ? "#66BB6A" : "#4CAF50";
                ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 2, gridSize - 2);
            });
        }

        function drawFood() {
            ctx.fillStyle = "#FF5252";
            ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 2, gridSize - 2);
        }

        function moveSnake() {
            const head = { x: snake[0].x + dx, y: snake[0].y + dy };
            snake.unshift(head);

            if (head.x === food.x && head.y === food.y) {
                score += 10;
                scoreElement.innerText = score;
                generateFood();
            } else {
                snake.pop();
            }
        }

        function generateFood() {
            food.x = Math.floor(Math.random() * tileCount);
            food.y = Math.floor(Math.random() * tileCount);
        }

        function checkGameOver() {
            const head = snake[0];
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                return true;
            }
            for (let i = 1; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    return true;
                }
            }
            return false;
        }

        function changeDirection(event) {
            const keyPressed = event.keyCode;
            const LEFT = 37, UP = 38, RIGHT = 39, DOWN = 40;

            if (!gameStarted && [LEFT, UP, RIGHT, DOWN].includes(keyPressed)) {
                gameStarted = true;
            }

            if (keyPressed === LEFT && dx === 0) { dx = -1; dy = 0; }
            if (keyPressed === UP && dy === 0) { dx = 0; dy = -1; }
            if (keyPressed === RIGHT && dx === 0) { dx = 1; dy = 0; }
            if (keyPressed === DOWN && dy === 0) { dx = 0; dy = 1; }
        }

        function resetGame() {
            snake = [{ x: 10, y: 10 }];
            dx = 0;
            dy = 0;
            score = 0;
            gameStarted = false;
            scoreElement.innerText = score;
            generateFood();
            clearCanvas();
            drawFood();
            drawSnake();
        }

        setInterval(gameLoop, 100);
        resetGame();
    </script>
</body>
</html>
"""

components.html(snake_game_html, height=530)
