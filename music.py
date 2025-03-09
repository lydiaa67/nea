import pygame, random

playlist = [
    "assets/music1.mp3",
    "assets/music2.mp3",
    "assets/music3.mp3",
    "assets/music4.mp3",
    "assets/music5.mp3"
]

pause_count = 0

current_song = random.randint(0,(len(playlist) - 1))

def play_next_song():
    global current_song
    current_song = random.randint(0, len(playlist) - 1)
    pygame.mixer.music.load(playlist[current_song])
    pygame.mixer.music.play()

pygame.mixer.init()

pygame.mixer.music.load(playlist[current_song])

pygame.mixer.music.set_endevent(pygame.USEREVENT)  #triggers event when the song ends

def control_music():
    global pause_count
    pause_count += 1
    if (pause_count % 2) == 1:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def skip_music():
    play_next_song() 

def stop_music():
    pygame.mixer.music.stop()

