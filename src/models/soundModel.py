import threading
import time

import pygame

from configs.assetsConf import MUSIC_PLAYLIST


class SoundController:
    def __init__(self):
        pygame.mixer.init()
        self.music_files = MUSIC_PLAYLIST


    def play_sound(self, sound_path, volume=1.0):
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(volume)
        sound.play()

    def play_music(self, music_path, volume=1.0, loops=-1):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def stop_all_sounds(self):
        pygame.mixer.stop()

    def play_sound_with_fadeout(self, sound_path, play_duration, fade_duration, volume=1.0):
        def play_and_fade():
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(volume)
            sound.play()

            time.sleep(play_duration - fade_duration / 1000)
            sound.fadeout(fade_duration)

            # Stop the sound after fadeout
            time.sleep(fade_duration / 1000)
            sound.stop()

        threading.Thread(target=play_and_fade).start()

    def play_sound_with_fadein(self, sound_path, fade_duration, final_volume=1.0):
        def fade_in():
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(0)  # Start with volume at 0
            sound.play()

            # Gradually increase the volume
            steps = int(fade_duration / 100)
            for step in range(steps):
                volume = (step / steps) * final_volume
                sound.set_volume(volume)
                time.sleep(0.1)

            # Keep playing sound after fade-in
            sound.set_volume(final_volume)

        threading.Thread(target=fade_in).start()

    def play_sound_with_fadein_fadeout(self, sound_path, fadein_duration, total_duration, fadeout_duration,
                                       final_volume=1.0):
        def fade_in_out():
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(0)
            sound.play()

            # Fade in
            steps = int(fadein_duration / 100)
            for step in range(steps):
                volume = (step / steps) * final_volume
                sound.set_volume(volume)
                time.sleep(0.1)

            # Play sound after fade in before fade out
            play_duration = total_duration - fadein_duration / 1000 - fadeout_duration / 1000
            time.sleep(play_duration)

            # Fade out
            sound.fadeout(fadeout_duration)
            time.sleep(fadeout_duration / 1000)

            # Stop the sound after fadeout
            sound.stop()

        threading.Thread(target=fade_in_out).start()

    def play_next_track(self, volume=1.0):
        if self.current_track < len(self.music_files):
            pygame.mixer.music.load(self.music_files[self.current_track])
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(1)
            self.current_track += 1
        else:
            self.current_track = 0  # Optionally, loop back to the first track

    def start_playlist(self, volume=1.0):
        self.current_track = 0
        self.play_next_track(volume)
