from graphics import *
from math import sin, cos, pi, modf
import time
import colorsys

def drawPen():
	l1.undraw()
	l2.undraw()
	c2.undraw()
	c1.undraw()

	a[0] += pi / 2
	a[1] += pi / 2

	l1.p2 = Point(zeroPos[0] + L[0] * cos((a[0])), zeroPos[1] + L[0] * sin((a[0])))
	l1.draw(win)
	l2.p1 = l1.p2
	l2.p2 = Point(l1.p2.x + L[1] * cos((a[1])), l1.p2.y + L[1] * sin((a[1])))
	l2.draw(win)

	c1.p1 = Point(l1.p2.x - r, l1.p2.y - r)
	c1.p2 = Point(l1.p2.x + r, l1.p2.y + r)
	c1.draw(win)
	c2.p1 = Point(l2.p2.x - r, l2.p2.y - r)
	c2.p2 = Point(l2.p2.x + r, l2.p2.y + r)
	c2.draw(win)

	a[0] -= pi / 2
	a[1] -= pi / 2
	
win = GraphWin("Pendulum", 600, 600, autoflush = False)
win.setBackground("black")

zeroPos = [300, 300]
L = [130, 130]
M = [40, 40]
a = [pi / 2, pi / 2]
aV = [0.1, 0]
aA = [0, 0]

g = 1
r = 10

l1 = Line(Point(zeroPos[0], zeroPos[1]), Point(0, 0))
l1.setFill("grey")
l1.setWidth(3)
c1 = Oval(Point(0, 0), Point(0, 0))
c1.setFill("red")

l2 = Line(Point(0, 0), Point(0, 0))
l2.setFill("grey")
l2.setWidth(3)
c2 = Oval(Point(0, 0), Point(0, 0))
c2.setFill("red")

last = 400
path = []
pastP = l2.p2
ones = 0
dtime = 0
while(not(win.checkMouse())):
	stime = time.time()

	num1 = -g * (2 * M[0] + M[1]) * sin(a[0])
	num2 = M[1] * g * sin(a[0] - 2 * a[1])
	num3 = 2 * sin(a[0] - a[1]) * M[1]
	num4 = aV[1] ** 2 * L[1] + aV[0] ** 2 * L[0] * cos((a[0] - a[1]))
	den = L[0] * (2 * M[0] + M[1] - M[1] * cos((2 * a[0] - 2 * a[1])))
	aA[0] = (num1 - num2 - num3 * num4) / den

	num1 = 2 * sin((a[0] - a[1]))
	num2 = aV[0] ** 2 * L[0] * (M[0] + M[1])
	num3 = g * (M[0] + M[1]) * cos((a[0]))
	num4 = aV[1] ** 2 * L[1] * M[1] * cos((a[0] - a[1]))
	den = L[1] * (2 * M[0] + M[1] - M[1] * cos((2 * a[0] - 2 * a[1])))
	aA[1] = num1 * (num2 + num3 + num4) / den
	
	aV[0] += aA[0] 
	aV[1] += aA[1]
	a[0] += aV[0]
	a[1] += aV[1]

	drawPen()
	#Draw Path Line
	if(True and ones):
		path.append(Line(pastP, l2.p2))
		path[-1].setFill("white")
		#RGB
		if(True):
			fractional, whole = modf(time.time() / 5)
			hlsrgb = colorsys.hls_to_rgb(fractional, 1/2, 1)
			rgb = [0, 0, 0]
			for i in range(3):
				rgb[i] = int(hlsrgb[i] * 255)
			path[-1].setFill(color_rgb(int(rgb[0]), int(rgb[1]), int(rgb[2])))
		path[-1].draw(win)

		if(len(path) >= last):
			path[0].undraw()
			path.remove(path[0])
	else:
		ones = 1
	pastP = l2.p2

	win.update()

	dtime = time.time() - stime
	time.sleep(0.01)