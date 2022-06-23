from PIL import Image
import os

def make_gif(frame_folder):
    path = [os.path.join(frame_folder, file) for file in os.listdir(frame_folder)]
    frames = [Image.open(image) for image in path]
    frame_one = frames[0]
    frame_one.save("output.gif", format="GIF", bbox_inches='tight', append_images=frames,
    save_all=True, duration=100, loop=0)
