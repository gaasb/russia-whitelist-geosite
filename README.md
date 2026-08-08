[English](README.en.md)

Основной проект: https://github.com/vahellame/russia-whitelist-routing

## Что это

Домены находящихся в белых списках РФ. Собираются в `geosite.dat` для Xray и в rule-set форматов `.srs`, `.mrs` и `.list` для sing-box, mihomo и Shadowrocket

К каждому релизу прикладывается `geosite.dat.sha256` — только хеш, 64 символа без имени файла. По нему INCY понимает, что файл не менялся, и не качает его заново. Подробнее [тут](https://docs.incy.cc/routing/#геофайлы-оптимизированное-скачивание). Рядом `geosite.dat.sha256sum` в стандартном формате GNU coreutils

## Категории

Домены сгруппированы по сервисам и категориям в `data/`; `whitelist` объединяет все списки кроме `category-ads` и `category-public-dns`

`category-ads` включает в себя сгруппированные по провайдеру рекламу и трекеры. Взяты популярные из [AdGuard DNS filter](https://github.com/AdguardTeam/AdGuardSDNSFilter), [HaGeZi Pro](https://github.com/hagezi/dns-blocklists#pro), [OISD Big](https://oisd.nl/), [Loyalsoldier](https://github.com/Loyalsoldier/v2ray-rules-dat)

`category-public-dns` включает в себя DoH- и HTTPDNS-резолверы, через них клиент резолвит домены сам, и правила роутинга и блокировки могут не примениться. Без доступа к ним он откатывается на DNS конфигурации

## Намеренно не включено в whitelist

Заявлены Минцифры, но в белых списках отсутствуют:

- ЛизаАлерт — `lizaalert.org`, `lizaalert.ru`
- Соловьёв Live — `soloviev.live`
- Рувики — `ruwiki.ru`

Также не в белых списках:

- `edgecdn.ru` — не у всех операторов
- `yandex.kz`, `yandex.kg`
