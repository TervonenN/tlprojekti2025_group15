import numpy as np
import matplotlib.pyplot as plt

data_points = []

test_0 = np.array([1500,1500,1200]) #ok
test_1 = np.array([1500,1200,1500]) #ok
test_2 = np.array([1200,1500,1500]) #ok
test_3 = np.array([1500,1800,1500]) #ok
test_4 = np.array([1800,1500,1500]) #ok
test_5 = np.array([1500,1500,1800]) #OK

data_points.append(test_0)
data_points.append(test_1)
data_points.append(test_2)
data_points.append(test_3)
data_points.append(test_4)
data_points.append(test_5)

'''
for i, test_array in enumerate (data_points):
    print(f"Testi_{i+1}:{test_array}")

value = data_points[0]

print("value: ", value)
#print("value: ", *value) jos tähti tuossa valuen edessä niin ei tule hakasulkeita tulostukseen
'''

x = np.array(data_points)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x[:,0], x[:,1], x[:,2],color='red')

# Akselien nimet
ax.set_xlabel('X-akseli')
ax.set_ylabel('Y-akseli')
ax.set_zlabel('Z-akseli')

plt.show()