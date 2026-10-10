"""Publish a dated snapshot of ComparaPix's documented public quotes API."""
import json
import math
import pathlib
import urllib.request
import time
from datetime import datetime, timezone


def normalize(payload):
    if not isinstance(payload, dict):
        raise ValueError('Unexpected response')
    providers = []
    for name, item in payload.items():
        if not isinstance(item, dict) or item.get('isPix') is not True:
            continue
        quotes = []
        for quote in item.get('quotes', []):
            price = quote.get('buy')
            if quote.get('symbol') in ('BRLARS', 'BRLUSD', 'BRLUSDT') and isinstance(price, (int, float)) and not isinstance(price, bool) and math.isfinite(price) and price > 0:
                quotes.append({'symbol': quote['symbol'], 'buy': price})
        url = item.get('url', '')
        updated = item.get('updatedAt')
        if not quotes or not isinstance(url, str) or not url.startswith('https://') or not isinstance(updated, str):
            continue
        try:
            datetime.fromisoformat(updated.replace('Z', '+00:00'))
        except ValueError:
            continue
        providers.append({'id': name, 'quotes': quotes, 'url': url, 'hasFees': item.get('hasFees') is True, 'stale': item.get('stale') is True, 'updatedAt': updated})
    if not providers:
        raise ValueError('No valid PIX providers; preserve previous snapshot')
    return {'source': 'ComparaPix', 'fetchedAt': datetime.now(timezone.utc).isoformat(), 'providers': providers}


if __name__ == '__main__':
    request = urllib.request.Request('https://api.comparapix.ar/quotes', headers={'User-Agent': 'PraiaIdeal/1.0 (praiaideal.com)', 'Accept': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = normalize(json.load(response))
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    target = pathlib.Path(__file__).resolve().parents[1] / 'pix-quotes.json'
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(target)
