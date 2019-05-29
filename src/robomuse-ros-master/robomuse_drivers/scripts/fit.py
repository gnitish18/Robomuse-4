import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


distances = np.array([0.61,0.75,0.915,1.1,1.22,1.525,1.83,2.135,2.44,2.745,3.05])
values = np.array([192,180,167,160,155,148,144,139,137,135,133])
xdata = np.arange(120,255)

def func(x,a,b,c):
    return a*x*x + b*x + c

print np.linspace(5,10)
print values


plt.plot(values, distances, 'b-', label='data')
plt.plot(xdata, func(xdata, 0.000164,-0.0836,11.264), 'r-',label='fit')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()


