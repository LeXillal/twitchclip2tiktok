# twitchclip2tiktok

Petit utilitaire python pour créer une vidéo tiktok à partir d'un clip twitch

1. Installer `ffmpg` ou l'importer via `os.environ["IMAGEIO_FFMPEG_EXE"] = "./bin/ffmpeg"` dans le code
2. Mettttre son template dans le dossier ou savoir ou il est :chat:
3. Pour un clip -> `python3 tiktok.py {template.png} {postion de la cam (top|bottom)} --clip {lien du clip}`
4. Pour une video -> `python3 tiktok.py {template.png} {postion de la cam (top|bottom)} --video {fichier de la video}`
