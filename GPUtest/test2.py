import torch as t
import cv2




x=t.rand(5,3)

y=t.rand(5,3)

if t.cuda.is_available():

	x=x.cuda()

	y=y.cuda()
	
	print(x+y)

