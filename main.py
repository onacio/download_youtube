import customtkinter as ctk
from tkinter import messagebox
import youtube

def obter(url):   
    try: 
        restorno = youtube.obter_res(url)
        # Ativa os componentes
        combobox.configure(state='normal') 
        radiobutton_video.configure(state='normal')   
        radiobutton_audio.configure(state='normal')   
        btn.configure(state='normal')
        # Passa a lista de resolução para o componentes combobox
        combobox.configure(values=restorno)
        combobox.set(restorno[0])
    except:
        messagebox.showerror('Erro', 'Erro ao obter dados do vídeo, verifique se a url está correta!')

def estado_resolucao(valor):    
    if valor == 'Áudio':
        combobox.configure(state='disabled')
    elif valor == 'Vídeo':
        combobox.configure(state='normal')
    

janela = ctk.CTk()
janela.title('Download do youtube')
janela._set_appearance_mode('system')
janela.geometry('540x350')
janela.resizable(width=False, height=False)

texto_url = ctk.CTkLabel(janela, text='Link do vídeo:').place(y=7, x=32)
url = ctk.CTkEntry(janela, width=400)
url.place(y=30, x=30)

obter_dados = ctk.CTkButton(janela, text='Obter dados', width=40, command=lambda: obter(url.get()))
obter_dados.place(y=30, x=440)

radiobutton_var = ctk.IntVar(value=1)
texto_checkbox = ctk.CTkLabel(janela, text='Selecione uma opção:').place(y=65, x=30)
radiobutton_video = ctk.CTkRadioButton(janela, text='Vídeo', variable=radiobutton_var, value=1, command=lambda:estado_resolucao(radiobutton_video._text))
radiobutton_video.place(y=90,x=30)
radiobutton_video.configure(state='disabled')
radiobutton_audio = ctk.CTkRadioButton(janela, text='Áudio', variable=radiobutton_var, value=2, command=lambda:estado_resolucao(radiobutton_audio._text))
radiobutton_audio.place(y=90,x=100)
radiobutton_audio.configure(state='disabled')

texto_combobox = ctk.CTkLabel(janela, text='Resolução:').place(y=125, x=30)
combobox = ctk.CTkComboBox(janela)
combobox.place(y=150, x=30)
combobox.set('')
combobox.configure(state='disabled')

btn = ctk.CTkButton(janela, 
                    text='BAIXAR', 
                    width=150, 
                    height=80, 
                    font=("Roboto", 20), 
                    border_width=4,                          
                    command=lambda: youtube.baixar(url.get(), radiobutton_var.get(), combobox.get()))
btn.place(y=220, x=195)
btn.configure(state='disabled')

janela.mainloop()