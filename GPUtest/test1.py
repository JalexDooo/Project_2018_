import os
import gc
import cv2
import sys
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process, Manager


'''
import queue as Queue

queue = Queue.Queue()

def thread(id):

	print('Thread %s get started!'%id)
	id = id[0]
	if id == 0:
		path = '/home/jonty/Videos/1.mp4'
		cap = cv2.VideoCapture(path)

		while True:
			ret, frame = cap.read()
			if not ret:
				break
			try:
				queue.put(frame)
			except Exception as e:
				print(e)

			cv2.imshow('test', frame)
			c = cv2.waitKey(1)
			if c & 0xFF == ord("q"):
				break

		print('000')

	elif id == 1:

		print('111')



	return 


class multiprocess_op(object):

	"""
	Assign tasks to all processes of CPUs.
	"""

	def __init__(self):
		super(multiprocess_op, self).__init__()
		self.process_images_in_process_pool()

	def process_images_in_process_pool(self):
		number_of_cpus = -1

		if number_of_cpus == -1:
			processes = None
		else:
			processes = number_of_cpus

		# macOS will crash due to a bug in libdispatch if you don't use 'forkserver'
		context = multiprocessing
		if "forkserver" in multiprocessing.get_all_start_methods():
			context = multiprocessing.get_context("forkserver")

		# pool = context.Pool(processes=processes)
		# pool = multiprocessing.Pool(processes)
		pool = ThreadPool(processes)



		index_th = []
		for i in range(3):
			index_th.append(i)
		
		function_parameters = zip(
			index_th,
			# itertools.repeat(label_list),
			# itertools.repeat(known_faces),
		)
		pool.map(thread, function_parameters)

		# pool.starmap(thread, function_parameters)

'''


def write(stack, cam, top: int) -> None:
	print('Process to write: %s' % os.getpid())
	cap = cv2.VideoCapture(cam)
	while True:
		ret, frame = cap.read()
		if ret:
			stack.append(frame)

			if len(stack) >= top:
				del stack[:]
				gc.collect()


def read(stack) -> None:
	print('Process to read: %s' % os.getpid())
	while True:
		if len(stack) != 0:
			frame = stack.pop()
			cv2.imshow('img', frame)
			c = cv2.waitKey(1)
			if c & 0xFF == ord("q"):
				break


if __name__ == '__main__':
	q = Manager().list()
	pr = Process(target=read, args=(q, ))
	pw = Process(target=write, args=(q, '/home/jonty/Videos/1.mp4', 100))

	pw.start()
	pr.start()

	pr.join()
	pw.terminate()

