from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Book

def get_recommendations(book_title, num_recommendations=5):
    try:
        # Get all books from the database
        books = Book.objects.all()

        # Extract book descriptions and other attributes
        book_descriptions = []
        for book in books:
            # Concatenate attributes like title, description, authors, and genres
            book_info = f"{book.title} {book.description} {book.authors} "
            book_descriptions.append(book_info)

        # Create a TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')

        # Fit and transform the TF-IDF vectorizer
        tfidf_matrix = tfidf_vectorizer.fit_transform(book_descriptions)

        # Compute the cosine similarity between books
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        # Get the book with the given title
        book = books.filter(title=book_title).first()

        if not book:
            # Handle the case where the book with the given title does not exist
            return []

        # Get the index of the book in the list
        book_list = list(books)
        book_index = book_list.index(book)

        # Get the cosine similarity scores for the book of interest
        similar_books_indices = list(enumerate(cosine_sim[book_index]))

        # Sort books by similarity score in descending order
        similar_books_indices.sort(key=lambda x: x[1], reverse=True)

        # Get the top N similar books
        top_n_books_indices = [i[0] for i in similar_books_indices[1:num_recommendations + 1]]

        # Get the actual book objects based on the indices
        recommended_books = []

        for i in top_n_books_indices:
            book = book_list[i]
            recommended_books.append({
                'title': book.title,
                'authors': book.authors,
                'description': book.description,
                'thumbnail': book.thumbnail,
                'price': book.price,
                'ratingsCount': book.ratingsCount,
                'id': book.id,
            })
        print(recommended_books)
        return recommended_books
    except Exception as e:
        # Handle any other exceptions that may occur
        print(f"Error: {str(e)}")
        return []
