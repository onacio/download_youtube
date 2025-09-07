from pytubefix import YouTube
from pytubefix.cli import on_progress
from tkinter import messagebox
import os

def baixar(url, op, res=None):    
    if op == 1: # Baixar Vídeo
        pasta = os.path.join(os.getcwd(), 'videos')
        yt = YouTube(url=url, on_progress_callback=on_progress)

        if res:
            # Tenta encontrar um stream progressivo (video+audio) com a resolução desejada
            ys = yt.streams.filter(progressive=True, res=res, file_extension='mp4').first()

            if not ys:
                # Se não encontrar um progressivo, pode ser uma resolução DASH.
                # Nesse caso, você precisará baixar vídeo e áudio separadamente e combiná-los.
                # Para simplificar agora, vamos pegar a melhor resolução progressiva disponível
                # se a específica não for encontrada progressivamente.
                print(f"Resolução {res} não disponível como stream progressivo. Baixando a melhor qualidade progressiva disponível.")
                ys = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            if ys:
                try:
                    ys.download(output_path=pasta, filename=f'{yt.title}[{res if ys.resolution else "best_progressive"}].mp4')
                    messagebox.showinfo('Sucesso', 'Download concluido com sucesso!!!')
                except:
                    messagebox.showerror('Erro', 'Não foi possível baixar o vídeo!')
            else:
                messagebox.showerror('Erro', 'Não foi possível encontrar um stream de vídeo para download.')                
        else:
            # Se nenhuma resolução específica for fornecida, baixe a melhor progressiva
            ys = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if ys:
                ys.download(output_path=pasta, filename=f'{yt.title}[{ys.resolution if ys.resolution else "best_progressive"}].mp4')
            else:
                messagebox.showerror('Erro', 'Não foi possível encontrar um stream de vídeo progressivo para download.')                                

    elif op == 2: # Baixar Áudio
        pasta = os.path.join(os.getcwd(), 'audios')
        if not os.path.exists(pasta):
            os.makedirs(pasta)

        yt = YouTube(url=url, on_progress_callback=on_progress)

        # --- Tenta baixar o áudio em 128 kbps ---
        ys = yt.streams.filter(only_audio=True, abr="128kbps").first()

        if not ys:
            print("Stream de áudio de 128kbps não encontrado. Buscando o melhor áudio disponível.")
            ys = yt.streams.filter(only_audio=True).order_by('abr').desc().first() # Pega o melhor ABR disponível            

        if ys:
            filename = f'{yt.title} [{ys.abr if ys.abr else "best_audio"}].mp3'
            ys.download(output_path=pasta, filename=filename)
            messagebox.showinfo('Sucesso', 'Áudio baixado com sucesso!!!')            
        else:
            messagebox.showerror("Erro", "Não foi possível encontrar um stream de áudio para download.")            

def obter_res(url):
    yt = YouTube(url)
    # Filtra apenas por streams progressivos (vídeo + áudio)
    video_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    resolutions = []
    for stream in video_streams:
        if stream.resolution:
            if stream.resolution not in resolutions: # Adiciona apenas resoluções únicas
                resolutions.append(stream.resolution)
    return resolutions