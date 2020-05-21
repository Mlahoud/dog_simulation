import numpy as np
import math as mt
import matplotlib.pyplot as plt


def T_04(q1, q2, q3, q4):
    l1 = 10
    l2 = 10
    l3 = 10
    l4 = 10
    q12 = q1 + q2
    q123 = q1 + q2 + q3
    q1234 = q1 + q2 + q3 + q4
    T = np.array([[mt.cos(q1234), -mt.sin(q1234), l1*mt.cos(q1)+l2*mt.cos(q12)+l3*mt.cos(q123)+l4*mt.cos(q1234)],
                  [mt.sin(q1234),  mt.cos(q1234), l1*mt.sin(q1)+l2*mt.sin(q12)+l3*mt.sin(q123)+l4*mt.sin(q1234)],
                  [0, 0, 1]])
    return T


def T_03(q1, q2, q3):
    l1 = 10
    l2 = 10
    l3 = 10
    q12 = q1 + q2
    q123 = q1 + q2 + q3
    T = np.array([[mt.cos(q123), -mt.sin(q123), l1*mt.cos(q1)+l2*mt.cos(q12)+l3*mt.cos(q123)],
                  [mt.sin(q123),  mt.cos(q123), l1*mt.sin(q1)+l2*mt.sin(q12)+l3*mt.sin(q123)],
                  [0, 0, 1]])
    return T


def T_02(q1, q2):
    l1 = 10
    l2 = 10
    q12 = q1 + q2
    T = np.array([[mt.cos(q12), -mt.sin(q12), l1*mt.cos(q1)+l2*mt.cos(q12)],
                  [mt.sin(q12),  mt.cos(q12), l1*mt.sin(q1)+l2*mt.sin(q12)],
                  [0, 0, 1]])
    return T


def T_01(q1):
    l1 = 10
    T = np.array([[mt.cos(q1), -mt.sin(q1), l1*mt.cos(q1)],
                  [mt.sin(q1),  mt.cos(q1), l1*mt.sin(q1)],
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
    q1 = mt.radians(270)
    q2 = mt.radians(30)
    q3 = mt.radians(300)
    q4 = mt.radians(300)
    return q1, q2, q3, q4
# Main


'''''
q1, q2, q3, q4 = init_q()
Tf = np.eye(3)
T1 = T_01(q1)
plot_frame(Tf, T1)
T2 = T_02(q1, q2)
plot_frame(T1, T2)
T3 = T_03(q1, q2, q3)
plot_frame(T2, T3)
T4 = T_04(q1, q2, q3, q4)
plot_frame(T3, T4)
plt.xlabel('[mm]')
plt.ylabel('[mm]')
plt.axis('square')
plt.show()
'''''

