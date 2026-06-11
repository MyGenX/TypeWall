from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple, Union

PathSegment = Union[str, int]
Path = Tuple[PathSegment, ...]
ROOT_PATH = "$"


def format_path(path: Path) -> str:
    if not path:
        return ROOT_PATH
    return ".".join(str(segment) for segment in path)


@dataclass(frozen=True)
class ValidationIssue:
    path: Path
    code: str
    message: str
    expected: Optional[str] = None
    received_type: Optional[str] = None
    branch_issues: Tuple[Tuple["ValidationIssue", ...], ...] = ()


def issues_to_dict(issues: Iterable[ValidationIssue]) -> Dict[str, List[str]]:
    grouped: Dict[str, List[str]] = {}
    for issue in issues:
        grouped.setdefault(format_path(issue.path), []).append(issue.message)
    return grouped


class ValidationError(ValueError):
    def __init__(self, issues: Iterable[ValidationIssue]) -> None:
        self.issues = tuple(issues)
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        count = len(self.issues)
        noun = "issue" if count == 1 else "issues"
        details = "; ".join(
            f"{format_path(issue.path)}: {issue.message}" for issue in self.issues
        )
        return f"Validation failed with {count} {noun}: {details}"

    def to_dict(self) -> Dict[str, List[str]]:
        return issues_to_dict(self.issues)
