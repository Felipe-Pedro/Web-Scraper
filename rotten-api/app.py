import urllib.error

from PIL import ImageTk, Image
from tkinter import Tk, Frame, Label, Entry, Button, PhotoImage, Scrollbar, Text, RIGHT, LEFT, Y, END
from tkinter.font import Font

from rotten import Rotten

class App:
    def __init__(self):

        self.background_color = "#DCDCDC"

        self.rotten = Rotten()

        self.window = Tk()
        self.window.config(bg=self.background_color)
        self.window.iconphoto(True, PhotoImage(file="tomate.png"))

        self.movie_search_frame = Frame(self.window, bg=self.background_color)
        self.movie_search_frame.grid(row=0, column=0, padx=10, sticky="N")

        self.movie_info_frame = Frame(self.window, bg=self.background_color)
        self.movie_info_frame.grid(row=0, column=1, padx=(50, 0))

        self.movie_cast_frame = Frame(self.window, bg=self.background_color)
        self.movie_cast_frame.grid(row=0, column=2)

        self.cast_scroll = Scrollbar(self.movie_cast_frame, orient="vertical")
        

        self.movie_cast_text = Text(self.movie_cast_frame, yscrollcommand=self.cast_scroll.set)
        self.movie_cast_text.configure(width=35, bg=self.background_color)
        

        self.cast_scroll.config(command=self.movie_cast_text.yview)

        self.search_status_label = Label(self.movie_search_frame, width=30, borderwidth=1, relief="solid")
        self.search_status_label.grid(row=0, column=0, pady=10, columnspan=10)

        self.movie_name_search_label = Label(self.movie_search_frame, text="Movie:", bg=self.background_color)
        self.movie_name_search_label.grid(row=1, column=0, sticky="W")

        self.movie_name_entry = Entry(self.movie_search_frame)
        self.movie_name_entry.grid(row=1, column=1, sticky="W")

        self.search_movie_button = Button(self.movie_search_frame, text="Search", width=10)
        self.search_movie_button["command"] = lambda: self.movie_searcher()
        self.search_movie_button.grid(row=2, column=0, pady=3, columnspan=3)


        self.movie_name_label = Label(self.movie_info_frame, bg=self.background_color)
        self.movie_name_label.grid(row=0, column=0, pady=(30, 0))

        self.movie_poster_label = Label(self.movie_info_frame, bg=self.background_color)
        self.movie_poster_label.grid(row=1, column=0)

        self.rotten_rating_label = Label(self.movie_info_frame, bg=self.background_color)
        self.rotten_rating_label.grid(row=2, column=0, sticky="W")

        self.audience_rating_label = Label(self.movie_info_frame, bg=self.background_color)
        self.audience_rating_label.grid(row=3, column=0, sticky="W")


        self.window.title("Filmax")
        self.window.geometry("800x500")
        self.window.resizable(False, False)
        self.window.mainloop()

    def organize_cast(self, cast):
        cast_names = cast.keys()

        self.movie_cast_text["state"] = "normal"
        self.movie_cast_text.delete(1.0, END)

        for name in cast_names:
            self.movie_cast_text.insert(END, f"{name}: {cast[name]}\n")
        self.movie_cast_text["state"] = "disabled"

    def movie_searcher(self):
    
        movie_name = self.movie_name_entry.get()
        
        try:
            movie = self.rotten.search_movie(movie_name)
            if movie.movie_name == 0:
                raise urllib.error.URLError("Filme nao existe")

            self.search_status_label["text"] = "Movie loaded successfully"
            self.search_status_label["bg"] = "#8FBC8F"

            self.rotten_rating_label["text"] = f"Rotten rating: {movie.rotten_rating_value.strip()}"

            self.audience_rating_label["text"] = f"Audience rating: {movie.audience_rating_value.strip()}"

            fonte = Font(size=12, weight="bold")
            self.movie_name_label["font"] = fonte
            self.movie_name_label["text"] = movie.movie_name

            self.cast_scroll.pack(side=RIGHT, fill=Y)
            self.movie_cast_text.pack(side=LEFT)
            self.organize_cast(movie.movie_cast)

            im = Image.open(movie.movie_poster)
            imtk = ImageTk.PhotoImage(im)

            self.movie_poster_label["image"] =  imtk

            self.movie_poster_label["width"] = imtk.size[0]     #Just work if it throw a attribute error
            self.movie_poster_label["heigh"] = imtk.size[1]     # for some reason
        except urllib.error.URLError:
            self.search_status_label["text"] = "Movie don't exist"
            self.search_status_label["bg"] = "#FF7F50"

App()