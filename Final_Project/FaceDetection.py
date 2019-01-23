# !/usr/bin/env python3
import csv
import cv2
import imutils
import numpy as np
import pandas as pd
import face_recognition
from imutils import face_utils
from PIL import Image, ImageDraw
from visual import HOG_features


def write_csv(features, filename):
	feat_to_csv_final = []
	with open(filename, 'a') as feat:
		wr = csv.writer(feat, delimiter=',')
		for i in features:
			feat_to_csv = []
			print i[0]
			for j in range(len(i[0])):
				feat_to_csv.append(float('%.5f'%(i[0][j])))
			wr.writerow(feat_to_csv)

def face_detection(path, filename):
	videopath = path + filename
	print videopath
	cap = cv2.VideoCapture(videopath)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
	fps = cap.get(cv2.CAP_PROP_FPS)
	length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	print( "video for face detection ", length )
	print ('fps = ', fps)
	fps_median = int((fps)/2)
	#print (fps_median )
	facesInFrame = []
	final_faces_feat = []
	times = 0
	next_time = fps_median
	while True:
		times +=1
		#print times
		ret, image_np = cap.read()
		if (times == next_time):
			if next_time < length:			
				next_time = times + int(fps + 1)
				#print "next_time", next_time
			else:
				next_time = length
			if not image_np is None:
				print ("processing the", times, "frame")
				image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
				rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
				rgb = imutils.resize(image_np, width=750)
				r = image_np.shape[1] / float(rgb.shape[1])
				boxes = face_recognition.face_locations(rgb, model="hog", number_of_times_to_upsample=2)
				#print "boxes", boxes
				box_num = len(boxes)
				faces_feat = []
				for (top, right, bottom, left) in boxes:
					top = int(top * r)
					right = int(right * r)
					bottom = int(bottom * r)
					left = int(left * r)
					cv2.rectangle(image_np, (left, top), (right, bottom), (0, 255, 0), 2)
					crop_img = image_np[top: bottom, left:right]
					
					crop_img = cv2.resize(crop_img, dsize=(100,100))
					crop_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)
					cv2.imshow("cropped", crop_img)						
					f, fn = HOG_features(crop_img)
					faces_feat.append(f)
				#print len(faces_feat[0])
				if len(faces_feat) == 1:
					x = faces_feat[0]
					final_faces_feat.append([x])
					#print "faces", x
				else:
					for i in range(len(faces_feat)):
						if i == 0:
							x = faces_feat[i]
						else:
							x = x + faces_feat[i]
					#print "x", x	
					final_faces_feat.append([x])
					
				facesInFrame.append(len(boxes))

				image_np = cv2.resize(image_np, dsize=(350,200))
				new_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
				cv2.imshow('Face Detection', new_image)

			else:
				break

			if cv2.waitKey(40) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break

	return final_faces_feat[:55]
