import re
from urllib.request import urlopen


def strip_tags(text: str) -> str:
    """Remove HTML tags and leading/trailing whitespace."""
    return re.sub(r"<[^>]+>", "", text).strip()


def fetch_fundamentals(papel: str) -> dict:
    """Fetch basic fundamentals from fundamentus.com.br for a given ticker.

    The returned dictionary contains textual values for:
    Papel, Cotacao, Data ult cot, Min 52 sem, Max 52 sem, P/L, LPA and VPA.
    """
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={papel}"
    with urlopen(url) as resp:
        html = resp.read().decode("latin1")

    # generic regex for <td>label</td><td>value</td>
    pattern = re.compile(r"<td[^>]*>\s*([^<]*?)\s*</td>\s*<td[^>]*>(.*?)</td>", re.S)

    data = {}
    labels = {
        "Papel": "Papel",
        "Cotação": "Cotacao",
        "Data últ cot": "Data ult cot",
        "Min 52 sem": "Min 52 sem",
        "Max 52 sem": "Max 52 sem",
        "P/L": "P/L",
        "LPA": "LPA",
        "VPA": "VPA",
    }

    for label, value in pattern.findall(html):
        clean_label = strip_tags(label)
        clean_value = strip_tags(value)
        if clean_label in labels:
            data[labels[clean_label]] = clean_value

    return data


def main():
    papel = "BBDC4"
    try:
        data = fetch_fundamentals(papel)
    except Exception as exc:
        print(f"Erro ao buscar dados: {exc}")
        return

    ordered_keys = [
        "Papel",
        "Cotacao",
        "Data ult cot",
        "Min 52 sem",
        "Max 52 sem",
        "P/L",
        "LPA",
        "VPA",
    ]

    values = [data.get(k, "") for k in ordered_keys]
    print(";".join(values))


if __name__ == "__main__":
    main()
