# krizky-json

Plugin pro JSON export do [krizky](https://github.com/your-org/krizky) generátoru statických webů.

Generuje JSON soubor vedle každé HTML stránky, která má v page configu sekci `json:`. Hodí se pro zpřístupnění strukturovaných dat JavaScriptovému frontendu, mobilním aplikacím nebo jiným konzumentům bez potřeby samostatného API.

## Instalace

```bash
pip install krizky-json
```

## Použití

Přidej klíč `json:` k libovolné stránce v `config.yaml`:

```yaml
pages:
  vsechna_mista:
    path: /mista.html
    template: mista.html
    json:
      fields: [slug, nazev, latitude, longitude]
      exclude: [interni_poznamka]
      pretty: true
```

Spusť `krizky build site` jako obvykle. Pro každou stránku s nastaveným `json:` vznikne JSON soubor vedle HTML výstupu:

```
docs/
├── mista.html
├── mista-2.html        ← stránkování: více HTML souborů
└── jsons/
    └── mista.json      ← JSON: všechny záznamy v jednom souboru (stránkování ignorováno)
```

### Chování dle typu stránky

| Typ stránky | JSON výstup |
|-------------|-------------|
| Jednoduchá / query | Jeden JSON array na definici stránky — všechny záznamy, stránkování ignorováno |
| Category | Jeden JSON array na hodnotu kategorie |
| Detail | Jeden JSON objekt na záznam |

### Volby konfigurace

| Klíč | Typ | Výchozí | Popis |
|------|-----|---------|-------|
| `fields` | list nebo `"*"` | `"*"` | Whitelist exportovaných polí. Použij `"*"` pro všechna pole. |
| `exclude` | list | `[]` | Pole, která se vynechají. Lze kombinovat s `fields: "*"`. |
| `pretty` | bool | `false` | Odsadí výstup 2 mezerami. |

## Výstupní cesta

JSON soubory zrcadlí cestu HTML souboru ve složce `jsons/` uvnitř výstupního adresáře:

| HTML cesta | JSON cesta |
|------------|------------|
| `/mista.html` | `<output>/jsons/mista.json` |
| `/priroda.html` | `<output>/jsons/priroda.json` |
| `/kamen-u-lesa.html` | `<output>/jsons/kamen-u-lesa.json` |

## Požadavky

- Python 3.12+
- krizky >= 0.1
