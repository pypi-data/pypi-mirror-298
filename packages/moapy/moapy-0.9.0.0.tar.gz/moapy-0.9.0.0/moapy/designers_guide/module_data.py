# Code > Ref > Symbol 계층 구조는 어디서나 공통
# description 과 같은 파라미터에 필요한 추가 정보는 openapi schema의 규칙을 따라야 함
module_list = [
    {
        'id': "G1_MODULE_1",
        'standard': 'EN1991-1-5',
        'name': 'Bridge deck types',
        'latex_symbol': r'Deck_types',
        'unit': '',
        'reference': '6.1.1(1)',
        'description': r"This section categorizes bridge decks into different types based on their material and structural design. The classification includes steel decks, composite decks, and concrete decks, each with distinct subtypes like steel box girders, concrete slabs, and concrete box girders.",
        'type': 'Text',
        'data': ''
    },
    {
        'id': "G1_MODULE_2",
        'standard': 'EN1991-1-5',
        'name': 'The initial bridge temperature',
        'latex_symbol': r'T_{0}',
        'unit': '°C',
        'reference': 'AnnexA.2(2)',
        'description': r"Initial temperature when the structural element is restrained",
        'type': 'Constant, User',
        'data': '10'
    },
    {
        'id': 'G1_MODULE_3',
        'standard': 'EN1991-1-5',
        'name': 'Return Period',
        'latex_symbol': r'p_{years}',
        'unit': 'years',
        'reference': '1.5.3, 1.5.4',
        'description': r"Annual probability of maximum (minimum) shade air temperature being exceeded",
        'type': 'Constant, User',
        'data': '50'
    },
    {
        'id': "G1_MODULE_4",
        'standard': 'EN1991-1-5',
        'name': 'Annual exceedance probability',
        'latex_symbol': r'p',
        'unit': '',
        'reference': '1.6',
        'description': r"Annual probability of maximum (minimum) shade air temperature being exceeded (equivalent to a mean return period of 1/p years)",
        'type': 'formula',
        'data': '1/{p_years}'
    },
    {
        'id': 'G1_MODULE_5',
        'standard': 'EN1991-1-5',
        'name': 'Minimum shade air temperature (exceedance probability 0.02)',
        'latex_symbol': r'T_{min}',
        'unit': '°C',
        'reference': '6.1.3.2(1)P',
        'description': r"Minimum shade air temperature with an annual probability of being exceeded of 0.02 (equivalent to a mean return period of 50 years)",
        'type': 'User',
        'data': ''
    },
    {
        'id': 'G1_MODULE_6',
        'standard': 'EN1991-1-5',
        'name': 'Maximum shade air temperature (exceedance probability 0.02)',
        'latex_symbol': r'T_{max}',
        'unit': '°C',
        'reference': '6.1.3.2(1)P',
        'description': r"Maximum shade air temperature with an annual probability of being exceeded of 0.02 (equivalent to a mean return period of 50 years)",
        'type': 'User',
        'data': ''
    },
    {
        'id': 'G1_MODULE_7',
        'standard': 'EN1991-1-5',
        'name': 'Minimum shade air temperature with exceedance probability p',
        'latex_symbol': r'T_{min,p}',
        'unit': '°C',
        'reference': 'AnnexA.2(2)',
        'description': r"Minimum shade air temperature with an annual probability of being exceeded p (equivalent to a mean return period of 1/p)",
        'type': 'formula',
        'data': 'T_{min,p} = T_{min} * {k_3+ k_4 * ln[-ln(1-p)]}'
    },
    {
        'id': 'G1_MODULE_8',
        'standard': 'EN1991-1-5',
        'name': 'Maximum shade air temperature with exceedance probability p',
        'latex_symbol': r'T_{max,p}',
        'unit': '°C',
        'reference': 'AnnexA.2(2)',
        'description': r"Maximum shade air temperature with an annual probability of being exceeded p (equivalent to a mean return period of 1/p)",
        'type': 'formula',
        'data': 'T_{max,p} = T_{max} * {k_1 - k_2 * ln[-ln(1-p)]}'
    },
    {
        'id': 'G1_MODULE_9',
        'standard': 'EN1991-1-5',
        'name': 'Coefficient for maximum shade air temperature',
        'latex_symbol': r'k_{1}',
        'unit': '',
        'reference': 'AnnexA.2(2)',
        'description': r"Coefficient for calculation of maximum (minimum) shade air temperature with an annual probability of being exceeded, p, other than 0.02",
        'type': 'Constant, User',
        'data': '0.781'
    },
    {
        'id': 'G1_MODULE_10',
        'standard': 'EN1991-1-5',
        'name': 'Scaling factor for maximum shade air temperature',
        'latex_symbol': r'k_{2}',
        'unit': '',
        'reference': 'AnnexA.2(2)',
        'description': r"Coefficient for calculation of maximum (minimum) shade air temperature with an annual probability of being exceeded, p, other than 0.02",
        'type': 'Constant, User',
        'data': '0.056'
    },
    {
        'id': 'G1_MODULE_11',
        'standard': 'EN1991-1-5',
        'name': 'Coefficient for minimum shade air temperature',
        'latex_symbol': r'k_{3}',
        'unit': '',
        'reference': 'AnnexA.2(2)',
        'description': r"Coefficient for calculation of maximum (minimum) shade air temperature with an annual probability of being exceeded, p, other than 0.02",
        'type': 'Constant, User',
        'data': '0.393'
    },
    {
        'id': 'G1_MODULE_12',
        'standard': 'EN1991-1-5',
        'name': 'Scaling factor for minimum shade air temperature',
        'latex_symbol': r'k_{4}',
        'unit': '',
        'reference': 'AnnexA.2(2)',
        'description': r"Coefficient for calculation of maximum (minimum) shade air temperature with an annual probability of being exceeded, p, other than 0.02",
        'type': 'Constant, User',
        'data': '-0.156'
    },
    {
        'id': 'G1_MODULE_13',
        'standard': 'EN1991-1-5',
        'name': 'Minimum uniform bridge temperature component',
        'latex_symbol': r'T_{e,min}',
        'unit': '°C',
        'reference': '6.1.3.1(Figure6.1)',
        'description': r"Minimum uniform bridge temperature component",
        'type': 'Table(Formula)',
        'data': ''
    },
    {
        'id': 'G1_MODULE_14',
        'standard': 'EN1991-1-5',
        'name': 'Maximum uniform bridge temperature component',
        'latex_symbol': r'T_{e,max}',
        'unit': '°C',
        'reference': '6.1.3.1(Figure6.1)',
        'description': r"Maximum uniform bridge temperature component",
        'type': 'Table(Formula)',
        'data': ''
    },
    {
        'id': 'G1_MODULE_15',
        'standard': 'EN1991-1-5',
        'name': 'Maximum contraction range of a uniform bridge temperature',
        'latex_symbol': r'\Delta T_{N,con}',
        'unit': '°C',
        'reference': '6.1.3.3(3)',
        'description': r"Maximum contraction range of uniform bridge temperature component (T0 ≥ Te.min)",
        'type': 'formula',
        'data': ''
    },
    {
        'id': 'G1_MODULE_16',
        'standard': 'EN1991-1-5',
        'name': 'Maximum expansion range of a uniform bridge temperature',
        'latex_symbol': r'\Delta T_{N,exp}',
        'unit': '°C',
        'reference': '6.1.3.3(3)',
        'description': r"Maximum expansion range of uniform bridge temperature component (Te.max ≥ T0)",
        'type': 'formula',
        'data': ''
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