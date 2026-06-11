from typing import List, Optional

from .errors import Path, PathSegment, ValidationIssue


class ParseContext:
    __slots__ = ("causes", "issues", "path")

    def __init__(
        self,
        path: Path = (),
        issues: Optional[List[ValidationIssue]] = None,
        causes: Optional[List[BaseException]] = None,
    ) -> None:
        self.path = path
        self.issues = [] if issues is None else issues
        self.causes = [] if causes is None else causes

    def child(self, segment: PathSegment) -> "ParseContext":
        return ParseContext((*self.path, segment), self.issues, self.causes)

    def add_issue(
        self,
        code: str,
        message: str,
        expected: Optional[str] = None,
        received_type: Optional[str] = None,
        branch_issues: tuple[tuple[ValidationIssue, ...], ...] = (),
    ) -> None:
        self.issues.append(
            ValidationIssue(
                path=self.path,
                code=code,
                message=message,
                expected=expected,
                received_type=received_type,
                branch_issues=branch_issues,
            )
        )

    def record_cause(self, error: BaseException) -> None:
        if not self.causes:
            self.causes.append(error)
