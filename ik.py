#   We will need the Jacobian matrix of the robot
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from fwk import fwk
import math
from math import pi, radians
from copy import deepcopy
from plotter import plot


# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


def jacobian(Frame):
    J = np.zeros((6, len(Frame)))
    O_e = Frame[-1][0:3, 3]
    O_o = np.zeros(3)
    z_1 = np.array([0, 0, 1])
    for i in range(len(Frame)):
        z_2 = Frame[i][0:3, 2]
        cp = np.cross(z_1.transpose(), O_e.transpose() - O_o.transpose())
        col = np.zeros((6, 1))
        col[0:3, 0] = cp
        col[3:6, 0] = z_2
        J[:, i] = col[:, 0]
        z_1 = z_2
        O_o = Frame[i][0:3, 3]
    return J


def update_DH(DH, q):
    dh_copy = deepcopy(DH)
    # iterate along q
    for i in range(len(q)):
        for j in range(len(dh_copy[i])):
            if type(dh_copy[i][j]) == str:
                if "q"+str(i+1) in dh_copy[i][j]:
                    # update q value
                    dh_copy[i][j] = dh_copy[i][j].replace("q"+str(i+1), str(q[i]))
                    dh_copy[i][j] = eval(dh_copy[i][j])
    return dh_copy


def ik(des_pose, q, DH):
    # des_pos is given in matrix form
    # q is the actual joint values vectors
    # DH is the Denavit Hartemberg parameters table of the robot
    alpha = 1
    # First update the DH values
    print(DH)
    dh = update_DH(DH, q)
    # From the actual dh table get the frame
    tr, frame = fwk(dh)
    # Get the actual pose in vector form
    act_pose = np.zeros((6, 1))
    act_pose[0:3] = np.array([[frame[-1][0, -1]], [frame[-1][1, -1]], [frame[-1][2, -1]]])
    RYZ = rotationMatrixToEulerAngles(frame[-1][0:3, 0:3])
    act_pose[3:6] = np.array([[RYZ[0]], [RYZ[1]], [RYZ[2]]])
    # Get the desired pose in vector form
    d_pose = np.zeros((6, 1))
    d_pose[0:3] = np.array([[des_pose[0, -1]], [des_pose[1, -1]], [des_pose[2, -1]]])
    RYZ = rotationMatrixToEulerAngles(des_pose[0:3, 0:3])
    d_pose[3:6] = np.array([[RYZ[0]], [RYZ[1]], [RYZ[2]]])
    # Get the vector e
    e = np.zeros((6, 1))
    e[0] = np.dot(frame[-1][0:3, 0], (des_pose[0:3, -1] - frame[-1][0:3, -1]))
    e[1] = np.dot(frame[-1][0:3, 1], (des_pose[0:3, -1] - frame[-1][0:3, -1]))
    e[2] = np.dot(frame[-1][0:3, 2], (des_pose[0:3, -1] - frame[-1][0:3, -1]))
    e[3] = (frame[-1][0:3, 2] @ des_pos[0:3, 1] - des_pose[0:3, 2] @ frame[-1][0:3, 1]) / 2
    e[4] = (frame[-1][0:3, 1] @ des_pos[0:3, 2] - des_pose[0:3, 0] @ frame[-1][0:3, 2]) / 2
    e[5] = (frame[-1][0:3, 0] @ des_pos[0:3, 0] - des_pose[0:3, 1] @ frame[-1][0:3, 0]) / 2
    # print(d_pose)
    print(e)
    # Compute error
    errP = np.linalg.norm(e[0:3])
    errR = np.linalg.norm(e[3:6])
    print('error', errR)
    # print(not all(err[i] < 0.00001 for i in range(len(err))))
    iter = 0
    while errP > 0.09:
        # Compute the Jacobian Matrix
        J = jacobian(frame)
        # Compute change in joints
        delta = np.linalg.pinv(J) @ e * alpha  # Next q value
        delta = (delta.transpose().tolist())
        for i in range(len(q)):
            q[i] = q[i] - delta[0][i]
        print("errorP", errP, "errorR", errR, ' iteration ', iter)
        # print(err.transpose())
        # new actual pose
        dh = update_DH(DH, q)
        tr, frame = fwk(dh)
        act_pose = np.zeros((6, 1))
        act_pose[0:3] = np.array([[frame[-1][0, -1]], [frame[-1][1, -1]], [frame[-1][2, -1]]])
        RYZ = rotationMatrixToEulerAngles(frame[-1][0:3, 0:3])
        act_pose[3:6] = np.array([[RYZ[0]], [RYZ[1]], [RYZ[2]]])
        # Get the vector e
        e = np.zeros((6, 1))
        e[0] = np.dot(frame[-1][0:3, 0], (des_pose[0:3, -1] - frame[-1][0:3, -1]))
        e[1] = np.dot(frame[-1][0:3, 1], (des_pose[0:3, -1] - frame[-1][0:3, -1]))
        e[2] = np.dot(frame[-1][0:3, 2], (des_pose[0:3, -1] - frame[-1][0:3, -1]))
        e[3] = (frame[-1][0:3, 2] @ des_pos[0:3, 1] - des_pose[0:3, 2] @ frame[-1][0:3, 1]) / 2
        e[4] = (frame[-1][0:3, 1] @ des_pos[0:3, 2] - des_pose[0:3, 0] @ frame[-1][0:3, 2]) / 2
        e[5] = (frame[-1][0:3, 0] @ des_pos[0:3, 0] - des_pose[0:3, 1] @ frame[-1][0:3, 0]) / 2
        # Compute error
        errP = np.linalg.norm(e[0:3])
        errR = np.linalg.norm(e[3:6])
        iter += 1
    print("errorP", errP, "errorR", errR, ' iteration ', iter)
    return q


# sample run...
# 1) Write the DH table of the Baxter robot
# Init plot
fig = plt.figure()
ax = plt.axes(projection="3d")
# Remember that the Dh table is in the form of: [theta, d, alpha, a] and
# actuated joints should be written in the form of the next example:

Dh = [["q1", 0.27, -pi/2, 0.069],
      ["q2+pi/2", 0, pi/2, 0],
      ["q3", 0.102+0.262, -pi/2, 0.069],
      ["q4", 0, pi/2, 0],
      ["q5", 0.104+0.271, -pi/2, 0.01],
      ["q6", 0, pi/2, 0],
      ["q7", 0.28, 0, 0]]
# 2) The desired position is written in homogeneous matrix form
des_pos = np.array([[1, 0, 0, -0.4],
                    [0, 1, 0, 0.24],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
# 3) Set an initial guess of the value of all actuated joints or
# if the robot is in already in a known position, you should use
# that value.
q = [radians(-60), radians(30), radians(-30), 1, 0, 0, 0]
# 4) Run the Inverse Kinematics function to find the value of the
# joint values for the desired given pose.
q_final = ik(des_pos, q, Dh)
print("q = ", q_final)
# 5) If you want the reached position using the ik function: First 
# update the DH table to the value found using the inverse kinematics 
dh = update_DH(Dh, q_final)
print("final dh table: ", dh)
# 6) If you want the final pose of the robot after the iterative
# computations you can use frame[-1] or if you only want the values xyz  (i.e. only the translations) use frame[-1][0:3, -1]
tr, frame = fwk(dh)
# 7) In case that you want to plot. You can use the plot function
# from plotter.py (already imported in this script)
plot(frame, ax)

