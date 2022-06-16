# os.environ["IMAGEIO_FFMPEG_EXE"] = "./bin/ffmpeg"
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

import sys
fileName = sys.argv[1]
print("Targeted file : %s" % (fileName))

# On récup la source
source = VideoFileClip(fileName)

# On chope la firstFrame pour le camcroping
source.save_frame("first-frame"+fileName+".jpeg", t='00:00:01')

# Cam posision et croping
# x1, y1 = coin haut gauche
x1, y1 = 18, 583
# x2, y2 = coin bas droit
x2, y2 = 340, 770

# ON récupère la caméra et on la place au bon endroit
sizing = 900/(x2-x1)
cam = source.crop(x1=x1, x2=x2, y1=y1, y2=y2)
cam = cam.resize(sizing)
cam = cam.set_position((90, 50))

# On défini le template
template = ImageClip(
    "template.png", transparent=True).set_duration(source.duration)

# On positione la source
source = source.resize(0.57)
source = source.set_position((0, 660))

print("Duration : %s" % (source.duration))

# On exporte la vidéo
clip = CompositeVideoClip([template, source, template, cam])

clip.write_videofile("Tiktok-"+fileName, temp_audiofile='temp-audio.m4a',
                     remove_temp=True, codec="libx264", audio_codec="aac")
