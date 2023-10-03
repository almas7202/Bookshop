from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Book

def get_recommendations(book_title, num_recommendations=5):
    try:
        # Get all books from the database
        books = Book.objects.all()

        # Create a TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')

        # Combine book attributes into a single text column for TF-IDF
        book_descriptions = books.values_list('title', 'authors', 'description')
        book_descriptions = [' '.join(description) for description in book_descriptions]

        # Fit and transform the TF-IDF vectorizer
        tfidf_matrix = tfidf_vectorizer.fit_transform(book_descriptions)

        # Compute the cosine similarity between books
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        # Get the index of the book with the given title
        book = books.filter(title=book_title).first()
        
        if not book:
            # Handle the case where the book with the given title does not exist
            return []

        book_index = book.id

        # Get the cosine similarity scores for the book of interest
        similar_books_indices = list(enumerate(cosine_sim[book_index]))

        # Sort books by similarity score in descending order
        similar_books_indices.sort(key=lambda x: x[1], reverse=True)

        # Get the top N similar books
        top_n_books_indices = [i[0] for i in similar_books_indices[1:num_recommendations+1]]

        # Get the actual book objects based on the indices
        recommended_books = []

        for i in top_n_books_indices:
            book = books.filter(id=i).first()
            if book:
                recommended_books.append({
                    'title': book.title,
                    'authors': book.authors,
                    'description': book.description,
                    'thumbnail': book.thumbnail,
                    'price': book.price,
                    'ratingsCount': book.ratingsCount,
                })

        return recommended_books
    except Exception as e:
        # Handle any other exceptions that may occur
        print(f"Error: {str(e)}")
        return []

