# Contributing

Thanks for helping. This list only works if it is accurate, so each change needs a little evidence.

## Adding a domain

1. Check that the service is in scope (see below).
2. Add the domain to `src/domains.txt`. Use lowercase, one domain per line, in alphabetical order.
   You can add a short note with `#` if the reason isn't obvious:
   ```
   example-chat.ai  # API backend for the ExampleChat Android app
   ```
3. Run `python3 scripts/build.py --check`, or `--fix` to sort the list for you. The script only needs Python 3.
4. Open a pull request. **Don't commit changes to `dist/`**: CI rebuilds it after the merge.

In the PR, explain **what the service is** and **how you know the domain belongs to it** (for example a link,
an app store listing, or a screenshot of the Pi-hole query log while using the app).

### In scope

**The rule:** if a service can be used to roleplay with an AI character without content filtering,
or with filters that are easy to get around, it belongs on the list. This includes:

- Services whose **primary purpose** is AI character creation, character chat or roleplay
- General or multi-model chat services that let users create characters or personas and chat with them uncensored
- Hosted "uncensored" or "unfiltered" model chat sites
- AI companion, girlfriend or boyfriend apps
- Domains a service needs to work: API, CDN or websocket hosts owned by the service
- Character-card sharing hubs and self-hosted roleplay frontends with a hosted web version

### Out of scope

- Mainstream assistants with enforced content policies (ChatGPT, Claude, Gemini, Copilot, Perplexity, and so on).
  A mainstream assistant is added only if it offers an unfiltered character or roleplay mode.
- Shared or third-party infrastructure: `cloudfront.net`, `firebaseio.com`, `googleapis.com`, analytics providers, and similar
- Individual pages or paths. DNS blocking works on whole domains only.
- Wildcards and regex. List the specific subdomain, or rely on the adblock format, which covers subdomains.

## Removing a domain

Open a **Remove a domain** issue or a PR if a domain:

- is a false positive (it isn't an AI character or roleplay service)
- has expired, is parked, or has been taken over by an unrelated business
- is shared infrastructure that breaks other things

If a domain must never be re-added, put it in `src/allowlist.txt`. The build fails if a domain appears in both files.

## Dead domains

A scheduled workflow checks every week for domains that no longer resolve and posts a report in the Actions tab.
A domain that doesn't resolve is **not removed automatically**: it may be down temporarily, geo-restricted, or used only
inside an app. Maintainers check it before removing it.

## Review

Pull requests need approval from a maintainer (see `.github/CODEOWNERS`). Please be patient and be kind. See the
[Code of Conduct](CODE_OF_CONDUCT.md).
