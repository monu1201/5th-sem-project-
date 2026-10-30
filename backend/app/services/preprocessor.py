"""
Code Preprocessing Service.
Handles language detection, size validation, AST parsing, and metric generation.
Ensures submitted code is treated as untrusted data and is never executed.
"""

import os
import re
from typing import Dict, Any, Tuple
from ml.feature_extraction import extract_code_metrics

MAX_CODE_SIZE_BYTES = 500 * 1024  # 500 KB limit for security and stability

EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "cpp",
    ".h": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".rb": "ruby",
    ".php": "php",
    ".sql": "sql",
}

def detect_language(filename: str = "", code: str = "") -> str:
    """Detect language from filename extension or code syntax signatures."""
    if filename:
        ext = os.path.splitext(filename)[1].lower()
        if ext in EXTENSION_LANGUAGE_MAP:
            return EXTENSION_LANGUAGE_MAP[ext]

    # Heuristic detection from code tokens
    code_strip = code.strip()
    if re.search(r"^\s*def\s+\w+\s*\(|^\s*import\s+\w+|^\s*from\s+\w+\s+import", code, re.MULTILINE):
        return "python"
    elif re.search(r"^\s*(const|let|var)\s+\w+|function\s*\w*\s*\(|console\.log\(", code, re.MULTILINE):
        return "javascript"
    elif re.search(r"public\s+class\s+\w+|System\.out\.println|public\s+static\s+void\s+main", code):
        return "java"
    elif re.search(r"#include\s*<|std::cout|int\s+main\s*\(", code):
        return "cpp"

    return "python"

def preprocess_code(code: str, filename: str = "", language: str = "") -> Tuple[str, str, Dict[str, Any]]:
    """
    Validates, sanitizes, and extracts foundational metrics from source code.
    Raises ValueError if code violates limits.
    """
    if not code or not code.strip():
        raise ValueError("Source code cannot be empty.")

    code_bytes = code.encode("utf-8")
    if len(code_bytes) > MAX_CODE_SIZE_BYTES:
        raise ValueError(f"Source code exceeds maximum allowed size of {MAX_CODE_SIZE_BYTES // 1024} KB.")

    lang = language.lower() if language else detect_language(filename, code)
    if lang not in ["python", "javascript", "typescript", "java", "cpp", "c", "csharp", "go"]:
        lang = "python"

    # Normalize line endings
    normalized_code = code.replace("\r\n", "\n").replace("\r", "\n")

    # Extract metrics using our AST/Lexical engine
    metrics = extract_code_metrics(normalized_code, lang)
    metrics["file_size_bytes"] = len(code_bytes)

    return normalized_code, lang, metrics
