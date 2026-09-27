# Pi-hole Dangerous NSFW Blocklists

Community-maintained blocklists for online services that are commonly used for dangerous or exploitative sexual
content, even when they advertise safety filters. They're built for Pi-hole, but work with most DNS and ad blockers.

## The lists

| List | What it blocks |
| --- | --- |
| **aicharacter** | AI character, roleplay and "AI companion" services that can be used uncensored (Character.AI, JanitorAI, Chai, Talkie, Replika…) |
| **anonvideochat** | Omegle-style random video chat that pairs you with strangers (OmeTV, Chatroulette, Monkey, Uhmegle…) |

## Using the lists

Each list comes in three formats. Use **adblock** on Pi-hole v6, because it also blocks subdomains.

| List | Adblock (Pi-hole v6, AdGuard Home, uBO) | Domains (Pi-hole v5) | Hosts |
| --- | --- | --- | --- |
| aicharacter | `https://raw.githubusercontent.com/Vulps22/pihole-block-dangerous-nsfw/main/dist/aicharacter.txt` | `https://raw.githubusercontent.com/Vulps22/pihole-block-dangerous-nsfw/main/dist/domains/aicharacter.txt` | `https://raw.githubusercontent.com/Vulps22/pihole-block-dangerous-nsfw/main/dist/hosts/aicharacter.txt` |
| anonvideochat | `https://raw.githubusercontent.com/Vulps22/pihole-block-dangerous-nsfw/main/dist/anonvideochat.txt` | `https://raw.githubusercontent.com/Vulps22/pihole-block-dangerous-nsfw/main/dist/domains/anonvideochat.txt` | `https://raw.githubusercontent.com/Vulps22/pihole-block-dangerous-nsfw/main/dist/hosts/anonvideochat.txt` |

**Pi-hole:** Go to *Lists* (or *Adlists* on v5), paste the URL, add it, then update gravity (*Tools → Update Gravity*, or `pihole -g`).

## What belongs on each list

**aicharacter.** The rule: *if a service can be used to roleplay with an AI character uncensored, or with filters that are easy to get around, it belongs.*
This covers character chat platforms, AI girlfriend/boyfriend/companion apps, character-card hubs, hosted "uncensored" model chat,
and the API or CDN domains these services use. Mainstream assistants with enforced content policies (ChatGPT, Claude, Gemini, Copilot) are left off.

**anonvideochat.** The rule: *if a service pairs users with random strangers over live video or webcam, it belongs.* This covers Omegle clones,
"roulette" sites and random video chat apps. Video calling with people you already know (FaceTime, Zoom, Discord) is left off.

Neither list includes shared infrastructure (CDNs, cloud providers, analytics). See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Contributing

- **Suggest a domain:** open an [issue](../../issues/new/choose), or a pull request that edits the right file in `src/`
- **Report a false positive:** open a removal issue

Only `src/` is edited by hand. `dist/` is rebuilt automatically when changes are merged.

## Repository layout

```
src/<list>.txt        source lists, edited by contributors
src/allowlist.txt     domains that must never be blocked (applies to all lists)
dist/<list>.txt       generated adblock-format lists (do not edit)
dist/domains/         generated plain-domain lists
dist/hosts/           generated hosts-file lists
scripts/build.py      validates src/ and builds dist/ (new lists are registered in LISTS here)
scripts/check_dead.py reports domains that no longer resolve
```

## License

[MIT](LICENSE)
