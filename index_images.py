from helper.hashing import convert_hash
from helper.hashing import hamming
from helper.hashing import dhash
from imutils import paths
import argparse
import pickle
import vptree
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, type=str,
	help="path to input directory of images")
ap.add_argument("-t", "--tree", required=True, type=str,
	help="path to output VP-Tree")
ap.add_argument("-a", "--hashes", required=True, type=str,
	help="path to output hashes dictionary")
args = vars(ap.parse_args())

# Initialize the dictionary
imagePaths = list(paths.list_images(args["images"]))
hashes = {}

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# load the input image
	print(" processing image {}/{}".format(i + 1,
		len(imagePaths)))
	image = cv2.imread(imagePath)

	# computing hash for the image
	h = dhash(image)
	h = convert_hash(h)

	# updating  hashes dictionary
	l = hashes.get(h, [])
	l.append(imagePath)
	hashes[h] = l

# build the VP-Tree
print(" building VP-Tree...")
points = list(hashes.keys())
tree = vptree.VPTree(points, hamming)

# pickle the VP-Tree to disk
print("saving VP-Tree...")
f = open(args["tree"], "wb")
f.write(pickle.dumps(tree))
f.close()

print(" serializing hashes...")
f = open(args["hashes"], "wb")
f.write(pickle.dumps(hashes))
f.close()