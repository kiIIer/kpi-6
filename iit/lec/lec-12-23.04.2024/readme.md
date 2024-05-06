# Лекція

Є істино калстерні засосунки які готові працювати на багатьох частинах кластера та комунікувати між собою, а є звичайні програми в яких є паралелізм, і ці стосунки відносяться до звичайних застосунків.

Открім того повинне кластерне програмне збезпечення яке встановлюється на операційну систему або частину операційної системи, зрозуміло що компоненти кластерного забезпечення треба на кожен сервер що є в кластрері.

Переваги кластерізації - абсолютна масштабованітсь, це здатність системи гарно працювати де в системи багато всього, кластерна система не залежна від кількості серверів що її складають. Далі це нарощувана масштабованість, це здатність працювати на невеликій кількості серверів та у разі потреби нароистити. Великий коефіцієнт готовності, надходить запит, система відповідає не залежно що якісь сервери не працюють, співвідношення ціна/вартість, бо там на відміну від блейд системи, там компоненти що є в кожному сервері, таке як живлення, мережеве обладнання, в кожному сервері є свій якийсь кормус.

Недолік - якщо в нас розподілена система, на взаємодію між собою уходить час, в мікросервісній на відміні від монолітній треба витрачати час на взаємодію на передавання.

Щоб пободувати мережу, потрібен адаптер, мережева пара, інтерфейсна карта, вона зазвичай інтегрована, вона на платі напаяна, вона реалізує мак підрівень, якщо в нас комп велики, в нас може бути мережева карта на материнській платі, або одна чи дві мережеві карти які ідуть в слоти.

Кількість стандартів швидкості езернет дуже велика, підрівень ллс не залежить від нижнього рівня, а от на рівні мак підрівня там є відмінності і ці відмінності вже реалізуються на фізичному рівні, різні швидкості, різні рівні лінії зв'язку, щоб робити пеердавання лініями зв'язку, і там сигнали для передавання даних, на мак підрівні є механізм захисту від помилок, там додається контрольна послідовність кадра, та якщо з'являються помилки, робиться перевірка та ці кадри відкидаються.

Розрізнять адаптери для робочих станцій та для серверу, якщо людина неосвідчена, там же типу принципи однакові, взаємодії не відрізняються, але от коли ми розглядали сервери, його основна задача - якумого ефективніше виконувати обчислювальні задачі, щоб давати сервіс користувачам, щоб він ефективно функціонував, він не повинен відволікатись, типу керувати передачею даних через мережевий інтерфейс, тому в адаптерах для сервера є додатковий процесор, який ефективно виконує команди передачі в мережу, не відволікаючи при цьому сервер. Найпростіший пристрій який забезпечує передачу між комп'ютерами, це концентратор або хаб, це повторювач з фунцією автовідключення, от там битовий, зазвичай він такий 19-дюймовий.

В лініях зв'язку виникають помилки, тому в нього одна з основних задач - захист від помилок та виявлення що помилки знайшлись. Концентратор приймає сигнал з одного порта та передає на всі інші, якщо він бачить що порт несправний, він відмикається, він просто повторює кад, і якщо він просто повторює, в нього простий механізм визначення конфлікту.

За допомогою хаба можно зробити багатосегментну мережу.

Переваги мереж зі спільним середовищем з хабом: економічне рішення, рпоста топологія, просте нарощування, нема втрати кадрів через переповнення буфера. Недолік: погана масштабованість, жорсткі обмеження на максимальну довжину мережі, через особливості доступу езернет.

Комутовані локальні мережі. Рішення масштабованості, бо дозволяли попарне з'єднання, і щоб комутатор працював - він повинен знати куди дані передавати та знати адресу комп'ютерта щоб передавати дані безпосередньо на той порт а не на всі як це робив комутатор, цей комутатор потрібен отримати додаткову інформацію.

Переваги це логічна структуризація, було в нас єдине середовище, що всі працюють та якщо там багато компів то ефективність менша, якщо його поділити на 2 частини то воно буде ефективніше працювати якщо передавань між сегментами нема, але якщо між середовищами будуть пересилки постійно, то через один міст який з'єднує 2 підмережі, будуть данні ходити та це буде неефективно.

І є комутатор, він підвище ефективність, бо передача 