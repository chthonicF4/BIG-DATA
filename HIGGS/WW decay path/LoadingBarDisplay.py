import time , math


def loadingbar(value:float,length:int,name:str):
    squares = value*length
    bar = ""
    for unit in range(length):
        if unit <= int(squares) : bar += "■"
        else: bar += " "
    return f"{name} [{bar}]"

def need_update(prev_value:float,current_value:float,length:int):
    prev_squares ,current_squares = prev_value*length , current_value*length
    if math.floor(prev_squares) < math.floor(current_squares):
        return True
    return False



if __name__ == "__main__" :
    for x in range(10):
        print(loadingbar(x/10,5,"BAR"),end="\r")
        time.sleep(0.5)
