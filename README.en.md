[Русский](README.md)

Main project: https://github.com/vahellame/russia-whitelist-routing

## What this is

Domains of services that are on Russian mobile internet whitelists. Compiled into a `geosite.dat` for Xray and into `.srs`, `.mrs` and `.list` rule sets for sing-box, mihomo and Shadowrocket, one set per category

Each release ships two checksums: `geosite.dat.sha256` with the bare 64-character hash, which INCY uses to tell whether the file changed ([more](https://docs.incy.cc/en/routing/#geo-files-optimized-downloading)), and `geosite.dat.sha256sum` in GNU coreutils format

## Categories

Domains are grouped by service and category in `data/`; `whitelist` combines every list except `category-ads`, `category-public-dns` and `private`

`category-ads` contains ads and trackers grouped by provider. Common ones taken from [AdGuard DNS filter](https://github.com/AdguardTeam/AdGuardSDNSFilter), [HaGeZi Pro](https://github.com/hagezi/dns-blocklists#pro), [OISD Big](https://oisd.nl/), [Loyalsoldier](https://github.com/Loyalsoldier/v2ray-rules-dat)

`category-public-dns` contains DoH and HTTPDNS resolvers: through them a client resolves domains on its own, so routing and blocking rules may not apply. With no access to them it falls back to the DNS from your config

## Intentionally left out of whitelist

Announced by Mintsifry, yet in practice absent from the whitelists:

- LizaAlert: `lizaalert.org`, `lizaalert.ru`
- Solovyov Live: `soloviev.live`
- Ruwiki: `ruwiki.ru`

Also not on the whitelists:

- `edgecdn.ru`, not let through by every carrier
- `yandex.kz`, `yandex.kg`
