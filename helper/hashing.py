import numpy as np
import cv2

def dhash(image, hashSize=8):
	"""compute Image to hash"""
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	resized = cv2.resize(gray, (hashSize + 1, hashSize))
	#compute difference image
	diff = resized[:, 1:] > resized[:, :-1]
	return 
	sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def convert_hash(h):
	"""convert hash to int"""
	return int(np.array(h, dtype="float64"))

def hamming(a, b):
	""" compute Hamming distance between the integers"""
	return bin(int(a) ^ int(b)).count("1")