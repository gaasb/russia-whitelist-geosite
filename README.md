[English](README.en.md)

Подробнее: https://github.com/vahellame/russia-whitelist-routing

Домены находящихся в белых списках РФ, для роутинга Xray/V2Ray

Домены сгруппированы по сервисам и категориям в `data/`; `whitelist` объединяет все списки кроме `category-ads` и `category-public-dns`

`category-ads` включает в себя сгруппированные по провайдеру рекламу и трекеры. Взяты популярные из [AdGuard DNS filter](https://github.com/AdguardTeam/AdGuardSDNSFilter), [HaGeZi Pro](https://github.com/hagezi/dns-blocklists#pro), [OISD Big](https://oisd.nl/), [Loyalsoldier](https://github.com/Loyalsoldier/v2ray-rules-dat)

`category-public-dns` включает в себя DoH- и HTTPDNS-резолверы, через них клиент резолвит домены сам, и правила роутинга и блокировки могут не примениться. Без доступа к ним он откатывается на DNS конфигурации

## Намеренно не включено в whitelist

Заявлены Минцифры, но в белых списках отсутствуют:

- `lizaalert.org`, `lizaalert.ru` — ЛизаАлерт
- `soloviev.live` — Соловьёв Live
- `ruwiki.ru` — Рувики

Также не в белых списках:

- `edgecdn.ru` — не у всех операторов
- `yandex.kz`, `yandex.kg`

## Скачать

```text
https://github.com/vahellame/russia-whitelist-geosite/releases/latest/download/geosite.dat
```

## Контрольные суммы

К каждому релизу прикладываются две контрольные суммы в разных форматах.

`geosite.dat.sha256` содержит только сам хеш — 64 символа, без имени файла и без перевода строки. Такой формат ожидает INCY: он запрашивает его при обновлении подписки и, если хеш совпадает с уже сохранённым, пропускает скачивание `geosite.dat`. Подробнее [тут](https://docs.incy.cc/routing/#геофайлы-оптимизированное-скачивание)

`geosite.dat.sha256sum` — стандартный формат GNU coreutils, для проверки вручную:

```sh
sha256sum -c geosite.dat.sha256sum
```
