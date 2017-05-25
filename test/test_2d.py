# coding=utf-8
import numpy
import scipy
from matplotlib import pyplot
from scipy import special

x = numpy.arange(-50, 100, 0.01)
y = scipy.special.erf(0.0447213595499958 * (x - 25)) - 0.050463 * scipy.e ** (-0.002 * (x - 25) * (x - 25))

pyplot.plot(x, y, 'r--')
pyplot.grid(True)
pyplot.show()
