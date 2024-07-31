from __future__ import annotations


class ListAnalysesResponse:
    """The model for the response from the genetic forensic portal API when listing analyses.

    Attributes:
    - `analyses`: The list of analyses that were retrieved.
    - `start_token`: The token that was used to get this page of results.
    - `next_token`: The token to use to get the next page of results.
    """

    def __init__(
        self, analyses: list[str], start_token: int = 0, next_token: int | None = None
    ):
        self.analyses = analyses
        self.start_token = start_token
        self.next_token = next_token
