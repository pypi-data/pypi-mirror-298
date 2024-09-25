import sympy as sp
from pydantic import BaseModel
from typing import Dict
from fastapi import FastAPI

# Step 1: Define the symbols and the expression
def define_symbols(input_symbols: Dict[str, str], expression: str):
    # Create sympy symbols based on the input
    symbols = {name: sp.symbols(name) for name in input_symbols.keys()}
    expr = sp.sympify(expression)
    return symbols, expr

# Step 2: Evaluate the expression using the symbols
def evaluate_expression(symbols: Dict[str, sp.Symbol], expr):
    return expr.subs(symbols)

# Step 3: Create OpenAPI schema for the input and output symbols
def create_openapi_schema(input_symbols: Dict[str, str], response_symbol: str):
    app = FastAPI()

    # Define the Pydantic model for OpenAPI schema
    class InputModel(BaseModel):
        __annotations__ = {name: float for name in input_symbols.keys()}
    
    class OutputModel(BaseModel):
        __annotations__ = {response_symbol: float}
    
    @app.post("/calculate", response_model=OutputModel)
    async def calculate(input: InputModel):
        # 가정된 계산 로직
        result_value = sum([getattr(input, key) for key in input_symbols.keys()])
        return {response_symbol: result_value}
    
    # FastAPI OpenAPI 스펙을 생성하고 반환
    openapi_schema = app.openapi()
    return openapi_schema

# Example usage:
input_symbols = {"Fy": "float", "Aw": "float"}
expression = "Fy * Aw"
response_symbol = "Result"

# Define the symbols and expression
symbols, expr = define_symbols(input_symbols, expression)

# Example substitution values
substitution_values = {"Fy": 250, "Aw": 300}

# Evaluate the expression
result = evaluate_expression(substitution_values, expr)

# Generate OpenAPI schema for input and output
openapi_schema = create_openapi_schema(input_symbols, response_symbol)

print(openapi_schema);
