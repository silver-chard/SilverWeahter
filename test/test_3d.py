# coding=utf-8
import numpy
import scipy
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from numpy.core.umath import exp
from scipy.special import erf

fig = pyplot.figure()
ax = Axes3D(fig)

new_temp, old_temp = numpy.mgrid[-50:60:0.5, 0:40:0.5]
sub_temp = new_temp - old_temp
# 标准分值
std_score_o = 0.0875 * sub_temp ** 2
# 标准分值(with负数)
std_score = 0.0875 * (sub_temp ** 3 / abs(sub_temp))
# 标准偏差值
std_sub = scipy.special.erf(0.044721 * (new_temp - 25)) - 0.050463 * (new_temp - 25) * exp(
    -0.002 * (new_temp - 25) ** 2)
# 标准偏差值 * 系数 = 偏差值公式
sub_score = std_score * std_sub
# 分数等于 偏差值+标准分值
score = std_score_o + sub_score

surf = ax.plot_surface(
    old_temp, new_temp, score,
    rstride=7, cstride=7, cmap='cool', alpha=0.8,
    vmin=0, vmax=650, linewidth=0.5)

fig.colorbar(surf, shrink=1, aspect=6)
pyplot.title(u"the relation between new temp and old temp and score")
pyplot.xlabel('old_temp')
pyplot.ylabel('new_temp')
pyplot.clabel('score')
pyplot.show()
