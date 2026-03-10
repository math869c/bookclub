import os
import json
import re

# Load the books.json file
books_json_path = os.path.join(os.path.dirname(__file__), "data", "books.json")
output_folder = "books_html/"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Names in the correct order
reviewers = ["Nikolaj", "Toke", "Marius", "Mathias"]

# Book HTML template
book_template = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>{BOOK_TITLE}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="../layout/styles/layout.css" rel="stylesheet">
</head>

<body>
<!-- ################################################################################################ -->
<!-- ################################################################################################ -->
<!-- ################################################################################################ -->
<div class="wrapper row2">
        <nav id="mainav" class="hoc clear">
            <button class="mobile-nav-toggle" aria-expanded="false" aria-controls="main-menu">
                Oversigt
            </button>
            <!-- ################################################################################################ -->
            <ul class="clear" id="main-menu">
                <li class="active"><a href="../index.html">Forside</a></li>
                <li><a href="../books.html">Vores Bøger</a></li>
                <li class="has-submenu">
                    <button type="button" class="submenu-toggle" aria-expanded="false">
                        Yndlings Bøger
                    </button>
                    <ul class="submenu">
                        <li><a href="../books/de_bedste.html">Højeste Ratings</a></li>
                        <li><a href="../books/nikolajs_yndlings.html">Nikolaj</a></li>
                        <li><a href="../books/Tokes_yndlings.html">Toke</a></li>
                        <li><a href="../books/Marius_yndlings.html">Marius</a></li>
                        <li><a href="../books/Mathias_yndlings.html">Mathias</a></li>
                    </ul>
                </li>
                <li class="has-submenu">
                    <button type="button" class="submenu-toggle" aria-expanded="false">
                        Bøger Valgt Af
                    </button>
                    <ul class="submenu">
                        <li><a href="../personer/Nikolaj.html">Nikolaj</a></li>
                        <li><a href="../personer/Toke.html">Toke</a></li>
                        <li><a href="../personer/Marius.html">Marius</a></li>
                        <li><a href="../personer/Mathias.html">Mathias</a></li>
                    </ul>
                </li>
            </ul>
            <!-- ################################################################################################ -->
        </nav>
</div>


    <div class="wrapper row4">
        <div class="hoc container clear">
            <h2 class="center">{BOOK_TITLE}</h2>
            <article class="book-detail">
                <figure>
                    <img src="../{BOOK_IMAGE}" alt="{BOOK_TITLE}" class="uniform-book-image">
                    <figcaption><a href="#">By {BOOK_AUTHOR}</a></figcaption>
                </figure>
                <div class="txtwrap">
                    <p><strong>Forfatter:</strong> {BOOK_AUTHOR}</p>
                    <p><strong>Gns. rating:</strong> {AVG_RATING}/10</p>
                    <h3>Kommentarer</h3>
                    <ul>
                        {COMMENTS_LIST}
                    </ul>
                </div>
            </article>
            <p><a href="../books.html">⬅ Tilbage til bøger</a></p>
        </div>
    </div>

    <div class="wrapper row5">
        <div id="copyright" class="hoc clear">
            <p class="fl_left">Copyright &copy; 2025 - All Rights Reserved - Pedggie</p>
        </div>
    </div>
    <script>
      document.addEventListener("DOMContentLoaded", function () {{
        const button = document.querySelector(".mobile-nav-toggle");
        const menu = document.querySelector("#main-menu");

        if (!button || !menu) return;

        function closeAllSubmenus() {{
          menu.querySelectorAll(".submenu-open").forEach(function (item) {{
            item.classList.remove("submenu-open");
          }});

          menu.querySelectorAll(".submenu-toggle").forEach(function (toggle) {{
            toggle.setAttribute("aria-expanded", "false");
          }});
        }}

        function closeMenu() {{
          menu.classList.remove("is-open");
          button.setAttribute("aria-expanded", "false");
          closeAllSubmenus();
        }}

        function openMenu() {{
          menu.classList.add("is-open");
          button.setAttribute("aria-expanded", "true");
        }}

        button.addEventListener("click", function () {{
          if (menu.classList.contains("is-open")) {{
            closeMenu();
          }} else {{
            openMenu();
          }}
        }});

        menu.querySelectorAll("a").forEach(function (link) {{
          link.addEventListener("click", function () {{
            closeMenu();
          }});
        }});

        menu.querySelectorAll(".submenu-toggle").forEach(function (toggle) {{
          toggle.addEventListener("click", function (e) {{
            e.preventDefault();

            const parent = toggle.closest(".has-submenu");
            const isOpen = parent.classList.contains("submenu-open");

            closeAllSubmenus();

            if (!isOpen) {{
              parent.classList.add("submenu-open");
              toggle.setAttribute("aria-expanded", "true");
            }}
          }});
        }});
      }});
    </script>

</body>
</html>
"""

with open(books_json_path, "r", encoding="utf-8") as f:
    books = json.load(f)

# Generate HTML files for each book
book_files = []
for book in books:
    # Format book data
    book_title = book["title"]
    book_author = book["author"]
    book_image = book["image"]
    avg_rating = round(sum(book["ratings"]) / len(book["ratings"]), 1)

    # Combine reviewer name, rating and comment
    comments_list = "".join(
        f"<li><strong>{name}:</strong> {book['ratings'][i]}/10 – {book['comments'][i]}</li>"
        for i, name in enumerate(reviewers)
    )

    # Format filename (lowercase, replace spaces and special chars)

    filename = re.sub(r'[^a-z0-9_]', '', book_title.lower().replace(' ', '_'))
    book_path = os.path.join(output_folder, f"{filename}.html")

    # Populate template
    book_html = book_template.format(
        BOOK_TITLE=book_title,
        BOOK_AUTHOR=book_author,
        BOOK_IMAGE=book_image,
        AVG_RATING=avg_rating,
        COMMENTS_LIST=comments_list,
    )

    # Save to file
    with open(book_path, "w", encoding="utf-8") as f:
        f.write(book_html)
    
    book_files.append(book_path)

# Print the generated file list
print("Generated HTML files:")
for file in book_files:
    print(file)
