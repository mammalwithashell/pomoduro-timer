from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty


class IncrediblyCrudeClock(Label):
    a = NumericProperty(16)  # seconds

    def start(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=1, duration=self.a)

        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "FINISHED"

        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

    def on_a(self, instance, value):
        self.text = str(value)


class TimeApp(App):
    def build(self):
        crudeclock = IncrediblyCrudeClock()
        crudeclock.start()
        return crudeclock


if __name__ == "__main__":
    TimeApp().run()
