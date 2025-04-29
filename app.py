import streamlit as st
import json
import os

LIBRARY_FILE = 'library.json'

# Load existing library
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Save updated library
def save_library(library):
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file, indent=4)

# Display books
def display_books(library):
    if not library:
        st.info("📭 Library is empty!")
        return
    read_books = [book for book in library if book.get("read")]
    unread_books = [book for book in library if not book.get("read")]

    st.subheader("✅ Read Books")
    for book in read_books:
        st.success(f"📖 {book['title']} by {book['author']} ({book['year']}) | Genre: {book['genre']}")

    st.subheader("🕐 Unread Books")
    for book in unread_books:
        st.warning(f"📚 {book['title']} by {book['author']} ({book['year']}) | Genre: {book['genre']}")

# Add new book
def add_book(library):
    with st.form("add_form"):
        st.subheader("➕ Add New Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Year", min_value=1000, max_value=2100, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Already Read?")
        submitted = st.form_submit_button("Add Book")
        if submitted:
            library.append({
                "title": title,
                "author": author,
                "year": str(year),
                "genre": genre,
                "read": read
            })
            save_library(library)
            st.success(f"✅ '{title}' added successfully!")

# Delete book
def delete_book(library):
    if not library:
        st.warning("❌ No books to delete.")
        return
    st.subheader("🗑 Delete a Book")
    book_titles = [f"{book['title']} by {book['author']}" for book in library]
    selected = st.selectbox("Select Book", book_titles)
    if st.button("Delete Book"):
        index = book_titles.index(selected)
        deleted = library.pop(index)
        save_library(library)
        st.success(f"❌ '{deleted['title']}' deleted.")

# Search book
def search_book(library):
    st.subheader("🔎 Search Book")
    query = st.text_input("Search by title, author, or genre")
    if query:
        result = [book for book in library if query.lower() in json.dumps(book).lower()]
        if result:
            st.info("🔍 Results:")
            for book in result:
                st.write(f"📘 {book['title']} by {book['author']} ({book['year']}) | Genre: {book['genre']} | {'✅ Read' if book['read'] else '🕐 Unread'}")
        else:
            st.error("❌ No match found.")

# Main App
def main():
    st.set_page_config(page_title="📚 VIP Library Manager", layout="centered")
    st.title("📚 VIP Personal Library Manager by Adeel Khan")

    library = load_library()

    menu = ["📖 View Books", "➕ Add Book", "🗑 Delete Book", "🔍 Search Book"]
    choice = st.sidebar.radio("Select Action", menu)

    if choice == "📖 View Books":
        display_books(library)
    elif choice == "➕ Add Book":
        add_book(library)
    elif choice == "🗑 Delete Book":
        delete_book(library)
    elif choice == "🔍 Search Book":
        search_book(library)

    st.markdown("---")
    st.markdown("<center>👑 Made with ❤️ by Adeel Khan</center>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
