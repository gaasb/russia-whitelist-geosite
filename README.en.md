[Русский](README.md)

Main project: https://github.com/vahellame/russia-whitelist-routing

Domains of services that are on Russian mobile internet whitelists, for Xray/V2Ray routing

Domains are grouped by service and category in `data/`; `whitelist` combines every list except `category-ads` and `category-public-dns`

`category-ads` contains ads and trackers grouped by provider. Common ones taken from [AdGuard DNS filter](https://github.com/AdguardTeam/AdGuardSDNSFilter), [HaGeZi Pro](https://github.com/hagezi/dns-blocklists#pro), [OISD Big](https://oisd.nl/), [Loyalsoldier](https://github.com/Loyalsoldier/v2ray-rules-dat)

`category-public-dns` contains DoH and HTTPDNS resolvers: through them a client resolves domains on its own, so routing and blocking rules may not apply. With no access to them it falls back to the DNS from your config

## Intentionally left out of whitelist

Announced by Mintsifry, yet absent from the whitelists:

- `lizaalert.org`, `lizaalert.ru` — LizaAlert
- `soloviev.live` — Solovyov Live
- `ruwiki.ru` — Ruwiki

Also not on the whitelists:

- `edgecdn.ru` — not with every carrier
- `yandex.kz`, `yandex.kg`

## Download

```text
https://github.com/vahellame/russia-whitelist-geosite/releases/latest/download/geosite.dat
```

## Rule sets

The same data for sing-box, mihomo and Shadowrocket in `.srs`, `.mrs` and `.list` formats

```text
https://github.com/vahellame/russia-whitelist-geosite/releases/latest/download/geosite-whitelist.srs
```

Sets: `geosite-whitelist`, `geosite-category-ads`, `geosite-category-public-dns`

## Checksums

Every release ships two checksums in different formats.

`geosite.dat.sha256` holds the bare hash — 64 characters, no filename, no trailing newline. This is the format INCY expects: it fetches the file on subscription update and skips downloading `geosite.dat` when the hash matches the one it already has. More on it [here](https://docs.incy.cc/en/routing/#geo-files-optimized-downloading)

`geosite.dat.sha256sum` is the standard GNU coreutils format, for manual verification:

```sh
sha256sum -c geosite.dat.sha256sum
```
