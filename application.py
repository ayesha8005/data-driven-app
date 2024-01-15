from tkinter import END, Entry, Image, Label, Listbox, Text, Tk, Toplevel, ttk, Canvas, Button, PhotoImage
from pathlib import Path
import tkinter.font as tkFont
from tkinter.tix import NoteBook
import requests
from PIL import Image, ImageTk
from io import BytesIO
from tkmacosx import Button
from tkinter import Canvas, Scrollbar, VERTICAL

# Set paths for assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH_1 = OUTPUT_PATH / Path("/Users/ayesha/Desktop/build/assets/frame0")
ASSETS_PATH_2 = OUTPUT_PATH / Path("/Users/ayesha/Desktop/build/assets/frame1")

# Function to create path relative to ASSETS_PATH_1
def relative_to_assets_1(path: str) -> Path:
    return ASSETS_PATH_1 / Path(path)


# Function to make a request to TMDB API
def tmdb_request(endpoint, params={}):
    # TMDB API base URL and API key
    base_url = "https://api.themoviedb.org/3"
    api_key = '8200c244af3336fa25e80dc5c1a77ebf'
    params['api_key'] = api_key

    # Make the request
    response = requests.get(f"{base_url}/{endpoint}", params=params)
    data = response.json()

    if response.status_code == 200:
        return data
    else:
        print(f"Error {response.status_code}: {data.get('status_message', 'Unknown Error')}")
        return None

# Function to get movie images from TMDB
def get_movie_images(movie_id): 
        # Make a request to the TMDB API to get images for a specific movie
        endpoint = f"movie/{movie_id}/images"
        images_data = tmdb_request(endpoint)

        if images_data:
            image_paths = images_data.get("posters", [])  # You can also use 'backdrops' for other types of images
            return [f"https://image.tmdb.org/t/p/w500/{path['file_path']}" for path in image_paths]
        return []


# Function to get trending movies and display them
def get_trending_movies(window):
    base_url = "https://api.themoviedb.org/3"
    api_key = '8200c244af3336fa25e80dc5c1a77ebf'
    trending_url = f'{base_url}/trending/movie/week'
    params = {'api_key': api_key}
    response = requests.get(trending_url, params=params)
    trending_movies = response.json().get('results', [])

    row, col = 0, 0
    for i, movie in enumerate(trending_movies):
        title = movie['title']
        release_date = movie['release_date']
        overview = movie['overview']
        poster_path = movie['poster_path']

        movie_frame = ttk.Frame(window, padding=(5, 5, 5, 5), borderwidth=2, relief='solid')
        movie_frame.grid(row=row, column=col, padx=5, pady=10)

        display_movie_poster(movie_frame, poster_path)

        ttk.Label(movie_frame, text=f"Title: {title}", font=('Helvetica', 12, 'bold')).grid(row=0, column=1)
        ttk.Label(movie_frame, text=f"Release Date: {release_date}").grid(row=1, column=1)
        ttk.Label(movie_frame, text=f"Overview: {overview}", wraplength=200).grid(row=2, column=1)

        col += 1
        if col == 3:
            col = 0
            row += 1

    window.update_idletasks()
    window.config(scrollregion=window.bbox("all"))

# Function to display movie poster in a frame
def display_movie_poster(frame, poster_path):
    if poster_path:
        poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
        poster_data = requests.get(poster_url).content
        image = Image.open(BytesIO(poster_data))

        window_width = frame.winfo_reqwidth()
        new_width = min(image.width, window_width // 3)
        new_height = int((new_width / image.width) * image.height)

        new_width = 100
        new_height = 150
        image = image.resize((new_width, new_height))

        
        image = ImageTk.PhotoImage(image)

        poster_label = ttk.Label(frame, image=image)
        poster_label.image = image
        poster_label.grid(row=0, column=0, rowspan=3, padx=10)
    else:

        # Use a placeholder image if no poster is available
        placeholder_path = 'path/to/placeholder/image.jpg'
        placeholder_image = Image.open(placeholder_path)
        placeholder_image = ImageTk.PhotoImage(placeholder_image)

        placeholder_label = ttk.Label(frame, image=placeholder_image)
        placeholder_label.image = placeholder_image
        placeholder_label.grid(row=0, column=0, rowspan=3, padx=10)


window = Tk()
window.geometry("808x650")
window.configure(bg="#FFFFFF")

# Create a canvas for the main window
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=650,
    width=808,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_2 = PhotoImage(
    file=relative_to_assets_1("image_2.png"))
image_2 = canvas.create_image(
    404.0,
    325.0,
    image=image_image_2
)

canvas.create_text(
    424.0,
    371.0,
    anchor="nw",
    text="Welcome to my application !",
    fill="#FFFFFF",
    font=("Times New Roman", 30)
)

canvas.create_rectangle(
    273.0,
    383.0,
    401.0,
    400.0,
    fill="#ECDFB9",
    outline=""
)

canvas.create_text(
    277.0,
    436.0,
    anchor="nw",
    text="This is a Movie Database API where the top most relevant movies \n and their  information will be displayed (title, release date, \n description etc.)",
    fill="#FFFFFF",
    font=("Times New Roman", 18)
)

# Function to open the second window
def open_window2():
    window2 = Toplevel()
    window2.geometry("808x650")
    window2.configure(bg="#8ecae6")

    # Function to open a details window for a selected movie
    def open_details_window(movie_id):
        movie_details = get_movie_details(movie_id)
        if movie_details:
            details_window = Toplevel()
            details_window.title(f"Details for {movie_details['title']}")

        poster_path = movie_details['poster_path']
        if poster_path:
            # Display the movie poster in the details window
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            poster_image = Image.open(requests.get(poster_url, stream=True).raw)
            poster_image_tk = ImageTk.PhotoImage(poster_image)
            poster_label = Label(details_window, image=poster_image_tk)
            poster_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
            poster_label.image = poster_image_tk

        details_text = Text(details_window, width=40, height=10)
        details_text.grid(row=0, column=1, padx=10, pady=10)
        details_text.insert(END, f"Title: {movie_details['title']}\n")
        details_text.insert(END, f"Overview: {movie_details['overview']}\n")
        details_text.insert(END, f"Release Date: {movie_details['release_date']}\n")

    # Function to get movie details from TMDB API
    def get_movie_details(movie_id):
        endpoint = f"movie/{movie_id}"
        return tmdb_request(endpoint)

    # Function to search for movies based on a query
    def search_movies(query):
        endpoint = "search/movie"
        params = {'query': query}
        return tmdb_request(endpoint, params)

    # Function to handle the search button click event
    def search_button_clicked():
        query = entry.get()
        results = search_movies(query)
        if results:
            result_listbox.delete(0, END)
        for result in results['results']:
            result_listbox.insert(END, result['title'])

    # Function to show details for the selected movie
    def show_details():
        selected_index = result_listbox.curselection()
        if selected_index:
            selected_movie_title = result_listbox.get(selected_index)
            results = search_movies(selected_movie_title)
        if results and results['results']:
            selected_movie_id = results['results'][0]['id']
            open_details_window(selected_movie_id)

    def yview(self, *args):
        NoteBook.yview(*args)

    # GUI components for window2
    header = Label(window2, text="MoviesBase", bg='#0096c7', fg='white', font=('Georgia', 20), width=30, height=3)
    header.place(x=200, y=30)

    entry = Entry(window2, width=30)
    entry.place(x=199, y=140)

    search_button = Button(window2, text="Search", activeforeground='#EE3B3B', overrelief='flat', relief='flat',
                            borderwidth=2,
                            highlightthickness=1, highlightbackground='#CD5555', foreground='#1F1F1F',
                            background='#fb6f92', fg='white',
                            borderless=1, command=search_button_clicked)
    search_button.place(x=510, y=139)

    result_listbox = Listbox(window2, width=40, height=10, bg='#8ecae6', bd=0, highlightthickness=0)
    result_listbox.place(x=200, y=173)

    details_button = Button(window2, text="Show Details", activeforeground='#EE3B3B', overrelief='flat', relief='flat',
                            borderwidth=2,
                            highlightthickness=1, highlightbackground='#CD5555', foreground='#1F1F1F',
                            background='#9381ff', fg='white',
                            borderless=1, command=show_details)
    details_button.place(x=300, y=380)

    details_text = Text(window2, width=40, height=10, bg='#8ecae6', bd=0, highlightthickness=0)
    details_text.place(x=10, y=460)

    trending_button = Button(window2, text="Show Trending", activeforeground='#EE3B3B', overrelief='flat', relief='flat',
                            borderwidth=2,
                            highlightthickness=1, highlightbackground='#CD5555', foreground='#1F1F1F',
                            background='#9381ff', fg='white',
                            borderless=1, command=open_window3)
    trending_button.place(x=300, y=420)

    

    window2.mainloop()


# Function to open the third window

def open_window3(): 
    window3 = Toplevel()
    window3.geometry("808x650")
    window3.configure(bg="#8ecae6")

    # Call the function to get trending movies and display them

    get_trending_movies(window3)

    window3.mainloop()

    
# Create a button with an image and set its properties
button_image_1 = PhotoImage(
    file=relative_to_assets_1("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_window2,
    relief="flat"
)
button_1.place(
    x=503.0,
    y=573.8951416015625,
    width=167,
    height=56
)

window.mainloop()
