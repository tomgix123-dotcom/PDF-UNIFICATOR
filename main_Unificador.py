import tkinter as tk
from pypdf import PdfWriter
from tkinter import filedialog
import os
import sys
import ctypes
import ctypes.wintypes
import threading

colores={"barra_tareas":"#5E0006","listbox":"#DCDCDC",
         "selectbackground":"#102E50","selectforeground":"#F5C45E",
         "C1":"#DCDCDC","C2Top":"#C9CDCF","C2Bot":"#2D0000",
         "C3Top":"#5E0006","C3Bot":"#150000"}

#======================[ MOVIMIENTO DE LA PANTALLA ]===============#
def empezar_movimiento(event):

    hwnd = ctypes.windll.user32.GetParent(ventana.winfo_id())

    # Posición actual del ratón en la pantalla
    ventana.x_raton = event.x_root
    ventana.y_raton = event.y_root

    # Posición REAL de la ventana en Windows
    rect = ctypes.wintypes.RECT()

    ctypes.windll.user32.GetWindowRect(
        hwnd,
        ctypes.byref(rect)
    )

    ventana.pos_x = rect.left
    ventana.pos_y = rect.top

def mover_ventana(event):

    hwnd = ctypes.windll.user32.GetParent(ventana.winfo_id())

    # Cuánto se ha movido el ratón
    diferencia_x = event.x_root - ventana.x_raton
    diferencia_y = event.y_root - ventana.y_raton

    # Nueva posición de la ventana
    x = ventana.pos_x + diferencia_x
    y = ventana.pos_y + diferencia_y

    SWP_NOSIZE = 0x0001
    SWP_NOZORDER = 0x0004
    SWP_NOACTIVATE = 0x0010

    ctypes.windll.user32.SetWindowPos(
        hwnd,
        0,
        x,
        y,
        0,
        0,
        SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE
    )

#=====================================================================#
#/////////////////////////////////////////////////////////////////////#

#======[ AÑADE LA FUENTE, OFICALMENTE EL CTYPES LO HACE ]=============#

def obtener_ruta(ruta):

    # Cuando ejecutamos el .py
    # usa la carpeta del proyecto.

    # Cuando ejecutamos el .exe de PyInstaller
    # usa la carpeta temporal de PyInstaller.

    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))

    return os.path.join(base_path, ruta)

fuente = obtener_ruta("Rexlia.otf")

ctypes.windll.gdi32.AddFontResourceW(fuente)

#==================[ EDITOR Y UNIFICADOR ]===============#

def iniciar_unir_pdfs():
    hilo = threading.Thread(target=unir_pdfs)
    hilo.start()

def unir_pdfs():

    ruta = filedialog.asksaveasfilename(title="GUARDAR PDF UNIFICADO",
                                    defaultextension=".pdf")

    if not ruta:
        return
    
    editor=PdfWriter()

    for pdf in selected_pdfs:
        editor.append(pdf)

    with open(ruta,"wb") as archivo:    

        editor.write(ruta)

    editor.close()
    

#===================[ INFO ]=============================#

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Tomgix.Unificador")

selected_pdfs=[]

#=========================================================#
#/////////////////////////////////////////////////////////#

#======================[ FUNCIONES PDF ]======================#

def añadir_mas_pdfs():
    pdfs= filedialog.askopenfilenames(title= "Selecciona los PDFs",
                                                   filetypes=[("Archivos PDF", "*.pdf")])

    if not pdfs:
        return
        
    selected_pdfs.extend(pdfs)
    
    for numero, pdf in enumerate(pdfs, start= len(selected_pdfs)):
        lista_pdfs.insert(tk.END,f"{numero} - {os.path.basename(pdf)}")

def seleccionar_pdfs():

    pdfs= filedialog.askopenfilenames(title= "Selecciona los PDFs",
                                    filetypes=[("Archivos PDF", "*.pdf")])

    if not pdfs:
        return
    
    selected_pdfs.clear()
    lista_pdfs.delete(0, tk.END)

    selected_pdfs.extend(pdfs)

    for numero, pdf in enumerate(pdfs, start=1):
        lista_pdfs.insert(tk.END,f"{numero} - {os.path.basename(pdf)}")

def seleccionar_carpeta():
    carpeta= filedialog.askdirectory(title= "Selecciona la carpeta de PDFs")

    if not carpeta:
        return

    selected_pdfs.clear()
    lista_pdfs.delete(0, tk.END)
        
    for pdf in os.listdir(carpeta):
        if pdf.lower().endswith(".pdf"):
            ruta = os.path.join(carpeta,pdf)
            selected_pdfs.append(ruta)

    for numero, pdf in enumerate(selected_pdfs,start=1):
        lista_pdfs.insert(tk.END,f"{numero} - {os.path.basename(pdf)}")       

def eliminar_pdf():

    indice = lista_pdfs.curselection()

    if not indice:
        return
    
    indice = indice[0]

    selected_pdfs.pop(indice)

    lista_pdfs.delete(0, tk.END)

    for numero, pdf in enumerate(selected_pdfs, start=1):
        lista_pdfs.insert(tk.END,f"{numero} - {os.path.basename(pdf)}")
    
def mover_arriba():

    #Esto selecciona el pdf al que le has hecho click.
    indice = lista_pdfs.curselection()

    if not indice:
        return

    indice = indice[0]

    if indice == 0:
        return

    selected_pdfs[indice], selected_pdfs[indice - 1] = selected_pdfs[indice - 1], selected_pdfs[indice]

    #Esto solo edita la Listbox para que se vea en vivo el orden final.
    lista_pdfs.delete(0, tk.END)

    for numero, pdf in enumerate(selected_pdfs, start=1):
            lista_pdfs.insert(tk.END,f"{numero} - {os.path.basename(pdf)}")

    lista_pdfs.selection_set(indice - 1)

def mover_abajo():

    #Esto selecciona el pdf al que le has hecho click.
    indice = lista_pdfs.curselection()

    if not indice:
        return

    indice = indice[0]

    if indice == len(selected_pdfs) - 1:
        return

    selected_pdfs[indice], selected_pdfs[indice + 1] = selected_pdfs[indice + 1], selected_pdfs[indice]


    #Esto solo edita la Listbox para que se vea en vivo el orden final.
    lista_pdfs.delete(0, tk.END)
    
    for numero, pdf in enumerate(selected_pdfs, start=1):
        lista_pdfs.insert(tk.END,f"{numero} - {os.path.basename(pdf)}")

    #Seleciona de nuevo lo que acabo de destruir.
    lista_pdfs.selection_set(indice + 1)

#==============================================================#
#//////////////////////////////////////////////////////////////#

#=======================[ UI ]============================#
def quitar_bordes(ventana):

    # Obtener el HWND de Tkinter
    hwnd = ventana.winfo_id()

    # Obtener la ventana raíz REAL de Windows
    GA_ROOT = 2

    hwnd = ctypes.windll.user32.GetAncestor(
        hwnd,
        GA_ROOT
    )

    # Estilo de la ventana
    GWL_STYLE = -16

    WS_CAPTION = 0x00C00000
    WS_THICKFRAME = 0x00040000
    WS_MINIMIZEBOX = 0x00020000
    WS_MAXIMIZEBOX = 0x00010000
    WS_SYSMENU = 0x00080000

    estilo = ctypes.windll.user32.GetWindowLongW(
        hwnd,
        GWL_STYLE
    )

    # Quitar barra de título
    estilo &= ~WS_CAPTION

    # Quitar bordes de redimensionamiento
    estilo &= ~WS_THICKFRAME

    # Quitar botón minimizar de Windows
    estilo &= ~WS_MINIMIZEBOX

    # Quitar botón maximizar
    estilo &= ~WS_MAXIMIZEBOX

    # Quitar menú del sistema
    estilo &= ~WS_SYSMENU

    ctypes.windll.user32.SetWindowLongW(
        hwnd,
        GWL_STYLE,
        estilo
    )

    # Avisar a Windows de que el marco ha cambiado
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    SWP_NOZORDER = 0x0004
    SWP_FRAMECHANGED = 0x0020

    ctypes.windll.user32.SetWindowPos(
        hwnd,
        0,
        0,
        0,
        0,
        0,
        SWP_NOSIZE |
        SWP_NOMOVE |
        SWP_NOZORDER |
        SWP_FRAMECHANGED
    )

def crear_ventana():
    ventana= tk.Tk()

    ventana.iconbitmap(obtener_ruta("Unificador.ico"))
    
    ventana.geometry("850x450+350+150")
    ventana.resizable(False, False)

    

    ventana.update_idletasks()
    quitar_bordes(ventana)

    return ventana

def crear_P_inicio(ventana):

    P_inicio= tk.Frame(ventana, bg="#2D0000")
    P_inicio.pack(fill="both", expand=True)

    P_inicio.grid_rowconfigure(0,weight=0) #Barra de tareas aqui.
    P_inicio.grid_rowconfigure(1,weight=1) #C1 aqui
    
    P_inicio.grid_columnconfigure(0,weight=1)
    

    #=====[ BARRA DE TAREAS ]================#

    barra_tareas = tk.Frame(P_inicio,bg="#5E0006")
    barra_tareas.grid(row=0,column=0,sticky="we",columnspan=3)

    barra_tareas.bind("<Button-1>", empezar_movimiento)
    barra_tareas.bind("<B1-Motion>", mover_ventana)

    #========================================#
    
    #=====[ CONTENEDOR 1º ]===============#
    C1=tk.Frame(P_inicio,bg="#DCDCDC")
    C1.grid(row=1,column=0,sticky="news")

    C1.grid_rowconfigure(0,weight=5)
    C1.grid_rowconfigure(1,weight=1)

    C1.grid_columnconfigure(0,weight=1)

    #=====================================#

    #====[ CONTENDORES 2º ]===============#
    C2Top = tk.Frame(C1,bg="#C9CDCF")
    C2Top.grid(row=0,column=0,sticky="news")

    C2Top.grid_rowconfigure(0,weight=1)
    C2Top.grid_rowconfigure(1,weight=0) #Cartel aqui.
    C2Top.grid_rowconfigure(2,weight=0) #Listbox aqui.
    C2Top.grid_rowconfigure(3,weight=0) #Boton unir aqui.
    C2Top.grid_rowconfigure(4,weight=1)
    
    C2Top.grid_columnconfigure(0,weight=1)
    C2Top.grid_columnconfigure(1,weight=0) #Listbox y Cartel aqui.
    C2Top.grid_columnconfigure(2,weight=0) #Botones arriba/abajo aqui.
    C2Top.grid_columnconfigure(3,weight=1)


    C2Bot = tk.Frame(C1,bg="#2D0000")
    C2Bot.grid(row=1,column=0,sticky="news")

    C2Bot.grid_rowconfigure(0,weight=1)
    C2Bot.grid_rowconfigure(1,weight=1)

    C2Bot.grid_columnconfigure(0,weight=1)



    #=======================================#

    #=====[ CONTENDORES 3º ]================#

    C3Top = tk.Frame(C2Bot,bg="#5E0006")
    C3Top.grid(row=0,column=0,sticky="news")

    C3Top.grid_rowconfigure(0,weight=1)
    C3Top.grid_rowconfigure(1,weight=0) #Ambos Botones aqui.
    C3Top.grid_rowconfigure(2,weight=1)

    C3Top.grid_columnconfigure(0,weight=1)
    C3Top.grid_columnconfigure(1,weight=0) #Boton Añadir más PDfs aqui.
    C3Top.grid_columnconfigure(2,weight=0) #Boton Seleccionar PDFs aqui.
    C3Top.grid_columnconfigure(3,weight=0) #Boton Seleccionar Carpeta de PDfs aqui.
    C3Top.grid_columnconfigure(4,weight=0) #Boton de Eliminar PDF aqui.
    C3Top.grid_columnconfigure(5,weight=1)

    C3Bot = tk.Frame(C2Bot,bg="#150000")
    C3Bot.grid(row=1,column=0,sticky="news")

    C3Bot.grid_rowconfigure(0,weight=1)
    C3Bot.grid_rowconfigure(1,weight=0)
    C3Bot.grid_rowconfigure(2,weight=1)

    C3Bot.grid_columnconfigure(0,weight=1)
    C3Bot.grid_columnconfigure(1,weight=0) 
    C3Bot.grid_columnconfigure(2,weight=1)
    
    #=======================================#

    return {"P_inicio":P_inicio, "barra_tareas":barra_tareas,"C1":C1,
            "C2Top":C2Top,"C2Bot":C2Bot,"C3Top":C3Top,"C3Bot":C3Bot}

def crear_botones():

    def cerrar_programa():
        ctypes.windll.gdi32.RemoveFontResourceW(fuente)
        ventana.destroy()
        sys.exit()

    X=tk.Button(P_inicio["barra_tareas"],bg="#5E0006",fg="#FAB12F",text="[ x ]",font=("Rexlia",11),
            relief="flat",command=cerrar_programa)
    X.pack(side="right")

    X.bind("<Enter>", lambda e: X.configure(bg="#82030C"))
    X.bind("<Leave>", lambda e: X.configure(bg="#5E0006"))

    _= tk.Button(P_inicio["barra_tareas"],bg="#5E0006",fg="#FAB12F",text="[ _ ]",font=("Rexlia",11),
            relief="flat",command=ventana.iconify)
    _.pack(side="right")

    _.bind("<Enter>", lambda e: _.configure(bg="#452023"))
    _.bind("<Leave>", lambda e: _.configure(bg="#5E0006"))

    #===========[ BOTONES DE SELECCIÓN ]================================================================#

    boton_añadir=tk.Button(P_inicio["C3Top"],bg="#C9CDCF",text="Añadir más PDFs",font=("Rexlia",11)
                               ,command=añadir_mas_pdfs)
    boton_añadir.grid(row=1,column=1,padx=5,pady=10)

    boton_añadir.bind("<Enter>", lambda e: boton_añadir.configure(bg="#E6ECEF"))
    boton_añadir.bind("<Leave>", lambda e: boton_añadir.configure(bg="#C9CDCF"))
    #///////////////
    boton_select=tk.Button(P_inicio["C3Top"],bg="#C9CDCF",text="Seleccionar PDFs",font=("Rexlia",11)
                           ,command=seleccionar_pdfs)
    boton_select.grid(row=1,column=2,padx=5,pady=10)
    
    boton_select.bind("<Enter>", lambda e: boton_select.configure(bg="#E6ECEF"))
    boton_select.bind("<Leave>", lambda e: boton_select.configure(bg="#C9CDCF"))
    #//////////////
    boton_select_carpeta=tk.Button(P_inicio["C3Top"],bg="#C9CDCF",text="Seleccionar Carpeta",font=("Rexlia",11),
                                   command=seleccionar_carpeta)
    boton_select_carpeta.grid(row=1,column=3,padx=5,pady=10)

    boton_select_carpeta.bind("<Enter>", lambda e: boton_select_carpeta.configure(bg="#E6ECEF"))
    boton_select_carpeta.bind("<Leave>", lambda e:  boton_select_carpeta.configure(bg="#C9CDCF"))
    #////////////////
    boton_eliminar_pdf=tk.Button(P_inicio["C3Top"],bg="#C9CDCF",text="Eliminar PDF",font=("Rexlia",11),
                                       command=eliminar_pdf)
    boton_eliminar_pdf.grid(row=1,column=4,padx=5,pady=10)

    boton_eliminar_pdf.bind("<Enter>", lambda e: boton_eliminar_pdf.configure(bg="#E6ECEF"))
    boton_eliminar_pdf.bind("<Leave>", lambda e: boton_eliminar_pdf.configure(bg="#C9CDCF"))

    #===================================================================================================#

    #========[ BOTON DE UNIR ]==================================================#
    boton_unir=tk.Button(P_inicio["C2Top"],bg="#5E0006",fg="#F5C45E"
                         ,text="> [ UNIFICAR ] <",font=("Rexlia",11),
                         command=iniciar_unir_pdfs)
    boton_unir.grid(row=3,column=1,pady=10)

    boton_unir.bind("<Enter>", lambda e: boton_unir.configure(bg="#7C020A"))
    boton_unir.bind("<Leave>", lambda e: boton_unir.configure(bg="#5E0006"))

    #===========================================================================#

    #============[ BOTONES DE CAMBIO DE POSICION ]==============================#

    color_fondo=tk.Frame(P_inicio["C2Top"],bg="#C2C1C1")
    color_fondo.grid(row=2,column=2,sticky="news")

    boton_arriba=tk.Button(P_inicio["C2Top"],text=" ⬆ ",command= mover_arriba)
    boton_arriba.grid(row=2,column=2,sticky="n")

    boton_abajo=tk.Button(P_inicio["C2Top"],text=" ⬇ ",command= mover_abajo)
    boton_abajo.grid(row=2,column=2,sticky="s")

    #===========================================================================#

    return {
    "X": X,
    "seleccionar": boton_select,
    "seleccionar_carpeta": boton_select_carpeta,
    "unir": boton_unir,
    "arriba": boton_arriba,
    "abajo": boton_abajo
}

#==========[ ELEMENTOS DEL PROGRAMA ]======================#
ventana = crear_ventana()

P_inicio = crear_P_inicio(ventana)

botones = crear_botones()

version="1.0.0"
#==========================================================#

Titulo = tk.Label(P_inicio["barra_tareas"],text=f"-[ UNIFICADOR ]- Version - {version}",font=("Rexlia",10),
                  bg="#5E0006",fg="#FAB12F")
Titulo.pack(side="left")

Titulo.bind("<Button-1>", empezar_movimiento)
Titulo.bind("<B1-Motion>", mover_ventana)

Cartel = tk.Label(P_inicio["C2Top"],bg="#C9CDCF",text="-Lista de PDFs Seleccionados-",
                  font=("Rexlia",12,"underline"))
Cartel.grid(row=1,column=1)

lista_pdfs = tk.Listbox(P_inicio["C2Top"],bg="#DCDCDC",width=65,height=15,font=("Rexlia",11),
                        relief="flat",
                        highlightbackground="#888888",activestyle="none",selectborderwidth=1,
                        selectbackground="#102E50",selectforeground="#F5C45E")
lista_pdfs.grid(row=2,column=1)





ventana.mainloop()


#====================================================================================#



