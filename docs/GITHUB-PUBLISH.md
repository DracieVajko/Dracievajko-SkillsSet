# Publikovanie na GitHub

1. Rozbaľ ZIP a otvor koreň knižnice.
2. Skontroluj obsah a odstráň prípadné vlastné súkromné poznámky.
3. Vytvor vlastný prázdny repozitár na GitHube.
4. Nahraj súbory cez web alebo použi Git. Nasledujúce kroky vykonáš ty; balík nič automaticky neposiela.

```sh
git init
git add .
git commit -m "Add modular agent rules and skill catalog"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Ak už repozitár používaš, neinicializuj ani neprepisuj ho naslepo.
Raw URL vlastného publikovaného skillu bude mať tvar:
`https://raw.githubusercontent.com/YOUR-USERNAME/YOUR-REPOSITORY/main/custom-skills/ACTUAL-SKILL/SKILL.md`
Tento vzor nie je funkčný odkaz, kým nedoplníš skutočné hodnoty a súbor nezverejníš.
Existujúce Odysseus TXT odkazujú priamo na upstreamy a nepotrebujú tvoje používateľské meno.
