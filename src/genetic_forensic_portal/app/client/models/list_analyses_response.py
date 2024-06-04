from __future__ import annotations


class ListAnalysesResponse:
    def __init__(
        self, analyses: list[str], start_token: int = 0, next_token: int | None = None
    ):
        self.analyses = analyses
        self.start_token = start_token
        self.next_token = next_token
