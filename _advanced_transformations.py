import math
from color import Color
import numpy as np

def translate(self, dx:float, dy:float):
  """ Translate the pixel (but don't translate the layer itself)"""
  new_width = self.width + math.ceil(dx)
  new_height = self.height + math.ceil(dy)
  new_pixels = [0, 0, 0] * new_width * new_height
  for y in range(new_height):
      for x in range(new_width):
          to_pixel_x = x
          to_pixel_y = y
          to_pixel_index = to_pixel_y*new_width + to_pixel_x

          from_x = to_pixel_x - math.ceil(dx)
          from_y = to_pixel_y - math.ceil(dy)
          if from_x < 0 or from_y < 0:
              continue
          from_index = self.pixelIndex(from_x, from_y)
          if(from_index >= 0):
              from_pixel = self.pixels[from_index]

              new_pixels[to_pixel_index] = from_pixel
  self.pixels = new_pixels
  self.width = new_width
  self.height = new_height

def scale_backward(self, dx:float, dy:float):
    """Scale the image"""
    new_width = math.floor(self.width * dx)
    new_height = math.floor(self.height * dy)
    new_pixels = [0, 0, 0] * new_width * new_height
    for y in range(new_height):
        for x in range(new_width):
            to_pixel_x = x
            to_pixel_y = y
            to_pixel_index = to_pixel_y*new_width + to_pixel_x

            from_x = math.floor(to_pixel_x / dx)
            from_y = math.floor(to_pixel_y/dy)
            if from_x < 0 or from_y < 0:
                continue
            from_index = self.pixelIndex(from_x, from_y)
            if(from_index >= 0):
                from_pixel = self.pixels[from_index]

                new_pixels[to_pixel_index] = from_pixel
    self.pixels = new_pixels
    self.width = new_width
    self.height = new_height

def scale_forward(self, dx, dy):
    new_width = math.floor(self.width * dx)
    new_height = math.floor(self.height * dy)
    new_pixels = [0, 0, 0] * new_width * new_height
    for y in range(self.height):
        for x in range(self.width):
            to_pixel_x = math.floor(x * dx)
            to_pixel_y = math.floor(y * dy)
            to_pixel_index = to_pixel_y*new_width + to_pixel_x

            from_x = x
            from_y = y
            from_index = self.pixelIndex(from_x, from_y)
            from_pixel = self.pixels[from_index]
            new_pixels[to_pixel_index] = from_pixel
    self.pixels = new_pixels
    self.width = new_width
    self.height = new_height

def interpolate_nearest_neighbor(self, x, y):
    from_x = math.floor(x + .5)
    from_y = math.floor(y + .5)
    if from_x < 0 or from_x >= self.width or from_y < 0 or from_y >= self.height:
        return None
    pixel_index = self.pixelIndex(from_x, from_y)
    return self.pixels[pixel_index]
    

def color_at(self, x, y):
    from_x = x
    from_y = y
    if from_x < 0 or from_x >= self.width or from_y < 0 or from_y >= self.height:
        return [0, 0, 0]
    pixel_index = self.pixelIndex(from_x, from_y)
    return self.pixels[pixel_index]
    

def interpolate_bilinear(self, x, y):
    # Get the percent in x and y
    
    # Get the x and y value of the pixels before and after
    
    # Get the x and y values of the four surrounding pixels
    
    # use self.color_at to get these four pixels

    # Calculate the top interpolation
    
    # Calculate the bottom interpolation

    # Calculate the final interpolation

    # This is just a placeholder
    return (0,0,255)
    #return color

def get_in_place_matrix(self, new_width, new_height, theta):
    translation = np.identity(3)
    # translation[0,2] = -new_width/2
    # translation[1,2] = -new_height/2

    rotation = np.identity(3)
    # rotation[0,0] = math.cos(-theta)
    # rotation[0,1] = -math.sin(-theta)
    # rotation[1,0] = math.sin(-theta)
    # rotation[1,1] = math.cos(-theta)

    untranslation = np.identity(3)
    # untranslation[0,2] = new_width/2
    # untranslation[1,2] = new_height/2

    first_half = np.matmul(rotation, translation)
    combined = np.matmul(untranslation, first_half)
    return combined

def get_expanded_matrix(self, new_width, new_height, theta, offset_x, offset_y):
    translation = np.identity(3)
    
    rotation = np.identity(3)
    
    untranslation = np.identity(3)
    
    first_half = np.matmul(rotation, translation)
    combined = np.matmul(untranslation, first_half)
    return combined

def rotate_same_size(self, theta):
    new_width = self.width
    new_height = self.height
    new_pixels = [0, 0, 0] * new_width * new_height

    combined = self.get_in_place_matrix(new_width, new_height, theta)

    for y in range(new_height):
        for x in range(new_width):
            
            to_pixel_x = x
            to_pixel_y = y
            to_pixel_index = to_pixel_y*new_width + to_pixel_x

            v = np.array([to_pixel_x, to_pixel_y, 1])            
            transformed = np.matmul(combined, v)

            from_x = transformed[0]
            from_y = transformed[1]

            from_color = self.interpolate_nearest_neighbor(from_x,from_y)
            #from_color = self.interpolate_bilinear(from_x, from_y)

            if from_color:
                new_pixels[to_pixel_index] = from_color

    self.pixels = new_pixels
    self.width = new_width
    self.height = new_height

def rotate_expand(self, theta):
    new_width = self.width
    new_height = self.height
    new_pixels = [0, 0, 0] * new_width * new_height

    combined = self.get_in_place_matrix(new_width, new_height, theta)

    # ul = np.matmul(combined, np.array([0,0,1]))
    # ur = np.matmul(combined, np.array([self.width,0,1]))
    # ll = np.matmul(combined, np.array([0,self.height,1]))
    # lr = np.matmul(combined, np.array([self.width,self.height,1]))

    # corners = [ul, ur, ll, lr]

    # max_x = max(map(lambda two:two[0], corners))
    # min_x = min(map(lambda two:two[0], corners))

    # max_y = max(map(lambda two:two[1], corners))
    # min_y = min(map(lambda two:two[1], corners))

    # rotated_width = max_x - min_x
    # rotated_height = max_y - min_y

    # new_width = math.ceil(rotated_width)
    # new_height = math.ceil(rotated_height)
    # new_pixels = [0, 0, 0] * new_width * new_height

    # self.parent.resize(new_width,new_height)
    # combined = self.get_expanded_matrix(new_width, new_height, theta, min_x, min_y)

    for y in range(new_height):
        for x in range(new_width):
            to_pixel_x = x
            to_pixel_y = y
            to_pixel_index = to_pixel_y*new_width + to_pixel_x

            v = np.array([to_pixel_x, to_pixel_y, 1])            
            transformed = np.matmul(combined, v)

            from_x = transformed[0]
            from_y = transformed[1]

            from_color = self.interpolate_nearest_neighbor(from_x,from_y)
            #from_color = self.interpolate_bilinear(from_x, from_y)

            if from_color:
                new_pixels[to_pixel_index] = from_color

    self.pixels = new_pixels
    self.width = new_width
    self.height = new_height
