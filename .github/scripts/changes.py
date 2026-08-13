#!/usr/bin/env python3
import collections
import re
import subprocess
import sys
import pathlib

DATA = "data"
INDEX = "index"
PREFIXES = ("full:", "domain:")
MAX_ITEMS = 25
DOMAINISH = re.compile(r"[a-z0-9][a-z0-9._-]*\.[a-z0-9-]{2,}\*?")
MAX_SCOPES = 3


def git(*args):
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8"
    )


def out(*args):
    r = git(*args)
    if r.returncode != 0:
        raise SystemExit(r.stderr.strip())
    return r.stdout


def data_files(rev):
    if rev == INDEX:
        listing = out("ls-files", "--", DATA)
    elif rev is None:
        root = pathlib.Path(DATA)
        return sorted(
            str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()
        )
    else:
        listing = out("ls-tree", "-r", "--name-only", rev, f"{DATA}/")
    return sorted(
        line.split("/", 1)[1] for line in listing.splitlines() if line.strip()
    )


def read(rev, name):
    if rev is None:
        path = pathlib.Path(DATA) / name
        return path.read_text(encoding="utf-8") if path.exists() else ""
    spec = f":{DATA}/{name}" if rev == INDEX else f"{rev}:{DATA}/{name}"
    r = git("show", spec)
    return r.stdout if r.returncode == 0 else ""


def header_name(line):
    return line.lstrip("#").split("#", 1)[0].strip()


def commented_rule(line):
    text = line.lstrip("#").strip()
    if not text:
        return False
    token = text.split()[0]
    if token.startswith(PREFIXES):
        return True
    return bool(DOMAINISH.fullmatch(token))


def split_comment(line):
    i = line.find("#")
    if i < 0:
        return line.strip(), ""
    return line[:i].strip(), line[i + 1 :].strip()


def bare(rule):
    value = rule.split("@", 1)[0].strip()
    for p in PREFIXES:
        if value.startswith(p):
            return value[len(p) :]
    return value


def kind(rule):
    value = rule.split("@", 1)[0].strip()
    for p in PREFIXES:
        if value.startswith(p):
            return p[:-1]
    return "domain"


def parse(text):
    sections = collections.OrderedDict()
    current = ""
    blank = True
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            blank = True
            continue
        if line.startswith("#"):
            if blank and not commented_rule(line):
                current = header_name(line)
                sections.setdefault(current, collections.OrderedDict())
            blank = False
            continue
        blank = False
        rule, comment = split_comment(line)
        if not rule:
            continue
        sections.setdefault(current, collections.OrderedDict())[bare(rule)] = (
            kind(rule),
            comment,
        )
    return sections


def snapshot(rev):
    return {name: parse(read(rev, name)) for name in data_files(rev)}


def index_of(tree):
    flat = {}
    for name, sections in tree.items():
        for section, rules in sections.items():
            for domain, meta in rules.items():
                flat[(name, section, domain)] = meta
    return flat


def compare(old, new):
    old_flat = index_of(old)
    new_flat = index_of(new)
    old_keys = set(old_flat)
    new_keys = set(new_flat)

    added = {k: new_flat[k] for k in new_keys - old_keys}
    removed = {k: old_flat[k] for k in old_keys - new_keys}
    retyped = {
        k: (old_flat[k][0], new_flat[k][0])
        for k in old_keys & new_keys
        if old_flat[k][0] != new_flat[k][0]
    }

    moved = []
    by_domain_removed = collections.defaultdict(list)
    for name, section, domain in removed:
        by_domain_removed[domain].append((name, section))
    for key in list(added):
        name, section, domain = key
        sources = by_domain_removed.get(domain)
        if not sources:
            continue
        src = sources.pop(0)
        moved.append((src, (name, section), domain))
        del added[key]
        del removed[(src[0], src[1], domain)]

    new_sections = {
        (name, section)
        for name, sections in new.items()
        for section in sections
        if section not in old.get(name, {})
    }
    dropped_sections = {
        (name, section)
        for name, sections in old.items()
        for section in sections
        if section not in new.get(name, {})
    }
    return {
        "added": added,
        "removed": removed,
        "retyped": retyped,
        "moved": moved,
        "new_sections": new_sections,
        "dropped_sections": dropped_sections,
    }


def group(items):
    grouped = collections.defaultdict(lambda: collections.defaultdict(list))
    for (name, section, domain), meta in sorted(items.items()):
        grouped[name][section].append((domain, meta))
    return grouped


def scope_label(section):
    return section.split("(", 1)[0].strip() or "прочее"


def render_group(title, items, new_sections=None):
    if not items:
        return []
    lines = [f"### {title}", ""]
    for name, sections in sorted(group(items).items()):
        for section, entries in sorted(sections.items()):
            mark = " (новый)" if new_sections and (name, section) in new_sections else ""
            head = f"**{name} / {section or 'без раздела'}**{mark}"
            lines.append(head)
            shown = entries[:MAX_ITEMS]
            for domain, meta in shown:
                note = f" — {meta[1]}" if meta[1] else ""
                prefix = "" if meta[0] == "domain" else f"{meta[0]}:"
                lines.append(f"- {prefix}{domain}{note}")
            rest = len(entries) - len(shown)
            if rest > 0:
                lines.append(f"- …и ещё {rest}")
            lines.append("")
    return lines


def whitelist_total(rev):
    text = read(rev, "whitelist")
    names = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if line.startswith("include:"):
            names.append(line[len("include:") :].strip())
    domains = set()
    for name in names:
        for rules in parse(read(rev, name)).values():
            domains.update(rules)
    return len(domains)


def changelog(old_rev, new_rev):
    old = snapshot(old_rev)
    new = snapshot(new_rev)
    diff = compare(old, new)

    lines = []
    lines += render_group("Добавлено", diff["added"], diff["new_sections"])
    lines += render_group("Удалено", diff["removed"])

    if diff["moved"]:
        lines += ["### Перенесено", ""]
        for (src_file, src_section), (dst_file, dst_section), domain in sorted(
            diff["moved"], key=lambda m: m[2]
        )[:MAX_ITEMS]:
            lines.append(
                f"- {domain}: {src_file} / {src_section} → {dst_file} / {dst_section}"
            )
        rest = len(diff["moved"]) - MAX_ITEMS
        if rest > 0:
            lines.append(f"- …и ещё {rest}")
        lines.append("")

    if diff["retyped"]:
        lines += ["### Изменён тип правила", ""]
        entries = sorted(diff["retyped"].items())
        for (name, section, domain), (was, now) in entries[:MAX_ITEMS]:
            lines.append(f"- {name} / {section}: {domain} — {was} → {now}")
        rest = len(entries) - MAX_ITEMS
        if rest > 0:
            lines.append(f"- …и ещё {rest}")
        lines.append("")

    before = whitelist_total(old_rev)
    after = whitelist_total(new_rev)
    delta = after - before
    sign = f"+{delta}" if delta > 0 else str(delta)
    lines += [
        "---",
        "",
        f"Доменов в `whitelist`: {after} ({sign})"
        if delta
        else f"Доменов в `whitelist`: {after}",
    ]

    body = "\n".join(lines).strip()
    return body or "Без изменений в списках доменов"


def subject(old_rev, new_rev):
    args = ["diff", "--name-only", old_rev]
    if new_rev == INDEX:
        args = ["diff", "--cached", "--name-only", old_rev]
    elif new_rev:
        args.append(new_rev)
    changed = out(*args).split()
    non_data = [p for p in changed if not p.startswith(f"{DATA}/")]

    old = snapshot(old_rev)
    new = snapshot(new_rev)
    diff = compare(old, new)

    touched = collections.defaultdict(set)
    for name, section, _ in list(diff["added"]) + list(diff["removed"]) + list(
        diff["retyped"]
    ):
        touched[name].add(section)
    for src, dst, _ in diff["moved"]:
        touched[src[0]].add(src[1])
        touched[dst[0]].add(dst[1])

    if not touched:
        if not non_data:
            return ""
        names = ", ".join(sorted(pathlib.Path(p).name for p in non_data)[:MAX_SCOPES])
        return f"fix: {names}"

    if diff["added"] and not (diff["removed"] or diff["retyped"]):
        verb = "add"
    elif diff["removed"] and not (diff["added"] or diff["retyped"]):
        verb = "del"
    else:
        verb = "fix"

    scopes = []
    for name in sorted(touched):
        sections = sorted(scope_label(s) for s in touched[name] if s)
        if not sections or len(sections) > MAX_SCOPES:
            scopes.append(name)
        else:
            scopes.append(f"{name}/{','.join(sections)}")
    if len(scopes) > MAX_SCOPES:
        names = sorted(touched)
        head = ", ".join(names[:MAX_SCOPES])
        return f"{verb}: {head} +{len(names) - MAX_SCOPES}"
    return f"{verb}: {' '.join(scopes)}"


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: changes.py changelog|subject [old] [new]")
    mode = sys.argv[1]
    old_rev = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    new_rev = sys.argv[3] if len(sys.argv) > 3 else None
    if mode == "changelog":
        print(changelog(old_rev, new_rev))
    elif mode == "subject":
        print(subject(old_rev, new_rev))
    else:
        raise SystemExit(f"unknown mode: {mode}")


if __name__ == "__main__":
    main()
