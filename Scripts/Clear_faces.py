

import numpy as np
import os
import json
known_names = []
known_name_encodings = []

#image = fr.load_image_file('image1.jpg')
#encoding = fr.face_encodings(image)[0]

#known_name_encodings.append(encoding)
#known_names.append('Tulsi')

np.save('faces.npy',known_name_encodings)
print(known_names)
#print(known_name_encodings)

with open('name.json', 'w') as file:
    json.dump([], file)
    
with open('names.json', 'w') as file:
    json.dump([], file)



