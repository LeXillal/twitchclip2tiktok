import sys
import cv2
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "./ffmpeg"

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

# Récupération du nom de fichier
file_name = sys.argv[1]
print("Targeted file:", file_name)

# Récupération de la première frame
source = VideoFileClip(file_name)
source.save_frame("first-frame.jpeg", t='00:00:01')
img = cv2.imread("first-frame.jpeg", -1)

# Fonction pour définir les coordonnées du rectangle
def set_rect_camera(event, x, y, flags, param):
    global x1, y1, x2, y2, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x1, y1 = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            x2, y2 = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x2, y2 = x, y
    if drawing:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('image', img)

# Fenêtre pour sélectionner la caméra
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', set_rect_camera)
cv2.imshow('image', img)
cv2.waitKey(0)

# Suppression de la première frame
os.remove("first-frame.jpeg")
cv2.destroyAllWindows()

# Récupération de la caméra et redimensionnement
if x1 and x2 and y1 and y2:
    cam = source.crop(x1=x1, x2=x2, y1=y1, y2=y2)
    sizing = 960 / (x2 - x1)
    cam = cam.resize(sizing)
    cam = cam.set_position((60, 1330))

    # Définition du template
    template = ImageClip("src/templateXi.png", transparent=True).set_duration(source.duration)

    # Redimensionnement de la source
    source_height = source.size[0]
    source = source.resize(1100/source_height)
    source = source.set_position((-10, 660))

    # Export de la vidéo
    clip = CompositeVideoClip([template, source, template, cam])
    clip.write_videofile(f"Tiktok-{file_name}", temp_audiofile='temp-audio.m4a', remove_temp=True, codec='libx264', audio_codec='aac')
