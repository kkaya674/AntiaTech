import numpy as np
from scipy.stats import rv_discrete

num_of_balls_returned = np.array([0, 0, 1, 0, 0, 30, 20, 7, 6, 26, 54, 14, 22, 11, 6, 5, 38, 25, 15, 9, 16])
num_of_balls_thrown = np.array([20, 30, 20, 55, 57, 36, 25, 17, 16, 29, 55, 17, 25, 22, 36, 25, 98, 45, 25, 15, 25])
print(num_of_balls_returned / num_of_balls_thrown)
temp = 1 - (num_of_balls_returned / (num_of_balls_thrown+1))


r_spin = rv_discrete(name='r_spin', values=([-2, -1, 0, 1, 2], temp[:5]/np.sum(temp[:5])))
print(temp[:5]/np.sum(temp[:5]))
r_freq = rv_discrete(name='r_freq', values=([0, 1, 2], temp[5:8]/np.sum(temp[5:8])))
print( temp[5:8]/np.sum(temp[5:8]))
r_speed = rv_discrete(name='r_speed', values=([1, 2, 3], temp[8:11]/np.sum(temp[8:11])))
print(temp[8:11]/np.sum(temp[8:11]))
r_dir = rv_discrete(name='r_dir', values=([-2, -1, 0, 1, 2], temp[11:16]/np.sum(temp[11:16])))
print(temp[11:16]/np.sum(temp[11:16]))
r_lau_ang = rv_discrete(name='r_lau_ang', values=([-2, -1, 0, 1, 2], temp[16:21]/np.sum(temp[16:21])))
print(temp[16:21]/np.sum(temp[16:21]))
