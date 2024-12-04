import cv2
import mediapipe as mp
import numpy as np
import random as rng
import time


class Wall:
    def __init__(self, height, w, breakable, color, y):
        self.height = height
        self.width = w
        self.breakable = breakable
        self.color = color
        self.x = 640 #640x480
        self.y = y
        self.open = False


    def update(self):
        self.x -= 10
        if self.x <= self.width * -1:
            send_delete_request()
        check = self.check_collide()
        if check is True:
            if self.breakable is True:
                if prev_fist is True:
                    if not self.open:
                        self.open = True
                elif self.open is False:
                    #pass
                    send_death_request()
            else:
                #pass
                send_death_request()




    def check_collide(self):
        a = False
        for i in get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape):
            if self.x <= i[0] <= self.x + self.width:
                if self.y <= i[1] <= self.y + self.height:
                    a = True
        if a:
            return True
        else:
            return False


class Coin:
    def __init__(self, y):
        self.height = 30
        self.width = 30
        self.color = (255, 255, 0)
        self.x = 640 #640x480
        self.y = y
        self.open = False


    def update(self):
        self.x -= 10
        if self.x <= self.width * -1:
            send_delete_request()
        check = self.check_collide()
        if check is True:
            if self.open is False:
                send_point_request()
                self.open = True


    def check_collide(self):
        a = False
        for i in get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape):
            if self.x <= i[0] <= self.x + self.width:
                if self.y <= i[1] <= self.y + self.height:
                    a = True
        if a:
            return True
        else:
            return False


def send_delete_request():
    inp = open('comms.txt', 'a')
    inp.write('DELETE_WALL\n')
    inp.close()
    inp = open('logs.txt', 'a')
    inp.write('DELETE_WALL request sent\n')


def send_point_request():
    inp = open('comms.txt', 'a')
    inp.write('GIVE_POINTS\n')
    inp.close()
    inp = open('logs.txt', 'a')
    inp.write('GIVE_POINTS request sent\n')


def send_death_request():
    inp = open('comms.txt', 'a')
    inp.write('KILL_PLAYER\n')
    inp.close()
    inp = open('logs.txt', 'a')
    inp.write('KILL_PLAYER request sent\n')


def satistfy_requests():
    include: walllist
    global count
    r = open('comms.txt', 'r')
    for i in r.readlines():
        if i == 'DELETE_WALL\n':
            walllist.remove(walllist[0])
        elif i == 'GIVE_POINTS\n':
            count += 1
        elif i == 'KILL_PLAYER\n':
            cap.release()
    r.close()
    deleter = open('comms.txt', 'w')
    deleter.close()
    inp = open('logs.txt', 'a')
    inp.write('REQUESTS SATISTFIED\n')


def get_points(landmark, shape):
    points = []
    for mark in landmark:
        points.append([mark.x * shape[1], mark.y * shape[0]])
    return np.array(points, dtype=np.int32)

def palm_size(landmark, shape):
    x1, y1 = landmark[0].x * shape[1], landmark[0].y * shape[0]
    x2, y2 = landmark[5].x * shape[1], landmark[5].y * shape[0]
    return ((x1 - x2)**2 + (y1 - y2) **2) **.5


#Log cleaning
deleter = open('logs.txt', 'w')
deleter.close()
deleter = open('comms.txt', 'w')
deleter.close()
#Inputs, inputted vars and intro here :^)
max_gap = 0
min_gap = 0
while True:
    print('Welcome to SnakyHand! Let me explain the rules.')
    print('Your goal is to collect yellow coins and avoid the walls.')
    print('You have to do this with your hand.')
    print('Some walls are gray and can be broken with a fist (you will see the circle around your hand turn green)')
    print('The game checks if the red is on the walls, so do not allow anyone hijack your controls :)')
    print('Also, if you ignore the instuctions below, I will stick you in an infinite loop!')
    diff = input('Choose your difficulty (0-noob, 1-easy, 2-medium, 3-hard, 4-DOOM): ')
    if diff.isdigit() is True:
        if 0 <= int(diff) <= 4:
            diff = int(diff)
            if diff == 0:
                max_gap = 120
                min_gap = 100
                spawn_timer = 100
            elif diff == 1:
                max_gap = 100
                min_gap = 80
                spawn_timer = 80
            elif diff == 2:
                max_gap = 80
                min_gap = 60
                spawn_timer = 60
            elif diff == 3:
                max_gap = 60
                min_gap = 40
                spawn_timer = 60
            else:
                max_gap = 40
                min_gap = 20
                spawn_timer = 30
            break
max_gapspawn = 480 - max_gap
#создаем детектор
handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
count = 0
prev_fist = False
finger_list = []
wall_timer = spawn_timer
coin_timer = int(spawn_timer * 1.5)
walllist = []
while(cap.isOpened()):
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    # переводим его в формат RGB для распознавания
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    # Распознаем
    results = handsDetector.process(flippedRGB)
    # Рисуем распознанное, если распозналось
    if results.multi_hand_landmarks is not None:
        for i in walllist:
            i.update()
        for i in results.multi_hand_landmarks[0].landmark:
            finger_list.append((int(i.x) * flippedRGB.shape[1], int(i.y) * flippedRGB.shape[0]))
        cv2.drawContours(flippedRGB, [get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)], 0, (255, 0, 0), 2)
        (x, y), r = cv2.minEnclosingCircle(get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape))
        ws = palm_size(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)
        if 2 * r / ws > 1.4:
             cv2.circle(flippedRGB,(int(x), int(y)), int(r), (0, 0, 255), 2)
             # кулак разжат
             prev_fist = False
        else:
             cv2.circle(flippedRGB,(int(x), int(y)), int(r), (0, 255, 0), 2)
             if not prev_fist:
                 # Сейчас кулак зажат
                 prev_fist = True
        # The timer is ticking...
        wall_timer -= 1
        coin_timer -= 1
        #Wall spawns if hand in screen cuz otherwise it will bug out
        if wall_timer == 0:
            wall_timer = spawn_timer
            wallthick = rng.randint(10, 50)
            gapstart = rng.randint(10, max_gapspawn)
            gaplen = rng.randint(60, 80)
            gapfull = rng.randint(0, 1)
            walllist.append(Wall(gapstart, wallthick, False, (0, 0, 255), 0))
            walllist.append(Wall(530 - gapstart - gaplen, wallthick, False, (0, 0, 255), gapstart + gaplen))
            if gapfull == 1:
                walllist.append(Wall(gaplen, wallthick, True, (128, 128, 128), gapstart))
        if coin_timer == 0:
            coin_timer = spawn_timer
            walllist.append(Coin(rng.randint(30, 420)))
    #Walls drawn lmao
    for i in walllist:
        if not i.open:
            cv2.rectangle(flippedRGB, (i.x, i.y), (i.x + i.width, i.y + i.height), i.color, -1)
    # Рисуем наш результат в каждом кадре, даже если рука не детектировалась
    cv2.putText(flippedRGB, str(count), (0, 45), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=2)

    # переводим в BGR и показываем результат
    res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow("Hands", res_image)

    #Memory cleaner
    satistfy_requests()

# освобождаем ресурсы
handsDetector.close()
#Results
print('You have scored ' + str(count) + ' points. Yay!')
