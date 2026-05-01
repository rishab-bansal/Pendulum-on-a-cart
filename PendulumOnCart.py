# Lets simulate the system for some initial theta
# We will record the variations in theta and x
import numpy as np
import matplotlib.pyplot as plt
import math

# Parameters
#Defining the dynamics
m = 0.1
M = 1
g = 9.81
l = 1
params = [m, M, g, l]


# Time step width
dt = 0.01

# Number of steps
N = 1000
# Defining the input force


def acc(theta,params,F,vtheta):
  m = params[0]
  M = params[1]
  g = params[2]
  l = params[3]

  n = (m+M)*g*math.sin(theta)-m*l*math.sin(theta)*math.cos(theta)*(vtheta)**2
  cost = math.cos(theta)
  d = m*l*(math.sin(theta))**2 + M*l

  acc_theta = n/d - F*cost/d
  # acc_x = (n/cost)/(d/l) + g*math.tan(theta) + F/(d/l)
  # acc_x = -(n/cost)/(d/l) + g*math.tan(theta) + F/(d/l)
  acc_x = (m*l*math.sin(theta)*(vtheta)**2 - m*g*math.sin(theta)*math.cos(theta))/(d/l) + F/(d/l)
  return [acc_theta, acc_x]


def ss(s, F):
  a1 = -m*g/M
  a2 = (m+M)*g/(M*l)
  b1 = 1/M
  b2 = -1/(M*l)

  A = np.matrix([[0, 1, 0, 0],[0, 0, a1, 0],[0,0,0,1],[0,0,a2,0]])
  B = np.matrix([0, b1, 0, b2]).T
  s = A @ s + B @ F

  return s

setpoint = np.array([0,0,0,0])

def lqr(s):
  K = np.matrix([-1.0000,   -2.0317,  -32.8597,  -10.0141])
  feedback = -setpoint + s
  F = float(- K @ feedback)
  # F = 0
  # if ct == 0:
  #   F = -10
  # else:
  #   F = 0
  sd = np.zeros(4)

  # Calculating the derivatives
  sd[0] = s[1]
  sd[2] = s[3]
  [sd[3], sd[1]] = acc(float(s[2]), params, F, float(s[3]))

  return sd


# Initial state
vx = 0            # Translational velocity of cart
x = 0.00          # Position of cart
tdi = 30        # Angle of pendulum in degrees
th = math.pi/180 * tdi # Angle in radians
wt = 0            # Angular velocity of pendulum

# Arrays to record the data
ct = 0 # Current time
t = np.array([])

arrx = np.array([])
arrv = np.array([])

arrt = np.array([])
arrw = np.array([])

arrax = np.array([])

s = np.array([x, vx, th, wt]) # Current states

for i in range(N):

  t = np.append(t,ct)

  # Calculating the new states using lqr
  
  # Point at which the system has to be stabilized
  setpoint = np.array([0,0,0,0])
  
  
  k1s = dt*lqr(s)
  k2s = dt*lqr(s+0.5*k1s)
  k3s = dt*lqr(s+0.5*k2s)
  k4s = dt*lqr(s+k3s)

  s += (k1s + 2*k2s + 2*k3s + k4s)/6 # New states
  arrx = np.append(arrx, s[0])
  arrv = np.append(arrv, s[1])

  arrt = np.append(arrt, s[2])
  arrw = np.append(arrw, s[3])

  ct += dt


# plt.plot(t, arrv, label = "Velocity of cart")
plt.plot(t, arrx, label = "Distance covered by the cart")
# plt.plot(t, arrt, label = "Angle of the pendulum")
plt.grid()
plt.legend()
plt.show()

# Saving the data genereated
# arrax, arrx, arrv, arrt, arrw
# data = np.array([[arrax[_], arrx[_], arrv[_], arrt[_], arrw[_]] for _ in range(N)])
data = np.column_stack((arrx, arrv, arrt, arrw))
np.savetxt("data.csv", data, delimiter = ",", header = "xp,xv,angle,w", comments = "")