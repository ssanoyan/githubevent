Подписатся на телеграм бот: [BOT](t.me/exsamtest_bot)  
Запустыить докер композ командой: docker-compose up --build  
Требуется предустановленый докер композ.  

### как подписатся:  
 - /sub <repo_url> [список событий без ковычек, разделенные запятой]. На данный момент доступна подписка только на события PullRequestEvent, PushEvent, IssuesEvent.
### как изменить подписку:  
 - /unsub <repo_url> [список событий без ковычек, разделенные запятой]
### как отписатся:  
 - /unsub <repo_url>  
  
  

## Что не сделано но стоило бы:  
### REDIS
  1. редис запускается без пароля (в идеале надо содать пользователя и пароль с ограничеными доступами)
  2. В контейнер не монтируется внешнее хранилище что приведет к тому что после остановки контейнера все пользователи, подписки и события исчезнут
  3. Я бы вообще не использовал бы redis для этих целей. Лучше взять какой небуд легкий СУБД.  

Все обращения к redis а так же к GithubAPI не взяты в try, catch.  
Тконе к телеграм боту захардкоден хотя следует вынести его в конфиг файл а лучше в секреты.  
Так же подключение к редис (hostname, port) захардкодены хотя следовало вынести в конфиг файл. Все изменения должны делатся в конфиг файле а код нелзья трогать если это не улутшение функционала или багфиксинг.  


