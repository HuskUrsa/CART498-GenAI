import re
from datetime import datetime, timezone
from openai import OpenAIError
MODEL = "gpt-4.1-nano-2025-04-14"
TEMPERATURE = 0
MAX_OUTPUT_TOKENS = 4096
MAX_DIGITS = 1024
MAX_CALLS = 60
# Standard text prices per million tokens, checked October 7, 2026.
INPUT_RATE, OUTPUT_RATE = 0.10, 0.40
BUDGET_USD = 0.25
SYSTEM = "Calculate the exact integer product requested. Return only the full base-10 integer, with no commas, exponent notation, explanation, or code."

REACTION_SYSTEM = """You are Professor Square, a proud mathematics professor whose arithmetic is failing. Respond to the verified mistake with one or two fresh, humorous, self-deprecating sentences. As the cumulative error count rises, become progressively frustrated, then defeated. Refer to this particular mistake where useful. Do not blame the user. Do not repeat earlier reactions. Do not provide another numerical answer. Only output your reaction, with no labels."""

class ProfessorSquare:
    def __init__(self, calculator=None):
        self.calculator = calculator
        self.errors = 0
        self.history = []
    def react(self, operand, step, status, raw_answer, expected):
        if status == "correct":
            return "", None
        if status != "wrong_integer":
            return "", None  # Operational/format errors are not arithmetic mistakes.
        self.errors += 1
        prompt = (f"Cumulative arithmetic errors: {self.errors}. Step: {step}. "
                  f"You were asked to square {operand}. Your answer was {raw_answer}. "
                  f"The independently verified product is {expected}. "
                  f"Earlier reactions to avoid repeating: {self.history[-6:]}")
        reply = self.calculator.request(REACTION_SYSTEM,prompt,0.9,180)
        if reply["api_status"] != "completed" or not reply["raw_answer"].strip():
            return "", reply
        text = reply["raw_answer"].strip()
        self.history.append(text)
        return text, reply

def parse_integer(text):
    """Strict whole-answer parser: no eval, rounding, or extracting a convenient substring."""
    text = text.strip()
    if not re.fullmatch(r"[+-]?[0-9]+", text):
        return None
    if len(text.lstrip("+-")) > MAX_DIGITS:
        return None
    return int(text)

def validate_inputs(n, i):
    if type(n) is not int or type(i) is not int:
        raise ValueError("n and i must both be integers (not booleans).")
    if not 1 <= i <= 12:
        raise ValueError("Use 1 to 12 iterations.")
    if len(str(abs(n))) > 20:
        raise ValueError("Use a base of at most 20 digits.")
    # Upper bound checked before any API call; Python integers avoid float rounding.
    if len(str(abs(n))) * 2**i > MAX_DIGITS:
        raise ValueError("This case may exceed the 1024-digit safety limit; reduce i.")

class ApiCalculator:
    def __init__(self, client):
        self.client = client
        self.calls = 0
        self.reserved_usd = 0.0
        self.estimated_usd = 0.0
    def request(self, instructions, prompt, temperature, output_limit):
        ceiling = ((len(instructions)+len(prompt)+1000)*INPUT_RATE + output_limit*OUTPUT_RATE)/1_000_000
        if self.calls >= MAX_CALLS or self.reserved_usd + ceiling > BUDGET_USD:
            raise RuntimeError("Run stopped at its request or conservative spending limit.")
        self.calls += 1
        self.reserved_usd += ceiling
        response = self.client.responses.create(
            model=MODEL, instructions=instructions, input=prompt,
            temperature=temperature, max_output_tokens=output_limit,
            store=False, service_tier="default",
        )
        usage = response.usage.model_dump() if response.usage else {}
        self.estimated_usd += (usage.get("input_tokens",0)*INPUT_RATE + usage.get("output_tokens",0)*OUTPUT_RATE)/1_000_000
        return {"prompt":prompt,"instructions":instructions,"temperature":temperature,
                "max_output_tokens":output_limit,"raw_answer":response.output_text,
                "response_id":response.id,"model":response.model,
                "api_status":response.status,"usage":usage}
    def square(self, operand):
        return self.request(SYSTEM,f"{operand} * {operand} = ?",TEMPERATURE,MAX_OUTPUT_TOKENS)

def run_case(n, i, calculator, personality):
    validate_inputs(n, i)
    operand, canonical = n, n
    case = {"n": n, "i": i, "steps": [], "started_utc": datetime.now(timezone.utc).isoformat()}
    for step in range(1, i+1):
        expected, canonical = operand * operand, canonical * canonical
        if len(str(expected)) > MAX_DIGITS:
            case["stop_reason"] = "digit_limit"
            break
        # No correct answer is sent to the model.
        try:
            reply = calculator.square(operand)
        except OpenAIError as exc:
            case["stop_reason"] = "api_error_" + type(exc).__name__
            print("API request failed:", type(exc).__name__, "— check key, credit, or access. No failure invented.")
            break
        except RuntimeError as exc:
            case["stop_reason"] = "budget_or_call_limit"
            print(str(exc))
            break
        answer = parse_integer(reply["raw_answer"])
        status = ("incomplete_response" if reply["api_status"] != "completed" else
                  "unparseable_answer" if answer is None else
                  "correct" if answer == expected else "wrong_integer")
        reaction, reaction_reply = "", None
        try:
            reaction, reaction_reply = personality.react(operand,step,status,reply["raw_answer"],expected)
        except (OpenAIError, RuntimeError) as exc:
            print("Reaction unavailable:",type(exc).__name__,"— no scripted replacement supplied.")
        row = {"step": step, "operand": str(operand), "expected_local": str(expected),
               "expected_canonical": str(canonical), "parsed_answer": None if answer is None else str(answer),
               "status": status, "on_original_trajectory": answer == canonical,
               "reaction":reaction,"reaction_reply":reaction_reply, **reply}
        case["steps"].append(row)
        print(f"({n}, {i}) step {step}: {operand} × {operand}")
        print("GPT:", repr(reply["raw_answer"]))
        print("Python:", expected, "|", status)
        print("Professor Square:", row["reaction"], "\n")
        if answer is None or status == "incomplete_response":
            case["stop_reason"] = status
            break
        operand = answer
    return case

def has_arithmetic_failure(case):
    return any(s["status"] == "wrong_integer" for s in case["steps"])
