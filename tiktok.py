import os
from time import sleep
os.environ["IMAGEIO_FFMPEG_EXE"] = "./ffmpeg"
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import cv2
import sys
import requests

# On vérifie qu'il y a bien les arguments
if len(sys.argv) < 4:
    print("Usage : python tiktok.py --video/--clip <clipName/videoName> <templateName> <top|bottom>")
    exit()

# On note le nom du fichier
fileName = sys.argv[2]
# On note le nom du template
templateName = sys.argv[3]
# Position de la caméra
camPosition = sys.argv[4]

# Si on as un clip à récupérer
if sys.argv[1] == "--clip":
    # On vérifie que le fichier existe
    if os.path.exists("clip.mp4"):
        os.remove("clip.mp4")

    # setup la commande et l'arg 1
    cmd = ("twitch-dl download -q source -o clip.mp4 "+fileName)
    os.system(cmd)
    fileName = "clip.mp4"
else:
    # On vérifie que le fichier existe
    if not os.path.exists(fileName):
        print("File %s doesn't exist" % (fileName))
        exit()

# On récupère la source
source = VideoFileClip(fileName)
print("Targeted file : %s" % (fileName))

# On ouvre la vidéo
source = VideoFileClip(fileName)
# On récupère la première frame
source.save_frame("first-frame.jpeg", t='00:00:01')
x1, y1, x2, y2 = 0, 0, 0, 0
drawing = False


def setRectCamera(event, x, y, flags, param):
    global x1, y1, x2, y2, drawing  # On défini les variables globales
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x1, y1 = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            x2, y2 = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x2, y2 = x, y
    if drawing and x1 and x2:
        drawRect()
# Fonction qui dessine un rectangle de prévisualisation


def drawRect():
    global x1, y1, x2, y2, imgCopy, img
    imgCopy = img.copy()
    cv2.rectangle(imgCopy, (x1-2, y1-2), (x2+2, y2+2), (0, 255, 0), 2)
    cv2.imshow('image', imgCopy)


# On ouvre une fenêtre avec la première frame
# pour pouvoir sélectionné l'emplacment de la caméra
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('image', 960, 540)
cv2.setWindowProperty('image', cv2.WND_PROP_TOPMOST, 1)
img = cv2.imread("first-frame.jpeg", -1)
imgCopy = img.copy()

cv2.setMouseCallback('image', setRectCamera)
cv2.imshow('image', img)
cv2.waitKey(0)
# On ferme la fenêtre et on supprime la première frame
os.remove("first-frame.jpeg")
# On attend que la fenêtre soit fermée pour continuer
cv2.destroyAllWindows()
cv2.waitKey(1)


# On vérifie que les coordonnées sont bien définies
if x1 and x2 and y1 and y2:
    # On récupère la caméra et on la place au bon endroit
    sizing = 960/(x2-x1)
    cam = source.crop(x1=x1, x2=x2, y1=y1, y2=y2)
    cam = cam.resize(sizing)
    if camPosition == "top":
        cam = cam.set_position((60, 60))
    else:
        cam = cam.set_position((60, 1330))

    # On défini le template
    template = ImageClip(templateName, transparent=True).set_duration(source.duration)

    # On redimensionne la source
    # Pour qu'elle rentre dans le cadre 1072*608
    sourceHeight = source.size[0]
    source = source.resize(1100/sourceHeight)

    source = source.set_position((-10, 660))

    print("Duration : %s" % (source.duration))

    # On exporte la vidéo
    clip = CompositeVideoClip([template, source, template, cam])

    clip.write_videofile("Tiktok-"+fileName, temp_audiofile='tmp.m4a',
                         remove_temp=True, codec="libx264", audio_codec="aac", fps=25)
