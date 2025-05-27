def paginate(
    data: list, page: int = 1, page_size: int = 10, **kwargs: dict
) -> list[dict]:
    """Gets records from the table that matches the filters.

    Args:
        page: page number
        page_size: number of records per page

    Returns: a list of orders
    """

    offset = calc_offset(page, page_size)
    return data[offset : page * page_size]


def calc_offset(page: int, page_size: int) -> int:
    """Calcules offset given a page and page_size"""
    if page < 1 or page_size < 1:
        raise ValueError("Page and page_size must be greater than 0")
    return page_size * (page - 1)
