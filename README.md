# Investra
Investra will be an AI-powered platform that analyzes markets, predicts trends, and optimizes investment decisions in real time.

## Fundamentus scraper

This repository contains a small utility named `fundamentus_scraper.py` that
collects some basic indicators from
[`fundamentus.com.br`](https://www.fundamentus.com.br/). The script fetches the
data for a specific ticker (by default `BBDC4`) and prints the values separated
by semicolons.

### Running

```bash
python fundamentus_scraper.py
```

The result will look similar to:

```
BBDC4;12.34;08/07/2024;10.50;14.80;8.50;1.20;2.50
```

The script relies only on the Python standard library. It requires internet
access to retrieve the HTML page from fundamentus.com.br.

## IFBOI index fetcher

`b3_ifboi_scraper.py` downloads the IFBOI index spreadsheet from B3's
"Índices on Demand" page and prints the latest available quotation. It also
uses only the Python standard library.

### Running

```bash
python b3_ifboi_scraper.py
```

The output contains the columns:
`Data_Referencia;Indice;Oscilacao;Nome_Resumido;Codigo_ISIN;Ultima_Atualizacao`.
