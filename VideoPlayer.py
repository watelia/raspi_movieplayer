from pyclbr import Function
from vlc import Instance, Media, MediaPlayer, EventManager
import vlc
import tkinter as tk
import os
import sys


class VideoPlayer:
    __display: tk.Tk
    __instance: Instance
    __player: MediaPlayer
    __media: Media
    __events: EventManager
    __cb_function: Function
    video_path: str
    playing: bool
    pausing: bool

    def __init__(self) -> None:
        os.environ.__setitem__('DISPLAY', ':0.0')
        os.system('xset r off')
        self.__display = tk.Tk()
        self.__display.attributes("-fullscreen", True)
        self.__display.update()

        self.__instance = Instance("--no-xlib --vout mmal_vout")
        self.__player = self.__instance.media_player_new()
        self.__player.set_xwindow(self.__display.winfo_id())

        self.__events = self.__player.event_manager()
        self.__events.event_attach(
            vlc.EventType.MediaPlayerEndReached, self.__callback_end)

        self.playing = False
        self.pausing = False

    def mainloop(self) -> None:
        self.__display.mainloop()

    def update(self) -> None:
        self.__display.update()

    def destroy(self) -> None:
        self.__display.destroy()

    def set_callback_end(self, function):
        self.__cb_function = function

    def __callback_end(self, event):
        self.__cb_function()
        self.playing = False
        self.pausing = False

    def play(self, video_path) -> None:
        if not self.__file_check(video_path):
            return

        self.__media = Media(video_path)
        self.__player.set_media(self.__media)
        self.__player.play()
        print(self.__player.is_playing())
        self.playing = True
        self.pausing = False

    def pause(self) -> None:
        if not self.playing:
            return
        self.__player.pause()
        self.pausing = not self.pausing

    def stop(self) -> None:
        if not self.playing:
            return
        self.__player.stop()
        self.playing = False
        self.pausing = False

    def get_current_video_length(self) -> int:
        return self.__player.get_length()

    def get_current_video_time(self) -> int:
        return self.__player.get_time()

    def get_video_length(self, video_path) -> int:
        result = -1
        if not self.__file_check(video_path):
            return result

        tmp_instance = Instance("--no-xlib")
        tmp_player: MediaPlayer = tmp_instance.media_player_new()
        tmp_media = Media(video_path)
        tmp_player.set_media(tmp_media)
        result = tmp_player.get_length()
        return result

    def __file_check(self, video_path) -> bool:
        if not os.path.isfile(video_path):
            print("指定したビデオファイルは存在しません", file=sys.stderr)
            return False

        _, ext = os.path.splitext(video_path)
        if not ext == ".mp4":
            print("指定したファイルはmp4形式ではありません", file=sys.stderr)
            return False

        return True

    def __cb_finished(self) -> bool:
        self.playing = False
        self.pausing = False

    def bind_press_event(self, f) -> None:
        self.__display.bind("<KeyPress>", f)
