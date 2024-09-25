# Desc. Get a result of Designers Guide Report from Modules
import module_data
import module_report_form

import re
import sympy
from sympy import Symbol
from sympy.parsing.latex import parse_latex
from moapy.designers_guide.example import InputModel
import pprint

import networkx as nx
import matplotlib.pyplot as plt

# Func Desc. Insert spaces around operators in LaTeX
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

# Func Desc. Replace LaTeX symbols with simple symbols and map them
def create_symbol_mappings(module_list):
    return {item['latex_symbol']: f'S_{{{i + 1}}}' for i, item in enumerate(module_list)}

# Func Desc. Replace LaTeX symbols with simple symbols in equations
def replace_symbols_in_equations(equations, symbol_mappings):
    # TODO : symbol 이 중복되는 상황이 발생할 수 있음. 추가 식별자 도입 필요
    for equation in equations:
        preprocessed_eq = equation['latex_equation']
        for latex_symbol, simple_symbol in symbol_mappings.items():
            preprocessed_eq = re.sub(rf'(?<!\w){re.escape(latex_symbol)}(?!\w)', simple_symbol, preprocessed_eq)
        equation['preprocessed_equation'] = preprocessed_eq
        equation['sympy_expr'] = parse_latex(preprocessed_eq)
    return equations

# Func Desc. Substitute simple symbols back to LaTeX symbols
def substitute_symbols_in_equation(equation, module_list):
    substitutions = [(Symbol(f'S_{{{i + 1}}}'), Symbol(item['latex_symbol']))
                     for i, item in enumerate(module_list)]
    return equation['sympy_expr'].subs(substitutions)

# Func Desc. Search functions for equations and symbols
def search_equation(equations, target_latex_equation):
    return next((eq for eq in equations if eq['latex_equation'] == target_latex_equation), None)

# Func Desc. Search a latex_equation by LaTeX symbols
def search_equation_by_lhs_latex(equations, lhs_latex_symbol, symbol_mappings):
    lhs_sympy_symbol = symbol_mappings.get(lhs_latex_symbol, None)
    for equation in equations:
        if lhs_sympy_symbol == str(equation['sympy_expr'].lhs):
            return equation
    return None

# Func Desc. Search a Module by LaTeX symbols
def search_content_by_lhs_latex(module_list, lhs_latex_symbol):
    for module in module_list:
        if lhs_latex_symbol == str(module['latex_symbol']):
            return module
    return None

# Func Desc. get report
def get_report(inp, target_symbol, processed_equations, module_list, symbol_mappings):
    # Step 1. Create a report
    current_content = search_content_by_lhs_latex(module_list, target_symbol)
    if current_content is None:
        return [None, None]
    
    current_report = module_report_form.ReportForm()
    current_report.standard = current_content['standard']
    current_report.title = current_content['name']
    current_report.unit = current_content['unit']
    current_report.reference = current_content['reference']
    current_report.description = current_content['description']
    current_report.symbol = current_content['latex_symbol']
    current_report.formula = []

    sub_symbols = current_content['latex_symbol']
    current_equation = search_equation_by_lhs_latex(processed_equations, target_symbol, symbol_mappings)
    if current_equation is not None:
        sub_symbols = current_equation['sympy_expr'].rhs.free_symbols
        current_report.formula.append(f"{current_equation['sympy_expr'].rhs}")        
        
    # Step 2. Substitute symbols in equations
    params_report = []
    params_relation = []
    symbol_result = []
    for sub_symbol in sub_symbols:
        for latex_symbol, simple_symbol in symbol_mappings.items():
            if str(sub_symbol) == simple_symbol:
                [sub_reports, relation] = get_report(latex_symbol, processed_equations, module_list, symbol_mappings)
                if sub_reports is None:
                    continue
                params_relation.extend(relation)
                params_relation.append([current_report.symbol, latex_symbol])
                for sub_report in sub_reports:
                    symbol_result.append(tuple([symbol_mappings[f"{sub_report.symbol}"], sub_report.symbol, sub_report.result]))
                params_report.extend(sub_reports)

    symbol_result = set(symbol_result)
    
    # Step 3. Get the result
    if current_content['type'] == 'Constant, User' or current_content['type'] == 'Constant':
        current_report.result = float(current_content['data'])
        # TODO : Constant, User 두가지 타입은 사용자 선택. 적절한 시기에 분기 필요
    elif current_content['type'] == 'User':
        user_defined = inp[current_report.symbol]# input('Enter the value of [' + current_report.symbol + '] : ') # TODO : 사실 symbol이 아니라 required가 들어가야 할 것 같음.
        current_report.result = float(user_defined)
    elif current_content['type'] == 'formula': # Calculate a formula using sympy
        if len(symbol_result) != 0:
            current_report.formula.append(current_report.formula[-1])

        expr = current_equation['sympy_expr']
        for sym, disp, res in symbol_result:
            x = sympy.symbols(f"{sym}")
            expr = expr.subs(x, res)
            current_report.formula[0] = current_report.formula[0].replace(sym, disp)
            current_report.formula[-1] = current_report.formula[-1].replace(sym, str(res))
        current_report.result = expr.evalf().rhs
                    
    params_report.append(current_report)
    return [params_report, params_relation]

# Main logic to preprocess and substitute symbols in equations
def calc(inp: InputModel):
    # Step 1: Insert spaces in LaTeX equations
    for eq in module_data.latex_equations:
        eq['latex_equation'] = insert_spaces(eq['latex_equation'])

    # Step 2: Create symbol mappings and replace symbols in equations
    symbol_mappings = create_symbol_mappings(module_data.module_list)
    symbol_mappings = dict(sorted(symbol_mappings.items(), key=lambda item: len(item[0]), reverse=True))
    processed_equations = replace_symbols_in_equations(module_data.latex_equations, symbol_mappings)

    # TODO : equation과 일치하는 symbol 혹은 data 없음
    # target_symbol = r'p = \frac{1}{p_{years}}'
    # target_symbol = r'T_{max,p} = k_{3} \cdot \left( T_{max} - T_{0} \right)'
    # target_symbol = r'T_{min,p} = k_{4} \cdot \left( T_{min} - T_{0} \right)'
    target_symbol = r'\Delta T_{N,exp}'
    target_symbol = r'\Delta T_{N,con}'

    # Step 3. Print Reports
    [res_reports, res_relations] = get_report(inp, target_symbol, processed_equations, module_data.module_list, symbol_mappings)
    if res_reports is None:
        print('No report found.')
        return
    for idx, res_report in enumerate(res_reports):
        print(str(idx+1) + '. ' + str(res_report) + '\n')

    # Step 4. Print Relation
    relation_graph = nx.DiGraph()
    for relation in res_relations:
        relation_graph.add_edge(relation[0], relation[1])
    pos = nx.spring_layout(relation_graph)
    nx.draw(relation_graph, pos, with_labels=True, node_color="lightblue", font_weight="bold", node_size=4321)
    plt.show()
    
main()