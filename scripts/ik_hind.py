import math as mt

def ik(x, y, qf1234):
    l1 = 55
    l2 = 71
    l3 = 55
    l4 = 40
    qf = mt.radians(292)
    qf1 = mt.atan2(y, x)  # sol of q1
    q1 = qf1 - qf
    # solving for q3
    X = l2
    Y = l3
    Z1 = x - l4*mt.cos(qf1234) - l1*mt.cos(qf1)
    Z2 = y - l4*mt.sin(qf1234) - l1*mt.sin(qf1)
    cosq3 = (Z1**2+Z2**2-X**2-Y**2)/(2*X*Y)
    q3 = mt.atan2(mt.sqrt(1-cosq3**2), cosq3)
    # q3 = qf3 - qf    # sol of q3
    # solving for q2
    B1 = X + Y*mt.cos(q3)
    B2 = Y*mt.sin(q3)
    sinqf2 = (B1*Z2-B2*Z1)/(B1**2 + B2**2)
    cosqf2 = (B1*Z1+B2*Z2)/(B1**2 + B2**2)
    qf12 = mt.atan2(sinqf2, cosqf2)
    q2 = qf12 - qf - q1   # sol of q2
    q4 = qf1234 - qf - q1 - q2 - q3
    return qf, q1, q2, q3, q4


# Main
'''
qf, q1, q2, q3, q4 = ik(-14, -26, mt.radians(180))
Tf = np.eye(3)
T1 = fk.T_01(qf, q1)
fk.plot_frame(Tf, T1)
T2 = fk.T_02(qf, q1, q2)
fk.plot_frame(T1, T2)
T3 = fk.T_03(qf, q1, q2, q3)
fk.plot_frame(T2, T3)
T4 = fk.T_04(qf, q1, q2, q3, q4)
fk.plot_frame(T3, T4)
plt.xlabel('[mm]')
plt.ylabel('[mm]')
plt.axis('square')
plt.show()
'''
