# HindTrace — Automated Test Suite

Unit and integration tests covering the 3-stage pipeline, Hindsight memory, ACL security, and prompt injection defense.

## Running Tests

Run all tests with `unittest`:
```powershell
python -m unittest discover tests
```

Or with `pytest`:
```powershell
pytest tests/ -v
```

## Test Coverage
1. **`test_memory.py`**: Verifies Hindsight `retain()`, `recall()`, entity matching, and `acl_ceiling` enforcement.
2. **`test_acl.py`**: Verifies squad boundaries and restricted document gating (Trap T6).
3. **`test_injection.py`**: Verifies prompt override detection and untrusted document tagging.
4. **`test_pipeline.py`**: Verifies end-to-end Router, Investigator, and Escalator execution.

