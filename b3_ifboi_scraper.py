"""Download IFBOI index file from B3 and print last day's quote.

The script fetches the 'Indices on Demand' page from B3, locates the link
for the IFBOI Excel file, downloads it and extracts the last row from the
worksheet. Only Python's standard library is used so it can run in minimal
environments.
"""

import re
import xml.etree.ElementTree as ET
from io import BytesIO
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from zipfile import ZipFile

B3_URL = "https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-on-demand/"
# Regex pattern to find the IFBOI Excel link (usually ends with .xls or .xlsx)
IFBOI_PATTERN = re.compile(r'href="([^"]*IFBOI[^"\']*\.(?:xlsx|xls))"', re.I)


def fetch_ifboi_url() -> str:
    """Return the absolute URL to the IFBOI Excel file."""
    req = Request(B3_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req) as resp:
        html = resp.read().decode("utf-8", "ignore")
    match = IFBOI_PATTERN.search(html)
    if not match:
        raise RuntimeError("IFBOI link not found on B3 page")
    href = match.group(1)
    return urljoin(B3_URL, href)


def download_bytes(url: str) -> bytes:
    """Download the file at *url* and return its content."""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req) as resp:
        return resp.read()


def parse_xlsx_last_row(data: bytes) -> dict:
    """Parse an XLSX file and return a dict mapping headers to the last row."""
    with ZipFile(BytesIO(data)) as zf:
        # read shared strings if present
        shared = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            ns = {"t": "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"}
            for si in root.findall(".//t:t", ns):
                shared.append(si.text or "")
        # assume first worksheet
        sheets = [n for n in zf.namelist() if n.startswith("xl/worksheets/")]
        if not sheets:
            raise RuntimeError("No worksheets found in Excel file")
        sheet_data = zf.read(sheets[0])

    root = ET.fromstring(sheet_data)
    ns = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rows = []
    for row in root.findall(".//main:sheetData/main:row", ns):
        cells = []
        for c in row.findall("main:c", ns):
            value = ""
            t = c.get("t")
            v = c.find("main:v", ns)
            if v is not None:
                value = v.text or ""
                if t == "s":
                    idx = int(value)
                    value = shared[idx] if idx < len(shared) else ""
            cells.append(value)
        rows.append(cells)
    if not rows:
        return {}
    header, *data_rows = rows
    # pick the last non-empty row
    for row in reversed(data_rows):
        if any(cell.strip() for cell in row):
            return dict(zip(header, row))
    return {}


def main():
    try:
        url = fetch_ifboi_url()
        xls_bytes = download_bytes(url)
        last = parse_xlsx_last_row(xls_bytes)
    except Exception as exc:
        print(f"Erro ao processar dados: {exc}")
        return

    if not last:
        print("Nenhum dado encontrado")
        return

    ordered_keys = [
        "Data_Referencia",
        "Indice",
        "Oscilacao",
        "Nome_Resumido",
        "Codigo_ISIN",
        "Ultima_Atualizacao",
    ]
    values = [last.get(k, "") for k in ordered_keys]
    print(";".join(values))


if __name__ == "__main__":
    main()
