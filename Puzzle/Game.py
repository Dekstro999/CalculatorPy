import customtkinter as ctk
from customtkinter import CTkImage  
import tkinter as tk
from tkinter import messagebox
import random
import time
import os
from PIL import Image
import threading

class JuegoPuzzle(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Juego de Puzzle")
        self.geometry("600x700")
        self.resizable(False, False)

        self.player_name = None
        self.grid_size = 4
        self.empty_tile = (self.grid_size - 1, self.grid_size - 1)
        self.tiles = []
        self.text_vars = []
        self.text_shuffled = tk.StringVar(value="Mezclar")
        self.moves = 0
        self.start_time = time.time()
        self.paused_time = 0
        self.mezclando = False
        
        
        self.shuffle_num = 100  



        self.sprites = []
        for i in range(8):
            file_path = os.path.join(os.path.dirname(__file__), f"Frame_loading_{i}.png")
            if os.path.exists(file_path):
                # Carga la imagen con PIL
                image = Image.open(file_path)
                # Convierte la imagen a CTkImage
                ctk_image = CTkImage(image, size=(80, 80))  
                self.sprites.append(ctk_image)
            else:
                print(f"Error: No se pudo cargar {file_path}")


        self.sprite_index = 0

        self.create_menu_widgets()
    def space (self, n):
        self.space_label = ctk.CTkLabel(self, text="")
        self.space_label.pack(pady=n*10)

    def create_menu_widgets(self):
        # Limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()

        self.welcome_label = ctk.CTkLabel(self, text="Bienvenido al \nPuzzle Deslizante", font=("Arial", 70))
        self.welcome_label.pack(pady=20)
        self.space(1)
        self.name_entry = ctk.CTkEntry(self, width=500, font=("Arial", 50), justify="center")
        self.name_entry.pack(pady=10)
        self.name_entry.insert(0, ">Ingrese su nombre<")
        self.name_entry.bind("<FocusIn>", self.on_entry_click)
        self.name_entry.bind("<FocusOut>", self.on_focus_out)
        self.name_entry.bind("<KeyRelease>", self.check_name_length)

        self.error_label = ctk.CTkLabel(self, text="", font=("Arial", 16), text_color="red")
        self.error_label.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="ENTRAR", command=self.start_game, font=("Arial", 36, 'bold'), fg_color='#157227', hover_color='#1f9d2d', text_color='black')
        self.start_button.pack(pady=20)

        self.bind("<Return>", lambda event: self.start_game())
        self.bind("<Escape>", lambda event: self.confirm_exit())

    def on_entry_click(self, event):
        if self.name_entry.get() == ">Ingrese su nombre<":
            self.name_entry.delete(0, "end")

    def on_focus_out(self, event):
        if self.name_entry.get() == "":
            self.name_entry.insert(0, ">Ingrese su nombre<")

    def check_name_length(self, event):
        if len(self.name_entry.get()) > 17:
            self.error_label.configure(text="Máximo 17 caracteres")
        else:
            self.error_label.configure(text="")
    def start_game(self):
        self.player_name = self.name_entry.get()
        if self.player_name:
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Por favor, ingrese su nombre.")

    def create_main_menu(self):
        if not self.mezclando:
            # Limpiar la ventana
            for widget in self.winfo_children():
                widget.destroy()
            self.space(1)
            
            for level in range(1, 4):
                button = ctk.CTkButton(self, text=f"Nivel {level}", command=lambda l=level: self.start_level(l), font=("Arial", 30))
                button.pack(pady=10)
            # Botón para mostrar el historial
            self.history_button = ctk.CTkButton(self, text="Mostrar Historial", command=self.show_history, font=("Arial", 30))
            self.history_button.pack(pady=10)

            self.bind("<Return>", lambda event: self.confirm_exit)
            self.bind("<BackSpace>", lambda event: self.create_menu_widgets())
            
            self.create_close_button()
            self.create_back_button(self.create_menu_widgets)

    def create_close_button(self):
        self.close_button = ctk.CTkButton(self, text="Cerrar", command=self.confirm_exit, font=("Arial", 16), fg_color='#9f0000', hover_color='#ff0000')
        self.close_button.place(relx=0.99, rely=0.99, anchor=tk.SE)
        
    def confirm_exit(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.quit()
            
    def confirm_return_to_menu(self):
        self.paused_time = time.time() - self.start_time  # Pausar el tiempo
        if messagebox.askokcancel("Regresar al menú", "¿Estás seguro de que quieres regresar al menú? \nTu progreso no se guardará."):
            self.create_main_menu()
        else:
            self.start_time = time.time() - self.paused_time  # Reanudar el tiempo
            self.update_time()

    def create_back_button(self, comando):
        self.back_button = ctk.CTkButton(self, text="Regresar", command=comando, font=("Arial", 16))
        self.back_button.place(relx=0.01, rely=0.99, anchor=tk.SW)

    def start_level(self, grid_size):
        self.grid_size = grid_size+3
        self.shuffle_num = 100*grid_size
        self.percentage_points = {
            1: "5",
            int(self.shuffle_num * 0.2): "4",
            int(self.shuffle_num * 0.4): "3",
            int(self.shuffle_num * 0.6): "2",
            int(self.shuffle_num * 0.8): "1",
            int(self.shuffle_num * 0.9): "¡Vamos!"
        }
        self.create_game_widgets()
        self.start_shuffle_thread()
        
        
    def create_game_widgets(self):
        # Limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()

        # Contenedor del tablero
        self.board_frame = ctk.CTkFrame(self, width=400, height=400)
        self.board_frame.pack(pady=20)

        # Crear botones de fichas
        self.tiles = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.text_vars = [[tk.StringVar() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                text_var = self.text_vars[row][col]
                tile = ctk.CTkButton(
                    self.board_frame,
                    textvariable=text_var,
                    width=80,
                    height=80,
                    font=("Mario Kart DS", 30, "bold"),
                    command=lambda r=row, c=col: self.move_tile(r, c),
                )
                tile.grid(row=row, column=col, padx=5, pady=5)
                self.tiles[row][col] = tile

        # Botón para mezclar
        self.shuffle_button = ctk.CTkButton(self, textvariable=self.text_shuffled, command=self.start_shuffle_thread)
        self.shuffle_button.pack(pady=10)
        self.create_close_button()
        self.create_back_button(self.confirm_return_to_menu)

        # Etiqueta de movimientos
        self.moves_label = ctk.CTkLabel(self, text="Movimientos: 0", font=("Arial", 16))
        self.moves_label.pack()

        # Etiqueta de tiempo
        self.time_label = ctk.CTkLabel(self, text="Tiempo: 0s", font=("OCR A Extended", 16), text_color='#157227', fg_color='black', corner_radius=20)
        self.time_label.pack()

        self._5_Go = ctk.CTkLabel(self, 
            textvariable=tk.StringVar(value=""), 

            font=("Arial", 100),
        )

        self._5_Go.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.loading_label = ctk.CTkLabel(self, text="")
        self.loading_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        
        self.bind("<Return>", lambda event: self.confirm_exit())
        self.bind("<BackSpace>", lambda event: self.confirm_return_to_menu())

        self.update_time() 
    

    def start_shuffle_thread(self):
        """Inicia un hilo separado para mezclar las fichas."""
        if not self.mezclando:  
            shuffle_thread = threading.Thread(target=self.shuffle_tiles)
            self.mezclando = True
            shuffle_thread.start()

    def shuffle_tiles(self):
        """Mezcla las fichas realizando movimientos válidos."""
        self.text_shuffled.set("Mezclando...")
        
        self.update_idletasks()

        self.start_loading_animation()

        self.mezclando = True
        
        self._5_Go.configure(textvariable=tk.StringVar(value=self.percentage_points[1]))
        self.update_idletasks()
        numbers = list(range(1, self.grid_size * self.grid_size))
        numbers.append(" ")

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                number = numbers.pop(0)
                self.text_vars[row][col].set(str(number) if number != " " else " ")
                self.update_tile_color(row, col)
                if number == " ":
                    self.empty_tile = (row, col)



        for i in range(self.shuffle_num):
            row, col = self.empty_tile
            possible_moves = []
            if row > 0: possible_moves.append((row - 1, col))
            if row < self.grid_size - 1: possible_moves.append((row + 1, col))
            if col > 0: possible_moves.append((row, col - 1))
            if col < self.grid_size - 1: possible_moves.append((row, col + 1))
            target = random.choice(possible_moves)
            self.move_tile(*target, update_moves=False)
            self.time_label.configure(text=f"Tiempo: 0:00")

            if i in self.percentage_points:
                self._5_Go.configure(textvariable=tk.StringVar(value=self.percentage_points[i]))
                self.update_idletasks()
            
        self._5_Go.configure(textvariable=tk.StringVar(value="")) 
        self.mezclando = False
        self.text_shuffled.set("Mezclar")
        self.moves = 0
        self.moves_label.configure(text="Movimientos: 0")
        self.start_time = time.time()
        self.stop_loading_animation()

    def move_tile(self, row, col, update_moves=True):
        """Mueve una ficha si es adyacente a la posición vacía."""
        if self.is_adjacent(row, col, *self.empty_tile):
            empty_row, empty_col = self.empty_tile

            self.text_vars[empty_row][empty_col].set(self.text_vars[row][col].get())
            self.text_vars[row][col].set(" ")

            self.update_tile_color(empty_row, empty_col)
            self.update_tile_color(row, col)

            self.empty_tile = (row, col)

            # Incrementar movimientos si no es parte del shuffle
            if update_moves:
                self.moves += 1
                self.moves_label.configure(text=f"Movimientos: {self.moves}")

            # Comprobar si el jugador ha ganado
            if not self.mezclando:
                if self.check_win():
                    self.save_score()
                    self.message_win()

    def update_tile_color(self, row, col):
        """Actualiza el color de la ficha según su texto."""
        if self.text_vars[row][col].get() == " ":
            self.tiles[row][col].configure(fg_color=self.board_frame.cget("fg_color"), hover_color=self.board_frame.cget("fg_color"))
        else:
            self.tiles[row][col].configure(fg_color='#02458a', hover_color='#025d8a')

    def is_adjacent(self, row1, col1, row2, col2):
        """Comprueba si dos celdas son adyacentes."""
        return abs(row1 - row2) + abs(col1 - col2) == 1

    def check_win(self):
        """Comprueba si las fichas están ordenadas correctamente."""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) != self.empty_tile:
                    expected_num = row * self.grid_size + col + 1
                    if self.text_vars[row][col].get() != str(expected_num):
                        return False
        return True

    def message_win(self):
        result = messagebox.askquestion("¡Ganaste!", "¡Felicidades! Completaste el puzzle.\n¿Quieres volver a jugar?", icon='info')
        if result == 'yes':
            self.shuffle_tiles()
        else:
            self.quit()

    def update_time(self):
        """Actualiza el tiempo transcurrido en formato minutos:segundos."""
        if hasattr(self, 'time_label') and self.time_label.winfo_exists():
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.time_label.configure(text=f"Tiempo: {minutes}:{seconds:02d}")
            self.after(1000, self.update_time)

    def save_score(self):
        """Guarda el puntaje del jugador en un archivo de texto."""
        elapsed_time = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        score = f"Movimientos: {self.moves}, Tiempo: {minutes}:{seconds:02d}"

        filename = f"{self.player_name}.txt"
        with open(filename, "a") as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {score}\n")

    def start_loading_animation(self):
        """Inicia la animación de carga."""
        if self.mezclando:
            if self.sprites:
                self.loading_label.configure(image=self.sprites[self.sprite_index])
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                self.loading_label.after(70, self.start_loading_animation)

    def stop_loading_animation(self):
        """Detiene la animación de carga."""
        self.mezclando = False
        self.loading_label.configure(image="")
        self.sprite_index = 0
        
    def show_history(self):
        history_file = f"{self.player_name}.txt"
        if os.path.exists(history_file):
            with open(history_file, "r") as file:
                history = file.read()
            messagebox.showinfo("Historial", history)
        else:
            messagebox.showinfo("Historial", "No hay historial disponible.")

if __name__ == "__main__":
    app = JuegoPuzzle()
    app.mainloop()