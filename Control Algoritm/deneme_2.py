import numpy as np
import re

num_of_balls_returned = np.array([0, 0, 1, 0, 0, 30, 20, 7, 6, 26, 54, 14, 22, 11, 6, 5, 38, 25, 15, 9, 16])
num_of_balls_thrown = np.array([20, 30, 20, 55, 57, 36, 25, 17, 16, 29, 55, 17, 25, 22, 36, 25, 98, 45, 25, 15, 25])

for i in np.arange(3)+1:
    num_of_balls_returned += i
    num_of_balls_thrown += i
    with open('readMe.txt', 'w') as f:
        f.write(str(num_of_balls_thrown))
        f.write('\n')
        f.write(str(num_of_balls_returned))
        f.close()

with open('readMe.txt', 'r') as f:
    temp = f.read()

integers = re.findall(r'\d+', temp)
integer_array = [int(num) for num in integers]
print(integer_array)
print(integer_array[1])
command = 'serving frequency'
print('serving' in command)
