# Захист рабораторної роботи №2

## Оператори

`intitle:рецепт -"без глютену" "шоколадний пиріг" OR "шоколадний \*" site:example.com OR site:anotherexample.com filetype:pdf inurl:2024 allinurl:рецепт/десерт allintext:інгредієнти intext:ваніль around(5) цукор cache:example.com/рецепти map:Київ source:кулінарний блог inanchor:"найкращі рецепти" blogurl:foodblog.com loc:placename"Львів"`

1. `intitle:рецепт` - шукає сторінки, де слово "рецепт" з'являється у заголовку.
2. `- "без глютену"` - виключає сторінки, що містять фразу "без глютену".
3. `"шоколадний пиріг" OR "шоколадний \*"` - шукає сторінки, які містять фразу "шоколадний пиріг" або "шоколадний торт".
4. `шоколадний *` - шукає сторінки де є комбінація шоколадний + щось, не важливо що.
5. `site:example.com OR site:anotherexample.com` - обмежує пошук тільки по цих сайтах
6. `filetype:pdf` - шукає тільки документи у форматі PDF.
7. `inurl:2024` - шукає URL, які містять "2024".
8. `allinurl:рецепт/десерт` - шукає URL, що містять обидва слова "рецепт" та "десерт".
9. `allintext:інгредієнти` - шукає сторінки, на яких слово "інгредієнти" з'являється у тексті.
10. `intext:ваніль` - шукає сторінки, де згадується слово "ваніль".
11. `around(5) цукор` - шукає сторінки, де слово "цукор" з'являється недалеко від попередніх ключових слів
12. `cache:example.com/рецепти` - показує кешовану версію конкретної сторінки.
13. `map:Київ` - шукає карту Києва.
14. `source:кулінарний блог` - цей оператор, як правило, використовується в Google News, щоб шукати статті з якогось джерела, але тут він може шукати в кулінарному блозі
15. `inanchor:"найкращі рецепти"` - шукає сторінки, на які посилають з якорним текстом "найкращі рецепти".
16. `blogurl:foodblog.com` - це типу шукати по сайту блогу, але можна просто site використати
17. `loc:"Львів"` - Буде шукати інформацію специфічну для міста Львів

Тут кілька операторів будуть трохи конфліктувати один з одним, але вони всі розписані та використані, тому наче нормально як для тестового запиту.

## Приклади запитів

### Запит за цікавими файлами

Запит: `(site:jsonformatter.org | site:codebeautify.org) & (intext:aws | intext:bucket | intext:password | intext:secret | intext:username)`

1. `(site:jsonformatter.org | site:codebeautify.org)` - Шукає сторінки виключно на двох сайтах: `jsonformatter.org` та `codebeautify.org`. Оператор `|` використовується як диз'юнкція, тобто результати можуть бути з одного сайту, іншого, або обох.

2. `&` - Логічний оператор кон'юнкції. Використовується для з'єднання двох умов пошуку, щоб обидві мали бути виконані. В цьому запиті робить так щоб виконались і умови з сайтами і умови з текстом

3. `(intext:aws | intext:bucket | intext:password | intext:secret | intext:username)` - Шукає сторінки, що містять хоча б одне з наступних слів у тексті сторінки: "aws", "bucket", "password", "secret", "username". І воно знову зроблене з "або" щоб хоча б одне з'явилось

### Запит до незахищеного серверу

Запит: `intitle:"index of" "/views/auth/passwords"`

1. `intitle:"index of"` - В титулі щоб було "index of", це зазвичай на сайтиках автоматично генерується перегляд директорії з браузера і якщо він не захищений його молгло проіндексувати та тепер ми можемо зайти

2. `"/views/auth/passwords"` - Це шлях по перегляду диркеторії, якщо він є на проіндексованій сторінці, то в нас скоріше за все є доступ до папочки з паролями цього сайтику.
