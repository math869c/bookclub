# bookclub
For bogklubben
Link for bogklubben: https://math869c.github.io/bookclub/?fbclid=IwY2xjawPkkKpleHRuA2FlbQIxMABicmlkETFpZ3psM2NJM0hhSGlDT0pJc3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHpFXNtn8Ln88e6vAxcRCZB3cjhZQfEI1HAXIi0GhF_YadhqXQZd1rIeNIRyN_aem_ilPSr53ZJODngCInk3JorA
## Ratings fra 4 eller 5 medlemmer

Hver bog har tre parallelle lister: `reviewers`, `ratings` og `comments`. De skal stå i samme rækkefølge og `reviewers` og `ratings` skal have samme antal elementer.

Eksempel, når Oliver også har rated en bog:

```json
"reviewers": ["Nikolaj", "Toke", "Marius", "Mathias", "Oliver"],
"ratings": [6, 8, 5, 7, 9],
"comments": ["...", "...", "...", "...", "Olivers kommentar"]
```

Gennemsnittet beregnes automatisk ud fra de numeriske ratings, så både 4 og 5 ratings virker. Kør derefter:

```bash
python generate_html.py
```

## Oliver på forsiden

Forsiden bruger billedet `images/demo/people/oliver.jpg`. Den medfølgende fil er kun en midlertidig pladsholder og kan overskrives direkte med det rigtige billede med samme filnavn.
