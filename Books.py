import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Book class
class Book:
    def __init__(self,id,title,genre,author,price):
        self.id = id
        self.title = title
        self.genre = genre
        self.author = author
        self.price = price
    # converts to string for print
    def __str__(self):
        return f"{self.id} | {self.title} | {self.genre} | {self.author} | {self.price}"

    # dict for json
    def to_dict(self):
      return {
            "ID": self.id,
            "Title": self.title,
            "Genre": self.genre,
            "Author": self.author,
            "Price": self.price

        }

class Gui:
    def __init__(self, json):
        # Json refrence
        self.json = json
        
        # Create main window
        root = tk.Tk()
        root.title("Books")
        root.geometry("500x400")
        
        # Dropdown menu for selecting search category
        self.combo = ttk.Combobox(root, values=["Title", "Genre", "Author", "Price"])
        self.combo.set("Title")
        self.combo.pack()
        
        # Search label and input field
        label_search = tk.Label(root, text="Search")
        label_search.pack()
        self.entry_search = tk.Entry(root)
        self.entry_search.pack()

        # Search button
        srchBtn = tk.Button(root, text="Search", command=self.submit)
        srchBtn.pack()

        # Add, Update and Delete buttons
        addBtn = tk.Button(root, text="Add",command=self.add_window)
        addBtn.pack()
        upBtn = tk.Button(root, text="Update",command=self.update_window)
        upBtn.pack()
        delBtn = tk.Button(root, text="Delete", command=self.delete)
        delBtn.pack()

        # Listbox to display books
        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack()

        #Start GUI
        root.mainloop()

    # Search function
    def submit(self):
        # text from search field
        usrInput = self.entry_search.get()
        #selected search category
        cat = self.combo.get()
        SrchRe = self.json.search(cat,usrInput)

        ## Clear previous results
        self.listbox.delete(0, tk.END)

        ## Insert new results into listbox
        for book in SrchRe:
            self.listbox.insert(tk.END, f"{book['ID']} | {book['Title']}| {book['Genre']} | {book['Author']} | {book['Price']}")

    # Add new book window
    def add_window(self):
        self.window = tk.Toplevel()
        self.window.title("Add Book")
        self.window.geometry("500x400")

        ## Input fields
        idLabel = tk.Label(self.window, text="ID")
        idLabel.pack()
        self.entry_id = tk.Entry(self.window)
        self.entry_id.pack()

        titlabel = tk.Label(self.window, text="Title")
        titlabel.pack()
        self.entry_title = tk.Entry(self.window)
        self.entry_title.pack()

        genLabel = tk.Label(self.window, text="Genre")
        genLabel.pack()
        self.entry_Genre = tk.Entry(self.window)
        self.entry_Genre.pack()

        AuthLabel = tk.Label(self.window, text="Author")
        AuthLabel.pack()
        self.entry_Auth = tk.Entry(self.window)
        self.entry_Auth.pack()

        prcLabel = tk.Label(self.window, text="Price")
        prcLabel.pack()
        self.entry_price = tk.Entry(self.window)
        self.entry_price.pack()

        # Save button
        addBtn = tk.Button(self.window, text="Add", command=self.add_submit)
        addBtn.pack()

    ## Save new book to JSON and close window
    def add_submit(self):
      book = Book(self.entry_id.get(),self.entry_title.get(),self.entry_Genre.get(),self.entry_Auth.get(),self.entry_price.get())
      self.json.add(book)
      self.window.destroy()

    # Open update window
    def update_window(self):
        self.listbox.curselection()
        self.window = tk.Toplevel()
        self.window.title("Update Book")
        self.window.geometry("500x400")

        # Select which field to update
        self.update_combo = ttk.Combobox(self.window, values=["Title", "Genre", "Author", "Price"])
        self.update_combo.set("Title")
        self.update_combo.pack()

        label_update = tk.Label(self.window, text="Update")
        label_update.pack()
        
        # Input field for new value
        self.entry_update = tk.Entry(self.window)
        self.entry_update.pack()

        upBtn = tk.Button(self.window, text="Update", command=self.update_submit)
        upBtn.pack()

    # Apply update to selected book
    def update_submit(self):
      selected = self.listbox.get(tk.ACTIVE)
      # If nothing is selected, exit
      if not selected:
         return
      # Extract book ID
      book_id = selected.split(" | ")[0]
      cat = self.update_combo.get()

      new_value = self.entry_update.get()

      # checks if empty
      if new_value == "":
          messagebox.showerror("fel", "Tomt fält")
          return
    # Checks if price is digit
      if cat == "Price":
          if not new_value.isdigit():
              messagebox.showerror("Fel", "Price måste vara ett tal!")
              return
      
      # Update data
      self.json.update(book_id, cat, new_value)
      self.window.destroy()

    # Removes book
    def delete(self):
      selected = self.listbox.get(tk.ACTIVE)
      
      # If nothing selected, do nothing
      if not selected:
         return

      book_id = selected.split(" | ")[0]

      self.json.delete(book_id)


# Json data
class Json:
    def __init__(self, filename):
        self.filename = filename
        # Load existing data from file
        with open(self.filename, "r") as f:
            self.books = json.load(f)

    # Search books by category and query
    def search(self, category, query):
        result = []
        for book in self.books:
          if query.lower() in str(book[category]).lower():
              result.append(book)
        return result

    # Add a new book
    def add(self, book):
      self.books.append(book.to_dict())
      self.save()

    # Save data to JSON file
    def save(self):
      with open(self.filename, "w") as f:
        json.dump(self.books,f, indent=4)

    # Update an existing book
    def update(self, book_id, category, input_value):
        for book in self.books:
              if book["ID"] == book_id:
                  book[category] = input_value
                  self.save()
                  return
    ## Delete a book
    def delete(self,book_id):
      for book in self.books:
        if book["ID"] == book_id:
            self.books.remove(book)
            self.save()


def main():
    data = Json("books.json")
    Gui(data)

if __name__ == "__main__":
    main()

