from dataclasses import asdict, dataclass


def is_present(value: object) -> bool:
    """Considera um valor como presente quando não é None nem string vazia."""
    return value is not None and value != ""


@dataclass
class Customer:
    name: str
    phone: str
    _id: str | None = None


@dataclass
class CreateCustomerResult:
    message: str
    id: str


@dataclass
class CustomerQuery:
    _id: str | None = None
    name: str | None = None
    phone: str | None = None

    def to_dict(self) -> dict:
        """Campos presentes, incluindo o _id."""
        return {k: v for k, v in asdict(self).items() if is_present(v)}

    @property
    def filters(self) -> dict[str, str]:
        """Campos presentes que servem de filtro, ignorando o _id."""
        return {k: v for k, v in self.to_dict().items() if k != "_id"}
