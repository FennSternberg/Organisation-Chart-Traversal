"""
Inspiration from https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
"""
from typing import Iterable
from .organization import Organization


def ascii_forest(org: Organization) -> Iterable[str]:
    """Yield a clean ASCII tree for each root in the org.

    Example:
    Root
    ├── Child A
    │   └── Grandchild
    └── Child B
    """
    for root in org.roots():
        yield org.format_label(root)
        yield from _ascii_subtree(org, root, prefix="")


def _ascii_subtree(org: Organization, eid: int, prefix: str) -> Iterable[str]:
    children = org.get_children(eid)
    if not children:
        return
    last_index = len(children) - 1
    for i, child in enumerate(children):
        connector = "└── " if i == last_index else "├── "
        yield f"{prefix}{connector}{org.format_label(child)}"
        continuation = "    " if i == last_index else "│   "
        # Recurse with extended prefix that keeps vertical bars for following siblings
        yield from _ascii_subtree(org, child, prefix + continuation)