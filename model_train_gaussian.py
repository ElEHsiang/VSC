import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats



def main():

    fName = input('input image name:\n')
    type = input('type:\n')

    f = open(fName + '_' + type + '_contour.txt', 'r')

    intensitySum = 0
    gradientSum = 0

    intensityVariance = 0
    gradientVariance = 0

    intensity = []
    gradient = []

    count = 0

    for line in f:
        x, y, i, g= line[:-1].split(' ')
        intensity.append(int(i))
        gradient.append(int(g))

    intensity = sorted(intensity)
    gradient = sorted(gradient)

    iStd = np.std(intensity)
    gStd = np.std(gradient)

    iMean = np.mean(intensity)
    gMean = np.mean(gradient)

    print('Mean')
    print('intensity : ' + str(iMean))
    print('gradient: ' + str(gMean))

    print('std')
    print('intensity : ' + str(iStd))
    print('gradient : ' + str(gStd))


    fig, ax = plt.subplots(1, 2)
    ax1, ax2 = ax.ravel()

    iFit = stats.norm.pdf(intensity, iMean, iStd)
    gFit = stats.norm.pdf(gradient, gMean, gStd)

    ax1.plot(intensity, iFit)
    ax1.hist(intensity, normed=True)
    ax2.plot(gradient, gFit)
    ax2.hist(gradient, normed=True)

    plt.show()

    f.close()

    fp = open(fName + '_' + type  + '_model.txt', 'w')
    fp.write(str(iMean) + ' ' + str(iStd) + '\n')
    fp.write(str(gMean) + ' ' + str(gStd) + '\n')
    fp.close()

if __name__ == '__main__':
    main()
