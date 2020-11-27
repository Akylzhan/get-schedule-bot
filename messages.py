startMsg = """Hello! Send me course name (eg. CSCI 152 or public speaking) and I will send you schedule of this course
use /help ples"""

help_msg = """напиши название курса \(аббревиатуру или название, не обяз полное\) и я отправлю тебе расписание\.
_Examples_:
Если написать боту csci, то он скинет лист всех CSCI курсов
Если написать public speaking, то скинет подходящие варианты

оничан, не пугайся, это всего лишь несколько моих команд:
1\. /start \- запустить меня \U0001F97A

2\. /help \- моя забота о тебе \U0001F49E

3\. /rating ProfName ProfSurname \- посмотреть рейтинг профа ProfName ProfSurname \U0001F47B
*Не обяз писать полное имя* профа, можно просто имя или фамилия
_Examples_:
_/rating Durvudkhan_
_/rating Aigerim_ \(don't do that, we had many Aigerim profs, TAs, therefore list will be loooooong, like my pp\)

4\. /rate ProfName ProfSurname \- оценить профа ProfName ProfSurname \U0001F929
**Examples: same as /rating**

5\. I can also reply in group\. The in group commands are same:
/start@nu\_course\_schedule\_bot
/help@nu\_course\_schedule\_bot
/rating@nu\_course\_schedule\_bot
/rate@nu\_course\_schedule\_bot

But to *search course in group* you should use
/course@nu\_course\_schedule\_bot
Otherwise I will not answer

for feedback write @shadowsan12\.
"""

smallQueryMsg = [
    "your query is smol", "your query is smol like your pp",
    "оничан, твой запрос слишком маленький",
    "Длина вашего запроса малюсенькая",
    "honey, this is not how it works: use longer queries",
    "hmm… your query doesn’t look good", "where’s the normal query, lebowski?"
]

emptyCourseListMsg = [
    "Такого курса нет в курс листе, либо я ошибка природы :(",
    "Я не панимат тебя, кажись такого курса нет :(",
    "Я не смог найти такой курс, пласти",
    "Прости меня сенпай, я не смог найти такой курс :(",
    "Я кажется слепой, потому что не вижу такого курса",
    "Я не нашёл курс, но хотя бы не потерял тебя",
    "Если ты ждал какого-то знака, то вот он. Такого курса нет",
    "Этот курс как твои недостатки. Его невозможно найти",
    "Я не нашел такой курс. Не наказывайте, позязя", "course not detected"
]

noScheduleMsg = "cannot find schedule or it was not uploaded"
registrarNotWorkingMsg = """Registrar is not working :C or working veryyyy sloooooowly.
Or maybe my creator is lazy to fix bugs.
Try again later, please.
By the way, you can check availability of NU websites in official NU Discord Server (https://discord.gg/SruKDaf)"""
