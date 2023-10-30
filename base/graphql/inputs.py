from uuid import UUID

import strawberry

@strawberry.input
class PaginationInput:
    page: int | None = None
    page_size: int | None = None
