from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

w_width , w_height = 750,600
left , right , bottom , top , near , far = -61 , 61 , -61 , 61 , 50 , -50
half_bottom = -3

aspect = float(w_width) / w_height 

count_hit = 0

bar_len = 15
bar_width = bar_len * 2
bar_height = 3
start_pos = [0,bottom+2.5]
cur_pos = [0,bottom+2.5]
accel = 0.1
bar_vel = 3

radius = 3
start_ball_pos = [0,bottom+7.5]
cur_ball_pos = [0,bottom+7.5]
vel = [0.75,0.75]

block_pos = []
block_len = 3

status_play = False

color_bucket = [[185/255, 243/255, 228/255],
                [234/255, 143/255, 234/255],
                [255/255, 170/255, 207/255],
                [246/255, 230/255, 194/255],
                [234/255, 199/255, 199/255],
                [160/255, 195/255, 210/255],
                [247/255, 245/255, 235/255],
                [234/255, 224/255, 218/255],
                [255/255, 179/255, 179/255],
                [255/255, 219/255, 164/255],
                [255/255, 233/255, 174/255],
                [193/255, 239/255, 255/255],
                [104/255, 103/255, 172/255],
                [162/255, 103/255, 172/255],
                [206/255, 123/255, 176/255],
                [255/255, 188/255, 209/255],
               ]

def init():
    global left , right , bottom ,top , near ,far
    glClearColor(0.2,0.2,0.2,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(left,right,bottom,top, near , far)
    glShadeModel(GL_SMOOTH)

def generate_block():
    for i in range(left+4, right-2, 6):
        for j in range(half_bottom, top, 6):
            block_pos.append([i, j])

def background():
    global left, right , bottom , top
    
    glColor3fv(color_bucket[15])
    glBegin(GL_QUADS)
    glVertex2f(left,top)
    glVertex2f(right,top)
    glVertex2f(right,bottom)
    glVertex2f(left,bottom)
    glEnd()

def display_blocks():
    global color_bucket
    for pos in block_pos:
        if pos[1] == half_bottom:
            glColor3fv(color_bucket[0])
        if pos[1] == half_bottom+6:
            glColor3fv(color_bucket[1])
        if pos[1] == half_bottom+12:
            glColor3fv(color_bucket[2])
        if pos[1] == half_bottom+18:
            glColor3fv(color_bucket[3])
        if pos[1] == half_bottom+24:
            glColor3fv(color_bucket[4])
        if pos[1] == half_bottom+30:
            glColor3fv(color_bucket[5])
        if pos[1] == half_bottom+36:
            glColor3fv(color_bucket[6])
        if pos[1] == half_bottom+42:
            glColor3fv(color_bucket[7])
        if pos[1] == half_bottom+48:
            glColor3fv(color_bucket[8])
        if pos[1] == half_bottom+54:
            glColor3fv(color_bucket[9])
        if pos[1] == half_bottom+60:
            glColor3fv(color_bucket[10])
        if pos[1] == half_bottom+66:
            glColor3fv(color_bucket[11])
        glPushMatrix()
        glTranslatef(pos[0], pos[1], 0)
        glBegin(GL_QUADS)
        glVertex2f(-3, -3)
        glVertex2f(-3, 3)
        glVertex2f(3, 3)
        glVertex2f(3, -3)
        glEnd()
        
        glLineWidth(3)
        glColor3f(0,0,0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(-3, -3)
        glVertex2f(-3, 3)
        glVertex2f(3, 3)
        glVertex2f(3, -3)
        glEnd()


        glPopMatrix()


def ball():
    global radius ,cur_ball_pos
    glColor3fv(color_bucket[13])
    glBegin(GL_POLYGON)
    for i in range(360):
        theta = i * 2 * np.pi / 360
        x = radius * np.cos(theta) + cur_ball_pos[0]
        y = radius * np.sin(theta) + cur_ball_pos[1]
        glVertex2f(x,y)
    glEnd()

    glColor3f(0,0,0)
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        theta = i * 2 * np.pi / 360
        x = radius * np.cos(theta) + cur_ball_pos[0]
        y = radius * np.sin(theta) + cur_ball_pos[1]
        glVertex2f(x,y)   
    glEnd()

def bar():
    global bar_len , bar_width , bar_height
    glColor3fv(color_bucket[12])
    glBegin(GL_QUADS)
    glVertex2f(-bar_len,-1.5)
    glVertex2f(-bar_len,1.5)
    glVertex2f(bar_len , 1.5)
    glVertex2f(bar_len , -1.5)
    glEnd()

    glColor3f(0,0,0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-bar_width / 2, -bar_height / 2)
    glVertex2f(-bar_width / 2, bar_height / 2)
    glVertex2f(bar_width / 2, bar_height / 2)
    glVertex2f(bar_width / 2, -bar_height / 2)
    glEnd()

def table():
    global left, right ,top , bottom
    glColor3f(0,0,1)

    glBegin(GL_QUADS)
    glVertex2f(-3,-3)
    glVertex2f(-3,3)
    glVertex2f(3,3)
    glVertex2f(3,-3)
    glEnd()

    glBegin(GL_LINES)
    for i in range(left+1, right+1 , 3):
        if i == 0 :
            glColor3f(0,1,0)
        else:
            glColor3f(0.5,0,0)
        glVertex2f(left , i)
        glVertex2f(right , i)
    glEnd()

    glBegin(GL_LINES)
    for i in range(bottom+1, top+1 , 3):
        if i == 0 :
            glColor3f(0,1,0)
        else:
            glColor3f(0.5,0,0)
        glVertex2f(i , bottom)
        glVertex2f(i, top)
    glEnd()

def border_box():
    global left , right , bottom , top
    glColor3f(0,0,0)
    glBegin(GL_QUADS)
    glVertex2f(left,top)
    glVertex2f(left,bottom)
    glVertex2f(left+1,bottom)
    glVertex2f(left+1,top)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(right,top)
    glVertex2f(right,bottom)
    glVertex2f(right-1,bottom)
    glVertex2f(right-1,top)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(right,top)
    glVertex2f(right,top-1)
    glVertex2f(left,top-1)
    glVertex2f(left,top)
    glEnd()

def display():
    global cur_pos , cur_ball_pos , count_hit

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    background()
    # table()

    glPushMatrix()
    display_blocks()
    glPopMatrix()
         
    ball()

    glPushMatrix()
    glTranslatef(*cur_pos,0)
    bar()
    glPopMatrix()

    border_box()

    if count_hit >= 10 and count_hit % 10 == 0:
         if vel[0] < 0:
            vel[0] -= 0.001
         elif vel[0] > 0:
            vel[0] += 0.001
         if vel[1] < 0:
            vel[1] -= 0.001
         elif vel[1] > 0:
            vel[1] += 0.001

    glFlush()
    glutSwapBuffers()
    glMatrixMode(GL_PROJECTION)

def reshape(w,h):
    global left , right , bottom , top ,near , far

    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect = float(w)/h
    k = (right-left) / (top-bottom)
    left_a = left
    right_a = right
    top_a = top
    bottom_a = bottom

    if aspect >= 1:
        left_a = aspect * left
        right_a = aspect * right
    else:
        top_a = top / aspect 
        bottom_a = bottom / aspect

    if k >= 1:
        left_a /= k
        right_a /= k
    else :
        top_a *= k
        bottom_a *= k

    glOrtho(left_a,right_a,bottom_a,top_a,near,far)
    glutPostRedisplay()
    w_width , w_height = w , h

def special(key,x,y):
    global cur_pos , left, right , bar_len , cur_ball_pos , radius , status_play
    global accel , bar_vel

    if status_play == False:
        if key == GLUT_KEY_LEFT:
            bar_vel += accel
            cur_pos[0] -= 2.5 * bar_vel
            cur_ball_pos[0] -= 2.5 * bar_vel
            if cur_pos[0] - bar_len <= left+1.5:
                cur_pos[0] = left + 1.5 + bar_len
                cur_ball_pos[0] = left + 1.5 + bar_len

        if key == GLUT_KEY_RIGHT:
            bar_vel += accel
            cur_pos[0] += 2.5 * bar_vel
            cur_ball_pos[0] += 2.5 * bar_vel
            if cur_pos[0]+bar_len >= right-1.5:
                cur_pos[0] = right - 1.5 - bar_len
                cur_ball_pos[0] = right - 1.5 - bar_len 
    
    else:
        if key == GLUT_KEY_LEFT:
            bar_vel += accel
            cur_pos[0] -= 2.5 * bar_vel
            if cur_pos[0] - bar_len <= left+1.5:
                cur_pos[0] = left + 1.5 + bar_len

        if key == GLUT_KEY_RIGHT:
            bar_vel += accel
            cur_pos[0] += 2.5 * bar_vel
            if cur_pos[0]+bar_len >= right-1.5:
                cur_pos[0] = right - 1.5 - bar_len

    glutPostRedisplay()

def check_collision(cur_ball_pos, bar_pos, bar_width, bar_height, radius):
    bar_left = bar_pos[0] - bar_width / 2
    bar_right = bar_pos[0] + bar_width / 2
    bar_top = bar_pos[1] + bar_height / 2
    bar_bottom = bar_pos[1] - bar_height / 2

    if (
        cur_ball_pos[0] + radius >= bar_left
        and cur_ball_pos[0] - radius <= bar_right
        and cur_ball_pos[1] + radius >= bar_bottom
        and cur_ball_pos[1] - radius <= bar_top
    ):
        return True
    return False

def distance(pos1,pos2):
    return np.linalg.norm(np.array(pos1) - np.array(pos2))
def check_block_collision(ball_pos , block_pos , radius , block_len):
    return distance(ball_pos , block_pos) < (radius + block_len)

def reset():
    global status_play , cur_ball_pos , cur_pos
    global start_ball_pos , start_pos , bar_vel , count_hit
    
    status_play = False
    cur_pos = list(start_pos)
    cur_ball_pos = list(start_ball_pos)
    bar_vel = 3
    count_hit = 0
    block_pos.clear()
    generate_block()

def idle():
    global ball_speed , cur_ball_pos , vel , status_play , bar_len
    global left , right , top , bar_width , bar_height , block_pos , block_len
    global count_hit

    if status_play:

        cur_ball_pos[0] += vel[0]
        cur_ball_pos[1] += vel[1]

        if cur_ball_pos[1] + radius <= bottom:
            reset()

        if cur_ball_pos[0] + radius >= right or cur_ball_pos[0] - radius <= left:
            vel[0] *= -1

        if cur_ball_pos[1] + radius >= top:
            vel[1] *= -1

        if check_collision(cur_ball_pos, cur_pos, bar_width, bar_height, radius):
            vel[1] *= -1 

        for pos in block_pos:
            if check_block_collision(cur_ball_pos , pos , radius , block_len):
                block_pos.remove(pos)
                vel[1] *= -1
                count_hit += 1

    glutPostRedisplay()

def keyboard(key,x,y):
    global status_play
    if key == b'p':
        status_play = True

    glutPostRedisplay()

def up_special(key, x, y):
    global bar_vel

    if key in [GLUT_KEY_LEFT, GLUT_KEY_RIGHT]:
        bar_vel = 3

    glutPostRedisplay()
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(w_width, w_height)
    glutInitWindowPosition(300,100)
    glutCreateWindow("Shooter".encode())

    init()
    generate_block()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutSpecialFunc(special)
    glutSpecialUpFunc(up_special)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    glutMainLoop()

main()