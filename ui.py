from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame


class MainView(Frame):
    def __init__(self, screen):
        super().__init__(screen, screen.height, screen.width, title='TTr 8)')


class RaView(Frame):
    def __init__(self, screen):
        super().__init__(screen, screen.height, screen.width, title='Raaaaaaaaaa!!!!')


def ui(screen, scene):
    scenes = [
        Scene(
            effects=[RaView(screen)],
            duration=-1,
            name='Main'
        )
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


if __name__ == '__main__':
    last_scene = None
    Screen.wrapper(func=ui, catch_interrupt=False, arguments=[last_scene])
