# Minimal shim for removed cgi module
from urllib.parse import parse_qs

def parse_header(line):
    parts = line.split(";")
    key = parts[0].strip().lower()
    pdict = {}
    for part in parts[1:]:
        if "=" in part:
            k, v = part.strip().split("=", 1)
            pdict[k.lower()] = v
    return key, pdict
