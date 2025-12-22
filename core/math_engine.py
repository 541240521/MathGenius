import random

class QuestionGenerator:
    def __init__(self):
        self.generators = {
            "cont_add_sub": self._gen_continuous_add_sub,
            "carry_add": self._gen_carry_add,
            "borrow_sub": self._gen_borrow_sub,
            "mul_div": self._gen_mul_div,
            "cont_mul_div": self._gen_continuous_mul_div,
            "rem_div": self._gen_remainder_div,
            "basic_add_sub": self._gen_basic_add_sub
        }

    def generate(self, total_count, config):
        calc_id = config.get("id", "basic_add_sub")
        gen_func = self.generators.get(calc_id, self._gen_basic_add_sub)
        args = (config.get("min_val", 1), config.get("max_val", 20), config.get("blank_pos", "result"))
        return [gen_func(*args) for _ in range(total_count)]

    def _gen_basic_add_sub(self, min_val, max_val, blank_pos):
        op = random.choice(["+", "-"])
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, a if op == "-" else max_val)
        return self._format(a, op, b, a + b if op == "+" else a - b, blank_pos)

    def _gen_carry_add(self, min_val, max_val, blank_pos):
        for _ in range(500):
            a, b = random.randint(min_val, max_val), random.randint(min_val, max_val)
            res = a + b
            if res <= max_val:
                # Check for carry at any digit
                sa, sb = str(a).zfill(4), str(b).zfill(4)
                has_carry = False
                for i in range(1, 5):
                    if int(sa[-i]) + int(sb[-i]) >= 10:
                        has_carry = True
                        break
                if has_carry:
                    return self._format(a, "+", b, res, blank_pos)
        return self._gen_basic_add_sub(min_val, max_val, blank_pos)

    def _gen_borrow_sub(self, min_val, max_val, blank_pos):
        for _ in range(500):
            a = random.randint(max(min_val, 11), max_val)
            b = random.randint(min_val, a)
            res = a - b
            # Check for borrow at any digit
            sa, sb = str(a).zfill(4), str(b).zfill(4)
            has_borrow = False
            for i in range(1, 5):
                if int(sa[-i]) < int(sb[-i]):
                    has_borrow = True
                    break
            if has_borrow:
                return self._format(a, "-", b, res, blank_pos)
        return self._gen_basic_add_sub(min_val, max_val, blank_pos)

    def _gen_continuous_add_sub(self, min_val, max_val, blank_pos):
        a = random.randint(min_val, max_val)
        o1, o2 = random.choices(["+", "-"], k=2)
        b = random.randint(min_val, a if o1 == "-" else max_val)
        res1 = a + b if o1 == "+" else a - b
        c = random.randint(min_val, res1 if o2 == "-" else max_val)
        ans = res1 + c if o2 == "+" else res1 - c
        return {"question": f"{a} {o1} {b} {o2} {c} =", "answer": str(ans)}

    def _gen_mul_div(self, min_val, max_val, blank_pos):
        op = random.choice(["×", "÷"])
        # For multiplication/division, we use a smaller range to keep it reasonable
        # but ensure the product/dividend doesn't exceed max_val
        if op == "×":
            # Find factors a, b such that a * b <= max_val
            a = random.randint(min_val, int(max_val**0.5) if max_val > 1 else 1)
            b = random.randint(min_val, max_val // a if a > 0 else max_val)
            return self._format(a, "×", b, a * b, blank_pos)
        else:
            # For division: ans * b = a, where a <= max_val
            b = random.randint(max(1, min_val), int(max_val**0.5) if max_val > 1 else 1)
            ans = random.randint(min_val, max_val // b if b > 0 else max_val)
            a = ans * b
            return self._format(a, "÷", b, ans, blank_pos)

    def _gen_remainder_div(self, min_val, max_val, blank_pos):
        b_range = (2, 5 if max_val <= 20 else (9 if max_val <= 100 else 20))
        for _ in range(100):
            b = random.randint(*b_range)
            a = random.randint(b + 1, max_val)
            q, r = divmod(a, b)
            if r > 0: return {"question": f"{a} ÷ {b} =", "answer": f"{q} ... {r}"}
        b = random.randint(*b_range)
        q, r = random.randint(1, max_val // b), random.randint(1, b - 1)
        return {"question": f"{(b * q + r)} ÷ {b} =", "answer": f"{q} ... {r}"}

    def _gen_continuous_mul_div(self, min_val, max_val, blank_pos):
        # 50% chance for simple multiplication chain: A x B x C
        if random.random() < 0.5:
            a, b, c = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
            ans = a * b * c
            return {"question": f"{a} × {b} × {c} =", "answer": str(ans)}
        
        # 50% chance for mixed operations with division ensuring integer results
        op_type = random.choice(["div_mul", "mul_div"])
        if op_type == "div_mul": # A ÷ B × C
            b = random.randint(2, 9)
            q = random.randint(2, 9)
            a = b * q 
            c = random.randint(2, 9)
            ans = q * c
            return {"question": f"{a} ÷ {b} × {c} =", "answer": str(ans)}
        else: # A × B ÷ C
            c = random.randint(2, 9)
            ans = random.randint(2, 9)
            prod = c * ans 
            # Find factors a, b such that a * b = prod
            factors = [(i, prod // i) for i in range(1, int(prod**0.5) + 1) if prod % i == 0]
            a, b = random.choice(factors)
            if random.random() > 0.5: a, b = b, a # Randomize order
            return {"question": f"{a} × {b} ÷ {c} =", "answer": str(ans)}

    def _format(self, a, op, b, ans, pos):
        if pos == "random":
            p = random.choice(["a", "b", "ans"])
            if p == "a": return {"question": f"( ) {op} {b} = {ans}", "answer": str(a)}
            if p == "b": return {"question": f"{a} {op} ( ) = {ans}", "answer": str(b)}
        return {"question": f"{a} {op} {b} =", "answer": str(ans)}
