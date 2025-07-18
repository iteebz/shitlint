# ShitLint Algorithm Design & Validation

## Core Philosophy
**Flag bullshit, enforce beauty, eliminate ceremony**

## Current Detection Rules (8 Total)

### 1. Giant Files 
```python
brutal: >= 500 lines    # "War crime detected"
moderate: >= 300 lines  # "Novel detected"
```

### 2. Import Ceremony 
```python
brutal: >= 25 imports   # "Import addiction"
moderate: >= 15 imports # "Import ceremony"
```

### 3. Complex Functions 
```python
brutal: >15 complexity OR >80 lines    # "Complexity nightmare"
moderate: >10 complexity OR >50 lines  # "Getting complex"
```

### 4. Duplicate Code 
```python
# AST hash matching for identical function structures
# Cross-file detection via structural similarity
```

### 5. Naming Violations 
```python
ceremony_vars = {'data', 'result', 'temp', 'obj', 'item', 'val', 'thing'}
ceremony_classes = {'Manager', 'Handler', 'Processor', 'Service', 'Factory'}
ai_monstrosities = len(name) > 25
```

### 6. Parameter Hell 
```python
brutal: >= 6 parameters    # "Parameter hell detected"  
moderate: >= 4 parameters  # "Consider refactoring"
# Excludes 'self' for methods
```

### 7. Magic Numbers 
```python
# Detects hardcoded numbers (excludes 0, 1, -1, 2, 10, 100, 1000)
# Skips proper constants: MAX_SIZE = 500
```

### 8. Over-Abstraction 
```python
god_abstraction: >= 15 abstract methods
wrapper_hell: >= 80% delegation methods  
inheritance_depth: > 4 levels
pointless_factory: Single create() method with simple instantiation
interface_overkill: Abstract classes with many methods
```

## Architecture

### Rule Engine (rules/engine.py)
```python
# 8 pluggable detection functions
# 3 brutality levels: brutal/professional/gentle
# AST parsing + cross-file analysis
# Configurable thresholds per rule
```

### LLM Integration  
```python
# BRUTAL scannable format - violations FRONT AND CENTER
# Rich markup: [red], [yellow], [bold]
# Direct commands: "DELETE THIS", "FIX THIS"
# Auto-detection: OpenAI/Anthropic/Gemini/Ollama
```

## Status
**All 8 core techniques.md patterns implemented ✅**

### Next Phase
- Cross-module coupling analysis
- Performance optimization for large codebases
- Team-specific pattern learning