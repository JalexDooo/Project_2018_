import face_recognition as fr
import cv2
import os
import time
import itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import multiprocessing

def thread(id, label_list, known_faces):
	# for id in index_th:
	video_catch = cv2.VideoCapture(id)
	# video_catch.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280);
	# video_catch.set(cv2.CAP_PROP_FRAME_WIDTH, 960);
	# video_catch.set(cv2.CAP_PROP_FPS, 30.0);


	face_locations = []
	face_encodings = []
	face_names = []

	print('%s isOpened!'%id, video_catch.isOpened())
	if not video_catch.isOpened():
		return

	passfps = 0

	starttime = time.time()
	while True:
		ret, frame = video_catch.read()
		curtime = time.time()
		passfps += 1
		if curtime - starttime >= 1:
			print(passfps)
			passfps = 0
			starttime = curtime
		

		# passfps += 1
		# if passfps % 2 != 0:
		# 	continue
		# passftp = 0



		if not ret:
			break
		# print(frame.shape)
		frameface = frame[100:400, 200:900, :]
		cv2.imwrite('test.png', frameface)
		small_frame = cv2.resize(frameface, (0, 0), fx=0.7, fy=0.7)
		# print(small_frame.shape)
		rgb_frame = small_frame[:, :, ::-1]
		

		face_locations = fr.face_locations(rgb_frame, model='cnn')  # ,model="cnn"
		# print(len(face_locations))
		face_encodings = fr.face_encodings(rgb_frame, face_locations)

		face_names = []

		for face_encoding in face_encodings:
			match = fr.compare_faces(known_faces, face_encoding, tolerance=0.425) # 0.425

			name = "???"
			for i in range(len(label_list)):
				if match[i]:
					name = label_list[i]

			face_names.append(name)

		for (top, right, bottom, left), name in zip(face_locations, face_names):

			if not name:
				continue
			top *= 1.4285
			right *= 1.4285
			bottom *= 1.4285
			left *= 1.4285
			

			top = int(top+0.5)
			right = int(right+0.5)
			bottom = int(bottom+0.5)
			left = int(left+0.5)

			top += 100
			bottom += 100
			left += 200
			right += 200
			pil_im = Image.fromarray(frame)
			draw = ImageDraw.Draw(pil_im)
			font = ImageFont.truetype('./STHeiti Medium.ttc', 24,
									  encoding='utf-8')
			draw.text((left + 6, bottom - 25), name, (0, 0, 255), font=font)

			frame = np.array(pil_im)
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
		cv2.imshow('Video_%s' % id, frame)

		c = cv2.waitKey(1)
		if c & 0xFF == ord("q"):
			break

	video_catch.release()
	cv2.destroyWindow('Video_%s' % id)


class multiprocessing_face_recognition(object):
	"""docstring for multiprocessing_face_recognition"""
	def __init__(self, number_of_cpu, num_cam_list, label_list, known_faces):
		super(multiprocessing_face_recognition, self).__init__()
		self.number_of_cpu = number_of_cpu
		self.label_list = label_list
		self.known_faces = known_faces
		self.num_cam_list = num_cam_list

		self.process_images_in_process_pool(self.num_cam_list, self.number_of_cpu, self.label_list, self.known_faces)

	def process_images_in_process_pool(self, index_th, number_of_cpus, label_list, known_faces):
		if number_of_cpus == -1:
			processes = None
		else:
			processes = number_of_cpus

		# macOS will crash due to a bug in libdispatch if you don't use 'forkserver'
		context = multiprocessing
		if "forkserver" in multiprocessing.get_all_start_methods():
			context = multiprocessing.get_context("forkserver")

		pool = context.Pool(processes=processes)

		function_parameters = zip(
			index_th,
			itertools.repeat(label_list),
			itertools.repeat(known_faces),
		)

		pool.starmap(thread, function_parameters)
		