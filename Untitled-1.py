
import random ,time ,os,numpy

def clr():
    os.system("cls")


height,width = 15,15

def print_out(out) :
    str = "■■"*(width+2) + "\n"
    for y in out :
        str += "■■"
        for x in y :
            if x == 1 :
                str += "@@"
            else : str += "  "

        str += "■■\n"
    str += "■■"*(width+2)
    return str

def next_to(coords:tuple,grid):
    count = [0,0]
    x,y = coords
    try:
        if grid[x+1][y] == 0 : count[0] += 1
        else: count[1] += 1
    except :
        pass
    try:
        if grid[x-1][y] == 0 : count[0] += 1
        else: count[1] += 1
    except :
        pass
    try:
        if grid[x][y+1] == 0 : count[0] += 1
        else: count[1] += 1
    except :
        pass
    try :
        if grid[x][y-1] == 0 : count[0] += 1
        else: count[1] += 1
    except :
        pass
    return tuple(count)



def chees():
    out = numpy.zeros((height,width))
    for x in range(width):
        for y in range(height) :
            if next_to((x,y),out)[0] >= 1 :
                numb = random.randint(0,1)
            elif next_to((x,y),out)[1] >= 3 :
                numb = 0
            else: numb = 0






            out[x][y] = numb
    return print_out(out)

while True :
    print(chees())
    time.sleep(1)
    clr()
    