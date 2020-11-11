from dataclasses import dataclass

@dataclass
class NumberNode:
  value: float

@dataclass
class OperatorNode:
  left: any
  right: any
  operator: any

