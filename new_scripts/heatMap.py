import numpy as np
from scipy.integrate import odeint
import sklearn.metrics
import math
import matplotlib.pyplot as plt
import csv

def main():
    size = 10
    incr = 0.05
    arr = [[0 for i in range(size)] for j in range(size)]    
    g1_s = 0.1325
    p_s = 0
    k_s = 0
    g11_s = 0.11
    l_s = 0
    n_s = 0
    for i in range (size):
        for j in range (size):
            arr[size - i - 1][j] = round(givenVars(g1_s, p_s - incr * i, k_s, g11_s, l_s + incr * j, n_s), 3)
    print (arr)
    left = l_s
    right = l_s + size*incr
    bottom = p_s
    top = p_s + size*incr
    extent = [left, right,bottom,top]
    plt.title('Grp. A1 B6 (100% C1)')
    plt.xlabel('l value')
    plt.ylabel('p value')
    plt.imshow(arr, cmap='hot', interpolation='nearest', extent = extent)
    plt.show()


def givenVars(g1, p, k, g11, l,  n):
    def eqs(x,t):
        # Extract variables
        C1 = x[0]
        C11 = x[1]
        T= x[2]
        dxdt = [(p * T + g1) * C1,
            (g11) * C11,
            (l * C1 ) * T]
        
        return dxdt

    # Set initial conditions
    y0 = [1, 0, 1]

    #choosing where to sample parameters from CSV file
    #writen here for close proximity to setting y0
    start = 1
    stop = 7

    # Set the time grid
    t = np.linspace(0, 100, 50)

    # Solve the ODE system
    sol = odeint(eqs, y0, t)

    tumorSize = [0] * 50
    for i in range (50):
        tumorSize[i] = float(sol[i][0]) + float(sol[i][1])


    # Open the CSV file in read mode
    with open('data/scaled_exbd_fit.csv', 'r') as csvfile:
        # Create a reader object
        csv_reader = csv.reader(csvfile)
        inspected = [row for idx, row in enumerate(csv_reader) if idx in range(start, stop)]
        #use longest lifetime

    inspected = np.asarray(inspected)

    expo = [[0]*50 for i in range(6)]
    for i in range(6):
        for j in range(50):
            expo[i][j] = math.exp(float(inspected[i][2]) * j * 2 + float(inspected[i][3]))
    
    rSquaredSum = 0

    for i in range(6):
                rSquaredSum  += sklearn.metrics.r2_score(expo[i][:int(inspected[i,5])], tumorSize[:int(inspected[i,5])])

    #print (rSquaredSum)
    return rSquaredSum

main()