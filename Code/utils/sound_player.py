import os
import winsound


class SoundPlayer:

    SOUND_PATH = "assets/sounds"

    @staticmethod
    def play_camera_click():

        SoundPlayer.play("camera_click.wav")

    @staticmethod
    def play_success():

        SoundPlayer.play("success.wav")

    @staticmethod
    def play_error():

        SoundPlayer.play("error.wav")

    @staticmethod
    def play(filename):

        path = os.path.join(SoundPlayer.SOUND_PATH, filename)

        if not os.path.exists(path):

            return

        try:

            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

        except Exception as e:

            print("BŁĄD DŹWIĘKU:", e)
