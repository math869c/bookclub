import os
import json
import re
from html import escape

# Load the books.json file
books_json_path = os.path.join(os.path.dirname(__file__), "data", "books.json")
output_folder = os.path.join(os.path.dirname(__file__), "books_html")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Used only for older data that does not yet contain an explicit reviewer list
DEFAULT_REVIEWERS = ["Nikolaj", "Toke", "Marius", "Mathias"]

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
                        <li><a href="../books/Olivers_yndlings.html">Oliver</a></li>
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
                        <li><a href="../personer/Oliver.html">Oliver</a></li>
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


def get_reviews(book):
    ratings = book.get("ratings", [])
    comments = book.get("comments", [])
    reviewers = book.get("reviewers", DEFAULT_REVIEWERS[:len(ratings)])

    if len(reviewers) != len(ratings):
        raise ValueError(
            f"{book.get('title', 'Unknown book')}: reviewers and ratings must have the same length "
            f"({len(reviewers)} reviewers, {len(ratings)} ratings)."
        )

    reviews = []
    for index, (reviewer, rating) in enumerate(zip(reviewers, ratings)):
        if isinstance(rating, bool) or not isinstance(rating, (int, float)):
            continue
        reviews.append({
            "reviewer": str(reviewer),
            "rating": rating,
            "comment": str(comments[index]) if index < len(comments) else "",
        })
    return reviews


# Generate HTML files for each book
book_files = []
for book in books:
    reviews = get_reviews(book)
    if not reviews:
        raise ValueError(f"{book.get('title', 'Unknown book')}: at least one numeric rating is required.")

    book_title = escape(str(book["title"]), quote=True)
    book_author = escape(str(book["author"]), quote=True)
    book_image = escape(str(book["image"]), quote=True)
    avg_rating = round(sum(review["rating"] for review in reviews) / len(reviews), 1)

    comments_list = "\n                        ".join(
        (
            f"<li><strong>{escape(review['reviewer'])}:</strong> "
            f"{review['rating']}/10"
            + (f" – {escape(review['comment'])}" if review["comment"] else "")
            + "</li>"
        )
        for review in reviews
    )

    filename = book.get("html_link")
    if not filename:
        filename = re.sub(r"[^a-z0-9_]", "", str(book["title"]).lower().replace(" ", "_")) + ".html"
    book_path = os.path.join(output_folder, filename)

    book_html = book_template.format(
        BOOK_TITLE=book_title,
        BOOK_AUTHOR=book_author,
        BOOK_IMAGE=book_image,
        AVG_RATING=avg_rating,
        COMMENTS_LIST=comments_list,
    )

    with open(book_path, "w", encoding="utf-8") as f:
        f.write(book_html)

    book_files.append(book_path)

print("Generated HTML files:")
for file in book_files:
    print(file)
