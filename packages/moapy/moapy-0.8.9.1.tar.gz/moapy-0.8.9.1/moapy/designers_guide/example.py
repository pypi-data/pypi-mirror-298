import re
from fastapi import FastAPI
from sympy import Symbol
from sympy.parsing.latex import parse_latex
from pydantic import BaseModel
from typing import Dict, List
import pprint
import json

# Code > Ref > Symbol 계층 구조는 어디서나 공통
# description 과 같은 파라미터에 필요한 추가 정보는 openapi schema의 규칙을 따라야 함
latex_symbols = [
    {
        'id': 'G1_MODULE_3',
        'latex_symbol': r'p_{years}',
        'description': r"Annual probability of maximum (minimum) shade air temperature being exceeded"
    },
    {
        'id': 'G1_MODULE_6',
        'latex_symbol': r'T_{max}',
        'description': r"Maximum shade air temperature with an annual probability of being exceeded of 0.02 (equivalent to a mean return period of 50 years)"
    },
    {
        'id': 'G1_MODULE_5',
        'latex_symbol': r'T_{min}',
        'description': r"Minimum shade air temperature with an annual probability of being exceeded of 0.02 (equivalent to a mean return period of 50 years)"
    },
    {
        'id': 'G1_MODULE_8',
        'latex_symbol': r'T_{max,p}',
        'description': r"Maximum shade air temperature with an annual probability of being exceeded p (equivalent to a mean return period of 1/p)"
    },
    {
        'id': 'G1_MODULE_7',
        'latex_symbol': r'T_{min,p}',
        'description': r"Minimum shade air temperature with an annual probability of being exceeded p (equivalent to a mean return period of 1/p)"
    },
    {
        'id': 'G1_MODULE_14',
        'latex_symbol': r'T_{e,max}',
        'description': r"Maximum uniform bridge temperature component"
    },
    {
        'id': 'G1_MODULE_13',
        'latex_symbol': r'T_{e,min}',
        'description': r"Minimum uniform bridge temperature component"
    },
    {
        'id': "G1_MODULE_2",
        'latex_symbol': r'T_{0}',
        'description': r"Initial temperature when the structural element is restrained"
    },
    {
        'id': 'G1_MODULE_16',
        'latex_symbol': r'\Delta T_{N,exp}',
        'description': r"Maximum expansion range of uniform bridge temperature component (Te.max ≥ T0)"
    },
    {
        'id': 'G1_MODULE_15',
        'latex_symbol': r'\Delta T_{N,con}',
        'description': r"Maximum contraction range of uniform bridge temperature component (T0 ≥ Te.min)"
    },
    {
        'id': 'G1_MODULE_9',
        'latex_symbol': r'k_{1}',
        'description': r"Coefficient for calculation of maximum (minimum) shade air temperature with an annual probability of being exceeded, p, other than 0.02"
    },
    {
        'id': 'G1_MODULE_10',
        'latex_symbol': r'k_{2}',
        'description': r"Coefficient for calculation of maximum (minimum) shade air temperature with an annual probability of being exceeded, p, other than 0.02"
    },
    {
        'id': 'G1_MODULE_11',
        'latex_symbol': r'k_{3}',
        'description': r"Coefficient for calculation of maximum (minimum) shade air temperature with an annual probability of being exceeded, p, other than 0.02"
    },
    {
        'id': 'G1_MODULE_12',
        'latex_symbol': r'k_{4}',
        'descri tion': r"Coefficient for calculation of maximum (minimum) shade air temperature with an annual probability of being exceeded, p, other than 0.02"
    },
    {
        'id': "G1_MODULE_4",
        'latex_symbol': r'p',
        'description': r"Annual probability of maximum (minimum) shade air temperature being exceeded (equivalent to a mean return period of 1/p years)"
    },
    {
        'id': "G1_MODULE_1",
        'latex_symbol': r'Deck_types',
        'description': r"This section categorizes bridge decks into different types based on their material and structural design. The classification includes steel decks, composite decks, and concrete decks, each with distinct subtypes like steel box girders, concrete slabs, and concrete box girders."
    },
]

# description 과 같은 파라미터에 필요한 추가 정보는 openapi schema의 규칙을 따라야 함
latex_equations = [
    {
        'id': "G1_MODULE_4",
        'latex_equation': r'p = \frac{1}{p_{years}}',
        'description': r"Minimum shade air temperature with an annual probability of being exceeded p (equivalent to a mean return period of 1/p)"
    },
    {
        'id': 'G1_MODULE_16',
        'latex_equation': r'\Delta T_{N,exp} = k_{1} \cdot \left( T_{max,p} - T_{0} \right)',
        'description': r"Maximum expansion range of uniform bridge temperature component (Te.max ≥ T0)"
    },
    {
        'id': 'G1_MODULE_15',
        'latex_equation': r'\Delta T_{N,con} = k_{2} \cdot \left( T_{0} - T_{min,p} \right)',
        'description': r"Maximum contraction range of uniform bridge temperature component (T0 ≥ Te.min)"
    },
    {
        'id': 'G1_MODULE_7',
        'latex_equation': r'T_{max,p} = k_{3} \cdot \left( T_{max} - T_{0} \right)',
        'description': r"Maximum shade air temperature with an annual probability of being exceeded p (equivalent to a mean return period of 1/p)"
    },
    {
        'id': 'G1_MODULE_8',
        'latex_equation': r'T_{min,p} = k_{4} \cdot \left( T_{min} - T_{0} \right)',
        'description': r"Minimum shade air temperature with an annual probability of being exceeded p (equivalent to a mean return period of 1/p)"
    },
]

data_table = [
    {
        "id" : "G1_MODULE_1",
        "name" : "Bridge deck types",
        "symbol": r'Deck_types',
        'description': r"This section categorizes bridge decks into different types based on their material and structural design. The classification includes steel decks, composite decks, and concrete decks, each with distinct subtypes like steel box girders, concrete slabs, and concrete box girders.",
        "data": [
            {
                'deck_type': 'steel box girder',
                'type_category': 'Type1',
            },
            {
                'deck_type': 'steel truss or plate girder',
                'type_category': 'Type1',
            },
            {
                'deck_type': 'Composite deck',
                'type_category': 'Type2',
            },
            {
                'deck_type': 'concrete slab',
                'type_category': 'Type3',
            },
            {
                'deck_type': 'concrete beam',
                'type_category': 'Type3',
            },
            {
                'deck_type': 'concrete box girder',
                'type_category': 'Type3',
            }
        ],
    },
]


equation_table = [
    {
        "name": "Minimum uniform bridge temperature component",
        "symbol": r'T_{e,min}',
        "description": r"The minimum uniform bridge temperature component, T_{e.min}, represents the lowest temperature that a bridge structure can uniformly experience. It should be determined based on local climatic conditions and national guidelines. The values are typically derived from a correlation with the minimum shade air temperature (T_{min}). National Annexes may specify exact values, and Figure 6.1 provides recommended ranges. For example, for steel truss and plate girders, the maximum value of Te.min for type 1 is reduced by 3°C from T_{min}.",
        "data": [
            {
                'Bridge Deck Type': 'Type1',
                "latex_equation": r'T_{e,min} = T_{min,p} - 3',
            },
            {
                'Bridge Deck Type': 'Type2',
                "latex_equation": r'T_{e,min} = T_{min,p} + 4',
            },
            {
                'Bridge Deck Type': 'Type3',
                "latex_equation": r'T_{e,min} = T_{min,p} + 8',
            },
        ]
    },
    {
        "name": "Maximum uniform bridge temperature component",
        "symbol": r'T_{e,max}',
        "description": r"The maximum uniform bridge temperature component, T_{e.max}, represents the highest temperature that a bridge structure can uniformly experience. It should be determined based on local climatic conditions and national guidelines. The values are typically derived from a correlation with the maximum shade air temperature (T_{max}). National Annexes may specify exact values, and Figure 6.1 provides recommended ranges. For example, for steel truss and plate girders, the maximum value of Te.max for type 1 is increased by 3°C from T_{max}.",
        "data": [
            {
                'Bridge Deck Type': 'Type1',
                "latex_equation": r'T_{e,max} = T_{max,p} + 16',
            },
            {
                'Bridge Deck Type': 'Type2',
                "latex_equation": r'T_{e,max} = T_{max,p} + 4',
            },
            {
                'Bridge Deck Type': 'Type3',
                "latex_equation": r'T_{e,max} = T_{max,p} + 2',
            },
        ]
    }
]

# 1. Insert spaces around operators in LaTeX
def insert_spaces(latex_expr):
    # List of operators
    binary_operators = [r'\\pm', r'\\cdot', r'\\times', r'\\div', r'\\mod', r'\\land', r'\\lor', r'\\cup', r'\\cap', r'\\oplus']
    relation_operators = [r'=', r'\\neq', r'\\leq', r'\\geq', r'<', r'>', r'\\approx', r'\\sim', r'\\equiv', r'\\subset', r'\\supset']
    function_operators = [r'\\sin', r'\\cos', r'\\log', r'\\lim', r'\\int', r'\\sum', r'\\left', r'\\right']
    operators = binary_operators + relation_operators + function_operators

    for op in operators:
        latex_expr = re.sub(f'({op})([^ ])', r'\1 \2', latex_expr)
        latex_expr = re.sub(f'([^ ])({op})', r'\1 \2', latex_expr)
    return re.sub(r'\s+', ' ', latex_expr).strip()


# 2. Replace LaTeX symbols with simple symbols and map them
def create_symbol_mappings(latex_symbols):
    return {item['latex_symbol']: f'S_{{{i + 1}}}' for i, item in enumerate(latex_symbols)}


def replace_symbols_in_equations(equations, symbol_mappings):
    for equation in equations:
        preprocessed_eq = equation['latex_equation']
        for latex_symbol, simple_symbol in symbol_mappings.items():
            preprocessed_eq = re.sub(rf'(?<!\w){re.escape(latex_symbol)}(?!\w)', simple_symbol, preprocessed_eq)
        equation['preprocessed_equation'] = preprocessed_eq
        equation['sympy_expr'] = parse_latex(preprocessed_eq)
    return equations


# 3. Substitute simple symbols back to LaTeX symbols
def substitute_symbols_in_equation(equation, latex_symbols):
    substitutions = [(Symbol(f'S_{{{i + 1}}}'), Symbol(item['latex_symbol']))
                     for i, item in enumerate(latex_symbols)]
    return equation['sympy_expr'].subs(substitutions)


# 4. Search functions for equations and symbols
def search_equation(equations, target_latex_equation):
    return next((eq for eq in equations if eq['latex_equation'] == target_latex_equation), None)


def search_equation_by_lhs_latex(equations, lhs_latex_symbol, symbol_mappings):
    lhs_sympy_symbol = symbol_mappings.get(lhs_latex_symbol, None)
    for equation in equations:
        if lhs_sympy_symbol == str(equation['sympy_expr'].lhs):
            return equation
    return None


# 5. get symbol parameters
def get_symbol_informations(equation, symbol_mappings, latex_symbols):
    input = equation.free_symbols
    params = []
    for symbol in input:
        for latex_symbol, simple_symbol in symbol_mappings.items():
            if str(symbol) == simple_symbol:
                params.append(next((item for item in latex_symbols if item['latex_symbol'] == latex_symbol), None))
    return params

class InputModel(BaseModel):
    # 빈 데이터로 초기화
    __data__ = {}

class OutputModel(BaseModel):
    # 빈 데이터로 초기화
    __data__ = {}

def create_input_model(input_symbols: List[Dict]):
    """InputModel의 필드를 동적으로 생성하는 함수."""
    InputModel.__data__ = {item['latex_symbol']: float for item in input_symbols}

def create_output_model(response_symbols: List[Dict]):
    """OutputModel의 필드를 동적으로 생성하는 함수."""
    OutputModel.__data__ = {item['latex_symbol']: float for item in response_symbols}

app = FastAPI()
# OpenAPI 스펙 생성 함수
def create_openapi_schema(input_symbols: List[Dict], response_symbols: List[Dict]):
    # InputModel과 OutputModel의 필드 설정
    create_input_model(input_symbols)
    create_output_model(response_symbols)

    @app.post("/execute?functionName=moapy/designers_guide/module_example/calc", response_model=OutputModel)
    async def calculate(input: InputModel):
        from moapy.designers_guide.module_example import calc  # 여기서 임포트

        # 입력값을 calc 함수에 전달하여 계산 수행
        input_data = {key: getattr(input, key) for key in InputModel.__annotations__.keys() if getattr(input, key) is not None}

        # calc 함수를 호출하고 결과를 반환
        result = calc(**input_data)

        # OutputModel의 인스턴스를 반환
        return result  # 또는 필요한 형태로 변환하여 반환

    # FastAPI OpenAPI 스펙을 생성하고 반환
    openapi_schema = app.openapi()
    # 서버 주소 추가
    openapi_schema["servers"] = [
        {
            "url": "https://moa.rpm.kr-dv-midasit.com/backend/python-executor/"
        },
        {
            "url": "https://moa.rpm.kr-st-midasit.com/backend/function-executor/python-execute/"
        }
    ]
    return openapi_schema


# 파일 이름에서 사용할 수 없는 문자를 처리하는 함수
def sanitize_filename(filename: str) -> str:
    # 정규식을 사용하여 파일 이름에 사용할 수 없는 문자를 대체
    sanitized = re.sub(r'[\/:*?"<>|\\]', '_', filename)  # Backslash도 포함
    sanitized = re.sub(r'\\', '_', sanitized)  # LaTeX의 백슬래시 처리
    return sanitized

# JSON 파일로 저장하는 함수
def save_openapi_schema_to_json(openapi_schema: Dict, output_id: str):
    # 파일 이름에서 사용할 수 없는 문자를 처리한 후 저장
    sanitized_output_id = sanitize_filename(output_id)
    file_name = f"{sanitized_output_id}.json"
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(openapi_schema, json_file, ensure_ascii=False, indent=4)
    print(f"OpenAPI schema saved as {file_name}")

# Main logic to preprocess and substitute symbols in equations
def main():
    # Step 1: Insert spaces in LaTeX equations
    for eq in latex_equations:
        eq['latex_equation'] = insert_spaces(eq['latex_equation'])

    # Step 2: Create symbol mappings and replace symbols in equations
    symbol_mappings = create_symbol_mappings(latex_symbols)
    processed_equations = replace_symbols_in_equations(latex_equations, symbol_mappings)

    # Step 3: Test searching and substitutions
    for equation in processed_equations:
        substituted_expr = substitute_symbols_in_equation(equation, latex_symbols)
        pprint.pprint(substituted_expr)

    # Example search for an equation by LaTeX symbol
    target_symbol = r'\Delta T_{N,con}'
    target_content = search_equation_by_lhs_latex(processed_equations, target_symbol, symbol_mappings)

    # get the function to solve the equation, and parameters
    input = get_symbol_informations(target_content['sympy_expr'].rhs, symbol_mappings, latex_symbols)
    for i, item in enumerate(input):
        sub_param = search_equation_by_lhs_latex(processed_equations, item['latex_symbol'], symbol_mappings)
        pprint.pprint(sub_param)
        item['equation'] = sub_param

    output = get_symbol_informations(target_content['sympy_expr'].lhs, symbol_mappings, latex_symbols)
    # 다음 코드를 실행하면(subs(...) 에 파라미터 채워줘야함), 실제 값을 계산할 수 있음
    # output['equation'].subs(...).evalf()
    
    # make content from output
    # create content function
    # create function or Solve function

    # pprint.pprint(input)
    # pprint.pprint(output)
    pprint.pprint(target_content)
    # OpenAPI 스펙 생성
    openapi_schema = create_openapi_schema(input, output)

    output_id = output[0]['latex_symbol']  # output 리스트의 첫 번째 항목의 id 사용
    save_openapi_schema_to_json(openapi_schema, output_id)

main()
