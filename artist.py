import imageio
import sys
import os
import glob

with imageio.get_writer('movie.gif', mode='I') as writer:
    files = glob.glob('images/**.jpg')
    files.sort(key=os.path.getmtime)
    for file in files:
        image = imageio.imread(file)
        writer.append_data(image)
