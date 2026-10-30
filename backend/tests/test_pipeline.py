"""
Unit and Integration test suite for:
- Preprocessor & Language Detection
- Feature Extraction & AST Static Analysis
- ML Defect Prediction
- Result Aggregator
- FastAPI REST Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.preprocessor import preprocess_code, detect_language
from backend.app.services.static_analyzer import run_static_analysis
from ml.feature_extraction import extract_code_metrics
from ml.predict import predict_defect_risk

client = TestClient(app)

def test_language_detection():
    assert detect_language(filename="app.py") == "python"
    assert detect_language(filename="index.js") == "javascript"
    assert detect_language(filename="Main.java") == "java"
    assert detect_language(filename="main.cpp") == "cpp"

def test_preprocessor_validation():
    with pytest.raises(ValueError):
        preprocess_code("", "test.py")

    code, lang, metrics = preprocess_code("def foo():\n    return 42\n", "test.py", "python")
    assert lang == "python"
    assert metrics["num_functions"] == 1
    assert metrics["loc"] == 2

def test_static_analyzer_python():
    vulnerable_code = """
def test_func():
    try:
        eval("2 + 2")
    except:
        pass
"""
    issues = run_static_analysis(vulnerable_code, "python")
    assert len(issues) >= 2
    types = [i["type"] for i in issues]
    assert "Security" in types # eval
    assert "Bug" in types      # bare except

def test_static_analyzer_javascript():
    js_code = """
function check(a) {
    if (a == 5) {
        eval("alert(1)");
    }
}
"""
    issues = run_static_analysis(js_code, "javascript")
    assert any(i["title"].startswith("Dangerous eval") for i in issues)
    assert any("Loose Equality" in i["title"] for i in issues)

def test_ml_prediction_risk_scoring():
    code = """
def complex_function(a, b, c):
    if a:
        if b:
            if c:
                for i in range(10):
                    if i > 5:
                        print(i)
    return a + b + c
"""
    pred = predict_defect_risk(code, "python")
    assert "defect_probability" in pred
    assert "risk_level" in pred
    assert pred["risk_level"] in ["Low", "Medium", "High"]
    assert 0.0 <= pred["defect_probability"] <= 100.0

def test_api_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "active_db" in data

def test_api_analyze_flow():
    payload = {
        "code": "def hello():\n    # greeting\n    print('Hello World')\n",
        "filename": "hello.py",
        "language": "python",
        "project_name": "Test Project"
    }
    resp = client.post("/api/analyze", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["filename"] == "hello.py"
    assert data["quality_score"] > 80
    assert "defect_probability" in data
    assert "issues" in data

    # Verify review can be retrieved
    review_id = data["id"]
    get_resp = client.get(f"/api/reviews/{review_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == review_id

    # Verify dashboard stats reflect the review
    dash_resp = client.get("/api/dashboard")
    assert dash_resp.status_code == 200
    dash_data = dash_resp.json()
    assert dash_data["total_reviews"] >= 1

    # Verify report download
    report_resp = client.get(f"/api/reviews/{review_id}/report?format=markdown")
    assert report_resp.status_code == 200
    assert "Code Review & Software Defect Prediction Audit Report" in report_resp.text

def test_static_analyzer_cpp():
    cpp_code = """
    #include <iostream>
    #include <cstring>
    void test(const char* src) {
        char buf[16];
        strcpy(buf, src);
        char* heap = new char[64];
    }
    """
    issues = run_static_analysis(cpp_code, "cpp")
    assert len(issues) >= 2
    # Check that section-wise fields exist
    assert any("Buffer Operation" in i["title"] for i in issues)
    assert any("Memory Leak" in i["title"] or "Heap Allocation" in i["title"] for i in issues)
    for i in issues:
        assert "software_defect" in i
        assert "bug_fix" in i
        assert "future_guidelines" in i

def test_static_analyzer_java():
    java_code = """
    import java.sql.*;
    import java.io.*;
    public class Sample {
        private static final String DB_PASS = "secret123";
        public void run(String val) {
            try {
                Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/db", "root", DB_PASS);
                Statement stmt = conn.createStatement();
                stmt.executeQuery("SELECT * FROM t WHERE name = '" + val + "'");
                BufferedWriter writer = new BufferedWriter(new FileWriter("out.txt"));
            } catch (Exception e) {}
        }
    }
    """
    issues = run_static_analysis(java_code, "java")
    assert len(issues) >= 3
    assert any("SQL Injection" in i["title"] for i in issues)
    assert any("Credentials" in i["title"] for i in issues)
    for i in issues:
        assert "software_defect" in i
        assert "bug_fix" in i
        assert "future_guidelines" in i

def test_api_analyze_cpp_and_java():
    # Test C++ analysis via API
    cpp_payload = {
        "code": "void run(const char* s) { char b[8]; strcpy(b, s); }",
        "filename": "packet.cpp",
        "language": "cpp"
    }
    resp_cpp = client.post("/api/analyze", json=cpp_payload)
    assert resp_cpp.status_code == 201
    data_cpp = resp_cpp.json()
    assert data_cpp["language"] == "cpp"
    assert len(data_cpp["issues"]) > 0
    assert "software_defect" in data_cpp["issues"][0]
    assert "bug_fix" in data_cpp["issues"][0]

    # Test Java analysis via API
    java_payload = {
        "code": "public class T { public void q(Statement s, String p) throws Exception { s.executeQuery(\"SELECT * FROM x WHERE id = '\" + p + \"'\"); } }",
        "filename": "Query.java",
        "language": "java"
    }
    resp_java = client.post("/api/analyze", json=java_payload)
    assert resp_java.status_code == 201
    data_java = resp_java.json()
    assert data_java["language"] == "java"
    assert len(data_java["issues"]) > 0
    assert "software_defect" in data_java["issues"][0]

def test_division_by_zero_all_languages():
    # C++ 5/0;
    cpp_res = run_static_analysis("int x = 5 / 0;", "cpp")
    assert any("Division by Zero" in i["title"] for i in cpp_res)
    assert any(i["severity"] == "Critical" for i in cpp_res)

    # Java 5/0;
    java_res = run_static_analysis("int x = 5 / 0;", "java")
    assert any("Division by Zero" in i["title"] for i in java_res)
    assert any(i["severity"] == "Critical" for i in java_res)

    # Python 5/0
    py_res = run_static_analysis("x = 5 / 0", "python")
    assert any("Division by Zero" in i["title"] for i in py_res)
    assert any(i["severity"] == "Critical" for i in py_res)

    # Python 5/0;
    py_semi_res = run_static_analysis("5/0;", "python")
    assert any("Division by Zero" in i["title"] for i in py_semi_res)

    # End-to-end API inspection: ensure quality score drops and risk is High
    resp = client.post("/api/analyze", json={"code": "5/0;", "language": "cpp", "filename": "calc.cpp"})
    assert resp.status_code == 201
    d = resp.json()
    assert d["quality_score"] <= 60
    assert d["risk_level"] == "High"
    assert any("Division by Zero" in i["title"] for i in d["issues"])


