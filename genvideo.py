import moviepy.editor as mvp
import sys

def gen(audiofile, outfilename='out.mp4', images=''):
    #namef = audiofile.split('.')[0]

    clip_image = mvp.ImageClip(images)
    clip_titulo = mvp.TextClip("Diário de Notícias com Ani Fátima Liu", fontsize=32, color='white')

    clip_audio = mvp.AudioFileClip(f"audiofile")
    #clip = mvp.VideoClip( clip_titulo.set_pos('center').set_duration(clip_audio.duration).make_frame, duration=clip_audio.duration)
    #v = clip.set_audio(clip_audio)


    clip = mvp.VideoClip( clip_image.make_frame, duration=clip_audio.duration )
    v = clip.set_audio( clip_audio )
    v.set_duration( clip_audio.duration )

    #clip_titulo = mvp.TextClip("Noticias do Dia \n\n www.dimensaoalfa.com.br", fontsize=28, color='white')
    #text = clip_titulo.set_pos('center').set_duration(clip_audio.duration)

    #v = clip.set_audio(clip_audio)

    #v.set_duration(clip_audio.duration)
    video = mvp.CompositeVideoClip( [ v  ], size=(1200, 800) )

 
    video.write_videofile(outfilename, fps=12)

  

if __name__ == "__main__":
    arg = sys.argv

    if len(arg) < 2:
        print('\n\nFormat\n')
        print('\tprog <audio name> <out file name mp4> <image bakground for vídeo>\n')
        exit(0)

    gen(arg[1], arg[2], arg[3] ) 
    #print(arg)
    
