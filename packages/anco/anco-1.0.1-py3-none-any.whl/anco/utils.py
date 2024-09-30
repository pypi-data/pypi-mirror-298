import taichi as ti

class Utils():
    def __init__(self):
        pass

    @staticmethod
    def create_single_float_field(a: float):
        field = ti.field(dtype=ti.f32, shape=())
        field[None] = a
        return field

    @staticmethod
    def create_single_int_field(a: int):
        field = ti.field(dtype=ti.i32, shape=())
        field[None] = a
        return field