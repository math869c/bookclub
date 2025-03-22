document.addEventListener('DOMContentLoaded', () => {
  fetch('data/books.json')
    .then(response => response.json())
    .then(books => {
      // Calculate average rating for each book
      books.forEach(book => {
        const totalRating = book.ratings.reduce((sum, rating) => sum + rating, 0);
        book.averageRating = totalRating / book.ratings.length;
      });

      // Sort books by average rating in descending order
      books.sort((a, b) => b.averageRating - a.averageRating);

      // Select top three books
      const topThreeBooks = books.slice(0, 3);

      // Render top three books
      const container = document.querySelector('.nospace.elements');
      container.innerHTML = ''; // Clear existing content

      topThreeBooks.forEach((book, index) => {
        // Set the correct class name for the first book
        const li = document.createElement('li');
        li.className = index === 0 ? 'one_third first' : 'one_third';

        li.innerHTML = `
          <article class="book-card">
            <figure>
              <img src="${book.image}" alt="${book.title}" class = "uniform-book-image">
              <figcaption><a href="${book.overview}">${book.title} &raquo;</a></figcaption>
            </figure>
            <div class="txtwrap">
              <h6 class="heading">${book.title}</h6>
              <p><strong>Gns. rating:</strong> ${book.averageRating.toFixed(2)}/10</p>
            </div>
          </article>
        `;

        container.appendChild(li);
      });
    })
    .catch(error => console.error('Error fetching books:', error));
});
