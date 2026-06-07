from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

W, H = 865, 600

ball_x, ball_y = 400.0, 150.0
dx, dy = 3.0, 3.0
radius = 10.0

paddle_x = 350.0
paddle_w = 100.0
paddle_h = 12.0
paddle_y = 30.0

COLS, ROWS = 10, 4
brick_w = 70
brick_h = 20
brick_gap = 8
bricks = []

colors = [
    (1.0, 0.3, 0.3),
    (1.0, 0.7, 0.2),
    (0.3, 0.9, 0.3),
    (0.3, 0.6, 1.0),
]

for row in range(ROWS):
    for col in range(COLS):
        x = 45 + col * (brick_w + brick_gap)
        y = H - 80 - row * (brick_h + brick_gap)
        bricks.append([x, y, True, colors[row]])

score = 0
game_over = False
won = False


def draw_rect(x, y, w, h):
    glBegin(GL_QUADS)  # কী করছে: চারকোণা shape আঁকা শুরু করছে
    glVertex2f(x, y)
    glVertex2f(x+w, y)
    glVertex2f(x+w, y+h)
    glVertex2f(x, y+h)
    glEnd()


def draw_circle(cx, cy, r):
    glBegin(GL_TRIANGLE_FAN)  # কী করছে: center থেকে চারদিকে triangle দিয়ে circle বানাচ্ছে
    glVertex2f(cx, cy)
    for i in range(361):
        a = math.radians(i)  # কেন লাগছে: degree কে radian এ convert করতে হয় cos/sin এর জন্য
        glVertex2f(cx + r*math.cos(a), cy + r*math.sin(a))
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)  # কী করছে: আগের frame মুছে নতুন করে আঁকার জন্য screen clear করছে

    glColor3f(0.05, 0.05, 0.15)  # কী করছে: background এর dark color set করছে
    draw_rect(0, 0, W, H)  # real world-এ এটা কোথায় দেখা যায়: সব game এ background এভাবে fill করা হয়

    for b in bricks:
        if b[2]:
            glColor3f(*b[3])  # কী করছে: প্রতিটা brick এর নিজের color set করছে
            draw_rect(b[0], b[1], brick_w, brick_h)  # কেন লাগছে: brick আর paddle দুইটাই rectangle

    glColor3f(0.4, 0.8, 1.0)
    draw_rect(paddle_x, paddle_y, paddle_w, paddle_h)  # কী করছে: paddle আঁকছে নিচে

    glColor3f(1.0, 1.0, 1.0)
    draw_circle(ball_x, ball_y, radius)  # কী করছে: ball আঁকছে current position এ

    glutSwapBuffers()  # real world-এ এটা কোথায় দেখা যায়: double buffering সব modern game এ use হয় flickering বন্ধ করতে


def update(value):
    global ball_x, ball_y, dx, dy, score, game_over, won

    if game_over or won:
        glutPostRedisplay()
        glutTimerFunc(16, update, 0)
        return

    ball_x += dx  # কী করছে: ball কে x direction এ move করাচ্ছে
    ball_y += dy  # কী করছে: ball কে y direction এ move করাচ্ছে

    if ball_x - radius <= 0 or ball_x + radius >= W:
        dx = -dx  # কী করছে: বাম বা ডান দেয়ালে লাগলে horizontal direction উল্টে দিচ্ছে

    if ball_y + radius >= H:
        dy = -dy  # কী করছে: উপরের দেয়ালে লাগলে vertical direction উল্টে দিচ্ছে

    if ball_y - radius <= 0:
        game_over = True  # কেন লাগছে: ball নিচে পড়ে গেলে game শেষ

    if (paddle_y <= ball_y - radius <= paddle_y + paddle_h and
            paddle_x <= ball_x <= paddle_x + paddle_w):
        dy = abs(dy)  # কী করছে: paddle এ লাগলে ball কে উপরে পাঠাচ্ছে | real world-এ এটা কোথায় দেখা যায়: physics engine এ collision response এভাবেই কাজ করে

    for b in bricks:
        if not b[2]:
            continue
        bx, by = b[0], b[1]
        if bx <= ball_x <= bx + brick_w and by <= ball_y <= by + brick_h:
            b[2] = False  # কী করছে: brick টা hide করে দিচ্ছে, মানে ভেঙে গেছে
            dy = -dy  # কেন লাগছে: brick এ লাগলে ball bounce করবে
            score += 1  # real world-এ এটা কোথায় দেখা যায়: সব game এ score এভাবে event এর সময় বাড়ানো হয়

    if all(not b[2] for b in bricks):
        won = True  # কী করছে: সব brick ভাঙলে জিতে গেছে বলে mark করছে

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)  # কেন লাগছে: 16ms পর আবার update চালাবে, মানে ~60fps animation


def keyboard(key, x, y):
    global paddle_x
    if key == b'a' and paddle_x > 0:
        paddle_x -= 20  # কী করছে: A চাপলে paddle বামে সরাচ্ছে
    if key == b'd' and paddle_x + paddle_w < W:
        paddle_x += 20  # কী করছে: D চাপলে paddle ডানে সরাচ্ছে | real world-এ এটা কোথায় দেখা যায়: সব game এ player movement এভাবে keyboard input দিয়ে হয়


def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W, 0, H)  # কী করছে: 2D coordinate system set করছে, bottom-left (0,0) থেকে top-right (800,600)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W, H)
glutCreateWindow(b"Brick Breaker - Press A/D to move paddle")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(16, update, 0)
glutMainLoop()
