document.addEventListener('DOMContentLoaded', () => {
  fetch('data/books.json')
    .then(response => response.json())
    .then(books => {
      books.forEach(book => {
        book.averageRating = BookRatings.average(book);
      });

      const ratedBooks = books
        .filter(book => book.averageRating !== null)
        .sort((a, b) => b.averageRating - a.averageRating)
        .slice(0, 3);

      const container = document.querySelector('.nospace.elements');
      if (!container) return;
      container.innerHTML = '';

      ratedBooks.forEach((book, index) => {
        const li = document.createElement('li');
        li.className = index === 0 ? 'one_third first' : 'one_third';

        li.innerHTML = `
          <article class="book-card">
            <figure>
              <img src="${book.image}" alt="${book.title}" class="uniform-book-image">
              <figcaption><a href="books_html/${book.html_link}">${book.title} &raquo;</a></figcaption>
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
