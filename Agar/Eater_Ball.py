from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random


w_width , w_height = 500,500
left , right , bottom , top , near , far = int(-w_width/2) , int(w_width/2) , int(-w_height/2) , int(w_height/2) , 50 , -50

aspect = float(w_width) / w_height 

mouse_velocity = [0.0,0.0]

vel = [0,0]
ball_pos = np.array([0.0,0.0])

num_food = 50
food_r = 15
food_pos = []

zoom = 1

ball_size = 30

PASTEL_PINK = [242/255, 190/255, 209/255]

color_list = [[178/255, 164/255, 255/255],[255/255, 180/255, 180/255],[255/255, 222/255, 180/255],[253/255, 247/255, 195/255],[204/255, 213/255, 174/255],
              [233/255, 237/255, 201/255],[254/255, 237/255, 205/255],[255/255, 222/255, 180/255],[250/255, 247/255, 240/255],[205/255, 252/255, 246/255],
              [188/255, 206/255, 248/255],[152/255, 168/255, 248/255],[85/255, 73/255, 148/255],[246/255, 117/255, 168/255],[242/255, 147/255, 147/255],
              [255/255, 212/255, 178/255],[255/255, 246/255, 206/255],[206/255, 237/255, 199/255],[134/255, 200/255, 188/255],[242/255, 147/255, 147/255],
              [255/255, 248/255, 234/255],[158/255, 118/255, 118/255],[129/255, 91/255, 91/255],[89/255, 69/255, 69/255],[120/255, 149/255, 178/255],]

def generate_food():
    global food_r
    for _ in range(num_food):
        x = random.uniform(-w_width ,w_width)
        y = random.uniform(-w_height, w_height)
        food_pos.append([round(x,1), round(y,1)])

def draw_Food(pos_x, pos_y , *color_ball):
    global food_pos , food_r

    glColor3fv(color_ball)
    glBegin(GL_POLYGON)
    for i in range(360): 
        theta = i * 2 * np.pi / 360
        x = food_r * np.cos(theta) + pos_x
        y = food_r * np.sin(theta) + pos_y
        glVertex2f(x,y)
    glEnd()

def update(mouseX,mouseY):
    global vel
    vel = np.array([mouseX - w_width /2 , mouseY - w_height/2])
    vel /= np.linalg.norm(vel)
    vel *= 3

def blob():
    global ball_size
    glColor3fv(PASTEL_PINK)
    glBegin(GL_POLYGON)
    for i in range(360):
        theta = i * 2 * np.pi / 360
        x = ball_size * np.cos(theta) + ball_pos[0]
        y = ball_size * np.sin(theta) + ball_pos[1]
        glVertex2f(x,y)
    glEnd()

def init():
    global left , right , bottom ,top , near ,far
    glClearColor(0.0,0.0,0.0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(left,right,bottom,top, near , far)
    glShadeModel(GL_SMOOTH)

def lerp(a, b, t):
    return (1 - t) * a + t * b

def display():
    global aspect , move_direc , angle , direc , num_food , move_x , move_z
    global cam_x , cam_y , zoom

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    new_zoom = 30 /ball_size
    zoom = lerp(zoom , new_zoom , 0.1)
    glScalef(zoom, zoom , 0)
    glTranslatef(-ball_pos[0],-ball_pos[1],0)
    

    for pos, color  in zip(food_pos , color_list):
        if color == len(color_list):
            color = 0
        draw_Food(*pos , *color)

    blob()

    glFlush()
    glutSwapBuffers()
    glMatrixMode(GL_PROJECTION)

def mouse_motion(x,y):
    update(x, w_height-y)
    glutPostRedisplay()

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

def distance(pos1,pos2):
    return np.linalg.norm(np.array(pos1) - np.array(pos2))

def check_collision(blob_pos, food_pos , blob_size , food_size):
    return distance(blob_pos , food_pos) < (blob_size + food_size)

def update_ball_pos():
    global ball_pos , vel , food_pos , food_r  , ball_size
    ball_pos[0] += vel[0]
    ball_pos[1] += vel[1]
    for pos in food_pos:
        if check_collision(ball_pos , pos , ball_size  , food_r):
            food_pos.remove(pos)
            sum = np.pi * ball_size * ball_size + np.pi * food_r * food_r
            ball_size = np.sqrt(sum / np.pi)
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(w_width, w_height)
    glutInitWindowPosition(100,100)
    glutCreateWindow("BLOB".encode())

    init()

    generate_food()
    glutDisplayFunc(display)
    glutIdleFunc(update_ball_pos)
    glutPassiveMotionFunc(mouse_motion)
    glutReshapeFunc(reshape)
    glutMainLoop()

main()