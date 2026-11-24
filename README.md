# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b26-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b26-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page front page summing up **23 November 2026** in 31 stories: the AI rout that hit Asian markets (Kospi −3.3%), Guterres' call to regulate AI before it's too late, and the US lead over China falling to a record low — plus 10 more stories, a world map with 13 pins, and 18 more in "ALSO ON MONDAY".

- `draw.py` — renders `entry.png` (1024×1024) with PIL.
- `main.py` — stdlib-only; copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` after checking the PNG header (1024×1024, ≤1 MiB, well-formed IEND).
- `entry.png` — the finished front page.

Run: `python3 draw.py`, then `MAKEFUN_OUTPUT_DIR=out python3 main.py`.
