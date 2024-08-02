from settings import *

def import_image(*path, format = 'png', alpha = True):
    # Pulls all the information from the path and converts the format to a string with an fstring
    full_path = join(*path) + f'.{format}'
    # Returns the file location and converts it to alpha if alpha is true otherwise it just converts it
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    # Using the walk method to walk through the folder path to the sub folders and grab the file names
    for folder_path, _, file_names in walk(join(*path)):
        # Grabs all the file names, sorts them by the name, starting with the first one and splitting the name on the '.'
        for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])): 
            full_path = join(folder_path, file_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames