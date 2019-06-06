import os
import pp
import sys
import multiprocessing
import JidouDetect.jidou_north
import JidouDetect.jidou_south
import GatePeopleIO.GatePeopleIO
from multiprocessing.dummy import Pool as ThreadPool



def thread(id):

	print('Thread %s get started!'%id)
	if id == 0:
		JidouDetect.jidou_south.main()
		print('000')

	elif id == 1:
		JidouDetect.jidou_north.main()
		print('111')

	elif id == 2:
		GatePeopleIO.GatePeopleIO.main()
		print('222')


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


if __name__ == '__main__':
	test = multiprocess_op()
