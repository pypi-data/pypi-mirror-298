from typing import List, Union
import numpy as np
from numpy.typing import NDArray
import taichi as ti
from .target import *

__version__ = "1.0.0"

@ti.data_oriented
class ImageSystem():
    def __init__(self,
                 resolution: List[int],
                 map: NDArray[Union[np.float32, np.float64]],
                 targets: List[Target],  # 目标，如巢穴、食物
                 particle_source_id: int = 0,  # 初始时刻粒子从第几个target上发射出
                 chemical_number: int = 2,  # 信息素种类数
                 particle_number: int = 5000,  # 粒子数
                 dt: float = 0.3,  # 时间步长
                 random_force_strength: float = 0.1163,  # 随机力系数
                 chemical_release_speed: Union[float, List[Union[float]], NDArray[Union[np.float32, np.float64]]] = 0.6569,  # 释放信息素速率
                 diffusion: float = 0.2451,  # 扩散系数
                 decay: float = 0.0069,  # 信息素衰减系数
                 attract_matrix = [[-0.0829, 5.3875], [5.3875, -0.0829]],
                 target_attract_strength: float = 29.6949,  # 目标吸引力
                 sensor_distance: float = 15.2773,  # 感知距离
                 particle_decay: float = 0.0037,  # 粒子携带信息素衰减
                 arch: str = 'gpu',  # 'gpu' or 'cpu'
                 create_window: bool = True,
                 window_title: str = "Ant Colony Optimization"):
        assert len(resolution) == 2
        assert map.ndim == 2
        ti.init(arch=ti.gpu if arch == 'gpu' else ti.cpu)

        # 基本参数设置
        self.resolution = resolution
        self.dimensional = len(resolution)
        self.image_width, self.image_height = resolution

        # Taichi字段
        self.map = ti.field(dtype=ti.f32, shape=(self.image_width, self.image_height))
        self.map.from_numpy(map)

        self.chemical_number = chemical_number
        self.particle_number = particle_number
        self.concentration = ti.field(dtype=ti.f32, shape=(self.image_width, self.image_height, chemical_number))  # 信息素浓度
        self.concentration_temp = ti.field(dtype=ti.f32, shape=(self.image_width, self.image_height, chemical_number))  # 信息素浓度
        self.particle_location = ti.Vector.field(self.dimensional, dtype=ti.f32, shape=(particle_number))  # 粒子位置
        self.particle_velocity = ti.Vector.field(self.dimensional, dtype=ti.f32, shape=(particle_number))  # 粒子速度
        self.particle_state = ti.field(dtype=ti.i32, shape=(particle_number))  # 粒子状态：0-未携带，1-携带食物
        self.particle_concentration = ti.field(dtype=ti.f32, shape=(particle_number))  # 信息素浓度
        self.image = ti.field(dtype=ti.f32, shape=(self.image_width, self.image_height, 3))  # 可视化

        self.dt = dt
        homeLocation = targets[0].location  # 巢穴位置
        homeRadius = targets[0].radius
        self.home_location = ti.Vector(homeLocation)
        self.home_radius = homeRadius
        self.random_force_strength = random_force_strength * dt ** 0.5
        if type(chemical_release_speed) == float:
            chemical_release_speed = [chemical_release_speed] * chemical_number
        chemical_release_speed = np.array(chemical_release_speed, dtype=np.float32)
        self.chemical_release_speed_field = ti.field(dtype=ti.f32, shape=chemical_number)
        self.chemical_release_speed_field.from_numpy(chemical_release_speed * dt)
        self.diffusion = diffusion * dt
        self.decay_strength = 1 - decay * dt
        self.attract_matrix = np.array(attract_matrix, dtype=np.float32)
        self.attract_matrix_field = ti.field(dtype=ti.f32, shape=self.attract_matrix.shape)
        self.attract_matrix_field.from_numpy(self.attract_matrix * dt)
        self.target_attract_strength = target_attract_strength * dt
        self.sensor_distance = sensor_distance
        self.particle_decay = 1 - particle_decay * dt

        self.targets = targets
        for target in targets:
            target.init_taichi_objects()
        self.in_food  = targets[1].get_in_target_function()
        self.in_home = targets[0].get_in_target_function()
        self.food_arrived = targets[1].get_target_arrived_function()

        if create_window:
            self.gui = ti.GUI(window_title, res=(self.image_width, self.image_height))

        # 初始化粒子
        targets[particle_source_id].get_scatter_function()(self.particle_location)
        self.initialize_particles(self.particle_velocity, self.particle_concentration, self.particle_state)            
    
    @ti.kernel
    def initialize_particles(self, particle_velocity: ti.template(), particle_concentration: ti.template(), particle_state: ti.template()):  # type: ignore
        for i in particle_velocity:
            theta = ti.random() * 2 * ti.math.pi
            particle_velocity[i] = ti.Vector([ti.cos(theta), ti.sin(theta)])
            particle_concentration[i] = 1.0
            particle_state[i] = 0  # 初始化为未携带食物

    @ti.kernel
    def update_location(self, dt: float, map: ti.template(), particle_location: ti.template(), particle_velocity: ti.template()):  # type: ignore
        image_width, image_height = map.shape
        for i in particle_location:
            # 粒子移动
            p = particle_location[i] + particle_velocity[i] * dt

            p_i = ti.cast(ti.round(p), ti.i32)
            if p_i[0] >= 0 and p_i[0] < image_width and p_i[1] >= 0 and p_i[1] < image_height:
                if map[p_i[0], p_i[1]] > 0.5:  # 发生碰撞
                    particle_velocity[i] *= (ti.random() - 1.) * 2.
                    p = particle_location[i] + particle_velocity[i] * dt

            # 边界碰撞
            if p[0] < 0:
                p[0] = -p[0]
                particle_velocity[i][0] = -particle_velocity[i][0]
                particle_velocity[i][1] = ti.random() * 2. - 1.
            if p[0] >= image_width:
                p[0] = image_width + image_width - p[0]
                particle_velocity[i][0] = -particle_velocity[i][0]
                particle_velocity[i][1] = ti.random() * 2. - 1.
            if p[1] < 0:
                p[1] = -p[1]
                particle_velocity[i][0] = ti.random() * 2. - 1.
                particle_velocity[i][1] = -particle_velocity[i][1]
            if p[1] >= image_height:
                p[1] = image_height + image_height - p[1]
                particle_velocity[i][0] = ti.random() * 2. - 1.
                particle_velocity[i][1] = -particle_velocity[i][1]
            
            # 更新位置
            particle_location[i] = p

    @ti.kernel
    def diffuse(self, diffusion: float, concentration: ti.template(), concentration_temp: ti.template()):  # type: ignore
        image_width, image_height, chemical_number = concentration.shape
        for i1, i2, i3 in ti.ndrange(image_width, image_height, chemical_number):
            i4 = 0
            f1 = 0.0
            if i1 > 0:
                f1 += concentration[i1 - 1, i2, i3]
                i4 += 1
            if i1 < image_width - 1:
                f1 += concentration[i1 + 1, i2, i3]
                i4 += 1
            if i2 > 0:
                f1 += concentration[i1, i2 - 1, i3]
                i4 += 1
            if i2 < image_height - 1:
                f1 += concentration[i1, i2 + 1, i3]
                i4 += 1
            f1 /= i4
            concentration_temp[i1, i2, i3] = diffusion * f1 + (1.0 - diffusion) * concentration[i1, i2, i3]

        for i1, i2, i3 in ti.ndrange(image_width, image_height, chemical_number):
            concentration[i1, i2, i3] = concentration_temp[i1, i2, i3]
    
    @ti.kernel
    def decay(self, decay: float, concentration: ti.template()):  # type: ignore
        image_width, image_height, chemical_number = concentration.shape
        for i1, i2, i3 in ti.ndrange(image_width, image_height, chemical_number):
            concentration[i1, i2, i3] *= decay

    @staticmethod
    @ti.func
    def grad(concentration, image_width, image_height, pheromoneId, i, j):
        i_last = ti.max(0, i - 1)
        i_next = ti.min(image_width - 1, i + 1)
        j_last = ti.max(0, j - 1)
        j_next = ti.min(image_height - 1, j + 1)
        gX = (concentration[i_next, j, pheromoneId] - concentration[i_last, j, pheromoneId]) / (i_next - i_last)
        gY = (concentration[i, j_next, pheromoneId] - concentration[i, j_last, pheromoneId]) / (j_next - j_last)
        return ti.Vector([gX, gY])

    @ti.kernel
    def apply_gradient_force(self, sensor_distance: float, target_attract_strength: float, attract_matrix_field: ti.template(), concentration: ti.template(), particle_location: ti.template(), particle_velocity: ti.template(), particle_state: ti.template()):  # type: ignore
        image_width, image_height, _ = concentration.shape
        chemical_number = attract_matrix_field.shape[0]
        for i1 in particle_location:
            x = particle_location[i1][0] + particle_velocity[i1][0] * sensor_distance
            i2 = int(ti.round(x))
            if x < 0 or x >= image_width:
                continue
            y = particle_location[i1][1] + particle_velocity[i1][1] * sensor_distance
            i3 = int(ti.round(y))
            if y < 0 or y >= image_height:
                continue
            
            if particle_state[i1] == 0:  # 未携带食物
                if self.in_food(x, y):  # 前方是食物
                    particle_velocity[i1] += target_attract_strength * particle_velocity[i1]
                    continue
            else:  # 携带食物
                if self.in_home(x, y):  # 前方是家
                    particle_velocity[i1] += target_attract_strength * particle_velocity[i1]
                    continue
            
            for i4 in range(chemical_number):
                g = self.grad(concentration, image_width, image_height, i4, i2, i3)
                particle_velocity[i1] += attract_matrix_field[particle_state[i1], i4] * g

    @ti.kernel
    def apply_random_force(self, random_force_strength: float, particle_velocity: ti.template()):  # type: ignore
        for i1 in particle_velocity:
            particle_velocity[i1] += (ti.Vector([ti.random(), ti.random()]) * 2.0 - 1.0) * random_force_strength

    @ti.kernel
    def normalize_velocity(self, particle_velocity: ti.template()):  # type: ignore
        for i1 in particle_velocity:
            particle_velocity[i1] *= 1.0 / ti.sqrt(particle_velocity[i1][0] ** 2 + particle_velocity[i1][1] ** 2)

    @ti.kernel
    def releaser_pheromone(self, particle_decay: float, chemical_release_speed_field: ti.template(), concentration: ti.template(), particle_location: ti.template(), particle_state: ti.template(), particle_concentration: ti.template()):  # type: ignore
        image_width, image_height, _ = concentration.shape
        for i in particle_location:
            # 释放信息素
            x, y = int(particle_location[i][0]), int(particle_location[i][1])
            if 0 <= x < image_width and 0 <= y < image_height:
                concentration[x, y, particle_state[i]] = ti.min(1., concentration[x, y, particle_state[i]] + chemical_release_speed_field[particle_state[i]] * particle_concentration[i])
                particle_concentration[i] *= particle_decay

    @ti.kernel
    def state_transition(self, particle_location: ti.template(), particle_velocity: ti.template(), particle_state: ti.template(), particle_concentration: ti.template()):  # type: ignore
        for i in particle_state:
            # 状态转移（检查是否找到食物或返回家）
            if self.in_food(particle_location[i].x, particle_location[i].y):  # 找到食物
                particle_concentration[i] = 1.
                if particle_state[i] == 0:
                    particle_state[i] = 1  # 携带食物
                    self.food_arrived(particle_location[i].x, particle_location[i].y)
                    particle_velocity[i] = -particle_velocity[i]  # 反向移动
            elif self.in_home(particle_location[i].x, particle_location[i].y):  # 返回家
                particle_concentration[i] = 1.
                if particle_state[i] == 1:
                    particle_state[i] = 0  # 卸下食物
                    particle_velocity[i] = -particle_velocity[i]  # 反向移动

    def evolve_one_step(self):
        self.update_location(self.dt, self.map, self.particle_location, self.particle_velocity)
        self.diffuse(self.diffusion, self.concentration, self.concentration_temp)
        self.decay(self.decay_strength, self.concentration)
        self.apply_gradient_force(self.sensor_distance, self.target_attract_strength, self.attract_matrix_field, self.concentration, self.particle_location, self.particle_velocity, self.particle_state)
        self.apply_random_force(self.random_force_strength, self.particle_velocity)
        self.normalize_velocity(self.particle_velocity)
        self.releaser_pheromone(self.particle_decay, self.chemical_release_speed_field, self.concentration, self.particle_location, self.particle_state, self.particle_concentration)
        self.state_transition(self.particle_location, self.particle_velocity, self.particle_state, self.particle_concentration)
    
    def get_image(self):
        return self.image.to_numpy()

    @ti.kernel
    def update_image(self):
        for i, j in ti.ndrange(self.resolution[0], self.resolution[1]):
            r = ti.max(self.in_home(i, j), self.concentration[i, j, 0])
            r = (0.1 + r) * (1. - self.map[i, j])
            self.image[i, j, 0] = r
            gb = ti.max(self.targets[1].image_field[i, j], self.concentration[i, j, 1])
            gb = (0.1 + gb) * (1. - self.map[i, j])
            self.image[i, j, 1] = gb
            self.image[i, j, 2] = gb
    
    def visualize(self):
        self.update_image()

        self.gui.set_image(self.image)
        self.gui.show()
