# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Module 7: The Oracle — Natural Language Query Interface.

Allows complex natural language questions over the system's
entire historical memory:
  'Trace the decline of Proof-of-Work since 2023'
  'Show gravitational impact of GPT-4 on adjacent AI concepts'

Combines Labyrinth similarity search with Crucible deep analysis.
"""

import logging

logger = logging.getLogger(__name__)


class Oracle:
    """Natural language memory query interface."""

    def __init__(self, labyrinth, crucible):
        self.labyrinth = labyrinth
        self.crucible = crucible

    async def answer(self, question: str) -> str:
        """Answer a natural language question about the knowledge base.

        Flow:
          1. Embed the question via Crucible
          2. Retrieve top-k similar concepts from Labyrinth
          3. Run deep analysis via Crucible with retrieved context
          4. Return synthesised answer
        """
        if not question.strip():
            return "Please ask a question."

        logger.info("Oracle: answering '%s'", question[:80])

        # Step 1: embed question
        query_embedding = await self.crucible._embed(question)

        # Step 2: retrieve relevant concepts
        context = await self.labyrinth.search(query_embedding, top_k=12)

        # Step 3: deep analysis
        answer = await self.crucible.analyse(question=question, context=context)

        return answer
