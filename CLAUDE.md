# krizky-json

Plugin pro [krizky](https://github.com/msgre/krizky), statický generátor webů. Vedle každé HTML stránky, která má v page configu sekci `json:`, vygeneruje JSON soubor do `<output>/jsons/`. Kód je v `krizky_json/plugin.py`, testy v `tests/`. Lokální checkout core je v `/Users/msgre/projects/muzeum/krizky`.

## Ověření: jediná brána „hotovo“

```bash
scripts/verify
```

Skript spustí `uv sync`, `ruff check`, `ruff format --check` a `pytest`. Na obrazovku vypíše jen souhrn, celé výstupy jsou v `.verify-logs/`. Hotovo je až tehdy, když skončí s exit 0. Pokud selže, oprav příčinu. Pravidla v `pyproject.toml` ani v samotném skriptu kvůli tomu neměň.

Opravy lintu a formátu: `uv run ruff check --fix .`, `uv run ruff format .`.

## Pravidla projektu

Guidelines jsou společné pro core i všechny pluginy a leží v `/Users/msgre/projects/muzeum/krizky/docs/guidelines/`. Před změnou si přečti ty, které se jí týkají:

- `python.md`: styl, logging, testy. `from __future__ import annotations` je zakázaný, hlídá to ruff (TID251).
- `docs-sync.md`: když se změní chování nebo konfigurace, aktualizuj i `README.md`.
- `security.md`

## Git

- Do `main` nikdy necommituj ani nepushuj. Práce jde přes větve `swarm/<heslo>` a PR.
- Commity jsou česky, s volitelným prefixem `feat:`, `fix:` nebo `refactor:`.

## Swarm

- Log běhu: `/Users/msgre/projects/muzeum/krizky/work/<YYYY-MM-DD>-<NN>-<heslo>.md`. `NN` začíná každý den od `01` (podívej se, co už v adresáři je).
- Po zapsání logu přidej řádek do tabulky „Stav fází“ v `/Users/msgre/projects/muzeum/krizky/work/OVERVIEW.md` se stavem a odkazem na log.
- Do core repa nic necommituj. Logy a `OVERVIEW.md` tam spravuje uživatel.
