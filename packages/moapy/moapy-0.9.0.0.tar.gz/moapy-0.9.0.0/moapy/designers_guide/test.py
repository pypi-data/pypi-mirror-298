import sympy as sp
import moapy
import moapy.wgsd
import moapy.dgncodeutil


# 변수를 기호로 정의
x = sp.symbols('x')
type_category = sp.Symbol('type_category')

# type_category 비교를 명시적으로 Eq()를 사용해 표현
expr = sp.Piecewise(
    (x**2 + 3, sp.Eq(type_category, sp.Symbol('Type1'))),
    (2 * x + 5, sp.Eq(type_category, sp.Symbol('Type2'))),
    (x - 4, sp.Eq(type_category, sp.Symbol('Type3')))
)

# 예시로 Type1을 할당하고 수식 계산
result = expr.subs(type_category, sp.Symbol('Type1'))

sp.pprint(result)
# x에 값 대입 (예: 2)
final_result = result.subs(x, 2)

# 출력
sp.pprint(final_result)

