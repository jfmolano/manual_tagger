
# coding: utf-8

# In[96]:


from os import listdir
from os.path import isfile, join
from random import shuffle
import shutil



class_dict = {
                0:'bus',
                1:'car',
                2:'moto',
                3:'truck'
             }

folder_dict = {}

for i in class_dict:
    folder_dict[class_dict[i]] = join('./', class_dict[i])

for i in class_dict:
    print('%s\t%s' % (i, class_dict[i]))

images_path = './images/'

while True:

	onlyfiles = [f for f in listdir(images_path) if isfile(join(images_path, f))]
	shuffle(onlyfiles)
	file_name = onlyfiles[0]

	img_path = join(images_path, file_name)
	print(img_path)

# shutil.copyfile(img_path, join(folder_dict[class_dict[classification]], file_name))

