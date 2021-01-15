""" BME - 2019 - Mesterseges Intelligencia HF - Zombor Mate - LHU0GL """

# object representing the parking "garage" or slots
# this is the main object the main loop's gonna be working on
class Map:
    # construct the object with given fields
    def __init__(self):
        self.data = ""
        self.width = 0
        self.height = 0
        self.cars = []
        self.map = []

    # initialize the object with the given data (string)
    def init(self, _data):
        # Prepare map as a two dimensional list
        self.data = _data
        self.height = int(data[0].split()[0])
        self.width = int(data[0].split()[-1])
        for i in range(self.height):
            row = []
            for i in range(self.width):
                row.append(0)
            self.map.append(row)

        # Prepare cars as simple list objects (unordered) 
        ucars = []
        idx = 1
        for i in data[2:]:
            line = i.split()
            ucars.append((int(line[0])*int(line[1]),int(line[0]),int(line[1]),idx))
            idx += 1

        # Arrange cars in decreasing order based on their "occupied" area
        for _ in range(len(ucars)):
        # save largest car, its index and a travelling index
            largest = ucars[0][1]
            idx = 0
            lidx = 0
            for car in ucars:
                if car[1] > largest or car[2] > largest:
                    if car[1] > car[2]:
                        largest = car[1]
                    else:
                        largest = car[2]
                    lidx = idx
                idx+=1
            # add largest car to ordered list
            self.cars.append(ucars.pop(lidx))

    # for testing purposes
    def prints(self):
        for i in range(self.height):
            for j in range(self.width):
                if j < self.width-1:
                    print(str(self.map[i][j]) + '\t', end='')
                else:
                    print(str(self.map[i][j]), end="\n")
                
        print("\n")

    # try placing car given the starting coordinates
    def tryCar(self, starty, startx, width, height):
        # try placing it vertically
        placedv = True
        for i in range(height):
            for j in range(width):
                try:
                    if self.map[starty+i][startx+j] != 0:
                        placedv = False
                except IndexError:
                    # todo
                    placedv = False
                    break
                    
        # if it didn't work try placing it horizontally
        placedh = True
        for i in range(width):
            for j in range(height):
                try:
                    if self.map[starty+i][startx+j] != 0:
                        placedh = False
                except IndexError:
                    # todo
                    placedh = False
                    break

        # return orientation marker based on results
        if placedv:
            return "v"
        elif placedh:
            return "h"
        else:
            return "n"

# Prepare data to be processed 
data = []
# read map size
mapsize = input()
data.append(mapsize)
# read car number and read car data based on value
carnum = input()
data.append(carnum)

for i in range(int(carnum)):
    data.append(input())

# Remove trailing new line characters
for i in range(len(data)):
    data[i] = data[i].rstrip("\n")

# Create the map for the loop
map = Map()
map.init(data)
# map.prints()

# print(map.width, map.height)
# for car in map.cars:
#     print(car)


# Loop over every car standing in the line
for car in map.cars:
    placed = False
    for i in range(map.height):
        for j in range(map.width):
            # try fitting it into the block
            res = map.tryCar(i,j,car[2],car[1])
            # if it fits vertically, fill up slots based on size
            if res is "v" and not placed:
                for k in range(car[1]):
                    for l in range(car[2]):
                        map.map[i+k][j+l] = car[3]
                # and mark as placed so it doesn't get placed twice
                placed = True
                break
            # if it fits horizontally, do the same as vertically but in reverse
            if res is "h" and not placed:
                for k in range(car[2]):
                    for l in range(car[1]):
                        map.map[i+k][j+l] = car[3]
                placed = True
                break
            # else just step over the block
            elif res is "n":
                continue


# DONE
map.prints()