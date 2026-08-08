[Русский](README.md)

Main project: https://github.com/vahellame/russia-whitelist-routing

## What this is

Domains of services that are on Russian mobile internet whitelists. Compiled into a `geosite.dat` for Xray and into `.srs`, `.mrs` and `.list` rule sets for sing-box, mihomo and Shadowrocket

Every release ships a `geosite.dat.sha256` — the bare hash, 64 characters with no filename. INCY uses it to tell the file has not changed and skips re-downloading it. More on it [here](https://docs.incy.cc/en/routing/#geo-files-optimized-downloading). Alongside it, `geosite.dat.sha256sum` in the standard GNU coreutils format

## Categories

Domains are grouped by service and category in `data/`; `whitelist` combines every list except `category-ads` and `category-public-dns`

`category-ads` contains ads and trackers grouped by provider. Common ones taken from [AdGuard DNS filter](https://github.com/AdguardTeam/AdGuardSDNSFilter), [HaGeZi Pro](https://github.com/hagezi/dns-blocklists#pro), [OISD Big](https://oisd.nl/), [Loyalsoldier](https://github.com/Loyalsoldier/v2ray-rules-dat)

`category-public-dns` contains DoH and HTTPDNS resolvers: through them a client resolves domains on its own, so routing and blocking rules may not apply. With no access to them it falls back to the DNS from your config

## Intentionally left out of whitelist

Announced by Mintsifry, yet absent from the whitelists:

- LizaAlert — `lizaalert.org`, `lizaalert.ru`
- Solovyov Live — `soloviev.live`
- Ruwiki — `ruwiki.ru`

Also not on the whitelists:

- `edgecdn.ru` — not with every carrier
- `yandex.kz`, `yandex.kg`
