from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image
import random

radius , nslice , nstack = 10 , 20 , 20
left , right , bottom , top , near , far = -100 , 100 , -100 , 100 , 100 , -100

near_per , far_per = 1 , 401

w_width , w_height = 720 , 580
aspect = float(w_width) / w_height 

block_pos_bottomside = [[85,5,95],[75,5,95],[65,5,95],[55,5,95],[45,5,95],[35,5,95],[25,5,95],[15,5,95],[5,5,95],
             [-5,5,95],[-15,5,95],[-25,5,95],[-35,5,95],[-45,5,95],[-55,5,95],[-65,5,95],[-75,5,95],[-85,5,95]]

block_pos_topside = [[85,5,-95],[75,5,-95],[65,5,-95],[55,5,-95],[45,5,-95],[35,5,-95],[25,5,-95],[15,5,-95],[5,5,-95],
             [-5,5,-95],[-15,5,-95],[-25,5,-95],[-35,5,-95],[-45,5,-95],[-55,5,-95],[-65,5,-95],[-75,5,-95],[-85,5,-95]]

block_pos_leftside = [[-95,5,85],[-95,5,75],[-95,5,65],[-95,5,55],[-95,5,45],[-95,5,35],[-95,5,25],[-95,5,15],[-95,5,5],
                      [-95,5,-5],[-95,5,-15],[-95,5,-25],[-95,5,-35],[-95,5,-45],[-95,5,-55],[-95,5,-65],[-95,5,-75],[-95,5,-85]]

block_pos_rightside = [[95,5,85],[95,5,75],[95,5,65],[95,5,55],[95,5,45],[95,5,35],[95,5,25],[95,5,15],[95,5,5],
                      [95,5,-5],[95,5,-15],[95,5,-25],[95,5,-35],[95,5,-45],[95,5,-55],[95,5,-65],[95,5,-75],[95,5,-85]]
max_min = [-95,95,-85,85]

plain_block  =0
corner_edge_block = 0

current_pos = [0,10,0]
init_pos = [0,10,0]
direction = 1
accel = [5,-10]
play = False
l_hit_color , r_hit_color , t_hit_color , b_hit_color = False , False , False , False
c_top , c_bottom , c_left , c_right = 0 , 0 ,0 ,0
angle = 0
count_t , count_b , count_l , count_r = len(block_pos_topside) , len(block_pos_bottomside), len(block_pos_leftside), len(block_pos_rightside)

camera = [[0,170,230],[0,250,1]]
look = [0,0,0]
up = [0,1,0]
top_view = False

colors = [ 	[55/255, 66/255, 89/255],#0
          	[255/255,223/255,186/255],#1
            [255/255,255/255,186/255],#2
            [186/255,255/255,201/255],#3
            [186/255,225/255,255/255],#4
            [139/255,108/255,108/255],#5
            [161/255,131/255,131/255],#6
            [192/255,160/255,160/255],#7
            [211/255,179/255,179/255],#8
            [211/255,179/255,179/255],#9
            [236/255,202/255,202/255],#10
            [255/255,212/255,229/255],#11
            [238/255,203/255,255/255],#12
            [254/255,255/255,163/255],#13
            [219/255,220/255,255/255],#14
            [242/255,215/255,251/255],#15
            [255/255,232/255,222/255],#16
            [239/255,251/255,205/255],#17
            [255/255,250/255,192/255],#18
            [214/255,241/255,242/255],#19
            [120/255,223/255,185/255],#20
            [128/255,70/255,116/255],#21
            ]

start_color = [[214/255, 248/255, 184/255],
               [172/255, 222/255, 170/255],
               [143/255, 187/255, 175/255],
               [107/255, 123/255, 142/255],
              ]

vertices = [[-5.0,-5.0,-5.0	],[5.0,-5.0,-5.0], [-5.0,5.0,-5.0], [5.0,5.0,-5.0],  [-5.0,-5.0,5.0], [5.0,-5.0,5.0],  [-5.0,5.0,5.0],  [5.0,5.0,5.0]]
edges = [[0,2],[2,3],[3,1],[1,0],[0,4],[4,6],[6,2],[2,0],[0,1],[1,5],[5,4],[4,0],[7,6],[6,4],[4,5],[5,7],[7,3],[3,2],[2,6],[6,7],[7,5],[5,1],[1,3],[3,7]]
surfaces = [[0,2,3,1],[0,4,6,2],[0,1,5,4],[7,6,4,5],[7,3,2,6],[7,5,1,3]]

texture = 0
hit_top_position = [[0,0,0],[0,0,0]]
hit_bottom_position = [[0,0,0],[0,0,0]]
hit_left_position = [[0,0,0],[0,0,0]]
hit_right_position = [[0,0,0],[0,0,0]]

def LoadTextures(filename):
    #global texture
    image = Image.open(filename) 
    ix = image.size[0]
    iy = image.size[1]
    #image = image.tostring('raw','RGBX',0,-1)
    image = image.tobytes("raw", "RGBX")
    # Create Texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glMatrixMode(GL_TEXTURE)
    glLoadIdentity()
    glScalef(-1,1,1)


def reset():
    global current_pos , init_pos , play

    current_pos = [0,10,0]
    if play == True:
        play = False

def Sphere():
    global radius , nslice , nstack

    LoadTextures('hologram.jpg')

    
    glEnable(GL_TEXTURE_2D)

    glColor3f(1,0,0)
    glPushMatrix()
    glBegin(GL_QUAD_STRIP)
    for j in range(0,nstack+1):
        for i in range (0, nslice+1):
            u = float(i)/nslice
            v = float(j)/nstack
            theta = i*2*math.pi/nslice
            phi = j*math.pi/nstack
            sin_phi = math.sin(phi)
            sin_theta = math.sin(theta)
            cos_phi = math.cos(phi)
            cos_theta = math.cos(theta)

            x = radius*sin_phi*cos_theta
            y = radius*cos_phi
            z = radius*sin_phi*sin_theta
            glTexCoord2d(u,v)
            glVertex3f(x,y,z)
        
            v_plus = float(j+1)/nstack
            phi_plus = (j+1)*math.pi/nstack
            sin_phi_plus = math.sin(phi_plus)
            cos_phi_plus = math.cos(phi_plus)
            x = radius*sin_phi_plus*cos_theta
            y = radius*cos_phi_plus
            z = radius*sin_phi_plus*sin_theta
            glTexCoord2d(u,v_plus)
            glVertex3f(x,y,z)
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)

def polygon(color = [1,0,0] ,posx =0 ,posy=0 ,posz=0):
    glPushMatrix()
    glTranslatef(posx,posy,posz)
    glPushMatrix()
    glScalef(1.05,1.05,1.05)
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(0,0,0)
    for k in edges:
        for l in k:
            glVertex3fv(vertices[l])
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glBegin(GL_QUADS)
    for i in range(len(surfaces)):
        glColor3fv(color)
        for j in surfaces[i]:
             glVertex3fv(vertices[j])
    glEnd()
    glPopMatrix()
    glPopMatrix()

def plain():
    global max_min , plain_block
    plain_block =  glGenLists(1)

    glNewList(plain_block, GL_COMPILE)
    glPushMatrix()
    for i in range(max_min[2],max_min[3]+1,10):
        for j in range(max_min[2],max_min[3]+1,10):
            glPushMatrix()
            polygon(colors[21], i , -5 , j)
            glPopMatrix()
    glPopMatrix()

    for i in range(max_min[0], max_min[1]+1, 10):
        glPushMatrix()
        polygon(colors[0], i ,-5 ,max_min[1])
        glPopMatrix()

    for i in range(max_min[0], max_min[1]+1, 10):
        glPushMatrix()
        polygon(colors[0], i ,-5 ,max_min[0])
        glPopMatrix()

    for i in range(max_min[0], max_min[1]+1, 10):
        glPushMatrix()
        polygon(colors[0], max_min[0] ,-5 ,i)
        glPopMatrix()

    for i in range(max_min[0], max_min[1]+1, 10):
        glPushMatrix()
        polygon(colors[0], max_min[1] ,-5 ,i)
        glPopMatrix()
    glEndList()


def edge_blocks():
    global max_min, corner_edge_block
    corner_edge_block = glGenLists(2)

    glNewList(corner_edge_block, GL_COMPILE)
    glPushMatrix()
    polygon(colors[21] , max_min[1],5,max_min[1]) #bottom right
    polygon(colors[21] , max_min[0],5,max_min[1]) #bottom left
    polygon(colors[21] , max_min[0],5,max_min[0]) #top left
    polygon(colors[21] , max_min[1],5 ,max_min[0]) #top right
    glPopMatrix()
    glEndList()

def init():
    global left , right , bottom ,top , near ,far
    glClearColor(0,0,0,0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    plain()
    edge_blocks()
    Sphere()

def display():
    global aspect , colors  , c_top , c_bottom , c_left ,c_right
    global radius , max_min , angle , current_pos
    global count_b , count_t , count_l , count_r
    global hit_bottom_position , hit_top_position , hit_left_position , hit_right_position , direction
    global t_hit_color , b_hit_color , l_hit_color , r_hit_color , play
    global w_width , w_height , camera , look , up , top_view , start_color
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, aspect, near_per, far_per)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if top_view:
        gluLookAt(*camera[1],*look,*up)
    else:    
        gluLookAt(*camera[0],*look,*up)
    print(camera)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPolygonMode(GL_FRONT_AND_BACK , GL_FILL)

    glCallList(plain_block)
    # glCallList(corner_edge_block)


    if current_pos[0] >= max_min[1]-(radius+5): #right
       r_hit_color = True
       hit_right_position.append([current_pos[0]+(radius+5), current_pos[1], current_pos[2]+5])

    elif current_pos[2] >= max_min[1]-(radius+5): # bottom
       b_hit_color = True
       hit_bottom_position.append([current_pos[0]-5, current_pos[1], current_pos[2]+(radius+5)])

    elif current_pos[0] <= max_min[0]+(radius+5): # left
       l_hit_color = True
       hit_left_position.append([current_pos[0]-(radius+5), current_pos[1], current_pos[2]-5])

    elif current_pos[2] <= max_min[0]+(radius+5):  # top
       t_hit_color = True
       hit_top_position.append([current_pos[0]+5, current_pos[1], current_pos[2]-(radius+5)])

    else:
        l_hit_color = False
        r_hit_color = False
        t_hit_color = False
        b_hit_color = False

    if  c_top >= len(block_pos_bottomside) or c_bottom >= len(block_pos_bottomside) or c_left >= len(block_pos_leftside) or c_right >= len(block_pos_topside):
        c_top , c_bottom , c_left , c_right = 0 ,0,0,0
    if l_hit_color:
        c_left = random.randint(1,17)
    elif t_hit_color:
        c_top = random.randint(1,17)
    elif b_hit_color:
        c_bottom = random.randint(1,17)
    elif r_hit_color:
        c_right = random.randint(1,17)

    hit_bottom_position = [list(x) for x in set(tuple(x) for x in hit_bottom_position)]
    hit_top_position = [list(x) for x in set(tuple(x) for x in hit_top_position)]
    hit_right_position = [list(x) for x in set(tuple(x) for x in hit_right_position)]
    hit_left_position = [list(x) for x in set(tuple(x) for x in hit_left_position)]

    for i in block_pos_bottomside:
        if i in hit_bottom_position:
            polygon(colors[c_bottom] , *i)
            # hit_bottom_position.remove(hit_bottom_position[0])
        else:
            polygon(start_color[0] , *i)
        count_b -= 1

    for i in block_pos_topside:
        if i in hit_top_position:
            polygon(colors[c_top] , *i)
            # hit_top_position.remove(hit_top_position[0])
        else:
            polygon(start_color[1] , *i)
        count_t -= 1
    
    for i in block_pos_rightside:
        if i in hit_right_position:
            polygon(colors[c_right] , *i)
            # hit_right_position.remove(hit_right_position[0])
        else:
            polygon(start_color[2] , *i)
        count_r -= 1

    for i in block_pos_leftside:
        if i in hit_left_position:
            polygon(colors[c_left] , *i)
            # hit_left_position.remove(hit_left_position[0])
        else:
            polygon(start_color[3] , *i)
        count_l -= 1


    glTranslatef(*current_pos)
    glRotatef(angle, 1,0,1)
    Sphere()

    if angle == 360 or angle == -360:
        angle = 0

    if current_pos[0] > 95 or current_pos[0] < -95 or current_pos[2] > 95 or current_pos[2] < -95:
        reset()

    if count_t == 0:
        count_t = len(block_pos_topside)
    if count_b == 0:
        count_b = len(block_pos_bottomside)
    if count_l == 0:
        count_l = len(block_pos_leftside)
    if count_r == 0:
        count_r = len(block_pos_rightside)

    glFlush()
    glutSwapBuffers()

def keyboard(key,x,y):
    global play , camera , top_view , accel

    if key == b'p':
        play = not play
        if play == True:
            print("Rolling the ball")
        else:
            print("Ball stop Rolling")

    if key == b't':
        top_view = not top_view

    if key == b'f':
        accel[0] *= -1
        if accel[0] <= 0:
            accel[0] *= -1
    if key == b'e':
        accel[1] *= -1
        if accel[1] <= 0:
            accel[1] *= -1
    
    if key == b'r':
        reset()

    glutPostRedisplay()

def reshape(w,h):
    global left , right , bottom , top ,near , far

    glViewport(0,0,w,h)

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

    # glOrtho(left_a,right_a,bottom_a,top_a,near,far)
    glutPostRedisplay()

    w_width , w_height = w , h
    left , bottom = bottom_a , left_a
    top , right = right_a , top_a
    
def idle():
    global play , current_pos , accel , radius , c_box_color , angle , direction , radius

    if play:
        if current_pos[1] > 5:
            current_pos[1] -= 1
        angle += 10 * direction
        if current_pos[1] == 5:
            current_pos[0] += accel[0] 
            current_pos[2] -= accel[1]

    if current_pos[0] >= max_min[1]-(radius+5): #right
       accel[0] *= -1
       direction *= -1
    if current_pos[2] >= max_min[1]-(radius+5): #bottom
       accel[1] *= -1
       direction *= -1
    if current_pos[0] <= max_min[0]+(radius+5): #left
       accel[0] *= -1
       direction *= -1
    if current_pos[2] <= max_min[0]+(radius+5):     #top
       accel[1] *= -1
       direction *= -1

    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(w_width, w_height)
    glutInitWindowPosition(100,100)
    glutCreateWindow("Rolling Ball".encode())

    init()

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutMainLoop()

main()