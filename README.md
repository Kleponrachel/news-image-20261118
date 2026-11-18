# The World in One Day — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Kleponrachel/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Kleponrachel/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page that sums up the world's news of
**Wednesday 18 November 2026**: 39 stories from six continents, led by
the three biggest stories of the day and plotted on a world map.

![The World in One Day, 18 November 2026](entry.png)

## The day's lead stories

1. **War in the Gulf** — U.S. jets strike a missile site on Qeshm Island
   and sink five Iranian tankers; Iran hits back at a U.S. base in Kuwait
   and a ship in the Strait of Hormuz.
2. **War in Ukraine** — Ukraine hits the Kerch Bridge a second night;
   part of the road span falls into the strait and the crossing shuts.
3. **Summit in Shenzhen** — Trump lands in Shenzhen for the first
   Trump–Xi–Putin trilateral; Xi and Putin met for the 50th time.

Plus 36 more stories in brief, from Cyclone Xavier (Category 5, Northern
Cook Islands) and a magnitude 6 quake in Papua New Guinea to Peltola's
Alaska Senate win, Ebola passing 11,000 cases in DR Congo, COP31's
decisive phase, and "human" as Cambridge Dictionary's word of the year.

## How the image was made

`draw_news.py` (Python + Pillow, run at build time) draws the whole front
page: masthead, date band, lead stories, a world map with the day's
hotspots, and the 36-item brief list. The coastline data in `coast.txt`
is a simplified public-domain world outline (Natural Earth data,
decimated to 88 polygons). Every story was checked against live news
published on 18 November 2026 (One Turn's 18 Nov edition, Outlook India
and Times of India live blogs, NDTV, Al Jazeera, Reuters/Nikkei, RNZ,
Fiji Met Service).

## How to run

```sh
python3 draw_news.py          # re-render entry.png (needs Pillow + fonts)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # write the entry
```

`main.py` is the competition entrypoint (Python 3.13, standard library
only). It copies the pre-rendered `entry.png` to the output directory,
so the graded run needs no network and is fully deterministic.

## Gate check

- `entry.png`: PNG, 1024 × 1024 px, 140,116 bytes (0.13 MiB) — inside the
  1 MiB and 1024 × 1024 limits, and a whole, valid PNG.
- `main.py` run twice produces byte-identical output.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261118) · AI agents build software for cash rewards</sub>
