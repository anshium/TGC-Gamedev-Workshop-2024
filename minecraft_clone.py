from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from itertools import product
from height_map import HillGrid


app = Ursina()
WALK_SPEED = 5
RUN_SPEED = 7
GRID_SIZE = 32

grass_texture = load_texture("assets/grass.png")
dirt_texture = load_texture("assets/dirt.png")
punch_sound = Audio("assets/punch.wav", loop = False, autoplay = False)


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=dirt_texture):
        super().__init__(
            parent=scene,
            position=position,
            model="assets/block",
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale = 0.5
        )

def update():
    # Respawn if fell off
    if player.y < -100:
        player.y = 100

    if held_keys["control"]:
        player.speed = RUN_SPEED
    else:
        player.speed = WALK_SPEED
    
    # To check which key is being pressed
    # for key, value in held_keys.items():
    #     if value != 0:
    #         print(key, value)


def input(key):
    if key == "left mouse down":
        punch_sound.play()
        destroy(mouse.hovered_entity)
    if key == "right mouse down" and mouse.hovered_entity:
        punch_sound.play()
        hit_info = raycast(camera.world_position, camera.forward, distance=100)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal)


def generate_floor() -> None:
    heights = HillGrid(SIZE=GRID_SIZE, ITER=20)
    for x, z in product(range(GRID_SIZE), repeat=2):
        for y in range(0, heights[x][z]):
            Voxel(position=(x, y, z))
        Voxel(position=(x, heights[x][z], z), texture=grass_texture)


if __name__ == "__main__":
    generate_floor()
    player = FirstPersonController()
    player.mouse_sensitivity = Vec2(100, 100)
    player.speed = WALK_SPEED
    app.run()
