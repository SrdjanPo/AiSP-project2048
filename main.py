from PIL import ImageGrab, ImageOps
import pyautogui, time

#Globalni niz koji predstavlja trenutno stanje kvadrata u mrezi

myMatrix = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

# niz koji ce pomagati pri odredjivanju skora
helperMatrix = [50, 30, 15, 5,
                30, -10, 0, 0,
                15, 0, 0, 0,
                5, 0, 0, 0]

UP = 1000
LEFT = 1001
DOWN = 1002
RIGHT = 1003

#Koordinate svakog kvadrata sam dobio preko pyautogui.displayMousePosition()
#Koordinate su uzimane iz donjeg desnog ugla svakog kvadrata

class Coordinates:
    cord11 = (197, 365)
    cord12 = (307, 365)
    cord13 = (417, 365)
    cord14 = (527, 365)
    cord21 = (197, 475)
    cord22 = (307, 475)
    cord23 = (417, 475)
    cord24 = (527, 475)
    cord31 = (197, 585)
    cord32 = (307, 585)
    cord33 = (417, 585)
    cord34 = (527, 585)
    cord41 = (197, 695)
    cord42 = (307, 695)
    cord43 = (417, 695)
    cord44 = (527, 695)

    #Niz svih koordinata da bi mogli prolaziti kroz svaki

    coordinatesArray = [cord11, cord12, cord13, cord14,
                        cord21, cord22, cord23, cord24,
                        cord31, cord32, cord33, cord34,
                        cord41, cord42, cord43, cord44]

class grayValues:

    #Svaki moguci kvadrat i njegova grayscale vrijednost

    null = 195
    two = 229
    four = 225
    eight = 190
    oneSix = 172
    threeTwo = 157
    sixFour = 135
    oneTwoEight = 205
    twoFiveSix = 201
    fiveOneTwo = 197
    oneZeroTwoFour = 193
    twoZeroFourEight = 189

    #Niz grayscale vrijednosti svih mogucih kvadrata

    grayArray = [null, two, four, eight, oneSix, threeTwo, sixFour
                  , oneTwoEight, twoFiveSix, fiveOneTwo, oneZeroTwoFour,
                 twoZeroFourEight]

#Fukncija koja prolazi kroz mrezu i poredi grayscale vrijednosti svakog kvadrata
def getMatrix():
    image = ImageGrab.grab() #Uzima screenshot cijelog ekrana
    grayImage = ImageOps.grayscale(image) #Pretvara screenshot u grayscale tako da bi dobili jedan integer kao vrijednost

    for index, cord in enumerate(Coordinates.coordinatesArray): #prolazi kroz svaku koordinatu i cuva indeks tako da mozemo azurirati trenutno stanje mreze
        pixel = grayImage.getpixel(cord) #vrijednost pixela na svakoj navedenoj koordinati
        position = grayValues.grayArray.index(pixel) #dobijemo grayscale vrijednost i nadjemo njen index u grayArray nizu

        #Posto su vrijednosti u grayArray nizu poredane od 0 do 2054, a svaka vrijednostu u tom nizu predstavlja broj 2 na odredjeni stepen(osim nule)
        #Svaku vrijednost osim nule mozemo naci kao 2^n tj. 2 na odredjeni stepen, a taj stepen je "position" varijabla
        if position == 0:
            myMatrix[index] = 0
        else:
            myMatrix[index] = pow(2, position)

#funkcija koja uzima jedan red kao parametar
def slideRow(row):
    #ova funkcija omogucava da se saberu dva ista broja, a da pri tome ignorise prazna mjesta izmedju njih tj. nule

    previous = -1 #prethodni element koji nije nula
    i = 0
    temp = [0, 0, 0, 0]

    for element in row:

        if element != 0: #preskacu se nule tj. prazna mjesta
            if previous==-1:
                previous = element
                temp[i] = element
                i += 1
            elif previous == element: #ako je element jednak prethodnom elementu sabiraju se
                temp[i-1] = 2*previous
                previous = -1
            else: #else dodajemo element u temp niz
                previous = element
                temp[i] = element
                i += 1

    return temp #vracamo novi dobijeni red

def getNextGrid(grid, move):

    #niz koji ce predstavljati finalnu mrezu

    temp = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

    if move == UP: #algoritam za pomjeranje na gore
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4*j])
            row = slideRow(row)
            for j, val in enumerate(row):
                temp[i + 4*j] = val

    elif move == LEFT: #algoritam za pomjeranje na lijevo
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4*i + j])
            row = slideRow(row)
            for j, val in enumerate(row):
                temp[4*i + j] = val

    elif move == DOWN: #algoritam za pomjeranje na dole
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * (3-j)])
            row = slideRow(row)
            for j, val in enumerate(row):
                temp[i + 4 * (3-j)] = val

    elif move == RIGHT: #algoritam za pomjeranje na desno
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4 * i + (3-j)])
            row = slideRow(row)
            for j, val in enumerate(row):
                temp[4 * i + (3-j)] = val

    return temp

def printMatrix(matrix):
    for i in range(16):
        if i%4 == 0:
            print("[ " + str(matrix[i]) + " " + str(matrix[i + 1]) + " " + str(matrix[i + 2]) + " " + str(matrix[i + 3]) + " ]")


def getScore(grid):
    score = 0
    for i in range(4):
        for j in range(4):
            score += grid[4*i+j] * helperMatrix[4 * i + j]
    return score

#funkcija koja provjerava da li je potez validan
def validMove(matrix, move):
    if getNextGrid(matrix, move) == matrix:
        return False
    else:
        return True

#funkcija koja odredjuje najbolji trenutni potez tj. potez koji ima najveci skor
def getBestSlide(matrix):
    scoreUp = getScore(getNextGrid(matrix, UP))
    scoreDown = getScore(getNextGrid(matrix, DOWN))
    scoreLeft = getScore(getNextGrid(matrix, LEFT))
    scoreRight = getScore(getNextGrid(matrix, RIGHT))

    if not validMove(matrix, UP):
        scoreUp = 0
    if not validMove(matrix, DOWN):
        scoreDown = 0
    if not validMove(matrix, LEFT):
        scoreLeft = 0
    if not validMove(matrix, RIGHT):
        scoreRight = 0

    maxPoints = max(scoreUp, scoreDown, scoreLeft, scoreRight) #pomocu "max" funkcije uzima najvecu vrijednost

    if scoreUp == maxPoints:
        return UP
    elif scoreDown == maxPoints:
        return DOWN
    elif scoreLeft == maxPoints:
        return LEFT
    else:
        return RIGHT


#implementacija funkcionalnosti automatskog pomjeranja
def performMove(move):
    if move == UP:
        pyautogui.keyDown('up')
        print("UP")
        time.sleep(0.05) #odlaganje izmedju keyDown i keyUp da bi browser mogao prepoznati da je dugme pritisnuto
        pyautogui.keyUp('up')
    elif move == DOWN:
        pyautogui.keyDown('down')
        print("DOWN")
        time.sleep(0.05) #odlaganje izmedju keyDown i keyUp da bi browser mogao prepoznati da je dugme pritisnuto
        pyautogui.keyUp('down')
    elif move == LEFT:
        pyautogui.keyDown('left')
        print("LEFT")
        time.sleep(0.05) #odlaganje izmedju keyDown i keyUp da bi browser mogao prepoznati da je dugme pritisnuto
        pyautogui.keyUp('left')
    else:
        pyautogui.keyDown('right')
        print("RIGHT")
        time.sleep(0.05) #odlaganje izmedju keyDown i keyUp da bi browser mogao prepoznati da je dugme pritisnuto
        pyautogui.keyUp('right')

def main():
    time.sleep(2) #odlaganje 2 sekunde da bi mogli fokusirati na 2048game prozor nakon pokretanja
    while True:
        getMatrix()
        performMove(getBestSlide(myMatrix))
        time.sleep(0.3) #svaki novi potez se izvodi za 0.3 sekundi

if __name__ == '__main__':
    main()
