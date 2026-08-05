[Русский](README.md)

More: https://github.com/vahellame/russia-whitelist-routing

Domains of services that are on Russian mobile internet whitelists, for Xray/V2Ray routing

Domains are grouped by service and category in `data/`; `whitelist` combines every list except `category-ads` and `category-public-dns`

`category-ads` contains ads and trackers grouped by provider. Common ones taken from [AdGuard DNS filter](https://github.com/AdguardTeam/AdGuardSDNSFilter), [HaGeZi Pro](https://github.com/hagezi/dns-blocklists#pro), [OISD Big](https://oisd.nl/)

`category-public-dns` contains DoH and HTTPDNS resolvers: through them a client resolves domains on its own, so routing and blocking rules may not apply. With no access to them it falls back to the DNS from your config

## Download
```
https://github.com/vahellame/russia-whitelist-geosite/releases/latest/download/geosite.dat
```
