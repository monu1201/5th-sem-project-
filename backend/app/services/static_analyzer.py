"""
Static Code Analysis Engine.
Performs deterministic multi-language static analysis across Python, JavaScript, Java, and C++.
Inspects AST trees, syntax constructs, and vulnerability patterns.
Provides section-wise multi-line output for software defects, issue details, bug fixes, and future guidelines.
"""

import ast
import re
from typing import List, Dict, Any

class PythonASTAnalyzer(ast.NodeVisitor):
    def __init__(self, code: str):
        self.code = code
        self.lines = code.splitlines()
        self.issues: List[Dict[str, Any]] = []

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.type is None:
            self.issues.append({
                "type": "Bug",
                "severity": "High",
                "line_number": node.lineno,
                "title": "Bare Exception Clause",
                "software_defect": (
                    "Defect Classification: Indiscriminate Exception Swallowing (CWE-391: Unchecked Error Condition)\n"
                    "Root Cause: A bare 'except:' catches all exceptions, including SystemExit, KeyboardInterrupt, and MemoryError.\n"
                    "Defect Impact: Suppresses unexpected fatal runtime errors, prevents graceful process termination, and masks root-cause debugging traces."
                ),
                "description": (
                    f"Line {node.lineno} uses an unconstrained 'except:' block without specifying an exception class.\n"
                    "This intercepts low-level interpreter signals and hides unexpected programming defects."
                ),
                "bug_fix": (
                    "1. Replace bare 'except:' with 'except Exception as err:' or explicit exception classes (e.g. ValueError, IOError).\n"
                    "2. Log caught exceptions with stack traces using logging.exception() instead of silent pass."
                ),
                "why_it_matters": "Masks unexpected fatal errors and prevents legitimate shutdown signals from terminating the process.",
                "recommendation": "Catch specific exception types (e.g., 'except ValueError:' or 'except Exception as err:').",
                "suggested_fix": "except Exception as err:\n    logger.error(f'Operation failed: {err}', exc_info=True)",
                "future_guidelines": (
                    "1. Configure Flake8 / Ruff rule E722 (do not use bare except) to block PRs.\n"
                    "2. Define explicit application exception hierarchies for business logic errors.\n"
                    "3. Enforce automated linter checks in CI/CD pipeline."
                )
            })
        elif isinstance(node.type, ast.Name) and node.type.id == "BaseException":
            self.issues.append({
                "type": "Code Smell",
                "severity": "Medium",
                "line_number": node.lineno,
                "title": "Catching BaseException",
                "software_defect": (
                    "Defect Classification: Root Exception Interception (CWE-396: Declaration of Catch for Generic Exception)\n"
                    "Root Cause: Catching BaseException intercepts KeyboardInterrupt, SystemExit, and GeneratorExit.\n"
                    "Defect Impact: Interferes with standard Python process lifecycle management and graceful shutdown."
                ),
                "description": (
                    f"Line {node.lineno} catches 'BaseException' directly.\n"
                    "BaseException is the root of the exception hierarchy and should not be intercepted in general application logic."
                ),
                "bug_fix": (
                    "1. Catch 'Exception' instead of 'BaseException' for standard application-level error handling."
                ),
                "why_it_matters": "Disrupts normal interpreter control flow.",
                "recommendation": "Derive custom exceptions from Exception and avoid catching BaseException directly.",
                "suggested_fix": "except Exception as err:\n    logger.warning(f'Handled expected failure: {err}')",
                "future_guidelines": (
                    "1. Restrict BaseException catches solely to top-level supervisor daemons.\n"
                    "2. Follow standard PEP 352 exception hierarchy guidelines."
                )
            })
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Check mutable default arguments (x=[])
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.issues.append({
                    "type": "Bug",
                    "severity": "High",
                    "line_number": node.lineno,
                    "title": "Mutable Default Argument",
                    "software_defect": (
                        "Defect Classification: Shared Mutable State (CWE-665: Improper Initialization)\n"
                        f"Root Cause: Function '{node.name}' uses a mutable literal (list/dict/set) in its parameter signature.\n"
                        "Defect Impact: Default arguments are bound once at function definition time; mutations accumulate across successive invocations, leading to corrupted state."
                    ),
                    "description": (
                        f"Function '{node.name}' defines a mutable object as a default argument at line {node.lineno}.\n"
                        "State changes made to this collection will unexpectedly persist between subsequent function calls across the process lifetime."
                    ),
                    "bug_fix": (
                        "1. Set default parameter to None in the function signature.\n"
                        "2. Dynamically assign a new collection instance inside the function body if the argument is None."
                    ),
                    "why_it_matters": "Python default arguments are evaluated once at definition time; mutations persist across successive calls.",
                    "recommendation": "Use None as the default argument value and initialize dynamically inside the function body.",
                    "suggested_fix": f"def {node.name}(param=None):\n    if param is None:\n        param = []",
                    "future_guidelines": (
                        "1. Enable Ruff / Pylint rule B006 (Do not use mutable data structures for argument defaults).\n"
                        "2. Use typing.Optional[List[T]] type hints to make optional parameters explicit."
                    )
                })

        # Function length smell
        if hasattr(node, "end_lineno") and node.end_lineno:
            func_len = node.end_lineno - node.lineno
            if func_len > 45:
                self.issues.append({
                    "type": "Maintainability",
                    "severity": "Medium",
                    "line_number": node.lineno,
                    "title": f"Long Method: '{node.name}' ({func_len} lines)",
                    "software_defect": (
                        "Defect Classification: Single Responsibility Principle Violation (ISO 25010 Maintainability Flaw)\n"
                        f"Root Cause: Method '{node.name}' spans {func_len} lines of code.\n"
                        "Defect Impact: Degrades cognitive comprehension, inflates unit testing complexity, and increases defect injection during maintenance."
                    ),
                    "description": (
                        f"Function '{node.name}' spans {func_len} lines of code from line {node.lineno} to line {node.end_lineno}.\n"
                        "Methods exceeding 40 lines typically mix multiple concerns and should be refactored."
                    ),
                    "bug_fix": (
                        "1. Identify independent logical steps within the function.\n"
                        "2. Extract helper sub-functions with clear input/output contracts."
                    ),
                    "why_it_matters": "Methods exceeding 40 lines violate the Single Responsibility Principle and increase regression risk.",
                    "recommendation": "Decompose into smaller helper functions with distinct purposes.",
                    "suggested_fix": "# Extract logical blocks into helper functions\ndef helper_task(data):\n    pass",
                    "future_guidelines": (
                        "1. Cap method length at 35-40 lines across coding standards.\n"
                        "2. Enforce Cyclomatic Complexity linters to guide modular decomposition."
                    )
                })

        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp):
        # Division by zero detection (e.g. 5/0, x // 0, x % 0)
        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
            is_zero = False
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                is_zero = True
            elif isinstance(node.right, ast.UnaryOp) and isinstance(node.right.operand, ast.Constant) and node.right.operand.value == 0:
                is_zero = True

            if is_zero:
                op_name = "Modulo" if isinstance(node.op, ast.Mod) else "Division"
                self.issues.append({
                    "type": "Bug",
                    "severity": "Critical",
                    "line_number": node.lineno,
                    "title": f"Fatal {op_name} by Zero (ZeroDivisionError)",
                    "software_defect": (
                        f"Defect Classification: Divide by Zero (CWE-369: Divide By Zero)\n"
                        f"Root Cause: The right operand of the arithmetic {op_name.lower()} operation is a constant zero.\n"
                        "Defect Impact: In Python, dividing or taking modulo by zero immediately raises an unhandled ZeroDivisionError, crashing the application."
                    ),
                    "description": (
                        f"Line {node.lineno} executes an arithmetic {op_name.lower()} by zero.\n"
                        "This will immediately raise a fatal ZeroDivisionError exception at runtime."
                    ),
                    "bug_fix": (
                        "1. Validate that the divisor is not equal to zero before performing the operation.\n"
                        "2. Provide a default fallback value or raise a handled validation error."
                    ),
                    "why_it_matters": "Division by zero aborts the current process or thread with an unhandled ZeroDivisionError.",
                    "recommendation": "Check that the denominator is non-zero before dividing: if denominator != 0: ...",
                    "suggested_fix": "if denominator != 0:\n    result = numerator / denominator\nelse:\n    result = 0",
                    "future_guidelines": (
                        "1. Implement defensive pre-condition assertions on all arithmetic calculations.\n"
                        "2. Configure Flake8 / Pylint to reject literal division by zero.\n"
                        "3. Add unit tests covering zero-denominator edge cases."
                    )
                })

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Dangerous eval / exec
        if isinstance(node.func, ast.Name):
            if node.func.id in ["eval", "exec"]:
                self.issues.append({
                    "type": "Security",
                    "severity": "Critical",
                    "line_number": node.lineno,
                    "title": f"Arbitrary Code Execution via '{node.func.id}()'",
                    "software_defect": (
                        "Defect Classification: Remote Code Execution / Dynamic Evaluation (CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code)\n"
                        f"Root Cause: Invocation of Python's built-in {node.func.id}() compiles dynamic string input as bytecode.\n"
                        "Defect Impact: An attacker can execute arbitrary system commands, exfiltrate environment credentials, or spawn reverse shells."
                    ),
                    "description": (
                        f"Line {node.lineno} executes '{node.func.id}()' on dynamic input.\n"
                        "Dynamic evaluation exposes the Python runtime environment directly to untrusted data."
                    ),
                    "bug_fix": (
                        "1. Replace eval() with ast.literal_eval() if parsing literal Python primitives (numbers, dicts, lists).\n"
                        "2. Use json.loads() for structured JSON payloads.\n"
                        "3. Use deterministic dispatcher dictionaries instead of dynamic code evaluation."
                    ),
                    "why_it_matters": "Allows attackers to execute arbitrary system commands or extract secrets.",
                    "recommendation": "Replace eval/exec with safe serialization libraries like json.loads or ast.literal_eval.",
                    "suggested_fix": "import ast\nsafe_data = ast.literal_eval(untrusted_str)",
                    "future_guidelines": (
                        "1. Run Bandit security scanner (bandit -r .) in pre-commit hooks to prohibit eval/exec.\n"
                        "2. Restrict dynamic language evaluation strictly in secure development policies."
                    )
                })

        # SQL Injection in cursor.execute with formatting / concat
        if isinstance(node.func, ast.Attribute) and node.func.attr in ["execute", "executemany"]:
            if node.args:
                arg0 = node.args[0]
                if isinstance(arg0, ast.BinOp) and isinstance(arg0.op, ast.Add):
                    self.issues.append({
                        "type": "Security",
                        "severity": "Critical",
                        "line_number": node.lineno,
                        "title": "SQL Injection Risk (String Concatenation in Query)",
                        "software_defect": (
                            "Defect Classification: SQL Injection (CWE-89: Improper Neutralization of Special Elements used in an SQL Command)\n"
                            "Root Cause: SQL statement is dynamically assembled using binary string addition (+) before execution.\n"
                            "Defect Impact: Allows malicious users to manipulate queries, bypass authentication filters, or extract confidential database records."
                        ),
                        "description": (
                            f"Line {node.lineno} concatenates strings directly into database execute().\n"
                            "Untrusted inputs can alter the query semantics, resulting in complete database compromise."
                        ),
                        "bug_fix": (
                            "1. Use parameterized SQL queries with placeholder markers (%s or ?).\n"
                            "2. Pass query parameters as a tuple/list in the second argument of cursor.execute()."
                        ),
                        "why_it_matters": "Attackers can inject malicious SQL payloads to bypass authentication or dump database contents.",
                        "recommendation": "Utilize parameterized query placeholders (e.g., %s or ?).",
                        "suggested_fix": "cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
                        "future_guidelines": (
                            "1. Mandate ORMs (SQLAlchemy, Django ORM) or strictly parameterized database drivers.\n"
                            "2. Run automated static analysis for SQL injection (Bandit B608) in CI/CD."
                        )
                    })
                elif isinstance(arg0, ast.JoinedStr):
                    self.issues.append({
                        "type": "Security",
                        "severity": "Critical",
                        "line_number": node.lineno,
                        "title": "SQL Injection Risk (F-String in Query)",
                        "software_defect": (
                            "Defect Classification: SQL Injection (CWE-89)\n"
                            "Root Cause: F-string interpolation formats dynamic parameters directly into SQL command text.\n"
                            "Defect Impact: Bypasses parameter escaping mechanisms, allowing SQL command alteration."
                        ),
                        "description": (
                            f"Line {node.lineno} uses an interpolated f-string directly inside execute().\n"
                            "Formatted strings are evaluated prior to database driver processing, disabling sanitization."
                        ),
                        "bug_fix": (
                            "1. Replace f-string with parameterized query syntax and pass arguments separately."
                        ),
                        "why_it_matters": "Variables interpolated into queries circumvent parameter sanitization.",
                        "recommendation": "Pass parameters as tuple arguments to the database driver.",
                        "suggested_fix": "cursor.execute('SELECT * FROM table WHERE col = %s', (param,))",
                        "future_guidelines": (
                            "1. Disallow raw string formatting in database execution functions."
                        )
                    })

        self.generic_visit(node)

def analyze_python(code: str) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    try:
        tree = ast.parse(code)
        visitor = PythonASTAnalyzer(code)
        visitor.visit(tree)
        issues.extend(visitor.issues)
    except SyntaxError as e:
        issues.append({
            "type": "Bug",
            "severity": "Critical",
            "line_number": e.lineno or 1,
            "title": "Syntax Error",
            "software_defect": (
                "Defect Classification: Fatal Syntax Malformation (CWE-1164)\n"
                f"Root Cause: Python parser encountered invalid syntax: {e.msg}\n"
                "Defect Impact: Code cannot be compiled into bytecode and will immediately abort execution."
            ),
            "description": f"Python syntax error encountered at line {e.lineno or 1}: {e.msg}",
            "bug_fix": "1. Verify balanced brackets, quotation marks, and indentation block structure.",
            "why_it_matters": "Code fails to parse and will trigger a fatal SyntaxError at runtime.",
            "recommendation": "Check parenthesis closure, colon indentation, and keyword syntax.",
            "suggested_fix": e.text.strip() if e.text else "",
            "future_guidelines": "1. Set up pre-commit hook running 'python -m py_compile' to ensure syntactic validity."
        })

    # Regex security patterns and syntax-tolerant checks
    lines = code.splitlines()
    for idx, line in enumerate(lines, 1):
        # Division by zero pattern: e.g. 5/0, x / 0, 5/0;
        clean_line = line.split("#")[0] # ignore python comments
        if re.search(r"(?<!/)/(?!/)\s*0+(?:\.0+)?(?:\b|;|,\s*|\))", clean_line) or re.search(r"%\s*0+(?:\.0+)?(?:\b|;|,\s*|\))", clean_line):
            # Avoid duplicate if AST already flagged it
            if not any(iss.get("line_number") == idx and "Zero" in iss.get("title", "") for iss in issues):
                issues.append({
                    "type": "Bug",
                    "severity": "Critical",
                    "line_number": idx,
                    "title": "Fatal Division by Zero (ZeroDivisionError)",
                    "software_defect": (
                        "Defect Classification: Divide by Zero (CWE-369: Divide By Zero)\n"
                        "Root Cause: Denominator expression evaluates to literal zero.\n"
                        "Defect Impact: Causes an immediate fatal ZeroDivisionError exception, crashing the process."
                    ),
                    "description": f"Line {idx} performs an arithmetic division or modulo by zero.",
                    "bug_fix": "1. Verify denominator is non-zero before division using a guard clause.",
                    "why_it_matters": "Division by zero triggers an unhandled ZeroDivisionError at runtime, aborting execution.",
                    "recommendation": "Check that the denominator is non-zero before dividing.",
                    "suggested_fix": "if denominator != 0:\n    result = numerator / denominator\nelse:\n    result = 0",
                    "future_guidelines": "1. Add unit tests covering zero-denominator boundary conditions."
                })

        if re.search(r"(?:api_key|password|secret|jwt_secret)\s*=\s*['\"][A-Za-z0-9_\-]{6,}['\"]", line, re.IGNORECASE):
            issues.append({
                "type": "Security",
                "severity": "High",
                "line_number": idx,
                "title": "Hardcoded Secret / Credential",
                "software_defect": (
                    "Defect Classification: Hardcoded Credential (CWE-798: Use of Hard-coded Credentials)\n"
                    "Root Cause: Plaintext credentials or secret tokens embedded directly in the source file.\n"
                    "Defect Impact: Stored credentials can be extracted through version control history, container images, or code leaks."
                ),
                "description": f"Line {idx} defines a hardcoded secret token or credential literal.",
                "bug_fix": (
                    "1. Extract the secret from source code into an environment variable.\n"
                    "2. Read using os.getenv() or a secret management service (HashiCorp Vault / AWS Secrets Manager)."
                ),
                "why_it_matters": "Credentials checked into source control are easily compromised.",
                "recommendation": "Store sensitive keys in environment variables or a secrets manager.",
                "suggested_fix": "import os\napi_key = os.getenv('API_KEY')",
                "future_guidelines": (
                    "1. Add TruffleHog / GitGuardian / Gitleaks to git pre-commit hooks.\n"
                    "2. Ensure all .env files are included in .gitignore."
                )
            })

    return issues

def analyze_javascript(code: str) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    lines = code.splitlines()

    for idx, line in enumerate(lines, 1):
        # Division by zero
        clean_js = line.split("//")[0]
        if re.search(r"(?<!/)/(?!/)\s*0+(?:\.0+)?(?:\b|;|,\s*|\))", clean_js) or re.search(r"%\s*0+(?:\.0+)?(?:\b|;|,\s*|\))", clean_js):
            issues.append({
                "type": "Bug",
                "severity": "High",
                "line_number": idx,
                "title": "Division by Zero (Produces Infinity / NaN)",
                "software_defect": (
                    "Defect Classification: Divide by Zero / Invalid Arithmetic (CWE-369: Divide By Zero)\n"
                    "Root Cause: Division or modulo operation with constant zero denominator.\n"
                    "Defect Impact: In JavaScript, dividing by zero evaluates to Infinity or NaN, causing numerical calculation errors and serialization corruption."
                ),
                "description": f"Line {idx} divides by zero, producing Infinity or NaN at runtime.",
                "bug_fix": "1. Guard against zero denominator before dividing: if (divisor !== 0) { ... }.",
                "why_it_matters": "Produces Infinity or NaN, corrupting application numerical state.",
                "recommendation": "Check divisor before division.",
                "suggested_fix": "const result = divisor !== 0 ? numerator / divisor : 0;",
                "future_guidelines": "1. Enforce mathematical validation checks in calculations."
            })

        # Loose equality
        if re.search(r"[^!=]==(?!=)", line):
            issues.append({
                "type": "Code Smell",
                "severity": "Low",
                "line_number": idx,
                "title": "Loose Equality Operator (==)",
                "software_defect": (
                    "Defect Classification: Type Coercion Bug (CWE-1024)\n"
                    "Root Cause: Use of loose equality operator (==) instead of strict equality (===).\n"
                    "Defect Impact: Triggers implicit JavaScript type coercion, causing unpredictable truthiness comparisons."
                ),
                "description": f"Line {idx} uses loose equality '==', which coerces dissimilar types implicitly.",
                "bug_fix": "1. Replace '==' with strict equality operator '===' and '!=' with '!=='.",
                "why_it_matters": "Type coercion in JavaScript causes unpredictable logic defects (e.g. 0 == '0' is true).",
                "recommendation": "Always enforce strict equality checking using '===' and '!=='.",
                "suggested_fix": line.replace("==", "==="),
                "future_guidelines": "1. Configure ESLint rule 'eqeqeq': ['error', 'always']."
            })

        # Eval
        if re.search(r"\beval\s*\(", line):
            issues.append({
                "type": "Security",
                "severity": "Critical",
                "line_number": idx,
                "title": "Dangerous eval() Execution",
                "software_defect": (
                    "Defect Classification: Dynamic Code Injection (CWE-95)\n"
                    "Root Cause: JavaScript eval() compiles and executes arbitrary script in caller context.\n"
                    "Defect Impact: Enables Cross-Site Scripting (XSS) and client/server-side code injection."
                ),
                "description": f"Line {idx} contains an invocation of eval().",
                "bug_fix": "1. Replace eval with JSON.parse() or deterministic dispatchers.",
                "why_it_matters": "Major vector for Cross-Site Scripting (XSS) and code injection.",
                "recommendation": "Parse data with JSON.parse() or use deterministic lookup maps.",
                "suggested_fix": "const data = JSON.parse(jsonString);",
                "future_guidelines": "1. Set Content-Security-Policy (CSP) with 'unsafe-eval' blocked."
            })

        # Hardcoded credentials
        if re.search(r"(?:apiKey|password|secret)\s*:\s*['\"][A-Za-z0-9_\-]{6,}['\"]", line, re.IGNORECASE):
            issues.append({
                "type": "Security",
                "severity": "High",
                "line_number": idx,
                "title": "Hardcoded Token or Secret",
                "software_defect": (
                    "Defect Classification: Hardcoded Credential (CWE-798)\n"
                    "Root Cause: Plaintext credential found in client-side script.\n"
                    "Defect Impact: Credentials delivered to browser clients can be harvested by end users and attackers."
                ),
                "description": f"Line {idx} contains hardcoded API key or credential literal.",
                "bug_fix": "1. Load keys via process.env or import.meta.env on server/build layer.",
                "why_it_matters": "Client-side or repository exposed secrets can be harvested by attackers.",
                "recommendation": "Load from process.env or secret storage.",
                "suggested_fix": "const secret = process.env.API_KEY;",
                "future_guidelines": "1. Never bundle production secret tokens into front-end build artifacts."
            })

    return issues

def analyze_cpp(code: str) -> List[Dict[str, Any]]:
    """
    Comprehensive C++ Static Analysis Engine.
    Detects memory safety issues, buffer overflows, resource leaks, exception slicing, and unsafe calls.
    """
    issues: List[Dict[str, Any]] = []
    lines = code.splitlines()

    has_new = False
    has_delete = bool(re.search(r"\bdelete(\[\])?\s+\w+", code))
    new_line_idx = 1

    for idx, line in enumerate(lines, 1):
        # Division by zero (CWE-369 / Undefined Behavior)
        clean_cpp = line.split("//")[0]
        if re.search(r"(?<!/)/(?!/)\s*0+(?:\.0+)?(?:\b|;|,\s*|\))", clean_cpp) or re.search(r"%\s*0+(?:\.0+)?(?:\b|;|,\s*|\))", clean_cpp):
            issues.append({
                "type": "Bug",
                "severity": "Critical",
                "line_number": idx,
                "title": "Fatal Division by Zero (Undefined Behavior / Crash)",
                "software_defect": (
                    "Defect Classification: Divide by Zero / Undefined Behavior (CWE-369: Divide By Zero)\n"
                    "Root Cause: The divisor in an integer division or modulo operation is zero.\n"
                    "Defect Impact: In C/C++, integer division by zero invokes Undefined Behavior (UB), triggering a hardware trap SIGFPE (Floating Point Exception) that crashes the process."
                ),
                "description": (
                    f"Line {idx} contains an arithmetic division or modulo by constant zero: '{line.strip()}'.\n"
                    "Dividing by zero is Undefined Behavior in C++ and causes an immediate fatal crash."
                ),
                "bug_fix": (
                    "1. Guard against zero denominator before dividing: if (denominator != 0) { ... }\n"
                    "2. Handle the zero denominator safely by returning an error or default value."
                ),
                "why_it_matters": "Invokes Undefined Behavior and triggers a fatal SIGFPE process crash.",
                "recommendation": "Check that the divisor is non-zero before performing division.",
                "suggested_fix": (
                    "if (denominator != 0) {\n"
                    "    result = numerator / denominator;\n"
                    "} else {\n"
                    "    // Handle division by zero safely\n"
                    "}"
                ),
                "future_guidelines": (
                    "1. Compile with '-fsanitize=integer-divide-by-zero,undefined' to trap zero divisions in CI.\n"
                    "2. Apply defensive programming assertions to all divisor variables."
                )
            })

        # 1. Unbounded Buffer Copy (CWE-120)
        buffer_func_match = re.search(r"\b(strcpy|gets|strcat|sprintf|vsprintf)\s*\(", line)
        if buffer_func_match:
            func_name = buffer_func_match.group(1)
            issues.append({
                "type": "Security",
                "severity": "Critical",
                "line_number": idx,
                "title": f"Unbounded Buffer Operation via '{func_name}()'",
                "software_defect": (
                    f"Defect Classification: Stack Buffer Overflow (CWE-120: Buffer Copy without Checking Size of Input)\n"
                    f"Root Cause: The legacy C function '{func_name}()' copies memory until encountering a null terminator without verifying destination capacity.\n"
                    "Defect Impact: Overwrites adjacent stack frames, causing memory corruption, denial of service crashes, or arbitrary code execution."
                ),
                "description": (
                    f"Line {idx} calls '{func_name}()' without destination buffer bounds enforcement.\n"
                    "If the source input exceeds the destination size, it triggers a catastrophic buffer overflow."
                ),
                "bug_fix": (
                    "1. For C++: Use std::string or std::vector<char> for automated dynamic memory management.\n"
                    "2. For bounded C APIs: Replace strcpy with strncpy_s / strncpy, and sprintf with snprintf."
                ),
                "why_it_matters": "Buffer overruns lead to stack corruption, denial of service, and arbitrary code execution.",
                "recommendation": "Use bounded alternatives such as strncpy_s, snprintf, or std::string.",
                "suggested_fix": (
                    "// Safe C++ alternative:\n"
                    "strncpy(dest, src, sizeof(dest) - 1);\n"
                    "dest[sizeof(dest) - 1] = '\\0';"
                ),
                "future_guidelines": (
                    "1. Enable compiler flags: -Wall -Wextra -Wformat-security -D_FORTIFY_SOURCE=2.\n"
                    "2. Run AddressSanitizer (-fsanitize=address) during unit test runs.\n"
                    "3. Standardize on modern C++ STL containers (std::string, std::array) over raw char buffers."
                )
            })

        # Track heap allocations
        if re.search(r"\bnew\s+\w+(\[|\s*)", line):
            has_new = True
            new_line_idx = idx

        # 2. Raw pointer dynamic allocation without smart pointers
        if re.search(r"\w+\*\s+\w+\s*=\s*new\s+", line):
            issues.append({
                "type": "Code Smell",
                "severity": "Medium",
                "line_number": idx,
                "title": "Raw Pointer Heap Allocation (Lack of RAII)",
                "software_defect": (
                    "Defect Classification: Resource Management Flaw (CWE-401: Missing Release of Memory)\n"
                    "Root Cause: Dynamic memory is allocated using raw 'new' instead of smart pointers (std::unique_ptr).\n"
                    "Defect Impact: High risk of memory leaks if exceptions occur before manual delete is executed."
                ),
                "description": (
                    f"Line {idx} performs dynamic heap allocation assigned to a raw pointer.\n"
                    "Raw pointers require manual deallocation and violate modern C++ RAII (Resource Acquisition Is Initialization) idioms."
                ),
                "bug_fix": (
                    "1. Replace raw pointer with std::unique_ptr or std::shared_ptr.\n"
                    "2. Use std::make_unique<T>() to allocate objects safely."
                ),
                "why_it_matters": "Raw pointer ownership frequently results in memory leaks and dangling pointers.",
                "recommendation": "Use std::unique_ptr or std::make_unique for automatic lifetime management.",
                "suggested_fix": "auto obj = std::make_unique<TargetType>();",
                "future_guidelines": (
                    "1. Follow C++ Core Guidelines rule R.11: Avoid calling new and delete explicitly.\n"
                    "2. Integrate Clang-Tidy check 'modernize-make-unique' into build workflows."
                )
            })

        # 3. Exception Slicing / Catching Exception by Value (CWE-398)
        if re.search(r"catch\s*\(\s*(?:std::)?(?:exception|runtime_error|invalid_argument|logic_error)\s+\w+\s*\)", line):
            issues.append({
                "type": "Bug",
                "severity": "High",
                "line_number": idx,
                "title": "Exception Caught by Value (Object Slicing Risk)",
                "software_defect": (
                    "Defect Classification: Object Slicing (CWE-398: Indicator of Poor Code Quality)\n"
                    "Root Cause: Exception object is caught by value rather than by constant reference ('const std::exception&').\n"
                    "Defect Impact: Slices the derived exception object, stripping polymorphic methods, type identity, and diagnostic details."
                ),
                "description": (
                    f"Line {idx} catches an exception by value.\n"
                    "Catching by value constructs a copy and slices away polymorphic subclass behavior."
                ),
                "bug_fix": (
                    "1. Change catch signature to catch by const reference: catch (const std::exception& e)."
                ),
                "why_it_matters": "Slices derived exception classes and invokes unnecessary copy constructors.",
                "recommendation": "Catch exceptions by const reference ('catch (const std::exception& e)').",
                "suggested_fix": "catch (const std::exception& e) {\n    std::cerr << e.what() << std::endl;\n}",
                "future_guidelines": (
                    "1. Enable compiler warning -Wcatch-value.\n"
                    "2. Enforce C++ Core Guidelines E.15: Catch exception types by reference."
                )
            })

        # 4. Dangerous system() invocation (CWE-78)
        if re.search(r"\b(system|popen)\s*\(", line):
            issues.append({
                "type": "Security",
                "severity": "Critical",
                "line_number": idx,
                "title": "Command Injection Risk via 'system()'",
                "software_defect": (
                    "Defect Classification: Command Injection (CWE-78: OS Command Injection)\n"
                    "Root Cause: Invocation of system() or popen() delegates command strings to the underlying shell (/bin/sh or cmd.exe).\n"
                    "Defect Impact: Attackers can append shell metacharacters (;, &&, |) to execute arbitrary OS commands."
                ),
                "description": f"Line {idx} executes external shell commands via system().",
                "bug_fix": "1. Replace shell execution with direct execvp / CreateProcess APIs with un-interpolated argument arrays.",
                "why_it_matters": "Allows unconstrained command execution if arguments originate from untrusted input.",
                "recommendation": "Avoid system(); invoke specific binaries using execvp or POSIX spawn.",
                "suggested_fix": "// Use execvp with explicit arguments vector",
                "future_guidelines": "1. Prohibit system() calls in production software architectures."
            })

    # Memory leak check: has new but no delete
    if has_new and not has_delete:
        issues.append({
            "type": "Bug",
            "severity": "High",
            "line_number": new_line_idx,
            "title": "Potential Memory Leak (Heap Allocation Without Deallocation)",
            "software_defect": (
                "Defect Classification: Memory Leak (CWE-401: Missing Release of Memory after Effective Lifetime)\n"
                "Root Cause: Heap memory allocated via 'new' has no matching 'delete' or 'delete[]' deallocation path.\n"
                "Defect Impact: Cumulative heap consumption causes application memory bloat, paging thrash, and eventual Out-Of-Memory (OOM) termination."
            ),
            "description": (
                f"Dynamic heap memory allocated at line {new_line_idx} is never released.\n"
                "The module lacks corresponding delete or delete[] statements."
            ),
            "bug_fix": (
                "1. If using raw memory, ensure delete[] is invoked on every exit path.\n"
                "2. Preferably, replace dynamic raw allocation with std::unique_ptr or std::vector."
            ),
            "why_it_matters": "Unreleased heap memory causes memory exhaustion and service failure over prolonged runtimes.",
            "recommendation": "Manage heap memory with std::unique_ptr or ensure delete[] is called.",
            "suggested_fix": "delete[] dynamic_buffer; // Or migrate to std::unique_ptr<char[]>",
            "future_guidelines": (
                "1. Run Valgrind (valgrind --leak-check=full) or LLVM LeakSanitizer in CI test suites.\n"
                "2. Standardize on zero-raw-pointer policies in code reviews."
            )
        })

    return issues

def analyze_java(code: str) -> List[Dict[str, Any]]:
    """
    Comprehensive Java Static Analysis Engine.
    Detects SQL injection, resource leaks, hardcoded credentials, swallowed exceptions, and equality bugs.
    """
    issues: List[Dict[str, Any]] = []
    lines = code.splitlines()

    for idx, line in enumerate(lines, 1):
        # Division by zero (CWE-369 / java.lang.ArithmeticException)
        clean_java = line.split("//")[0]
        if re.search(r"(?<!/)/(?!/)\s*0+(?:\.0+)?(?:\b|;|,\s*|\))", clean_java) or re.search(r"%\s*0+(?:\.0+)?(?:\b|;|,\s*|\))", clean_java):
            issues.append({
                "type": "Bug",
                "severity": "Critical",
                "line_number": idx,
                "title": "Fatal Division by Zero (java.lang.ArithmeticException)",
                "software_defect": (
                    "Defect Classification: Divide by Zero (CWE-369: Divide By Zero)\n"
                    "Root Cause: Integer division or remainder operation with a literal zero denominator.\n"
                    "Defect Impact: In Java, integer division by zero throws an unchecked java.lang.ArithmeticException: / by zero, immediately crashing the thread."
                ),
                "description": (
                    f"Line {idx} performs integer division or modulo by zero: '{line.strip()}'.\n"
                    "This triggers a fatal java.lang.ArithmeticException at runtime."
                ),
                "bug_fix": (
                    "1. Validate that the divisor is non-zero before division: if (divisor != 0) { ... }\n"
                    "2. Provide appropriate fallback handling or throw a checked validation exception."
                ),
                "why_it_matters": "Throws an unhandled ArithmeticException: / by zero that crashes the executing thread.",
                "recommendation": "Validate that the denominator is not zero prior to division.",
                "suggested_fix": (
                    "if (divisor != 0) {\n"
                    "    int result = numerator / divisor;\n"
                    "} else {\n"
                    "    // Safe fallback handling\n"
                    "}"
                ),
                "future_guidelines": (
                    "1. Configure SpotBugs rule for division by zero.\n"
                    "2. Implement defensive zero-checks on all user-supplied arithmetic parameters."
                )
            })

        # 1. SQL Injection via Statement string concatenation (CWE-89)
        if re.search(r"stmt\.execute(?:Query|Update)?\s*\(.*['\"]\s*\+", line) or \
           re.search(r"createStatement\(\).*\.execute", line) or \
           (re.search(r"SELECT\s+.*FROM\s+.*WHERE\s+.*['\"]\s*\+", line, re.IGNORECASE)):
            issues.append({
                "type": "Security",
                "severity": "Critical",
                "line_number": idx,
                "title": "SQL Injection Risk (Dynamic Query Concatenation)",
                "software_defect": (
                    "Defect Classification: SQL Injection (CWE-89: Improper Neutralization of Special Elements used in an SQL Command)\n"
                    "Root Cause: java.sql.Statement query is constructed via string concatenation with dynamic parameter input.\n"
                    "Defect Impact: Attackers can inject arbitrary SQL payloads to bypass access controls, dump database contents, or modify records."
                ),
                "description": (
                    f"Line {idx} executes a dynamically concatenated SQL query.\n"
                    "Using java.sql.Statement with string concatenation enables SQL injection attacks."
                ),
                "bug_fix": (
                    "1. Replace java.sql.Statement with java.sql.PreparedStatement.\n"
                    "2. Use positional parameter placeholders (?) and bind variables with pstmt.setString() / pstmt.setInt()."
                ),
                "why_it_matters": "Enables malicious users to execute arbitrary database commands and extract sensitive records.",
                "recommendation": "Use PreparedStatement with parameterized query placeholders (?).",
                "suggested_fix": (
                    "String sql = \"SELECT * FROM reports WHERE category = ?\";\n"
                    "PreparedStatement pstmt = conn.prepareStatement(sql);\n"
                    "pstmt.setString(1, filter);\n"
                    "ResultSet rs = pstmt.executeQuery();"
                ),
                "future_guidelines": (
                    "1. Mandate JPA / Hibernate or PreparedStatement across enterprise persistence layers.\n"
                    "2. Enable SpotBugs check 'SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE' in Maven/Gradle builds."
                )
            })

        # 2. Hardcoded Database Credentials / Secrets (CWE-798)
        if re.search(r"(?:DriverManager\.getConnection\(.*password\s*=\s*)|(?:String\s+(?:DB_PASS|password|apiKey|secret)\s*=\s*['\"][^'\"]+['\"])", line, re.IGNORECASE):
            issues.append({
                "type": "Security",
                "severity": "High",
                "line_number": idx,
                "title": "Hardcoded Database Credentials / Secret",
                "software_defect": (
                    "Defect Classification: Hardcoded Credential (CWE-798: Use of Hard-coded Credentials)\n"
                    "Root Cause: Plaintext database password or API secret is embedded directly in Java source code.\n"
                    "Defect Impact: Credentials can be extracted from compiled .class bytecode, decompiled artifacts, or git repositories."
                ),
                "description": (
                    f"Line {idx} defines a hardcoded database password or secret token literal."
                ),
                "bug_fix": (
                    "1. Retrieve secrets from environment variables using System.getenv().\n"
                    "2. Or inject configuration via Spring Boot application.properties or Vault."
                ),
                "why_it_matters": "Exposes credentials to anyone with bytecode, container, or repository access.",
                "recommendation": "Use environment variables (System.getenv) or Spring configuration vault.",
                "suggested_fix": "String dbPass = System.getenv(\"DB_PASSWORD\");",
                "future_guidelines": (
                    "1. Use Spring Cloud Vault or AWS Secrets Manager for secret injection.\n"
                    "2. Run automated credential scanners (Gitleaks) in CI/CD pipelines."
                )
            })

        # 3. Unclosed I/O Resources / Missing Try-With-Resources (CWE-775 / CWE-404)
        if re.search(r"new\s+(?:BufferedWriter|BufferedReader|FileWriter|FileReader|FileInputStream|FileOutputStream)\s*\(", line):
            # Check if wrapped in try-with-resources
            if "try (" not in line and "try(" not in line:
                issues.append({
                    "type": "Code Smell",
                    "severity": "Medium",
                    "line_number": idx,
                    "title": "Unclosed Resource (Missing Try-With-Resources)",
                    "software_defect": (
                        "Defect Classification: Resource Leak (CWE-775: Missing Release of Resource after Effective Lifetime)\n"
                        "Root Cause: Stream or Writer resource is instantiated without Java 7+ try-with-resources statement.\n"
                        "Defect Impact: If an exception occurs, the file descriptor or network socket remains open, exhausting OS handles."
                    ),
                    "description": (
                        f"Line {idx} allocates an AutoCloseable I/O resource without try-with-resources.\n"
                        "If an exception is thrown before explicit close(), the underlying OS file handle leaks."
                    ),
                    "bug_fix": (
                        "1. Enclose the resource instantiation within try (Resource res = new Resource(...)) { ... } block."
                    ),
                    "why_it_matters": "Leaked file descriptors and socket handles cause OS resource exhaustion and application crashes.",
                    "recommendation": "Wrap all AutoCloseable resources in try-with-resources statements.",
                    "suggested_fix": (
                        "try (BufferedWriter writer = new BufferedWriter(new FileWriter(path))) {\n"
                        "    writer.write(data);\n"
                        "}"
                    ),
                    "future_guidelines": (
                        "1. Enforce try-with-resources for all AutoCloseable types via Checkstyle or SpotBugs.\n"
                        "2. Configure SonarQube rule java:S2095 (Resources should be closed)."
                    )
                })

        # 4. Swallowed / Generic Exception Handling (CWE-391)
        if re.search(r"catch\s*\(\s*(?:Exception|Throwable)\s+\w+\s*\)", line):
            issues.append({
                "type": "Bug",
                "severity": "Medium",
                "line_number": idx,
                "title": "Generic Exception Catch & Swallowing",
                "software_defect": (
                    "Defect Classification: Broad Catch Block (CWE-396: Declaration of Catch for Generic Exception)\n"
                    "Root Cause: Catching generic java.lang.Exception or Throwable.\n"
                    "Defect Impact: Obscures specific failure modes, swallows unexpected runtime errors, and impedes diagnosis."
                ),
                "description": (
                    f"Line {idx} catches generic 'Exception'.\n"
                    "Catching broad exceptions intercepts unintended RuntimeExceptions (such as NullPointerException)."
                ),
                "bug_fix": (
                    "1. Catch specific checked exceptions (e.g. SQLException, IOException).\n"
                    "2. Log with structured logging framework (SLF4J / Logback) instead of System.out.println or e.printStackTrace()."
                ),
                "why_it_matters": "Hides specific errors and interferes with proper error handling and retry workflows.",
                "recommendation": "Catch specific exceptions (SQLException, IOException) and log via SLF4J.",
                "suggested_fix": "catch (SQLException | IOException e) {\n    logger.error(\"Operation failed: {}\", e.getMessage(), e);\n}",
                "future_guidelines": (
                    "1. Configure Checkstyle rule 'IllegalCatch' to forbid catching Exception/Throwable.\n"
                    "2. Mandate SLF4J structured logging standards."
                )
            })

        # 5. String equality using == instead of .equals() (CWE-595)
        if re.search(r"\b[a-zA-Z_]\w*\s*==\s*['\"][^'\"]*['\"]", line) or re.search(r"['\"][^'\"]*['\"]\s*==\s*[a-zA-Z_]\w*", line):
            issues.append({
                "type": "Bug",
                "severity": "High",
                "line_number": idx,
                "title": "String Comparison Using Reference Equality ('==')",
                "software_defect": (
                    "Defect Classification: Object Reference Comparison (CWE-595: Comparison of Object References Instead of Object Contents)\n"
                    "Root Cause: Comparing String literals or objects with '==' checks memory addresses rather than content equality.\n"
                    "Defect Impact: Evaluates to false for Strings with identical character sequences if they reside at different memory addresses."
                ),
                "description": (
                    f"Line {idx} compares strings using reference equality '=='.\n"
                    "In Java, '==' tests whether references point to the exact same memory object, causing intermittent comparison bugs."
                ),
                "bug_fix": (
                    "1. Replace '==' with '.equals()' or Objects.equals(a, b)."
                ),
                "why_it_matters": "Causes subtle logic errors when strings are allocated dynamically outside the string pool.",
                "recommendation": "Always use .equals() or Objects.equals() to compare Java objects.",
                "suggested_fix": "if (\"targetValue\".equals(variable)) { ... }",
                "future_guidelines": (
                    "1. Enable SpotBugs rule 'ES_COMPARING_STRINGS_WITH_EQ'.\n"
                    "2. Adopt 'Yoda conditions' (constant.equals(variable)) to avoid NullPointerExceptions."
                )
            })

    return issues

def run_static_analysis(code: str, language: str = "python") -> List[Dict[str, Any]]:
    """Execute static analysis based on source code language."""
    lang = (language or "python").lower()
    if lang in ["python", "py"]:
        return analyze_python(code)
    elif lang in ["javascript", "js", "typescript", "ts"]:
        return analyze_javascript(code)
    elif lang in ["cpp", "c", "h", "hpp"]:
        return analyze_cpp(code)
    elif lang in ["java"]:
        return analyze_java(code)
    else:
        return analyze_python(code)
