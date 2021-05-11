from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label

TIME = 25.0


class Menu(Screen):
    def to_timer(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "timer"


class Time(Label):
    pomoduro = NumericProperty(TIME)  # number of minutes

    def on_pomoduro(self, instance, value):
        minutes, seconds = str(value).split(".")
        seconds = str(round(3 * int(seconds) / 5))
        self.text = f"{minutes}:{seconds[:2]}"


class Timer(Screen):
    def on_enter(self, *args):
        self.start()
        return super().on_enter(*args)

    def on_leave(self, *args):
        timer = self.ids.time
        Animation.cancel_all(timer)
        timer.pomoduro = TIME
        return super().on_leave(*args)

    def to_menu(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "menu"

    def start(self):
        Animation.cancel_all(self)
        self.anim = Animation(pomoduro=0, duration=60 * self.ids.time.pomoduro)

        def timer_finished(animation, time_label):
            time_label.text = "FINISHED"
            self.manager.sound.play()

        self.anim.bind(on_complete=timer_finished)
        self.anim.start(self.ids.time)


class Manager(ScreenManager):
    def __init__(self, timer_sound, **kwargs):
        self.sound = timer_sound
        super(Manager, self).__init__(**kwargs)


class PomoduroTimerApp(App):
    def build(self):
        sound = SoundLoader.load("nuclear-warning.mp3")
        return Manager(sound)


def main():
    # Load in gui
    Builder.load_file("timer.kv")

    # start app
    PomoduroTimerApp().run()


if __name__ == "__main__":
    main()
