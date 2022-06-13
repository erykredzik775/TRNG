import imageio
import numpy
import math

from itertools import chain
from moviepy.editor import *

#=============================================================================
#   image[?][?][?])
#         y  x rgb
#==============================================================================

numNeeded = 10000
maxRange  = 256

#==============================================================================

numPossibles = 0
schouldCont = True
frame = 0
bitsRange = math.ceil(math.log(maxRange, 2))
tmp = 0
count = 0
sublist = []
tempSublist = []
outputList = []

#==============================================================================
# Przygotowanie klatek z filmu
#==============================================================================

def frameCut():
  clip = VideoFileClip('example.mp4')
  clip.save_frame('frame.png', t = frame)

#==============================================================================
# Sczytywanie liczb z klatek
#==============================================================================

numNeeded *= bitsRange

while(schouldCont):
  frameCut()
  image = imageio.imread('frame.png')
  imgHigth, imgWidth, imgChannel = image.shape

  # Wczytywanie do listy pomocniczej wartosci z calej klatki
  for i in range(0,imgHigth):
    for j in range(0,imgWidth):
      for k in range(0,imgChannel):
        if(image[i][j][k] >= 2 and image[i][j][k] <= 253):
          sublist.append(image[i][j][k] & 0b1)
          numPossibles += 1
  frame += 1 
  if(numPossibles >= numNeeded):
    schouldCont = False

# Obliczanie wielkosci macierzy kwadratowej
square = math.floor(math.sqrt(numNeeded))

for i in range(0,square*square):
  tempSublist.append(sublist[i])

# Mieszanie macierzy
tempSublist = numpy.array(tempSublist).reshape(square,square)
transpose = tempSublist.T
tempSublist = transpose.tolist()
tempSublist = list(chain.from_iterable(tempSublist))

# Jesli ilość liczb w macierzy kwadratowej jest niewystarczająca
# dodawne sa liczby z ostatniej użytej klatki, od momentu uciecią jej
# do macierzy kwadratowej
if(square*square < numNeeded):
  for i in range(0, numNeeded - square*square):
    tempSublist.append(sublist[i+(square*square)])

x = 0
# Skladanie bitow w liczby z zakresu
while(count < numNeeded/bitsRange):
  for j in range(0,bitsRange):
    valTmp = tempSublist[x]
    # 0000000
    # 0000001
    # 0000010
    # 0000000
    # 0001000
    # -------
    # 0001011
    tmp = tmp | (valTmp << j)
  #if(tmp <= 0 and tmp <= maxRange):
    #print("tmp" + str(tmp))
    x += 1
  outputList.append(tmp)
  tmp = 0
  count += 1

output = open("output.txt", "w")
for element in outputList:
    output.write(str(element) + "\n")
output.close()

