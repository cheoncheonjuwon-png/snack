import turtle
import time
import random

delay = 0.1
score = 0
high_score = 0

# 1. 화면 설정
wn = turtle.Screen()
wn.title("파이썬 지렁이 게임")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0) # 화면 갱신을 수동으로 설정

# 2. 지렁이 머리 설정
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# 3. 먹이 설정
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# 4. 몸통 리스트
segments = []

# 5. 점수판 설정
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("점수: 0  최고 점수: 0", align="center", font=("Courier", 18, "normal"))

# 6. 이동 함수
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# 7. 키보드 바인딩
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# 8. 메인 게임 루프
while True:
    wn.update()

    # 벽 충돌 체크
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # 몸통 제거
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        # 점수 초기화
        score = 0
        pen.clear()
        pen.write(f"점수: {score}  최고 점수: {high_score}", align="center", font=("Courier", 18, "normal"))

    # 먹이를 먹었을 때
    if head.distance(food) < 20:
        # 먹이 위치 이동
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        food.goto(x, y)

        # 몸통 추가
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        # 점수 증가
        score += 10
        if score > high_score:
            high_score = score

        pen.clear()
        pen.write(f"점수: {score}  최고 점수: {high_score}", align="center", font=("Courier", 18, "normal"))

    # 몸통 따라오게 하기 (뒤에서부터 앞 몸통의 위치로)
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # 자기 몸통 충돌 체크
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()

            score = 0
            pen.clear()
            pen.write(f"점수: {score}  최고 점수: {high_score}", align="center", font=("Courier", 18, "normal"))

    time.sleep(delay)

wn.mainloop()
