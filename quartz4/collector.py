# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Module 1: The Collector — live multi-threaded data ingestion.

Continuously ingests from concurrent API streams:
  - arXiv (science / pre-prints)
  - Alpha Vantage (finance)
  - NewsAPI (global events)

Normalises all data into ConceptEvent objects and funnels
them into the Labyrinth memory layer.  After each batch,
passes the top concepts to the Sentinel for hypothesis
detection.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime

import httpx

logger = logging.getLogger(__name__)


@dataclass
class ConceptEvent:
    id: str
    source: str
    title: str
    summary: str
    url: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: dict = field(default_factory=dict)


class Collector:
    """Multi-source async data collector."""

    ARXIV_URL = "https://export.arxiv.org/api/query"
    NEWS_URL = "https://newsapi.org/v2/top-headlines"

    def __init__(self, labyrinth, sentinel=None, poll_interval: int = 300):
        self.labyrinth = labyrinth
        self.sentinel = sentinel  # injected after Sentinel is constructed
        self.poll_interval = poll_interval
        self._tasks: list[asyncio.Task] = []
        self._running = False

    async def start(self):
        """Launch all collection loops concurrently."""
        self._running = True
        self._tasks = [
            asyncio.create_task(self._arxiv_loop()),
            asyncio.create_task(self._news_loop()),
        ]
        logger.info("Collector started — %d streams active", len(self._tasks))

    async def stop(self):
        """Gracefully cancel all collection tasks."""
        self._running = False
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        logger.info("Collector stopped")

    async def _after_batch(self) -> None:
        """Post-ingest hook: run Sentinel scan over current top concepts."""
        if self.sentinel is None:
            return
        try:
            concepts = await self.labyrinth.top_concepts(limit=50)
            alerts = await self.sentinel.scan(concepts)
            if alerts:
                logger.info("Sentinel: generated %d new alert(s)", len(alerts))
        except Exception as exc:  # pragma: no cover
            logger.warning("Sentinel scan failed: %s", exc)

    # ── arXiv ──────────────────────────────────────────────

    async def _arxiv_loop(self):
        while self._running:
            try:
                events = await self._fetch_arxiv()
                for event in events:
                    await self.labyrinth.ingest(event)
                logger.info("arXiv: ingested %d concepts", len(events))
                await self._after_batch()
            except Exception as exc:
                logger.warning("arXiv fetch failed: %s", exc)
            await asyncio.sleep(self.poll_interval)

    async def _fetch_arxiv(
        self,
        query: str = "all:artificial intelligence OR all:quantum computing OR all:neuroscience",
        max_results: int = 25,
    ) -> list[ConceptEvent]:
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(self.ARXIV_URL, params=params)
            resp.raise_for_status()

        events = []
        import re

        entries = re.findall(r"<entry>(.*?)</entry>", resp.text, re.DOTALL)
        for i, entry in enumerate(entries):
            title_match = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
            summary_match = re.search(r"<summary>(.*?)</summary>", entry, re.DOTALL)
            id_match = re.search(r"<id>(.*?)</id>", entry)
            if title_match and summary_match and id_match:
                events.append(
                    ConceptEvent(
                        id=f"arxiv-{i}-{hash(id_match.group(1))}",
                        source="arxiv",
                        title=title_match.group(1).strip(),
                        summary=summary_match.group(1).strip()[:500],
                        url=id_match.group(1).strip(),
                    )
                )
        return events

    # ── News ───────────────────────────────────────────────

    async def _news_loop(self):
        while self._running:
            try:
                events = await self._fetch_news()
                for event in events:
                    await self.labyrinth.ingest(event)
                logger.info("News: ingested %d articles", len(events))
                await self._after_batch()
            except Exception as exc:
                logger.warning("News fetch failed: %s", exc)
            await asyncio.sleep(self.poll_interval)

    async def _fetch_news(
        self,
        category: str = "technology",
        page_size: int = 20,
    ) -> list[ConceptEvent]:
        import os

        api_key = os.getenv("NEWS_API_KEY", "")
        if not api_key:
            return []
        params = {"category": category, "pageSize": page_size, "apiKey": api_key}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(self.NEWS_URL, params=params)
            resp.raise_for_status()
        articles = resp.json().get("articles", [])
        return [
            ConceptEvent(
                id=f"news-{hash(a.get('url', str(i)))}",
                source="news",
                title=a.get("title", ""),
                summary=a.get("description", "")[:500],
                url=a.get("url", ""),
            )
            for i, a in enumerate(articles)
            if a.get("title")
        ]
