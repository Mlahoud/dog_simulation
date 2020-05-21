import math as mt

def ik(x, y, q1234):
    l1 = 71
    l2 = 71
    l3 = 71
    l4 = 40
    q1 = mt.atan2(y, x)  # sol of q1
    # solving for q3
    X = l2
    Y = l3
    Z1 = x-l4*mt.cos(q1234)-l1*mt.cos(q1)
    Z2 = y-l4*mt.sin(q1234)-l1*mt.sin(q1)
    cosq3 = (Z1**2+Z2**2-X**2-Y**2)/(2*X*Y)
    q3 = mt.atan2(mt.sqrt(1-cosq3**2), cosq3)    # sol of q3
    # solving for q2
    B1 = X + Y*mt.cos(q3)
    B2 = Y*mt.sin(q3)
    sinq2 = (B1*Z2-B2*Z1)/(B1**2 + B2**2)
    cosq2 = (B1*Z1+B2*Z2)/(B1**2 + B2**2)
    q12 = mt.atan2(sinq2, cosq2)
    q2 = q12 - q1   # sol of q2
    q4 = q1234 - q1 - q2 - q3
    return q1, q2, q3, q4


# Main
'''
q1, q2, q3, q4 = ik(-10, -27.5, mt.radians(180))
Tf = np.eye(3)
T1 = fk.T_01(q1)
fk.plot_frame(Tf, T1)
T2 = fk.T_02(q1, q2)
fk.plot_frame(T1, T2)
T3 = fk.T_03(q1, q2, q3)
fk.plot_frame(T2, T3)
T4 = fk.T_04(q1, q2, q3, q4)
fk.plot_frame(T3, T4)
plt.xlabel('[mm]')
plt.ylabel('[mm]')
plt.axis('square')
plt.show()
'''

