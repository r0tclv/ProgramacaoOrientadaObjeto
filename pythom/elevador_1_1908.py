import time
import winsound  # windows apenas
print('Olá mundo')
class Elevator:
    def __init__(self, maxFloor: int = 0, minFloor: int = 0, currentFloor: int = 0, isDoorOpen: bool = False):
        self.__maxFloor = maxFloor
        self.__minFloor = minFloor
        self.__currentFloor = currentFloor
        self.__isDoorOpen = isDoorOpen
    @property    
    def maxFloor(self):
        return self.__maxFloor
    @property
    def minFloor(self):
        return self.__minFloor
    @property
    def currentFloor(self):
        return self.__currentFloor
    @property
    def isDoorOpen(self):
        return self.__isDoorOpen
    @maxFloor.setter
    def maxFloor(self, newMaxFloor: int):
        if 0 < newMaxFloor < 15:
            self.__maxFloor = newMaxFloor
    @minFloor.setter
    def minFloor(self, newMinFloor: int):
        if 0 < newMinFloor < 15:
            self.__minFloor = newMinFloor
    @currentFloor.setter
    def currentFloor(self, newCurrentFloor: int):
        if 0 <= newCurrentFloor <= self.maxFloor:
            self.__currentFloor = newCurrentFloor
    @isDoorOpen.setter
    def isDoorOpen(self, doorState: bool):
        self.__isDoorOpen = doorState
    def move(self, newFloor: int):
        if self.isDoorOpen:
            print(" Feche a porta antes de mover o elevador!")
            winsound.Beep(1000, 600)
            winsound.Beep(600, 800)  
            return
        if newFloor > self.maxFloor or newFloor < self.minFloor:
            print(" Andar inválido!")
            return
        print(f"\nPlimPlomm\nSaindo do andar {self.currentFloor} para o andar {newFloor}...\nPlimPlomm\n")
        if newFloor > self.currentFloor:  #up
            for andar in range(self.currentFloor + 1, newFloor + 1):
                time.sleep(1)
                winsound.Beep(800, 200)
                print(f"Elevador no andar {andar}")
                self.__currentFloor = andar
        elif newFloor < self.currentFloor:  #dowm
            for andar in range(self.currentFloor - 1, newFloor - 1, -1):
                time.sleep(1)
                winsound.Beep(600, 200)
                print(f"Elevador no andar {andar}")
                self.__currentFloor = andar
        else:
            print("Elevador já está nesse andar!")
serviceElevator = Elevator(maxFloor=10, isDoorOpen=False)
socialElevator = Elevator(maxFloor=10)
serviceElevator.move(5)
serviceElevator.move(2)
serviceElevator.move(8)
serviceElevator.move(1)
print("Max Floor:", serviceElevator.maxFloor)      
print("Door Open:", serviceElevator.isDoorOpen)
print("Current Floor:", serviceElevator.currentFloor)