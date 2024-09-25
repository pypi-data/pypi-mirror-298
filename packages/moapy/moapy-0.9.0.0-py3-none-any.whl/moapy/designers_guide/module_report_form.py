from dataclasses import dataclass

@dataclass
class ReportForm:
    standard: str = 'Standard',
    reference: str = '',
    title: str = 'Title',
    description: str = 'Description',
    symbol: str = 'Symbol',
    formula: list = [],
    result: float = 0.0,
    unit: str = 'Unit'

    def __repr__(self) -> str:
        full_formula = ""
        full_formula += f"{self.symbol}"
        for curr_formula in self.formula if self.formula else []:
            full_formula += " = " + f"{curr_formula}"
        full_formula += " = " + f"{self.result}" + f" {self.unit}"
                
        return (
            f"[{self.standard} {self.reference}] "
            f"{self.title}\n"
            f"{self.description}\n"
            f"{full_formula}"
        )