# ============================================================
#  F.CSB305 Программчлалын хэлний зарчмууд
#  ЛАБОРАТОРИЙН АЖИЛ 1 — Арифметик илэрхийлэл интерпретатор
# ============================================================

# ── Алхам 2: Токенчлол (Tokenizer) ──────────────────────────

def tokenize(expression: str) -> list[str]:
    """
    Илэрхийллийг токенуудад задална.
    Тоо, оператор (+, -, *, /), хашилт ( ) зэргийг таних.
    """
    tokens = []
    i = 0
    while i < len(expression):
        ch = expression[i]

        # Цагаан зай алгасах
        if ch.isspace():
            i += 1
            continue

        # Тоо (олон оронтой тоог бүтнээр нь авна)
        if ch.isdigit():
            num = ""
            while i < len(expression) and expression[i].isdigit():
                num += expression[i]
                i += 1
            tokens.append(num)
            continue

        # Оператор ба хашилт
        if ch in "+-*/()":
            tokens.append(ch)
            i += 1
            continue

        # Танигдаагүй тэмдэгт
        raise ValueError(f"Танигдаагүй тэмдэгт: '{ch}'")

    return tokens


# ── Алхам 3: Рекурсив задлагч (Recursive Descent Parser) ────
#
#  Дүрмийн дарааллал (оператор давуу эрэмбэ):
#    expr   → term   { ('+' | '-') term }
#    term   → factor { ('*' | '/') factor }
#    factor → NUMBER | '(' expr ')'

class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        """Одоогийн токен."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        """Одоогийн токеныг авч, дараагийн руу шилжинэ."""
        tok = self.current()
        self.pos += 1
        return tok

    # expr → term { ('+' | '-') term }
    def expr(self):
        result = self.term()
        while self.current() in ('+', '-'):
            op = self.consume()
            right = self.term()
            if op == '+':
                result += right
            else:
                result -= right
        return result

    # term → factor { ('*' | '/') factor }
    def term(self):
        result = self.factor()
        while self.current() in ('*', '/'):
            op = self.consume()
            right = self.factor()
            if op == '*':
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Тэгд хуваах боломжгүй!")
                result /= right
        return result

    # factor → NUMBER | '(' expr ')'
    def factor(self):
        tok = self.current()

        # Хашилтай илэрхийлэл
        if tok == '(':
            self.consume()          # '(' залгих
            result = self.expr()
            if self.current() != ')':
                raise SyntaxError("')' хаах хашилт байхгүй байна")
            self.consume()          # ')' залгих
            return result

        # Тоо
        if tok is not None and tok.isdigit():
            self.consume()
            return int(tok)

        raise SyntaxError(f"Тоо эсвэл '(' хүлээгдэж байхад '{tok}' олдлоо")


# ── Нийтийн интерфейс ────────────────────────────────────────

def interpret(expression: str):
    """
    Арифметик илэрхийллийг задлан бодно.
    Бүхэл тоо эсвэл бутархай тоо буцаана.
    """
    tokens = tokenize(expression)
    parser = Parser(tokens)
    result = parser.expr()

    # Бүх токен дуусаагүй бол синтаксийн алдаа
    if parser.current() is not None:
        raise SyntaxError(f"Илэрхийлэл дуусаагүй байна: '{parser.current()}' үлдлээ")

    # Бүхэл тоо бол int хэлбэрт хөрвүүлнэ
    return int(result) if isinstance(result, float) and result.is_integer() else result


# ── Алхам 1: main функц ─────────────────────────────────────

def main():
    print("=" * 45)
    print("  Арифметик илэрхийлэл интерпретатор")
    print("  Гарахын тулд 'exit' бичнэ үү")
    print("=" * 45)
    while True:
        try:
            expression = input("\nИлэрхийлэл оруулна уу: ").strip()
            if expression.lower() in ("exit", "quit", "гар"):
                print("Программаас гарлаа.")
                break
            if not expression:
                continue
            result = interpret(expression)
            print(f"Үр дүн: {result}")
        except (ValueError, SyntaxError, ZeroDivisionError) as e:
            print(f"Алдаа: {e}")
        except KeyboardInterrupt:
            print("\nПрограммаас гарлаа.")
            break


if __name__ == "__main__":
    main()