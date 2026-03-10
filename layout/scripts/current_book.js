document.addEventListener("DOMContentLoaded", () => {

  fetch("data/current_book.json")
    .then(response => response.json())
    .then(data => {

      const book = data[0]; // first book
      const container = document.getElementById("current-book");

      container.innerHTML = `
        <li class="one_third first featured-current-book">
          <article class="book-card">
            <figure>
              <img src="${book.image}" alt="${book.title}" class="uniform-book-image">
            </figure>

            <div class="txtwrap">
              <h6 class="heading">${book.title}</h6>
              <p><strong>Valgt af:</strong> ${book.picked_by}</p>
            </div>
          </article>
        </li>
      `;
    })

    .catch(error => console.error("Error loading current book:", error));

});