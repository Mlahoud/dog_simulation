import numpy as np
import math as mt
import matplotlib.pyplot as plt


def T_04(qf, q1, q2, q3, q4):
    l1 = 10
    l2 = 10
    l3 = 10
    l4 = 10
    qf1 = qf + q1
    qf12 = qf + q1 + q2
    qf123 = qf + q1 + q2 + q3
    qf1234 = qf + q1 + q2 + q3 + q4
    T = np.array([[mt.cos(qf1234), -mt.sin(qf1234), l1*mt.cos(qf1)+l2*mt.cos(qf12)+l3*mt.cos(qf123)+l4*mt.cos(qf1234)],
                  [mt.sin(qf1234),  mt.cos(qf1234), l1*mt.sin(qf1)+l2*mt.sin(qf12)+l3*mt.sin(qf123)+l4*mt.sin(qf1234)],
                  [0, 0, 1]])
    return T


def T_03(qf, q1, q2, q3):
    l1 = 10
    l2 = 10
    l3 = 10
    qf1 = qf + q1
    qf12 = qf + q1 + q2
    qf123 = qf + q1 + q2 + q3
    T = np.array([[mt.cos(qf123), -mt.sin(qf123), l1*mt.cos(qf1)+l2*mt.cos(qf12)+l3*mt.cos(qf123)],
                  [mt.sin(qf123),  mt.cos(qf123), l1*mt.sin(qf1)+l2*mt.sin(qf12)+l3*mt.sin(qf123)],
                  [0, 0, 1]])
    return T


def T_02(qf, q1, q2):
    l1 = 10
    l2 = 10
    qf1 = qf + q1
    qf12 = qf + q1 + q2
    T = np.array([[mt.cos(qf12), -mt.sin(qf12), l1*mt.cos(qf1)+l2*mt.cos(qf12)],
                  [mt.sin(qf12),  mt.cos(qf12), l1*mt.sin(qf1)+l2*mt.sin(qf12)],
                  [0, 0, 1]])
    return T


def T_01(qf, q1):
    l1 = 10
    qf1 = qf + q1
    T = np.array([[mt.cos(qf1), -mt.sin(qf1), l1*mt.cos(qf1)],
                  [mt.sin(qf1),  mt.cos(qf1), l1*mt.sin(qf1)],
                  [0, 0, 1]])
    return T


def plot_frame(Tprev, T):
    i = T[0:2, 0]
    j = T[0:2, 1]
    p = T[0:2, 2]
    pp = Tprev[0:2, 2]
    plt.plot([Tprev[0, 2], T[0, 2]], [Tprev[1, 2], T[1, 2]], '-k')
    plt.plot([p[0], p[0]+i[0]], [p[1], p[1]+i[1]], '-r')
    plt.plot([p[0], p[0]+j[0]], [p[1], p[1]+j[1]], '-g')
    plt.plot(pp[0], pp[1], 'ko')
    plt.plot(p[0], p[1], 'ko')


def init_q():
    qf = mt.radians(292)
    q1 = mt.radians(308)
    q2 = mt.radians(60)
    q3 = mt.radians(300)
    q4 = mt.radians(300)
    return qf, q1, q2, q3, q4
# Main


'''''
qf, q1, q2, q3, q4 = init_q()
Tf = np.eye(3)
Tf[0, 0] = mt.cos(qf)
Tf[1, 0] = mt.sin(qf)
Tf[0, 1] = -mt.sin(qf)
Tf[1, 1] = mt.cos(qf)
T1 = T_01(qf, q1)
plot_frame(Tf, T1)
T2 = T_02(qf, q1, q2)
plot_frame(T1, T2)
T3 = T_03(qf, q1, q2, q3)
plot_frame(T2, T3)
T4 = T_04(qf, q1, q2, q3, q4)
plot_frame(T3, T4)
plt.xlabel('[mm]')
plt.ylabel('[mm]')
plt.axis('square')
plt.show()
'''''

