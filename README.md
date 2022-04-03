# <center > Systemy Operacyjne 2 - Projekt </center>
<center> Prowadzący: mgr inż. Tomasz Szandała </center> <br>
<center> Autorzy: Daria Jeżowska 252731</center> <br>
<center> Wiktoria Rekić 252830 </center>  <br>
<br></br>

<div style="text-align: justify">
Zadaniem było stworzenie aplikacji w języku Python działającej na wątkach. W naszym wypadku jest to gra "Pixel Invaders".</div> <br> 
<center><h2> Opis gry</h2></center>

<div style="text-align: justify">
Gra polegaja na poknaniu mini-bossów oraz statków przeciwników na każdym poziomie. Statki przeciwników, które strzelają pojawiają się od trzeciego poziomu, a ich liczba zwiększa się co każdy kolejny. Mini-bossy natomiast nie strzelają, ale nie znikają z ekranu, dopóki się ich nie pokona. Obijają się od krawędzi ekranu gry i na wszystkich poziomach jest ich stała ilość.  
</div>

<center> <h2>Użyte technologie </h2></center>

<div style="text-align: justify">
Projek został wykonany w języku Python w głównej mierze za pomocą bibliotek `threading` oraz `PyGame`. Użyte biblioteki pomocnicze to `os` oraz `random`.
</div>

<center> <h2> Budowa programu </h2> </center>

<div style="text-align: justify">

Gra składa się z pięciu głównych klas - `ship`, `player`, `enemy`, `boss` oraz `weapon`. `Ship` jest klasą bazową dla statków - tzn. gracza oraz przeciwników (odpowiednio klasy `player` oraz `enemy` i `boss`). Zdefiniowane jest w niej rysowanie statku na ekranie oraz strzelanie. W klasie `player` dodatkowo mamy nadpisaną funkcje poruszania, a także dodane sprawdzanie kolizji broni z przeciwnikami, poruszanie oraz pasek życia. W `enemy` jest dodane strzelanie z jakimś prawdopodobieństwem, aby statek przeciwnika nie mógł strzelać bez przew. Klasa `boss` jest oparta także na `threading.Thread` i jej działanie odbywa się na wątku. Mini-bossy mają dodane paski życia, rysowanie (rysowane są na oddzielnych płaszczyznach, które są przezroczyste), odbijanie się od ekranu oraz funkcję `run`, która jest używana, aby rozpocząć działanie obiektu na wątku. Klasa `weapon` odpowiedzialna jest za strzelanie do siebie przeciwników. W funkcji `main` tworzone są wszystkie statki oraz jest zdefiniowane działanie gry. W pliku `funcs` znajdują się dwie funkcje, jedna z nich jest odpowiedzialna za sprawdzani kolizji, a druga za uzyskiwanie ścieżki bezwzględnej, aby program mógł się uruchomić poprawnie niezależnie od lokalizacji. 

</div>

