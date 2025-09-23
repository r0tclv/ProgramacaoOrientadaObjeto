import time


#precisa instalar a bibioteca= w
import keyboard  


class RobotCleaner:
    def __init__(self, rows=15, cols=15, start=(0,0), battery=15, recharge_time=1):
        self.__rows = rows
        self.__cols = cols
        self.__environment = [["." for _ in range(cols)] for _ in range(rows)]
        self.__position = start  
        self.__battery = battery
        self.__max_battery = battery
        self.__recharge_time = recharge_time  
        self.__environment[start[0]][start[1]] = "R"


    @property
    def rows(self):
        return self.__rows
    @property
    def cols(self):
        return self.__cols
    @property
    def environment(self):
        return self.__environment
    @property
    def position(self):
        return self.__position
    @property
    def battery(self):
        return self.__battery
    @property
    def max_battery(self):
        return self.__max_battery
    @property
    def recharge_time(self):
        return self.__recharge_time
   
    @position.setter
    def position(self, new_pos):
        x, y = new_pos
        if 0 <= x < self.__rows and 0 <= y < self.__cols:
            self.__position = (x, y)


    @battery.setter
    def battery(self, new_battery):
        if 0 <= new_battery <= self.__max_battery:
            self.__battery = new_battery


    def show_environment(self):
        for row in self.__environment:
            print(" ".join(row))
        print("\n================================")
        print(f"bateria: {self.__battery}")
    def move(self, direction):
        if self.__battery <= 0:
            print("descarregado")
            self.recharge()
            return


        x, y = self.__position
        self.__environment[x][y] = " "
        if direction == "up" and x > 0:
            x -= 1
        elif direction == "down" and x < self.__rows - 1:
            x += 1
        elif direction == "left" and y > 0:
            y -= 1
        elif direction == "right" and y < self.__cols - 1:
            y += 1
        self.__position = (x, y)
        self.__environment[x][y] = "R"
        self.__battery -= 1


    def recharge(self):
        print("carregando")
        while self.__battery < self.__max_battery:
            time.sleep(self.__recharge_time)
            self.__battery += 1
            print(f"Bateria: {self.__battery}")
        print("carregado")


robot = RobotCleaner(start=(2,2), battery=55)


print("use as setas para mover \n")
robot.show_environment()
print("================================\n")
while True:
    if keyboard.is_pressed("up"):
        robot.move("up")
        robot.show_environment()
        time.sleep(0.2)
        print("================================\n")
    elif keyboard.is_pressed("down"):
        robot.move("down")
        robot.show_environment()
        time.sleep(0.2)
        print("================================\n")
    elif keyboard.is_pressed("left"):
        robot.move("left")
        robot.show_environment()
        time.sleep(0.2)
        print("================================\n")
    elif keyboard.is_pressed("right"):
        robot.move("right")
        robot.show_environment()
        time.sleep(0.2)
        print("================================\n")
    elif keyboard.is_pressed("esc"):
        print("xau...")
        break
