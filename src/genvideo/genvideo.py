import moviepy.editor as mvp
import sys

def gen(audiofile, image='', outfilename='out.mp4', dim = ( 1200,800), fps = 24 ):
    #namef = audiofile.split('.')[0]

    clip_image = mvp.ImageClip(image)
    clip_titulo = mvp.TextClip("Diário de Notícias com Ani Fátima Liu", fontsize=32, color='white')

    clip_audio = mvp.AudioFileClip(audiofile)
    #clip = mvp.VideoClip( clip_titulo.set_pos('center').set_duration(clip_audio.duration).make_frame, duration=clip_audio.duration)
    #v = clip.set_audio(clip_audio)


    clip = mvp.VideoClip( clip_image.make_frame, duration=clip_audio.duration )
    v = clip.set_audio( clip_audio )
    v.set_duration( clip_audio.duration )

    video = mvp.CompositeVideoClip( [ v  ], size=dim )
 
    video.write_videofile(outfilename, codec='mpeg4', audio=True,  fps = fps)

  

if __name__ == "__main__":
    arg = sys.argv

    if len(arg) < 4:
        print('\n\nFormat\n')
        print('\tprog <audio name> <image bakground for vídeo> <out file name mp4>\n')
        exit(0)
	#elif len(arg)==5:
	#	gen(arg[1], arg
    else:
        print(arg)
        gen(arg[1], arg[2], arg[3], (720, 1280), 16  ) 
    print(arg)
    
