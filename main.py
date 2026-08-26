import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="프리미엄 지렁이 게임", page_icon="🍎", layout="wide")

st.title("🍎 프리미엄 지렁이 게임 (Smooth Snake)")
st.write("키보드 **화살표 키(↑, ↓, ←, →)**를 사용하여 지렁이를 조종하세요!")

snake_game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: #0e1117;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
        }
        #game-container {
            position: relative;
            text-align: center;
        }
        #score-board {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #81C784;
            text-shadow: 0 0 10px rgba(129, 199, 132, 0.5);
        }
        canvas {
            border: 5px solid #333;
            border-radius: 15px;
            background-color: #1a1c23;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        }
        .btn {
            margin-top: 20px;
            padding: 12px 24px;
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            transition: background-color 0.3s, transform 0.1s;
        }
        .btn:hover {
            background-color: #d43b3b;
        }
        .btn:active {
            transform: scale(0.98);
        }
    </style>
</head>
<body>

    <div id="game-container">
        <div id="score-board">점수: <span id="score">0</span></div>
        <canvas id="gameCanvas" width="600" height="600"></canvas>
        <br>
        <button class="btn" onclick="resetGame()">게임 다시 시작</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");

        const gridSize = 25;
        const tileCount = canvas.width / gridSize;

        let snake = [];
        let food = { x: 15, y: 15 };
        let dx = 0;
        let dy = 0;
        let score = 0;
        let gameInterval;
        let gameStarted = false;
        let isGameOver = false;

        document.addEventListener("keydown", changeDirection);

        function gameLoop() {
            if (!gameStarted || isGameOver) return;
            moveSnake();
            if (checkGameOver()) {
                isGameOver = true;
                drawGameOver();
                return;
            }
            clearCanvas();
            drawGrid();
            drawApple();
            drawSmoothSnake();
        }

        function clearCanvas() {
            ctx.fillStyle = "#1a1c23";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        function drawGrid() {
            ctx.strokeStyle = "rgba(255, 255, 255, 0.03)";
            ctx.lineWidth = 1;
            for (let i = 0; i <= tileCount; i++) {
                ctx.beginPath();
                ctx.moveTo(i * gridSize, 0);
                ctx.lineTo(i * gridSize, canvas.height);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(0, i * gridSize);
                ctx.lineTo(canvas.width, i * gridSize);
                ctx.stroke();
            }
        }

        // 1. 마디 없는 매끄러운 지렁이 그리기
        function drawSmoothSnake() {
            if (snake.length === 0) return;

            const radius = gridSize / 2;

            // [A] 마디 연결선 (두꺼운 선으로 선을 이어 마디 경계를 완전히 없앰)
            ctx.beginPath();
            ctx.lineCap = "round";
            ctx.lineJoin = "round";
            ctx.lineWidth = radius * 2 - 2; // 몸통 두께
            ctx.strokeStyle = "#4CAF50";    // 몸통 색상

            // 꼬리부터 머리까지 선 연결
            const headCenter = { x: snake[0].x * gridSize + radius, y: snake[0].y * gridSize + radius };
            ctx.moveTo(headCenter.x, headCenter.y);

            for (let i = 1; i < snake.length; i++) {
                const cx = snake[i].x * gridSize + radius;
                const cy = snake[i].y * gridSize + radius;
                ctx.lineTo(cx, cy);
            }
            ctx.stroke();

            // [B] 머리 디자인 (더 큰 원 + 눈)
            ctx.fillStyle = "#66BB6A";
            ctx.beginPath();
            ctx.arc(headCenter.x, headCenter.y, radius, 0, Math.PI * 2);
            ctx.fill();

            // 눈 위치 계산
            const eyeOffset = radius / 2;
            const eyeRadius = radius / 3.5;
            let eyeX1, eyeY1, eyeX2, eyeY2;

            if (dx === 1) { // 오른쪽
                eyeX1 = headCenter.x + eyeOffset; eyeY1 = headCenter.y - eyeOffset;
                eyeX2 = headCenter.x + eyeOffset; eyeY2 = headCenter.y + eyeOffset;
            } else if (dx === -1) { // 왼쪽
                eyeX1 = headCenter.x - eyeOffset; eyeY1 = headCenter.y - eyeOffset;
                eyeX2 = headCenter.x - eyeOffset; eyeY2 = headCenter.y + eyeOffset;
            } else if (dy === -1) { // 위
                eyeX1 = headCenter.x - eyeOffset; eyeY1 = headCenter.y - eyeOffset;
                eyeX2 = headCenter.x + eyeOffset; eyeY2 = headCenter.y - eyeOffset;
            } else { // 아래 또는 대기
                eyeX1 = headCenter.x - eyeOffset; eyeY1 = headCenter.y + eyeOffset;
                eyeX2 = headCenter.x + eyeOffset; eyeY2 = headCenter.y + eyeOffset;
            }

            // 눈 흰자 & 동공
            ctx.fillStyle = "#ffffff";
            ctx.beginPath(); ctx.arc(eyeX1, eyeY1, eyeRadius, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(eyeX2, eyeY2, eyeRadius, 0, Math.PI * 2); ctx.fill();

            ctx.fillStyle = "#000000";
            ctx.beginPath(); ctx.arc(eyeX1, eyeY1, eyeRadius / 2, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(eyeX2, eyeY2, eyeRadius / 2, 0, Math.PI * 2); ctx.fill();

            // [C] 꼬리 디자인 (끝부분을 살짝 다듬기)
            const tail = snake[snake.length - 1];
            const tailCenter = { x: tail.x * gridSize + radius, y: tail.y * gridSize + radius };
            ctx.fillStyle = "#388E3C";
            ctx.beginPath();
            ctx.arc(tailCenter.x, tailCenter.y, radius - 2, 0, Math.PI * 2);
            ctx.fill();
        }

        // 2. 사과 그리기 (빨간 열매 + 잎사귀 + 나뭇가지 + 발광 효과)
        function drawApple() {
            const cx = food.x * gridSize + gridSize / 2;
            const cy = food.y * gridSize + gridSize / 2;
            const radius = gridSize / 2 - 2;

            // 글로우(Glow) 효과
            ctx.shadowBlur = 12;
            ctx.shadowColor = "#FF5252";

            // 빨간 사과 몸통
            ctx.fillStyle = "#FF3333";
            ctx.beginPath();
            ctx.arc(cx, cy + 1, radius, 0, Math.PI * 2);
            ctx.fill();

            // 글로우 끄기 (다른 그림 영향 방지)
            ctx.shadowBlur = 0;

            // 광택 (하이라이트)
            ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
            ctx.beginPath();
            ctx.arc(cx - radius / 2.5, cy - radius / 2.5, radius / 3, 0, Math.PI * 2);
            ctx.fill();

            // 꼭지 (갈색 가지)
            ctx.strokeStyle = "#795548";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(cx, cy - radius);
            ctx.lineTo(cx + 2, cy - radius - 5);
            ctx.stroke();

            // 초록색 잎사귀
            ctx.fillStyle = "#4CAF50";
            ctx.beginPath();
            ctx.ellipse(cx + 5, cy - radius - 3, 4, 2, Math.PI / 4, 0, Math.PI * 2);
            ctx.fill();
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
            let validPosition = false;
            while (!validPosition) {
                food.x = Math.floor(Math.random() * tileCount);
                food.y = Math.floor(Math.random() * tileCount);
                
                validPosition = true;
                for (let part of snake) {
                    if (part.x === food.x && part.y === food.y) {
                        validPosition = false;
                        break;
                    }
                }
            }
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

        function drawGameOver() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = "#ff4b4b";
            ctx.font = "bold 60px 'Segoe UI'";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText("게임 오버!", canvas.width / 2, canvas.height / 2 - 30);
            
            ctx.fillStyle = "white";
            ctx.font = "30px 'Segoe UI'";
            ctx.fillText(`최종 점수: ${score}`, canvas.width / 2, canvas.height / 2 + 40);
        }

        function changeDirection(event) {
            const keyPressed = event.keyCode;
            const LEFT = 37, UP = 38, RIGHT = 39, DOWN = 40;

            if (!gameStarted && [LEFT, UP, RIGHT, DOWN].includes(keyPressed)) {
                gameStarted = true;
                isGameOver = false;
            }

            if (keyPressed === LEFT && dx !== 1) { dx = -1; dy = 0; }
            if (keyPressed === UP && dy !== 1) { dx = 0; dy = -1; }
            if (keyPressed === RIGHT && dx !== -1) { dx = 1; dy = 0; }
            if (keyPressed === DOWN && dy !== -1) { dx = 0; dy = 1; }
        }

        function resetGame() {
            clearInterval(gameInterval);
            snake = [
                { x: 10, y: 10 },
                { x: 9, y: 10 },
                { x: 8, y: 10 }
            ];
            dx = 1;
            dy = 0;
            score = 0;
            gameStarted = true;
            isGameOver = false;
            scoreElement.innerText = score;
            generateFood();
            
            clearCanvas();
            drawGrid();
            drawApple();
            drawSmoothSnake();
            
            gameInterval = setInterval(gameLoop, 100);
        }

        clearCanvas();
        drawGrid();
        drawGameOver();
        ctx.fillStyle = "white";
        ctx.font = "24px 'Segoe UI'";
        ctx.textAlign = "center";
        ctx.fillText("화살표 키를 눌러 게임 시작", canvas.width / 2, canvas.height / 2 + 100);

    </script>
</body>
</html>
"""

components.html(snake_game_html, height=800, scrolling=False)
