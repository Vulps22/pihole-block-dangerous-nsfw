# Pi-hole AI Character / Roleplay Blocklist

A community-maintained blocklist for **AI character creation, roleplay and "AI companion" services**,
such as Character.AI, Chai, JanitorAI, Talkie, Replika and similar.

Many of these services allow, or can easily be pushed into, sexual roleplay despite their safety filters, and
some are advertised as "limitless". This list is for parents, schools and anyone else who wants to block this
category on their network.

## Using the list

Pick the format that suits your blocker:

| Format | URL | Works with |
| --- | --- | --- |
| Domains | `https://raw.githubusercontent.com/Vulps22/pihole-block-ai-character-rp/main/dist/domains.txt` | Pi-hole v5/v6, Technitium, most DNS blockers (exact match) |
| Adblock | `https://raw.githubusercontent.com/Vulps22/pihole-block-ai-character-rp/main/dist/adblock.txt` | Pi-hole v6, AdGuard Home, uBlock Origin (**also blocks subdomains**) |
| Hosts | `https://raw.githubusercontent.com/Vulps22/pihole-block-ai-character-rp/main/dist/hosts.txt` | Anything that reads a hosts file |

**Pi-hole:** Go to *Lists* (or *Adlists* on v5), paste the URL, add it, then run `pihole -g` or update gravity from the web UI.
On Pi-hole v6, use **adblock.txt** so subdomains are blocked too.

## What belongs on this list

**The rule:** if a service can be used to roleplay with an AI character uncensored, it belongs on this list.

In scope:

- Platforms where the main purpose is creating or chatting with AI characters or personas (e.g. `character.ai`, `janitorai.com`)
- AI girlfriend, boyfriend and companion apps (e.g. `replika.com`, `candy.ai`)
- The API, CDN and app backend domains these services need to work
- Character-card hubs and roleplay frontends (e.g. `chub.ai`)

Out of scope:

- Mainstream assistants with enforced content policies (ChatGPT, Claude, Gemini, Copilot). Use a separate "AI" list if you want to block those.
- Shared infrastructure such as CDNs or cloud providers that would break unrelated sites

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full criteria.

## Contributing

- **Suggest a domain:** open an [issue](../../issues/new/choose) or a pull request that edits `src/domains.txt`
- **Report a false positive:** open a removal issue

Only `src/` is edited by hand. `dist/` is rebuilt automatically when changes are merged.

## Repository layout

```
src/domains.txt       the source list, edited by contributors
src/allowlist.txt     domains that must never be blocked
dist/                 generated lists (do not edit)
scripts/build.py      validates src/ and builds dist/
scripts/check_dead.py reports domains that no longer resolve
```

## License

[MIT](LICENSE)
