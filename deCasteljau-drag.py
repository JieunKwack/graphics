"""
compute the mean and stddev of 100 data sets and plot mean vs stddev.
When you click on one of the mu, sigma points, plot the raw data from
the dataset that generated the mean and stddev
"""
import numpy as np
import math as math
import matplotlib.pyplot as plt

# # of line segments
NR_SEG = 100
# # of control points
NR_CP  = 4

def onpick(event):
	global select
	event.ind
	N = len(event.ind) # length of event.ind(ex? only my think)
	if not N: return True
	select = event.ind[0]

	return True


def ondrag(event):
	global select, line, curve, P, fig, bezier
	if select==-1: return True;
	if(event.xdata is None or event.ydata is None): return True;

#Update
	P[select, :] = [event.xdata, event.ydata];
	Bezier = deCasteljau(NR_CP-1, 0);
	line.set_data(P[:,0], P[:,1]);
	bezier.set_data(Bezier[:,0], Bezier[:,1]);
	fig.canvas.draw()

	return True


def onrelease(event):
	global select
	select = -1
	return True;

def deCasteljau(level, i):
	global P, Bezier
	t = np.arange(0, 1.01, 0.01).reshape(101,1)
	if(level == 0): return P[i,:]
	Bezier = (1-t)*deCasteljau(level-1, i)+t*deCasteljau(level-1, i+1)
	return Bezier

select = -1; # select : point that was changed

P = np.random.rand(NR_CP, 2) # 4개의 control points(that 4x2 matrix format)를 랜덤하게 생성

fig	   = plt.figure() # create a new figure
# 마치 매틀랩에서 plot찍기전에 figure 하나 생성하는 것과 같은 느낌!할 수 있다 지은아.
line,  = plt.plot(P[:,0], P[:,1], 's-', picker=5)  # 5 points tolerance
Bezier = deCasteljau(NR_CP-1, 0);
bezier, = plt.plot(Bezier[:,0],Bezier[:,1],'-')
# P[:,0], P[:,1] : plot x=(P[:,0]) and y=(P[:,1]), using 4개의 점을 찍음
# '-' : solid line style, 's' : square marker
# *not perfect* picker : float distance in points or callable pick function fn(artist, event)

#register event handler
fig.canvas.mpl_connect('pick_event', onpick) # returns a connection id which is simply an integer
# when you want to disconnect the callback, just call: fig.canvas.mpl_disconnect(cid)
# event name: 'pick_event' - PickEvent(an object in the canvas is selected)
# 점 하나를 클릭했을때
fig.canvas.mpl_connect('button_release_event', onrelease)
# 'button_release_event' - MouseEvent(mouse button is released)
# 마우스 버튼을 놓았을때
fig.canvas.mpl_connect('motion_notify_event', ondrag)
# 'motion_notify_event' - MouseEvent(mouse motion)
# 마우스가 움직일때
plt.show()
