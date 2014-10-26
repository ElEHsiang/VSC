import sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def main():

    prefix = input('input image fileame :\n')

    fBone = open('model/'+ prefix + '_bone_model.txt', 'r')
    biMean, biStd = fBone.readline()[:-1].split(' ')
    bgMean, bgStd = fBone.readline()[:-1].split(' ')
    fBone.close()

    biMean = float(biMean)
    biStd = float(biStd)
    bgMean = float(bgMean)
    bgStd = float(bgStd)

    fNBone = open('model/' + prefix + '_non-bone_model.txt', 'r')
    nbiMean, nbiStd = fNBone.readline()[:-1].split(' ')
    nbgMean, nbgStd = fNBone.readline()[:-1].split(' ')
    fNBone.close()

    nbiMean = float(nbiMean)
    nbiStd = float(nbiStd)
    nbgMean = float(nbgMean)
    nbgStd = float(nbgStd)

    fig, ax = plt.subplots(2, 1)
    ax1, ax2 = ax.ravel()

    iScale = np.arange(0, 255, 1)
    gScale = np.arange(0, 200, 1)

    Pbi = mlab.normpdf(iScale, biMean, biStd)
    Pbg = mlab.normpdf(gScale, bgMean, bgStd)
    Pnbi = mlab.normpdf(iScale, nbiMean, nbiStd)
    Pnbg = mlab.normpdf(gScale, nbgMean, nbgStd)

    print(Pbi[180])
    print(Pnbi[180])

    ax1.plot(iScale, mlab.normpdf(iScale, biMean, biStd), label='bone')
    ax1.plot(iScale, mlab.normpdf(iScale, nbiMean, nbiStd), label='non-bone')
    ax1.legend()
    ax1.set_title('intensity')

    ax2.plot(gScale, mlab.normpdf(gScale, bgMean, bgStd), label='bone')
    ax2.plot(gScale, mlab.normpdf(gScale, nbgMean, nbgStd), label='non-bone')
    ax2.legend()
    ax2.set_title('gradient')

    plt.show()

if __name__ == '__main__':
    main()
