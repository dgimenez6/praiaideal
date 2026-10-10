"""Cache public astronomical tide tables; refresh at most once per day."""
import calendar
import json
import pathlib
import urllib.request
from datetime import datetime, timedelta, timezone

target = pathlib.Path(__file__).resolve().parents[1] / 'tide-data.json'
now = datetime.now(timezone(timedelta(hours=-3)))
if target.exists():
    old = json.loads(target.read_text())
    age = now - datetime.fromisoformat(old['fetchedAt'])
    if timedelta(0) <= age < timedelta(hours=24):
        raise SystemExit(0)
months = [(now.year, now.month)]
if now.day == 1:
    previous = now.replace(day=1) - timedelta(days=1)
    months.insert(0, (previous.year, previous.month))
if now.day >= calendar.monthrange(now.year, now.month)[1] - 1:
    following = now.replace(day=28) + timedelta(days=4)
    months.append((following.year, following.month))
tables = []
for year, month in months:
    # The provider currently supports the current year only.
    if year != now.year:
        continue
    days = calendar.monthrange(year, month)[1]
    url = f'https://tabuamare.api.br/api/v2/geo-tabua-mare/%5B-22.76%2C-41.88%5D/rj/{month}/%5B1-{days}%5D'
    request = urllib.request.Request(url, headers={'User-Agent': 'PraiaIdeal/1.0 (praiaideal.com)'})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response).get('data')
    if not isinstance(data, list) or not data:
        raise ValueError('Missing tide table; retain previous file')
    tables.extend(data)
payload = {'fetchedAt': now.isoformat(), 'data': tables}
temporary = target.with_suffix('.tmp')
temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
temporary.replace(target)
