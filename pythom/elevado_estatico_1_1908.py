import time
import random


class RobotCleaner:
    def __init__(self, rows=5, cols=5, start=(0,0), battery=15, recharge_time=1):
        self.environment = [["." for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.position = start  
        self.battery = battery
        self.max_battery = battery
        self.recharge_time = recharge_time
        self.environment[start[0]][start[1]] = "R"


    def show_environment(self):
        for row in self.environment:
            print(" ".join(row))
        print()


    def move(self, direction):
        if self.battery <= 0:
            print(" Bateria zerada! Recarregando...")
            self.recharge()
            return


        x, y = self.position
        self.environment[x][y] = " "
        if direction == "up" and x > 0:
            x -= 1
        elif direction == "down" and x < self.rows - 1:
            x += 1
        elif direction == "left" and y > 0:
            y -= 1
        elif direction == "right" and y < self.cols - 1:
            y += 1
        else:
            print("Movimento inválido!")
            return
        self.position = (x, y)
        self.environment[x][y] = "R"
        self.battery -= 1
        print("================================\n")
        print(f"Robô moveu para {self.position}, bateria: {self.battery}")
        time.sleep(1)
        robot.show_environment()


    def recharge(self):
        robot.show_environment()
        print("================================\n")
        print(" Iniciando recarga...")
        for i in range(self.max_battery):
            time.sleep(self.recharge_time)
            self.battery += 1
            print(f"Bateria: {self.battery}")
        print(" Bateria carregada!")


    def clean(self):
        x, y = self.position
        if self.environment[x][y] == ".":
            self.environment[x][y] = "R"
            print("🧹 Sujeira limpa!")
        else:
            print("Nada para limpar aqui.")
robot = RobotCleaner(start=(2,2), battery=5)
robot.show_environment()
robot.move("up")
robot.move("up")
robot.move("left")
robot.move("left")
robot.move("down")
robot.move("down")
robot.move("right")
robot.move("down")
robot.move("left")
robot.move("down")
robot.move("down")
robot.move("right")
robot.move("up")
robot.move("right")
robot.move("down")
robot.move("right")
robot.move("up")
robot.move("right")
robot.move("down")
robot.move("right")
robot.move("up")
robot.move("up")
robot.move("up")
robot.move("up")
robot.move("up")
robot.move("right")
robot.move("down")
robot.move("down")
robot.move("down")
robot.move("down")
robot.move("down")


#robot.move("up")
#robot.move("left")
#robot.move("down")
#robot.move("right")
