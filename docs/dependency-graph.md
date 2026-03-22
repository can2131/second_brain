# Module Dependency Graph

No circular dependencies detected — all imports flow in one direction toward `app`.

```mermaid
flowchart LR
    subgraph core["Core Package (second_brain)"]
        init["__init__.py"]
        main["__main__.py"]
        app["app.py"]
    end

    subgraph scripts["Scripts"]
        serve["serve_docs.py"]
    end

    subgraph tests["Tests"]
        conftest["conftest.py"]
        test_app["test_app.py"]
    end

    main -- "main()" --> app
    test_app -- "console_format(), main()" --> app

    style core fill:#e8f4fd,stroke:#2196F3
    style scripts fill:#f3e8fd,stroke:#9C27B0
    style tests fill:#e8fde8,stroke:#4CAF50
```

## Safe-to-change analysis

| Module | Dependents | Risk |
|---|---|---|
| `app.py` | `__main__.py`, `test_app.py` | Highest — central module, changes cascade to entry point and tests |
| `__main__.py` | none | Safe — leaf node, only consumes `app.main()` |
| `serve_docs.py` | none | Safe — standalone script, no internal imports |
| `conftest.py` | none | Safe — only provides pytest fixtures |
| `test_app.py` | none | Safe — leaf node, only consumes from `app` |
| `__init__.py` | none | Safe — empty package marker |
