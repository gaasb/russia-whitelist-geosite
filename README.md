[English](README.en.md)

Подробнее: https://github.com/vahellame/russia-whitelist-routing

Домены находящихся в белых списках РФ, для роутинга Xray/V2Ray

Домены сгруппированы по сервисам и категориям в `data/`; `whitelist` объединяет все списки кроме `category-ads` и `category-public-dns`

**`category-ads`** включает в себя сгруппированные по провайдеру рекламу и трекеры. Взяты популярные из [AdGuard DNS filter](https://github.com/AdguardTeam/AdGuardSDNSFilter), [HaGeZi Pro](https://github.com/hagezi/dns-blocklists#pro), [OISD Big](https://oisd.nl/)

**`category-public-dns`** включает в себя DoH-резолверы Google, Cloudflare и Apple: через них клиент резолвит домены сам, и правила роутинга и блокировки могут не примениться. Без доступа к ним он откатывается на DNS конфигурации

## Скачать

```
https://github.com/vahellame/russia-whitelist-geosite/releases/latest/download/geosite.dat
```