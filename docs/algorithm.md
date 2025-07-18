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
# File-level patterns
vague_names = {'utils', 'helpers', 'common', 'misc', 'stuff', 'base', 'core', 'main'}
```
**Validation:** Catches ceremony names, enforces descriptive naming

## LLM Prompt Engineering Status

### Current Prompt (Needs CLAUDE.md Alignment)
- Generic code review language
- Missing CLAUDE.md specific terminology
- Not aggressive enough about ceremony
- Doesn't emphasize "beautiful code" criteria

### Target Improvements
- Use CLAUDE.md vocabulary ("ceremony", "bullshit", "beautiful")
- Reference specific violations against doctrine
- More aggressive about deletion recommendations
- Emphasize "Zero Line Philosophy"

## Known Gaps & Next Targets

### High-Impact Additions
1. **Cross-file DRY violations** - Detect identical patterns across files
2. **Abstraction bullshit** - Wrapper classes with no value
3. **Over-engineering detection** - Abstract base classes adding complexity
4. **Wheel reinvention** - Custom parsers when stdlib exists

### Current Validation Issues
1. **False positives:** Small files flagged for having imports
2. **Missing context:** Can't detect tight coupling across modules
3. **Prompt quality:** LLM output doesn't match CLAUDE.md style

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
# Known violations in our own code:
- roaster.py:format_violations (11 branches, 26 lines) ✅ Valid
- core.py naming violation ✅ Valid  
- Multiple __init__.py files ✅ Valid
```

## Success Metrics
- **Accuracy:** No false positives in self-test
- **Completeness:** Catches all CLAUDE.md violations
- **Tone:** LLM output matches brutal honesty requirement
- **Actionability:** Clear refactoring recommendations

## Next Algorithm Improvements
1. **Prompt engineering** - Align LLM with CLAUDE.md style
2. **Cross-file analysis** - Detect DRY violations across modules
3. **Abstraction detection** - Flag unnecessary wrapper classes
4. **Performance** - Optimize for large codebases