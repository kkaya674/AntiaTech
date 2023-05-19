

def readData():
    from sys import stdin
    from machine import Pin
    import _thread, uselect
    from time import sleep



    while True:
        buffer = []
        select_result = uselect.select([stdin], [], [], 0)
        while select_result[0]:
            char = stdin.read(1)
            buffer.append(char)
            select_result = uselect.select([stdin], [], [], 0)
        
        message = "".join(buffer) if buffer != [] else None
        if message != None:
            with open("in.txt", "w") as f:
     
        
                f.write(message)
                msg = message.split(" ")
                return msg


