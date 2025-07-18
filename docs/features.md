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

### 9. Commit Message Violations ✅ 
- **Intelligent Detection:** Skips good conventional commits (`feat: meaningful description`)
- **Garbage Patterns:**
  - Single word laziness: "fix", "update", "wip", "temp", "asdf"
  - Vague bullshit: "fix stuff", "update things", "minor changes"
  - Emotional commits: "FUCK THIS", "why doesn't this work"
  - Copy-paste commits: identical messages in recent history
  - Keyboard mashing: "...", "---", "123", "asdf"
- **Smart Analysis:** Length + context + meaningful words detection
- **Git Integration:** Analyzes last 20 commits via `git log`

### 10. Dependencies Audit ✅ NEW
- **Multi-Format Support:** package.json, requirements.txt, pyproject.toml
- **Bloat Detection:** ≥50 deps = dependency hell, ≥25 deps = package bloat
- **Left-pad Syndrome:** Flags micro-deps like 'left-pad', 'is-odd', 'six', 'typing-extensions'
- **Ecosystem Aware:** Different rules for npm vs pip packages
- **Zero Configuration:** Auto-discovers dependency files from project root

### 11. Documentation Audit ✅ NEW
- **Lazy Placeholder Detection:** "TODO: write docs", "Coming soon", "Under construction"
- **Dead Link Detection:** Suspicious domains (localhost, example.com, test.com)
- **Outdated Versions:** Python 2.x, old Node versions, beta/alpha/rc references
- **Empty README:** <100 chars = brutal violation
- **Broken Markdown:** Malformed anchor links and references
- **Auto-Discovery:** Scans README files and docs/ directory

## Architecture Features ✅

### Rule Engine
- 11 pluggable detection functions
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

## v0.1.0 Complete! 🔥
All core features implemented:
- ✅ 11 detection rules covering files, functions, imports, naming, dependencies, docs, commits
- ✅ 3 brutality levels with configurable thresholds
- ✅ LLM integration with rich markup
- ✅ CLI tool with flexible scanning
- ✅ Cross-file analysis and AST parsing

## Next Up (Phase 2) 🚀
- **Memory Foundation:** Track patterns over time, learn from violations
- **Advanced Rules:** AI-generated code detection, framework-specific patterns
- **Team Integration:** Git hooks, CI/CD pipeline integration