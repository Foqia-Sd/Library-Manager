import streamlit as st
import json

LIBRARY_FILE = "library.json"

# Load file
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:  # Corrected variable usage
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save book data
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:  # Corrected variable usage
        json.dump(library, file, indent=4)

# Add Book
def add_book(library, title, author, year, genre, read_status):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    }
    library.append(book)
    save_library(library)
    st.success("Book added successfully!")

# Remove Book
def remove_book(library, title):
    library[:] = [book for book in library if book['title'].lower() != title.lower()]
    save_library(library)
    st.success("Book removed successfully!")

# Search for Book
def search_book(library, search_term, search_by):
    return [book for book in library if search_term.lower() in book[search_by].lower()]

# Display Books
def display_books(library):
    if library:
        for book in library:
            st.write(f"**Title:** {book['title']}, **Author:** {book['author']}, **Year:** {book['year']}, **Genre:** {book['genre']}, **Read:** {'Yes' if book['read'] else 'No'}")
    else:
        st.write("No books found.")

# Books statistics
def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])  # Fixed incorrect variable name
    percentage_read = (read_books / total_books * 100) if total_books else 0
    st.write(f"**Total Books:** {total_books}")
    st.write(f"**Percentage Read:** {percentage_read:.2f}%")  # Fixed spacing issue

# Main Browser Display
def main():
    st.title("📚 Personal Library Manager")
    library = load_library()

    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Handling Menu
    if choice == "Add a Book":
        with st.form("add_book_form"):
            title = st.text_input("Enter the book title:")
            author = st.text_input("Enter the author:")
            year = st.number_input("Enter the publication year:", min_value=0, step=1)
            genre = st.text_input("Enter the genre:")
            read_status = st.radio("Have you read this book?", (True, False))
            submit = st.form_submit_button("Add Book")
            if submit and title and author and genre:
                add_book(library, title, author, year, genre, read_status)

    elif choice == "Remove a Book":
        title = st.text_input("Enter the title of the book to remove:")
        if st.button("Remove Book") and title:
            remove_book(library, title)

    elif choice == "Search for a Book":
        search_by = st.radio("Search by:", ["title", "author"])
        search_term = st.text_input("Enter your search term:")
        if st.button("Search") and search_term:
            results = search_book(library, search_term, search_by)  # Fixed function call
            if results:
                display_books(results)
            else:
                st.write("No matching books found.")

    elif choice == "Display All Books":
        display_books(library)

    elif choice == "Display Statistics":
        display_statistics(library)

if __name__ == "__main__":
    main()
