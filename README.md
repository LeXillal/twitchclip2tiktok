# twitchclip2tiktok

Petit utilitaire python pour créer une vidéo tiktok à partir d'un clip twitch

1. Installer `ffmpg` ou l'importer via `os.environ["IMAGEIO_FFMPEG_EXE"] = "./bin/ffmpeg"` dans le code
2. Mettttre son template dans le dossier ou savoir ou il est :chat:
3.
- Pour un clip -> `python3 tiktok.py {template.png} {postion de la cam (top|bottom)} clip`
- Pour une video -> `python3 tiktok.py {template.png} {postion de la cam (top|bottom)} video`
4. Mettre le lien du clip ou de la video
5. Selectionner la caméra
6. Appuyer sur `q` pour quitter la fenêtre
7. Le tiktok se crée sous le nom TikTok-clip.mp4
