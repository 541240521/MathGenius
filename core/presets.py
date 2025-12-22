class GradePresets:
    L1 = {
        "id": "L1",
        "name": "一年级 (20以内基础加减法)",
        "min_val": 1,
        "max_val": 20,
        "default_count": 60,
        "default_calc": "basic_add_sub"
    }
    L2 = {
        "id": "L2",
        "name": "二年级 (100以内进位退位加减)",
        "min_val": 1,
        "max_val": 100,
        "default_count": 60,
        "default_calc": "basic_add_sub"
    }
    L3 = {
        "id": "L3",
        "name": "三年级 (表内乘除法及混合运算)",
        "min_val": 1,
        "max_val": 81,
        "default_count": 60,
        "default_calc": "mul_div"
    }
    L4 = {
        "id": "L4",
        "name": "四年级 (大数运算及有余数除法)",
        "min_val": 1,
        "max_val": 1000,
        "default_count": 60,
        "default_calc": "rem_div"
    }
    L5 = {
        "id": "L5",
        "name": "五年级 (多步运算及小数(预留))",
        "min_val": 1,
        "max_val": 100,
        "default_count": 60,
        "default_calc": "basic_add_sub"
    }
    L6 = {
        "id": "L6",
        "name": "六年级 (综合四则运算及未知数)",
        "min_val": 1,
        "max_val": 100,
        "default_count": 60,
        "default_calc": "basic_add_sub"
    }

    @classmethod
    def get_all(cls):
        return [cls.L1, cls.L2, cls.L3, cls.L4, cls.L5, cls.L6]

    @classmethod
    def get_by_id(cls, grade_id):
        for preset in cls.get_all():
            if preset["id"] == grade_id:
                return preset
        return cls.L1

class CalculationMethods:
    BASIC_ADD_SUB = {
        "id": "basic_add_sub",
        "name": "基础加减算术练习题",
        "operators": ["+", "-"]
    }
    CONT_ADD_SUB = {
        "id": "cont_add_sub",
        "name": "连续加减算术练习题",
        "operators": ["+", "-"]
    }
    CARRY_ADD = {
        "id": "carry_add",
        "name": "进位加法算术练习题",
        "operators": ["+"]
    }
    BORROW_SUB = {
        "id": "borrow_sub",
        "name": "退位减法算术练习题",
        "operators": ["-"]
    }
    MUL_DIV = {
        "id": "mul_div",
        "name": "乘法和除法算术练习题",
        "operators": ["×", "÷"]
    }
    CONT_MUL_DIV = {
        "id": "cont_mul_div",
        "name": "连续乘除算术练习题",
        "operators": ["×", "÷"]
    }
    REM_DIV = {
        "id": "rem_div",
        "name": "有余数的除法练习题",
        "operators": ["÷"]
    }

    @classmethod
    def get_all(cls):
        return [
            cls.BASIC_ADD_SUB, cls.CONT_ADD_SUB, cls.CARRY_ADD, 
            cls.BORROW_SUB, cls.MUL_DIV, cls.CONT_MUL_DIV, cls.REM_DIV
        ]

    @classmethod
    def get_by_id(cls, calc_id):
        for method in cls.get_all():
            if method["id"] == calc_id:
                return method
        return cls.BASIC_ADD_SUB
