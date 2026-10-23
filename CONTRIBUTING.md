# Contributing

Thanks for writing a plugin! The full guide is in [docs/publishing.md](docs/publishing.md); the
short version:

1. Fork, then add `plugins/<your plugin id>/` with `plugin.json` and your JavaScript.
2. Add the plugin to `marketplace.json`, then run `python3 scripts/validate.py --update-hashes`
   and `python3 scripts/validate.py`.
3. Try it in NtfyBar from a local folder.
4. Open a pull request — one plugin (or one update) per PR. `main` is protected: CI must pass and
   a maintainer reviews every change before it is squash-merged.

What gets accepted, and what doesn't, is listed under
[Review rules](docs/publishing.md#review-rules). In short: fewest permissions with honest
reasons, readable code, no tricks.

Writing plugins: [docs/authoring.md](docs/authoring.md) · [docs/permissions.md](docs/permissions.md) ·
[docs/popup-spec.md](docs/popup-spec.md)

By contributing you agree your plugin is published under this repository's MIT license, and you
follow the [Code of Conduct](CODE_OF_CONDUCT.md).
