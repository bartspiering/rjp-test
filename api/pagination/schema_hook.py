pagination_schema_hook = lambda current_page, page_obj: {
    "current_page": current_page,
    "has_next": page_obj.has_next,
    "has_prev": page_obj.has_prev,
    "next": page_obj.next if isinstance(page_obj.next, str) else None,
    "pages": page_obj.pages,
    "size": page_obj.per_page,
    "total": page_obj.total,
}
