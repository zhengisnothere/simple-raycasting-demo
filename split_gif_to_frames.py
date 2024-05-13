from PIL import Image
from math import floor
import os
import shutil

def clear_folder_content(folder_path):
  for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))

def extract_images(gif_path,out_path,frame_rate):
  clear_folder_content(out_path)
  with Image.open(gif_path) as im:
    #33 is the frame rate of gif
    num_key_frames=floor(im.n_frames/33*frame_rate)
    print(im.n_frames)
    for i in range(num_key_frames):
      im.seek(floor(im.n_frames / num_key_frames * i))
      im.save(out_path+'{}.png'.format(i))

extract_images('gif/jinitaimei_1.gif','images/jinitaimei/',12)
print('done')
