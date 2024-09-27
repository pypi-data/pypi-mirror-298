#!/usr/bin/env python3

import imfind

directory = '/home/ramya/Desktop/backgrounds/'
prompt = "Generate a detailed description of this image. Include any details like backgrounds, patterns, colours, setting/context, actvities depicted etc., that might help uniquely identify the image."

#images = imfind.find_all_image_paths(directory, imfind.config.file_types)
#des = imfind.describe_images_and_cache(images, prompt)
top = imfind.image_search("profile pic of girl", prompt, directory, imfind.config.file_types)
#__import__("IPython").embed()

