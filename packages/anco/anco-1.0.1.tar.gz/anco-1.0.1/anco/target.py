import numpy as np
import taichi as ti
from .utils import *

class Target():
    def __init__(self):
        pass

    def init_taichi_objects(self):
        pass

    def get_scatter_function(self):
        return None

    def get_in_target_function(self):
        return None
    
    def get_target_arrived_function(self):
        return None

class PointTarget(Target):
    def __init__(self, location, radius):
        self.location = location
        self.radius = radius
    
    def init_taichi_objects(self):
        self.location_vector = ti.Vector(self.location)
        self.radius_field = Utils.create_single_float_field(self.radius)
    
    def get_scatter_function(self):
        @ti.kernel
        def scatter_in_target(particle_location: ti.template()):  # type: ignore
            for i in particle_location:
                f1 = ti.random()
                f2 = ti.random()
                if(f2 > f1):
                    f1, f2 = f2, f1
                f2 = f2 / f1 * 2. * ti.math.pi
                f1 *= self.radius_field[None]
                particle_location[i] = self.location_vector + ti.Vector([ti.cos(f2), ti.sin(f2)]) * f1
        return scatter_in_target

    def get_in_target_function(self):
        @ti.func
        def in_target(x, y):
            return (x - self.location_vector[0]) ** 2 + (y - self.location_vector[1]) ** 2 < self.radius_field[None] ** 2
        return in_target
    
    def get_target_arrived_function(self):
        @ti.func
        def target_arrived(x, y):
            pass
        return target_arrived

class ImageTarget(Target):
    def __init__(self, image, remove_after_arrived=True):
        self.image = image
        self.remove_after_arrived = remove_after_arrived
    
    def init_taichi_objects(self):
        self.image_field = ti.field(dtype=ti.f32, shape=self.image.shape)
        self.image_field.from_numpy(np.array(self.image, dtype=np.float32))
    
    def get_scatter_function(self):
        number_of_pixels = np.sum(self.image > 0.5)
        if number_of_pixels == 0:
            raise ValueError("Number of pixels of the ImageTarget object is 0.")
        number_of_pixels_field = Utils.create_single_int_field(number_of_pixels)
        @ti.kernel
        def scatter_in_target(particle_location: ti.template()):  # type: ignore
            for i in particle_location:
                pixel_id = int(ti.random() * number_of_pixels_field[None])
                for j, k in ti.ndrange(self.image_field.shape[0], self.image_field.shape[1]):
                    if self.image_field[j, k] > 0.5:
                        if pixel_id == 0:
                            particle_location[i] = ti.Vector([j + ti.random() - 0.5, k + ti.random() - 0.5])
                            break
                        pixel_id -= 1
        return scatter_in_target

    def get_in_target_function(self):
        @ti.func
        def in_target(x, y):
            return self.image_field[int(ti.round(x)), int(ti.round(y))] > 0.5
        return in_target
    
    def get_target_arrived_function(self):
        if self.remove_after_arrived:
            @ti.func
            def target_arrived(x, y):
                self.image_field[int(ti.round(x)), int(ti.round(y))] = 0.
        else:
            @ti.func
            def target_arrived(x, y):
                pass
        return target_arrived