# USAGE
# python stress_test.py

# import the necessary packages
from threading import Thread
import requests
import time

# initialize the Keras REST API endpoint URL along with the input
# image path
KERAS_REST_API_URL = "http://localhost:6601/predict"
IMAGE_PATH = "/home/hs/caffedl/hs-serving-master/caffe-rest-api/test_images/corrected_walmart_walmart_20200901080459_C02324200401000196.jpg"

# initialize the number of requests for the stress test along with
# the sleep amount between requests
NUM_REQUESTS = 500
SLEEP_COUNT = 0.05

def call_predict_endpoint(n):
	# load the input image and construct the payload for the request
	image = open(IMAGE_PATH, "rb").read()
	payload = {"image": image}

	# submit the request
	r = requests.post(KERAS_REST_API_URL, files=payload).json()

	# ensure the request was sucessful
	if r["success"]:
		print("[INFO] thread {} OK".format(n))
		for (i, result) in enumerate(r["predictions"]):
			print("{}. {}: {:.4f}".format(i + 1, result["label"],
				result["probability"]))		

	# otherwise, the request failed
	else:
		print("[INFO] thread {} FAILED".format(n))

# loop over the number of threads
for i in range(0, NUM_REQUESTS):
	# start a new thread to call the API
	t = Thread(target=call_predict_endpoint, args=(i,))
	t.daemon = True
	t.start()
	time.sleep(SLEEP_COUNT)

# insert a long sleep so we can wait until the server is finished
# processing the images
time.sleep(300)
