import matplotlib.pyplot as mat
import numpy as np
import random as rand
import math

fig, ax = mat.subplots(1, 3)

# val[standard deviation, mean] -> efffective diffusivities
# in order - AP, 75/25 AP/TG18, 50/50 AP/TG18, 25/75 AP/TG18, TG18
nums = []
val = [[0.008877, 0.04555],
       [0.0268, 0.07407],
       [0.018, 0.0678],
       [0.0242, 0.02231],
       [0.0269, 0.03123]]
labels = ["AP", "75/25 AP/TG18", "50/50 AP/TG18", "25/75 AP/TG18", "TG18"]
total = 0
y_axis = []
x_axis = []

thick = float(input("Enter thickness (um): "))
t = float(input("Enter time (sec): "))
r = int(input("How many times do you want to run the simulation? "))

def normalcdf(o, u, name, points):
    tot = 0
    x = np.linspace(u - (4 * o), u + (4 * o), points)
    p1 = 1 / (o * np.sqrt(2 * np.pi))
    p2 = (np.e ** (-0.5 * ((x - u) / o) ** 2))
    dist = p1 * p2
    graph, = ax[0].plot(x, dist, label=name)
    xdata = graph.get_xdata().tolist()
    for i in range(100):
        num = rand.randint(0, 499 - i)
        nums.append(xdata[num])
        tot += xdata[num]
        xdata.pop(num)
    return tot, xdata

# use ficks second law to calculate probability
def diffusion(thickness, time, diff):
    probability = 1 - math.erf(thickness / (2*np.sqrt(diff * time)))
    return probability


for i in range(len(val)):
    var, a = normalcdf(val[i][0], val[i][1], labels[i], 500)
    total += var
mean = total / len(nums)
devtotal = 0
for i in range(len(nums)):
    devtotal += ((nums[i] - mean) ** 2)
stdev = np.sqrt(devtotal / 500)
a, arr = normalcdf(stdev, mean, "Simulated Normal Distribution", 500)
arr = [ele for ele in arr if ele > 0]
meanp = 0
for i in range(r):
    p = diffusion(thick, t, arr[rand.randint(0, len(arr) - 1)])
    meanp += p
print(str((meanp / r) * 100) + '%')

#thickness to percentage graph
for i in range(100):
    x_axis.append(i * 10)
    y_axis.append(diffusion(i * 10, 86400, arr[rand.randint(0, len(arr) - 1)]) * 100)
ax[1].plot(x_axis, y_axis)
ax[1].set_title("Thickness vs Mucus Penetration")
ax[1].set_xlabel("Thickness")
ax[1].set_ylabel("Mucus penetration %")

#time to percentage graph
x_axis.clear()
y_axis.clear()
for i in range(101):
    x_axis.append(i * 864)
    y_axis.append(diffusion(10, i * 864, arr[rand.randint(0, len(arr) - 1)]) * 100)
ax[2].plot(x_axis, y_axis)
ax[2].set_xlim(0, 90000)
ax[2].set_title("Time vs Mucus Penetration")
ax[2].set_xlabel("Time")
ax[2].set_ylabel("Mucus penetration %")

#normal distribution graph
ax[0].legend(loc='upper right')
ax[0].set_title("Distributions of 5 different particle diffusivities")
ax[0].set_xlabel("Effective Diffusivity")
ax[0].set_ylabel("% of Particles")

#display
mat.show()





