import moviepy.editor as mvp

# Criando clip de audio e imagem que serão adicionados ao vídeo.
clip_image = mvp.ImageClip('<sua imagem aqui>')

clip_audio = mvp.AudioFileClip("<seu audio aqui>")


# Criamos um frame com a imagem anterior e usamos a duração do audio usado.
clip = mvp.VideoClip( clip_image.make_frame, duration=clip_audio.duration )
# Adicionamos o audio aos clip criado
v = clip.set_audio( clip_audio )
# Definimos duração do vídeo com tempo do audio
v.set_duration( clip_audio.duration )

# FAzmos a composição do vídeo integrando os clips criados caso haja mais de um ou som um.
video = mvp.CompositeVideoClip( [ v  ], size=(1200, 800) )
# Salvamos o vídeo criado.
video.write_videofile("meu-video.mp4", fps=12)

