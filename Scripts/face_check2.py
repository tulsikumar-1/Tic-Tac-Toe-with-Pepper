import os
import subprocess
import time
import json
import cv2
import face_recognition as fr
import numpy as np

with open('names.json', 'r') as file:
 known_names = json.load(file)
#known_names =np.array(known_names)

known_name_encodings = np.load('faces.npy')


def main():
	face_encoding=np.array([])
	match=[False]
	try:
	    subprocess.run(['python3', '/home/kumar/playground/demo/sample/scripts/capture.py'])
	    image = fr.load_image_file('/home/kumar/playground/demo/sample/scripts/web/captured_image.jpg')
	    face_encoding = fr.face_encodings(image)[0]
	    with open('face.json', 'w') as file:
	      json.dump([1], file)
	except:
	    #print('Please come closer to Camera'
	    time.sleep(1)
	if face_encoding.size==0:
	    with open('face.json', 'w') as file:
	      json.dump([0], file)
	    return
	    

	match = fr.compare_faces(known_name_encodings, face_encoding)
	print('match:',match)
	if len(match)==0:
	  match=[False]
	face_distances = fr.face_distance(known_name_encodings, face_encoding)
	try:
	   best_match = np.argmin(face_distances)
	except: 
	   best_match=0

	if match[best_match]==False:
	   print('Match Not found')
	   #name=input('Please tell me your name')
	   known_name_encodings1=known_name_encodings.tolist()
	  # known_names1=known_names.tolist()
	  # known_names1.append(name)
	   known_name_encodings1.append(face_encoding)
	  # np.save('names.npy', known_names1)
	   np.save('faces.npy',known_name_encodings1)
	   # Save the variable to a file
	   with open('name.json', 'w') as file:
	    json.dump([], file)
	  # print('Hello', name)
	   
	  
	else:
	  # print('Hello',known_names[best_match])
	   with open('name.json', 'w') as file:
	     json.dump([known_names[best_match]], file)
	     
	     
if __name__ == "__main__":
    main()

