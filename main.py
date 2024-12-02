import cv2
import mediapipe as mp
import numpy as np
import random as rng


class Wall:
    def __init__(self, height, w, breakable, color, y):
        self.height = height
        self.width = w
        self.breakable = breakable
        self.color = color
        self.x = 640 #640x530
        self.y = y
        self.open = False


    def update(self):
        self.x -= 10
        if self.x <= self.width * -1:
            send_delete_request()
        check = self.check_collide()
        if check is True and prev_fist is True:
            print(1)
            if self.breakable is True:
                print(2)
                if not self.open:
                    self.open = True
                    print('opened wall')



    def check_collide(self):
        for i in get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape):
            if self.x <= i[0] <= self.x + self.width:
                if self.y <= i[1] <= self.y + self.height:
                    return True
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


def satistfy_requests():
    r = open('comms.txt', 'r')
    for i in r.readlines():
        if i == 'DELETE_WALL':
            walllist = walllist[1:]
        else:
            count += 1
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

#создаем детектор

handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
count = 0
prev_fist = False
finger_list = []
wall_timer = 60
walllist = []
while(cap.isOpened()):
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    # переводим его в формат RGB для распознавания
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    #The timer is ticking...
    wall_timer -= 1
    if wall_timer == 0:
        wall_timer = 60
        wallthick = rng.randint(10, 50)
        gapstart = rng.randint(10, 440)
        gaplen = rng.randint(40, 60)
        gapfull = rng.randint(0, 1)
        walllist.append(Wall(gapstart, wallthick, False, (0, 0, 255), 0))
        walllist.append(Wall(530 - gapstart - gaplen, wallthick, False, (0, 0, 255), gapstart + gaplen))
        if gapfull == 1:
            walllist.append(Wall(gaplen, wallthick, True, (128, 128, 128), gapstart))
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
        if 2 * r / ws > 1.3:
             cv2.circle(flippedRGB,(int(x), int(y)), int(r), (0, 0, 255), 2)
             # кулак разжат
             prev_fist = False
        else:
             cv2.circle(flippedRGB,(int(x), int(y)), int(r), (0, 255, 0), 2)
             if not prev_fist:
                 # произошло сжимание
                 count += 1
                 # Сейчас кулак зажат
                 prev_fist = True
    #Walls drawn and updated lmao
    for i in walllist:
        if not i.open:
            cv2.rectangle(flippedRGB, (i.x, i.y), (i.x + i.width, i.y + i.height), i.color)
    # Рисуем наш результат в каждом кадре, даже если рука не детектировалась
    cv2.putText(flippedRGB, str(count), (600, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=2)

    # переводим в BGR и показываем результат
    res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow("Hands", res_image)

# освобождаем ресурсы
handsDetector.close()
