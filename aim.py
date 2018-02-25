import pickle
from numpy import *
from scipy.optimize import fmin
from scipy.interpolate import interp1d
with open('theta.pickle', 'rb') as f:
    theta_f = pickle.load(f)

with open('v.pickle', 'rb') as f:
    v_f = pickle.load(f)

g = 9.8

def get_traj(args):
    v, theta = args
    return lambda x: -g*x**2 / (2.0*v**2*cos(radians(theta))**2) + tan(radians(theta))*x

def get_cost2(x, y):
    def cost(alpha):
        theta = theta_f(alpha)
        v = v_f(alpha)
        traj = get_traj(array([v, theta]))
        return (traj(x) - y)**2
    return cost

def get_to(x, y):
    try:
        return fmin(get_cost2(x, y), 25)
    except ValueError:
        raise ValueError('unhittable')
