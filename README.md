<<<<<<< HEAD
# lv-trainer-monitor
=======
# Sneaker Monitor — LV Trainer

Polls Rakuten Ichiba and 2nd STREET Online Store for new listings matching
configured keywords (default: Louis Vuitton Trainer) and posts new hits to a
Discord webhook.

## Layout

```
sneaker-monitor/
├── main.py               # Polling loop / orchestration
├── scraper_rakuten.py    # Rakuten search scraper
├── scraper_2ndstreet.py  # 2nd STREET search scraper
├── notifier.py           # Discord webhook
├── storage.py            # Persistent JSON store of seen URLs
├── utils.py              # HTTP session, retries, logging
├── config.py             # Env-driven config + KEYWORDS list
├── requirements.txt
├── render.yaml           # Render.com blueprint (worker + disk)
└── .env.example
```

## Local run

```bash
cd sneaker-monitor
cp .env.example .env       # fill in DISCORD_WEBHOOK_URL
pip install -r requirements.txt
python main.py
```

The first cycle silently seeds `seen.json` so you don't get spammed by the
existing backlog. New listings appearing afterwards will be posted to Discord.

## Deploy to Render

1. Push this repo to GitHub.
2. In Render, **New → Blueprint** and select the repo.
3. Render reads `sneaker-monitor/render.yaml` and provisions a worker + 1 GB disk.
4. Set `DISCORD_WEBHOOK_URL` in the dashboard (it is marked `sync: false`).
5. Deploy. Logs are visible from the Render dashboard.

The persistent disk is mounted at `/var/data`, where `seen.json` lives, so
notification dedup state survives restarts and redeploys.

## Adding keywords / sites

- **Keywords**: edit `KEYWORDS` in `config.py`.
- **New site**: create `scraper_<site>.py` exposing `search(session, keywords) -> list[dict]`
  returning items shaped like `{"site","title","price","url"}`, then add it to
  `SCRAPERS` in `main.py`.
- **HTML changed**: update the `SELECTORS` dict at the top of the relevant
  scraper module — that's the only place you should need to touch.
>>>>>>> ced963f (initial commit)
