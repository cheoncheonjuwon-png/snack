import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정 (넓게 보기 위해 wide 모드 사용)
st.set_page_config(page_title="프리미엄 지렁이 게임", page_icon="🐍", layout="wide")

st.title("🐍 프리미엄 지렁이 게임 (Premium Snake)")
st.write("키보드 **화살표 키(↑, ↓, ←, →)**를 사용하여 지렁이를 조종하세요!")

# 더 크고 화려한 HTML/JavaScript 게임 코드
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
            background-color: #0e1117; /* Streamlit 테마와 맞춤 */
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
            color: #4CAF50;
            text-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
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
        <!-- 캔버스 크기를 600x600으로 확대 -->
        <canvas id="gameCanvas" width="600" height="600"></canvas>
        <br>
        <button class="btn" onclick="resetGame()">게임 다시 시작</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");

        // 게임 설정
        const gridSize = 25; // 그리드 크기를 키워서 지렁이를 더 크게 함
        const tileCount = canvas.width / gridSize;

        // 게임 상태 변수
        let snake = [];
        let food = { x: 15, y: 15 };
        let dx = 0;
        let dy = 0;
        let score = 0;
        let gameInterval;
        let gameStarted = false;
        let isGameOver = false;

        document.addEventListener("keydown", changeDirection);

        // 둥근 사각형 그리기 함수 (지렁이 몸통용)
        function drawRoundedRect(x, y, width, height, radius, color) {
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.moveTo(x + radius, y);
            ctx.lineTo(x + width - radius, y);
            ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
            ctx.lineTo(x + width, y + height - radius);
            ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
            ctx.lineTo(x + radius, y + height);
            ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
            ctx.lineTo(x, y + radius);
            ctx.quadraticCurveTo(x, y, x + radius, y);
            ctx.closePath();
            ctx.fill();
        }

        // 원 그리기 함수 (지렁이 머리/꼬리, 먹이용)
        function drawCircle(x, y, radius, color) {
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fill();
        }

        function gameLoop() {
            if (!gameStarted || isGameOver) return;
            moveSnake();
            if (checkGameOver()) {
                isGameOver = true;
                drawGameOver();
                return;
            }
            clearCanvas();
            drawGrid(); // 배경 그리드 추가
            drawFood();
            drawSnake();
        }

        function clearCanvas() {
            ctx.fillStyle = "#1a1c23";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        // 배경에 은은한 그리드 그리기 (화려함 추가)
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

        function drawSnake() {
            snake.forEach((part, index) => {
                const centerX = part.x * gridSize + gridSize / 2;
                const centerY = part.y * gridSize + gridSize / 2;
                const radius = gridSize / 2 - 2;

                if (index === 0) {
                    // 머리: 가장 밝은 녹색 원 + 눈
                    drawCircle(centerX, centerY, radius + 2, "#81C784");
                    
                    // 눈 그리기 (이동 방향에 따라 위치 조정)
                    ctx.fillStyle = "#fff"; // 눈 흰자
                    const eyeOffset = radius / 2;
                    const eyeRadius = radius / 4;
                    
                    let eyeX1, eyeY1, eyeX2, eyeY2;
                    if (dx === 1) { // 우
                        eyeX1 = centerX + eyeOffset; eyeY1 = centerY - eyeOffset;
                        eyeX2 = centerX + eyeOffset; eyeY2 = centerY + eyeOffset;
                    } else if (dx === -1) { // 좌
                        eyeX1 = centerX - eyeOffset; eyeY1 = centerY - eyeOffset;
                        eyeX2 = centerX - eyeOffset; eyeY2 = centerY + eyeOffset;
                    } else if (dy === -1) { // 상
                        eyeX1 = centerX - eyeOffset; eyeY1 = centerY - eyeOffset;
                        eyeX2 = centerX + eyeOffset; eyeY2 = centerY - eyeOffset;
                    } else { // 하 (또는 정지)
                        eyeX1 = centerX - eyeOffset; eyeY1 = centerY + eyeOffset;
                        eyeX2 = centerX + eyeOffset; eyeY2 = centerY + eyeOffset;
                    }
                    drawCircle(eyeX1, eyeY1, eyeRadius, "#fff");
                    drawCircle(eyeX2, eyeY2, eyeRadius, "#fff");
                    drawCircle(eyeX1, eyeY1, eyeRadius/2, "#000"); // 눈동자
                    drawCircle(eyeX2, eyeY2, eyeRadius/2, "#000");

                } else if (index === snake.length - 1) {
                    // 꼬리: 몸통보다 약간 작고 어두운 녹색 원
                    drawCircle(centerX, centerY, radius - 3, "#2E7D32");
                } else {
                    // 몸통: 중간 녹색 둥근 사각형 (둥글게 표현)
                    const colorValue = 100 - (index * 3); // 뒤로 갈수록 살짝 어두워지는 효과
                    drawRoundedRect(part.x * gridSize + 2, part.y * gridSize + 2, gridSize - 4, gridSize - 4, 8, `hsl(122, 39%, ${Math.max(colorValue, 40)}%)`);
                }
            });
        }

        function drawFood() {
            const centerX = food.x * gridSize + gridSize / 2;
            const centerY = food.y * gridSize + gridSize / 2;
            const radius = gridSize / 2 - 2;

            // 먹이: 붉은색 원 + 빛나는 효과(Glow)
            ctx.shadowBlur = 15;
            ctx.shadowColor = "#FF5252";
            drawCircle(centerX, centerY, radius, "#FF5252");
            ctx.shadowBlur = 0; // 다른 그림에는 효과 없도록 초기화
        }

        function moveSnake() {
            const head = { x: snake[0].x + dx, y: snake[0].y + dy };
            snake.unshift(head);

            // 먹이 충돌
            if (head.x === food.x && head.y === food.y) {
                score += 10;
                scoreElement.innerText = score;
                generateFood();
            } else {
                snake.pop(); // 먹지 않았으면 꼬리 자르기
            }
        }

        function generateFood() {
            // 지렁이 몸 위에 생성되지 않도록 루프 돌며 위치 확인
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
            // 벽 충돌
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                return true;
            }
            // 자기 몸 충돌
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

            // 게임 시작
            if (!gameStarted && [LEFT, UP, RIGHT, DOWN].includes(keyPressed)) {
                gameStarted = true;
                isGameOver = false;
            }

            // 반대 방향 이동 금지 로직 포함
            if (keyPressed === LEFT && dx !== 1) { dx = -1; dy = 0; }
            if (keyPressed === UP && dy !== 1) { dx = 0; dy = -1; }
            if (keyPressed === RIGHT && dx !== -1) { dx = 1; dy = 0; }
            if (keyPressed === DOWN && dy !== -1) { dx = 0; dy = 1; }
        }

        function resetGame() {
            clearInterval(gameInterval);
            // 초기 위치 및 지렁이 길이(3칸) 설정
            snake = [
                { x: 10, y: 10 },
                { x: 9, y: 10 },
                { x: 8, y: 10 }
            ];
            dx = 1; // 시작할 때 우측으로 이동
            dy = 0;
            score = 0;
            gameStarted = true; // 버튼 누르면 바로 시작
            isGameOver = false;
            scoreElement.innerText = score;
            generateFood();
            
            clearCanvas();
            drawGrid();
            drawFood();
            drawSnake();
            
            // 게임 속도 (100ms)
            gameInterval = setInterval(gameLoop, 100);
        }

        // 초기 화면 그리기
        clearCanvas();
        drawGrid();
        drawGameOver(); // 시작 전 화면
        ctx.fillStyle = "white";
        ctx.font = "24px 'Segoe UI'";
        ctx.textAlign = "center";
        ctx.fillText("화살표 키를 눌러 게임 시작", canvas.width / 2, canvas.height / 2 + 100);

    </script>
</body>
</html>
"""

# Streamlit 화면에 HTML 컴포넌트 렌더링
# 캔버스 600 + 여백 고려하여 높이 설정
components.html(snake_game_html, height=800, scrolling=False)
