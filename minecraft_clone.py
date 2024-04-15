from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from itertools import product


app = Ursina()
WALK_SPEED = 5
RUN_SPEED = 7

grass_texture = load_texture("assets/grass.png")
punch_sound = Audio("assets/punch.wav", loop = False, autoplay = False)


class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model="assets/block",
            origin_y=0.5,
            texture=grass_texture,
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
    for x, z in product(range(16), repeat=2):
        Voxel(position=(x, 0, z))


if __name__ == "__main__":
    generate_floor()
    player = FirstPersonController()
    player.speed = WALK_SPEED
    app.run()
