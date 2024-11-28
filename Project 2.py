class Wall:
    def __init__(self, height, w, breakable, color, y):
        self.height = height
        self.width = w
        self.breakable = breakable
        self.color = color
        self.x = 1280
        self.y = y
        self.open = False


    def update(self):
        self.x -= 10
        if self.x <= self.width * -1:
            send_delete_request()
        check = self.check_collide()
        kc = fistcheck()
        if check:
            if self.breakable:
                if self.open:
                    self.open = False



    def check_collide(self):
        for i in finger_list:
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


def fistcheck():
    return True


wallist = []
finger_list = []
wallist.append(Wall(350, 50, False, (255, 0, 255), 0))
