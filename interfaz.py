import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pantalla fija con secciones")
        self.geometry("400x300")

        # Contenedor principal para los frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Diccionario para guardar los frames
        self.frames = {}

        # Inicializamos las pantallas
        for F in (Inicio, Seccion1, Seccion2):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame(Inicio)

    def mostrar_frame(self, contenedor):
        frame = self.frames[contenedor]
        frame.tkraise()  # Trae el frame al frente

class Inicio(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Pantalla de Inicio").pack(pady=10)
        tk.Button(self, text="Ir a Sección 1",
                  command=lambda: controller.mostrar_frame(Seccion1)).pack()
        tk.Button(self, text="Ir a Sección 2",
                  command=lambda: controller.mostrar_frame(Seccion2)).pack()

class Seccion1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Sección 1").pack(pady=10)
        tk.Button(self, text="Volver al inicio",
                  command=lambda: controller.mostrar_frame(Inicio)).pack()

class Seccion2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Sección 2").pack(pady=10)
        tk.Button(self, text="Volver al inicio",
                  command=lambda: controller.mostrar_frame(Inicio)).pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()