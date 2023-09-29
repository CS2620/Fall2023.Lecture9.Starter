import math
from color import Color

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
    from_x = math.floor(x)
    from_y = math.floor(y)
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
    

# def interpolate_nearest_neighbor(self, x, y):
#     return self.color_at(x, y)

def interpolate_bilinear(self, x, y):
    fx = math.floor(x)
    fy = math.floor(y)
    fx_1 = fx+1
    fy_1 = fy+1

    
    ul_x, ul_y = fx, fy
    ur_x, ur_y = fx_1, fy
    ll_x, ll_y = fx, fy_1
    lr_x, lr_y = fx_1, fy_1

    

    color_UL = self.color_at(ul_x, ul_y)
    color_UR = self.color_at(ur_x, ur_y)
    color_LL = self.color_at(ll_x, ll_y)
    color_LR = self.color_at(lr_x, lr_y)

    

    x_percent = math.modf(x)[0]
    y_percent = math.modf(y)[0]

    left = 1-x_percent
    up = 1 - y_percent

    

    top = (
        color_UL[0]*(left)+color_UR[0]*x_percent, 
        color_UL[1]*(left)+color_UR[1]*x_percent, 
        color_UL[2]*(left)+color_UR[2]*x_percent)
    bottom = (
        color_LL[0]*(1-x_percent)+color_LR[0]*x_percent, 
        color_LL[1]*(1-x_percent)+color_LR[1]*x_percent, 
        color_LL[2]*(1-x_percent)+color_LR[2]*x_percent)
    
    color = (
        math.floor(top[0]*(up) + bottom[0]*y_percent),
        math.floor(top[1]*(up) + bottom[1]*y_percent),
        math.floor(top[2]*(up) + bottom[2]*y_percent),
    )

    # return (0,0,255)
    

    return color

def rotate(self, theta):
    new_width = self.width*2
    new_height = self.height*2
    new_pixels = [0, 0, 0] * new_width * new_height
    for y in range(new_height):
        for x in range(new_width):
            
            to_pixel_x = x
            to_pixel_y = y
            to_pixel_index = to_pixel_y*new_width + to_pixel_x

            to_radius = math.sqrt(to_pixel_x**2 + to_pixel_y**2)
            to_theta = math.atan2(to_pixel_y, to_pixel_x)
            from_radius = to_radius
            from_theta = to_theta - theta
            from_x = math.cos(from_theta) * from_radius
            from_y = math.sin(from_theta) * from_radius
            from_color = self.interpolate_nearest_neighbor(from_x,from_y)
            # from_color = self.interpolate_bilinear(from_x, from_y)

            if from_color:
                new_pixels[to_pixel_index] = from_color

    self.pixels = new_pixels
    self.width = new_width
    self.height = new_height
