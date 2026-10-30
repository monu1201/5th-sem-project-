"""
Feature extraction module for Software Defect Prediction.
Extracts static metrics (McCabe, Halstead, Line metrics, OO metrics, Smells)
from source code across Python, JavaScript, Java, and C++.
"""

import ast
import re
import math
from typing import Dict, Any, List

FEATURE_NAMES = [
    "loc",
    "sloc",
    "comment_lines",
    "blank_lines",
    "cyclomatic_complexity",
    "max_nesting_depth",
    "num_functions",
    "num_classes",
    "avg_func_loc",
    "halstead_volume",
    "halstead_difficulty",
    "code_smell_indicators",
    "security_risk_indicators"
]

def extract_code_metrics(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Extract comprehensive software engineering metrics from source code.
    """
    lang = (language or "python").lower()
    lines = code.splitlines()
    loc = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())
    
    # Detect comment lines
    comment_lines = 0
    in_block_comment = False
    for line in lines:
        stripped = line.strip()
        if lang in ["python"]:
            if stripped.startswith("#"):
                comment_lines += 1
            elif stripped.startswith('"""') or stripped.startswith("'''"):
                comment_lines += 1
        else: # c-style: js, java, cpp
            if in_block_comment:
                comment_lines += 1
                if "*/" in stripped:
                    in_block_comment = False
            elif stripped.startswith("//"):
                comment_lines += 1
            elif "/*" in stripped:
                comment_lines += 1
                if "*/" not in stripped:
                    in_block_comment = True

    sloc = max(0, loc - blank_lines - comment_lines)

    # Nesting depth & indentation
    max_nesting = 0
    current_indent = 0
    for line in lines:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        current_indent = indent // 4 if indent >= 4 else (indent // 2)
        if current_indent > max_nesting:
            max_nesting = min(current_indent, 15)

    # Cyclomatic Complexity & AST metrics
    complexity = 1.0
    num_functions = 0
    num_classes = 0
    smell_indicators = 0
    security_indicators = 0

    if lang == "python":
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    num_functions += 1
                    # Function length smell
                    if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                        if (node.end_lineno - node.lineno) > 40:
                            smell_indicators += 1
                    # Too many args smell
                    if len(node.args.args) > 5:
                        smell_indicators += 1
                elif isinstance(node, ast.ClassDef):
                    num_classes += 1
                elif isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With, ast.Assert)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
                # Security indicators
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ["eval", "exec", "compile"]:
                            security_indicators += 1
        except Exception:
            # Fallback regex if AST parsing encounters syntax error
            complexity += len(re.findall(r"\b(if|elif|while|for|except|catch)\b", code))
            num_functions = len(re.findall(r"\bdef\s+\w+", code))
            num_classes = len(re.findall(r"\bclass\s+\w+", code))
    else:
        # C-family syntax (JavaScript, Java, C++)
        branch_matches = re.findall(r"\b(if|else\s+if|for|while|case|catch|\?\s*[^:]+:)\b", code)
        complexity += len(branch_matches)
        
        func_patterns = [
            r"function\s+\w+\s*\(",
            r"\w+\s*\([^)]*\)\s*\{",
            r"const\s+\w+\s*=\s*\(?[^)]*\)?\s*=>",
            r"(public|private|protected|static|\w+)\s+[\w<>\[\]]+\s+\w+\s*\([^)]*\)\s*\{"
        ]
        num_functions = sum(len(re.findall(p, code)) for p in func_patterns)
        num_classes = len(re.findall(r"\bclass\s+\w+", code))

    # Halstead estimation
    # Operators & Operands token approximation
    operators = re.findall(r"[+\-*/%=&|<>!^~]+|\b(if|else|return|while|for|class|function|def|var|let|const|import)\b", code)
    operands = re.findall(r"\b[a-zA-Z_]\w*\b|\b\d+(\.\d+)?\b", code)
    
    n1 = len(set(operators)) or 1
    n2 = len(set(operands)) or 1
    N1 = len(operators) or 1
    N2 = len(operands) or 1
    
    vocabulary = n1 + n2
    length = N1 + N2
    volume = round(length * math.log2(max(vocabulary, 2)), 2)
    difficulty = round((n1 / 2.0) * (N2 / max(n2, 1)), 2)

    # General smells & security heuristics
    if max_nesting >= 4:
        smell_indicators += (max_nesting - 3)
    if loc > 300:
        smell_indicators += 2

    # Common security patterns across languages
    sec_patterns = [
        r"(SELECT|INSERT|UPDATE|DELETE).*\+.*", # SQL concat
        r"password\s*=\s*['\"][^'\"]+['\"]",   # hardcoded secret
        r"api_key\s*=\s*['\"][^'\"]+['\"]",
        r"\b(system|popen|spawn)\s*\(",        # command injection
        r"dangerouslySetInnerHTML",
        r"\b(strcpy|strcat|gets)\s*\("          # c buffer overflow
    ]
    for sp in sec_patterns:
        if re.search(sp, code, re.IGNORECASE):
            security_indicators += 1

    avg_func_loc = round(sloc / max(num_functions, 1), 2)

    return {
        "loc": loc,
        "sloc": sloc,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines,
        "cyclomatic_complexity": round(float(complexity), 2),
        "max_nesting_depth": max_nesting,
        "num_functions": num_functions,
        "num_classes": num_classes,
        "avg_func_loc": avg_func_loc,
        "halstead_volume": volume,
        "halstead_difficulty": difficulty,
        "code_smell_indicators": smell_indicators,
        "security_risk_indicators": security_indicators
    }

def metrics_to_feature_vector(metrics: Dict[str, Any]) -> List[float]:
    """Convert metrics dictionary into standardized feature vector array."""
    return [float(metrics.get(feat, 0.0)) for feat in FEATURE_NAMES]
