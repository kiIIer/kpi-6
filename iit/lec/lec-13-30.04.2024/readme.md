# Лекція

Логічна структуризація позволяє підвищити продуктивність, якщо мережа побудована на хабах, якщо одна станція передає, адреса станції що потрібна прийняти вона сусідня, але за принципом хаба, воно передає на всі порти, а не тому кому треба. І ось хаб який не знає що до нього під'єднано, до нього перший хаб, він передає до другого, і той усім до свого.

Якщо встановити одинкомутатор, він вже дозволяє підвищити ефективність, бо в нас дані передавались на всіх, а так вони не пройдут комутатор, він не пустить їх якщо не потрібно

Таку штуку можна тількя якщо передачі зачасту між одними хабами, але якщо є сервер та всі до нього ідуть, нічого не підвищиться.

Ось в нього 2 порти і там 2 мережі з однаковими протоколами, якщо це так то нам не міст потрібен а шлюз, в нас от є міст

І в нього 2 порти, один приймає і передає в цей сегмент і передає в цей сегмент, він аналізує адресу і якщо призначено в сигмент другий, він приймає цей кадр, та починає передавати в другий сегмент

Комутатор він дороще але за тим же стандартом що і міст. Міст оброблює послідовно, комутатор - паралельно

Процедура обробки вхідного кадру залижить від того з якої мережі він прибув та в яку направляється.

Якщо адреса відправника і мережа одержувача така сама, то кадр ігнорується, якщо в різних сегментах, то він перенаправляється, якщо адреса невідома, то він кидає всім

Такий самий алгоритм і в комутаторах.

Комутатор будує свою адресну таблиці, виходячи з пасивного спостереження за трафіком, який передається в сегментах, що підключені до його портів. Такий процес це самонавчення комутатора, і якщо хтось не передає дані, він ніколи не буде знати де він і буде передавати всім

Комутатор знає що в нього є порти і він аналізує адресу відправника кадру

коли передаються всім, це алгоритм заливки, якщо

Процедура старіння таблиці, в нас є остання дата яка в нас тут є, і ця дата аналізується, і якщо вона застара, адреса видаляється. далі якщо в нас є таблиця, і розмір обмежений, а розмір таблиці обмежений, та коли вже нікуди розміщувати, то вона видаляє старі записи, коли станцій багато, а таблиця обмежена, він починає працювати неефективно, та якщо надходять дані станції яку било видалено, в нього зрову лавинне передавання

Короче якщо там станція під'єднана до двох комутаторів, кадр надходить до двох, та вони передають далі, бо вони з'єднані, і вони побачать що станція відправник тепер вгорі та вони оновлять таблицю, далі самі кадри надходять друг другу та вони знову передають один одному

Використовується автоматиний алгоритм побудови дерева, ми будемо називати це кістякове дерево, треба перетворити будь-яку архтектуру, на малюнку в нас надписа англ мовою, цей малюнок запозичений зі стандарту, треба зробити щоб була топологія дерева, це доцільно зробити за допомогою алгоритму побудови кістякового дерава, щоб перетворити топології, нам не можна використовувати кадри езернет, нічого додаткові записи ми не можемо зробити, нам треба спеціальний алгоритм щоб кадр пройшов та зібрав інформацію, він збере вузли через які він пройшов. От кадр який пройшов з лан с до лан в, маршрут і треба за метриками зробити топологію, треба робити 