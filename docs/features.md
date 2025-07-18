# ShitLint Features Implemented

## Core Detection Rules ✅

### 1. Giant Files
- **Brutal:** ≥500 lines ("War crime detected")
- **Professional:** ≥300 lines ("Novel detected") 
- **Gentle:** ≥800 lines

### 2. Import Ceremony
- **Brutal:** ≥15 imports ("Import addiction")
- **Professional:** ≥25 imports ("Import ceremony")
- **Gentle:** ≥35 imports

### 3. Complex Functions
- **Brutal:** >12 complexity OR >50 lines ("Complexity nightmare")
- **Professional:** >15 complexity OR >80 lines ("Getting complex")
- **Gentle:** >25 complexity OR >120 lines

### 4. Duplicate Code
- AST hash matching for identical function structures
- Cross-file detection via structural similarity

### 5. Naming Violations
- Ceremony variables: 'data', 'result', 'temp', 'obj', 'item', 'val', 'thing'
- Ceremony classes: 'Manager', 'Handler', 'Processor', 'Service', 'Factory'
- AI monstrosities: names >25 characters

### 6. Parameter Hell
- **Brutal:** ≥5 parameters ("Parameter hell detected")
- **Professional:** ≥6 parameters ("Consider refactoring")
- **Gentle:** ≥8 parameters
- Excludes 'self' for methods

### 7. Magic Numbers
- Detects hardcoded numbers (excludes 0, 1, -1, 2, 10, 100, 1000)
- Skips proper constants: MAX_SIZE = 500

### 8. Over-Abstraction
- God abstraction: ≥15 abstract methods
- Wrapper hell: ≥80% delegation methods
- Inheritance depth: >4 levels
- Pointless factory: Single create() method with simple instantiation
- Interface overkill: Abstract classes with many methods

### 9. Commit Message Violations ✅ NEW
- **Intelligent Detection:** Skips good conventional commits (`feat: meaningful description`)
- **Garbage Patterns:**
  - Single word laziness: "fix", "update", "wip", "temp", "asdf"
  - Vague bullshit: "fix stuff", "update things", "minor changes"
  - Emotional commits: "FUCK THIS", "why doesn't this work"
  - Copy-paste commits: identical messages in recent history
  - Keyboard mashing: "...", "---", "123", "asdf"
- **Smart Analysis:** Length + context + meaningful words detection
- **Git Integration:** Analyzes last 20 commits via `git log`

## Architecture Features ✅

### Rule Engine
- 9 pluggable detection functions
- 3 brutality levels: brutal/professional/gentle
- AST parsing + cross-file analysis
- Configurable thresholds per rule

### LLM Integration
- BRUTAL scannable format - violations FRONT AND CENTER
- Rich markup: [red], [yellow], [bold]
- Direct commands: "DELETE THIS", "FIX THIS"
- Auto-detection: OpenAI/Anthropic/Gemini/Ollama

### CLI Tool
- `shitlint .` - Scan current directory
- `shitlint path/to/file.py` - Scan specific file
- `--brutality brutal/professional/gentle` - Override severity
- `--context "additional context"` - Add context for roasting
- `--init` - Create default .shitlint/config.json

### Configuration
- `.shitlint/config.json` for custom settings
- Brutality levels with different thresholds
- Ignore patterns (respects .gitignore)
- Max file size limits

## Next Up 🔥
- **Dependencies Audit:** package.json/requirements.txt parsing for bloat detection
- **Documentation Audit:** README analysis for dead links, outdated content
- **Memory Foundation:** Track patterns over time (Phase 2)