from typing import List, Optional

from .errors import Path, PathSegment, ValidationIssue


class ParseContext:
    __slots__ = ("issues", "path")

    def __init__(
        self,
        path: Path = (),
        issues: Optional[List[ValidationIssue]] = None,
    ) -> None:
        self.path = path
        self.issues = [] if issues is None else issues

    def child(self, segment: PathSegment) -> "ParseContext":
        return ParseContext((*self.path, segment), self.issues)

    def add_issue(
        self,
        code: str,
        message: str,
        expected: Optional[str] = None,
        received_type: Optional[str] = None,
    ) -> None:
        self.issues.append(
            ValidationIssue(
                path=self.path,
                code=code,
                message=message,
                expected=expected,
                received_type=received_type,
            )
        )
