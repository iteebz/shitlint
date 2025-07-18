# ShitLint Algorithm Design & Validation

## Core Philosophy
**Flag bullshit, enforce beauty, eliminate ceremony**

Based on CLAUDE.md doctrine:
- DRY + SOLID over wet spaghetti
- Decoupled + Extensible over tight ceremony
- Pragmatic + Modular over monolithic monsters
- Auto-magical over manual ceremony
- Beautiful over bullshit

## Current Detection Rules

### 1. Giant Files (Working ✅)
```python
# Thresholds
brutal: >= 500 lines    # "War crime detected"
moderate: >= 300 lines  # "Novel detected" 
gentle: >= 200 lines    # "File getting chubby"
```
**Validation:** Catches real bloat, matches CLAUDE.md "giant files" criterion

### 2. Import Ceremony (Working ✅)
```python
# Thresholds
brutal: >= 25 imports   # "Import addiction - architectural heroin"
moderate: >= 15 imports # "Import ceremony - tight coupling"
```
**Validation:** Detects dependency addiction, aligns with "import ceremony" bullshit

### 3. Complex Functions (Working ✅)
```python
# Cyclomatic complexity + line count
brutal: >15 complexity OR >80 lines    # "Complexity nightmare"
moderate: >10 complexity OR >50 lines  # "Getting complex"
```
**Validation:** Catches real cognitive load, enforces single responsibility

### 4. Duplicate Code (Working ✅)
```python
# AST hash matching for identical function structures
```
**Validation:** Direct DRY violation detection

### 5. Naming Violations (Working ✅)
```python
# AST visitor pattern - scans ALL names in code
ceremony_vars = {'data', 'result', 'temp', 'obj', 'item', 'val', 'thing', 'params'}
ceremony_classes = {'Manager', 'Handler', 'Processor', 'Service', 'Factory'}
ai_monstrosities = len(name) > 25  # "AI-generated bullshit"

# Captures:
visit_FunctionDef()  # Function names + parameters  
visit_ClassDef()     # Class names
visit_Assign()       # Variable assignments
```
**Validation:** Catches ceremony parameters, AI-generated names, vague classes

### 6. Cross-File Duplicates (Working ✅)
```python
# Structural similarity detection via AST normalization
# Replaces variable names with placeholders: VAR_0, VAR_1, PARAM_0
# Generates MD5 hash of normalized function structure
# Groups identical structures across files
```
**Validation:** Catches copy-paste with different variable names across modules

## LLM Prompt Engineering Status

### Current Prompt (Fixed ✅)
- BRUTAL, scannable format - violations FRONT AND CENTER
- Rich markup for terminal colors ([red], [yellow], [bold])
- Direct action commands: "DELETE THIS", "FIX THIS", "REFACTOR"
- No verbose explanations - just brutal facts
- Both LLM and static fallback use same format

## Known Gaps & Next Targets

### High-Impact Additions
1. **Parameter hell** - Functions with 6+ parameters (ceremony overload)
2. **Magic numbers** - Hardcoded values without constants
3. **Abstraction bullshit** - Wrapper classes with no value
4. **Over-engineering detection** - Abstract base classes adding complexity

### Current Validation Issues
1. **False positives:** Small files flagged for having imports  
2. **Missing context:** Can't detect tight coupling across modules
3. **Loop variables:** `i`, `j`, `k` flagged as ceremony (maybe acceptable in loops)

## Algorithm Evolution

### Phase 1 (Current): Heuristic Detection
- AST-based static analysis
- File-level pattern matching
- Single-file scope violations

### Phase 2 (Roadmap): Cross-File Intelligence
- Project-wide DRY detection
- Module coupling analysis
- Architectural pattern recognition

### Phase 3 (Future): Memory-Based Learning
- Track patterns across analyses
- Learn team-specific anti-patterns
- Predictive violation warnings

## Validation Methodology

### Self-Testing Protocol
1. Run shitlint on itself
2. Manually verify each violation
3. Ensure no false positives
4. Validate roast quality matches CLAUDE.md tone

### Current Self-Test Results
```bash
# Our own code is now clean:
poetry run python -c "from src.shitlint.core import analyze_code..."
🤨 SUSPICIOUSLY CLEAN CODE DETECTED
# All complexity violations fixed ✅
# No ceremony naming violations ✅
```

## Success Metrics
- **Accuracy:** No false positives in self-test
- **Completeness:** Catches all CLAUDE.md violations
- **Tone:** LLM output matches brutal honesty requirement
- **Actionability:** Clear refactoring recommendations

## Next Algorithm Improvements
1. **Cross-file analysis** - Detect DRY violations across modules
2. **Abstraction detection** - Flag unnecessary wrapper classes  
3. **Performance** - Optimize for large codebases
4. **Loop context** - Don't flag `i`, `j`, `k` in actual loops