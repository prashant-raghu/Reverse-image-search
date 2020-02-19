from helper.hashing import convert_hash
from helper.hashing import dhash
import argparse
import pickle
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tree", required=True, type=str,
	help="path to pre-constructed VP-Tree")
ap.add_argument("-a", "--hashes", required=True, type=str,
	help="path to hashes dictionary")
ap.add_argument("-q", "--query", required=True, type=str,
	help="path to input query image")
ap.add_argument("-d", "--distance", type=int, default=10,
	help="maximum hamming distance")
args = vars(ap.parse_args())

print(" loading VP-Tree and hashes...")
tree = pickle.loads(open(args["tree"], "rb").read())
hashes = pickle.loads(open(args["hashes"], "rb").read())

image = cv2.imread(args["query"])
cv2.imshow("Query", image)

queryHash = dhash(image)
queryHash = convert_hash(queryHash)

# search
print(" performing search...")
start = time.time()
results = tree.get_all_in_range(queryHash, args["distance"])
results = sorted(results)
end = time.time()
print(" search took {} seconds".format(end - start))

# loop over the results
for (d, h) in results:
	# grab all image paths in our dataset with the same hash
	resultPaths = hashes.get(h, [])
	print(" {} total image(s) with d: {}, h: {}".format(
		len(resultPaths), d, h))

	# loop over the result paths
	for resultPath in resultPaths:
		# load the result image and display it to our screen
		result = cv2.imread(resultPath)
		cv2.imshow("Result", result)
		cv2.waitKey(0)