import datetime
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar

import requests
from PIL import Image, ImageTk
from pytube import YouTube

# Cores utilizadas no layout
co0 = "#444466"  # Preta
co1 = "#feffff"  # branca
co2 = "#6f9fbd"  # azul
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra
fundo = "#3b3b3b"

# Layout da janela
janela = Tk()
janela.title()
janela.geometry('600x300')
janela.configure(bg=fundo)
# Separador do título
ttk.Separator(janela, orient=HORIZONTAL).grid(row=0,columnspan=1,ipadx=250)

# divisão de frames da janela
# Frame superior
frame_cima = Frame(janela, width=600, height=110, bg=fundo, pady=5,padx=0)
frame_cima.grid(row=1, column=0)

logo = Image.open('images/icone_youtube.png')
logo = logo.resize((50,50), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)

l_logo = Label(frame_cima,image=logo, compound=LEFT, bg=fundo, font=('Ivy 10 bold'), anchor='nw')
l_logo.place(x=5, y=2)

l_name = Label(frame_cima,text='pyTube Download App', width=32, bg=fundo, fg=co1, font=('Ivy 15 bold'), anchor='nw')
l_name.place(x=65, y=15)

# Funçao de pesquisa do vídeo
def search():
    global img
    
    # pegar o link
    url = e_url.get()
    yt = YouTube(url)
    # Título
    title = yt.title
    # Views
    view = yt.views
    # Duração
    time = str(datetime.timedelta(seconds=yt.length))
    # photo
    thumb = yt.thumbnail_url
    img = Image.open(requests.get(thumb, stream=True).raw)
    img = img.resize((230,150), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    
    l_image['image'] = img
    
    l_title['text'] = "Título : " + title
    l_views['text'] = "Views : " + str('{:,}'.format(view))
    l_time['text'] = "Duração : " + time
    

# Função para barra de progresso
previousprogress = 0

def on_progress(stream, chunk, bytes_remaining):
    global previousprogress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    
    liveprogress = (int)(bytes_downloaded / total_size * 100)
    if liveprogress > previousprogress:
        previousprogress = liveprogress
        print(liveprogress)
        
        # apresenta barra de progresso
        bar.place(x=250, y=120)
        bar['value'] = liveprogress
        janela.update_idletasks()

# Função Download
def download():
    url=e_url.get()
    yt=YouTube(url)
    
    yt.register_on_progress_callback(on_progress)
    # original yt.streams.filter(only_audio=False).first().download()
    yt.streams.filter(file_extension='mp4')
    yt.streams.get_by_itag(22).download()

# Criaçao dos elementos da janela
l_url = Label(frame_cima,text='URL do vídeo', bg=fundo, fg=co1, font=('Ivy 10 bold'), anchor='nw')
l_url.place(x=10, y=80)

e_url = Entry(frame_cima, width=40, justify='left',relief=SOLID)
e_url.place(x=100, y=80)


b_search = Button(frame_cima, command=search,text='Pesquisar', width=10, bg=co2, fg=co1, font=('Ivy 15 bold'),relief=RAISED,overrelief=RIDGE)
b_search.place(x=404, y=80)

# Frame inferior
frame_baixo = Frame(janela, width=600, height=300, bg=fundo, pady=12,padx=0)
frame_baixo.grid(row=2, column=0,sticky=NW)

# Operações
l_image = Label(frame_baixo, compound=LEFT, bg=fundo, font=('Ivy 10 bold'), anchor='nw')
l_image.place(x=10, y=10)

l_title= Label(frame_baixo,text='', height=2, wraplength = 225, compound=LEFT,bg=fundo, fg=co1, font=('Ivy 10 bold'), anchor='nw')
l_title.place(x=250, y=15)

l_views = Label(frame_baixo,text='', bg=fundo, fg=co1, font=('Ivy 8 bold'), anchor='nw')
l_views.place(x=250, y=60)

l_time = Label(frame_baixo,text='', bg=fundo, fg=co1, font=('Ivy 8 bold'), anchor='nw')
l_time.place(x=250, y=85)

down = Image.open('images/icone_download.png')
down = down.resize((20,20), Image.ANTIALIAS)
down = ImageTk.PhotoImage(down)

b_down= Button(frame_baixo, command=download, image=down, compound=LEFT, bg=fundo, font=('Ivy 10 bold'), anchor='nw', overrelief=RIDGE)
b_down.place(x=450, y=85)

# Estilo da Barra de Progresso
style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", backgroud='#00E676')
style.configure("TProgressbar", thickness=6)

bar = Progressbar(frame_baixo, length=190, style="black.Horizontal.TProgressbar")

# execução
janela.mainloop()

