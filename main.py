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
        self.x = vwidth #640x480
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
        self.x = vwidth #640x480
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


class AntiCheat:
    def __init__(self, x, y, w, h, color):
        self.height = h
        self.width = w
        self.color = color
        self.x = x
        self.y = y


    def update(self):
        check = self.check_collide()
        if check is True:
           send_death_request()


    def check_collide(self):
        a = False
        if str(type(results.multi_hand_landmarks)) == "<class 'NoneType'>":
            return False
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
    print("By the way, you can pause by not having your hand in your camera's view.")
    print('Be careful tho, only get outside or inside through the left side of the board.')
    print('Also, if you ignore the instuctions below, I will stick you in an infinite loop!')
    diff = input('Choose your difficulty (0-noob, 1-easy, 2-medium, 3-hard, 4-DOOM): ')
    if diff.isdigit() is True:
        if 0 <= int(diff) <= 4:
            diff = int(diff)
            if diff == 0:
                spawn_timer = 100
            elif diff == 1:
                spawn_timer = 80
            elif diff == 2 or diff == 3:
                spawn_timer = 60
            else:
                spawn_timer = 30
            break
#создаем детектор
handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
count = 0
prev_fist = False
finger_list = []
wall_timer = 1
coin_timer = int(spawn_timer * 0.5)
walllist = []
diff = int(diff)
r = 0
anti_cheat_list = []
while(cap.isOpened()):
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    vheight, vwidth = frame.shape[:2]
    if diff == 0:
        max_gap = vheight // 2
        min_gap = vheight // 3
    elif diff == 1:
        max_gap = vheight // 3
        min_gap = vheight // 4
    elif diff == 2:
        max_gap = vheight // 4
        min_gap = vheight // 5
    elif diff == 3:
        max_gap = vheight // 5
        min_gap = vheight // 6
    else:
        max_gap = vheight // 6
        min_gap = vheight // 7
    #Anti-cheat
    if r == 0:
        r = 1
        anti_cheat_list.append(AntiCheat(0, 0, vwidth, 10, (255, 0, 0)))
        anti_cheat_list.append(AntiCheat(0, vheight-10, vwidth, 10, (255, 0, 0)))
        anti_cheat_list.append(AntiCheat(vwidth - 10, 0, 10, vheight, (255, 0, 0)))
    # Gap calculations
    max_gapspawn = vheight - max_gap
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
        if 2 * r / ws > 1.5:
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
            gaplen = rng.randint(min_gap, max_gap)
            gapfull = rng.randint(0, 1)
            walllist.append(Wall(gapstart, wallthick, False, (0, 0, 255), 0))
            walllist.append(Wall(vheight - gapstart - gaplen, wallthick, False, (0, 0, 255), gapstart + gaplen))
            if gapfull == 1:
                walllist.append(Wall(gaplen, wallthick, True, (128, 128, 128), gapstart))
        if coin_timer == 0:
            coin_timer = spawn_timer
            walllist.append(Coin(rng.randint(30, 420)))
    for i in anti_cheat_list:
        i.update()
        cv2.rectangle(flippedRGB, (i.x, i.y), (i.x + i.width, i.y + i.height), i.color, -1)
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
exit(32767)
