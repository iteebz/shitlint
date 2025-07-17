# ShitLint 💩🔍

**Your code is shit. Here's why.**

ShitLint is the AI code reviewer that cuts through the fluff and calls out the architectural dumpster fires hiding in your codebase. Because sometimes, brutal honesty is what is needed, even when it hurts.

## Why ShitLint Exists

Ever wonder why your "simple feature" took 3 weeks to implement? It's because your code is a tangled mess of:
- Copy-pasted functions everywhere (DRY? Never heard of it)
- 200+ line files of spaghetti bullshit
- Abstractions that abstract nothing
- Imports that look like some shat on your keyboard

Traditional linters catch typos. ShitLint catches **architectural bullshit**.

## What ShitLint Actually Does

```bash
$ shitlint .
```

```
⏺ FLAGGED BULLSHIT:

🚨 DRY VIOLATION:
- user_service.py:45-67 and admin_service.py:12-34 are literally the same function
- Did you copy-paste this? Be honest.

🚨 GIANT FILE ALERT:
- database.py:847 lines - This isn't a file, it's a novel
- Split this monstrosity before it gains sentience

🚨 BULLSHIT ABSTRACTION:
- utils.py:23 - A function called "doStuff" that does 47 different things
- Name your functions like a human, not a caffeinated squirrel

🚨 IMPORT CEREMONY:
- 23 imports for a 15-line file
- This isn't dependency injection, it's dependency addiction

VERDICT: Your code looks like it was written during a earthquake
```

## Installation

```bash
npm install -g shitlint
# or
pip install shitlint
# or just clone this repo and suffer with the rest of us
```

## Usage

```bash
# Scan current directory
shitlint .

# Scan specific file
shitlint path/to/your/disaster.py

# Get roasted in real-time
shitlint --watch ./src

# Extra brutal mode (not recommended for sensitive developers)
shitlint --brutal ./src
```

## Configuration

Create a `.shitlint.json` file to customize how brutally honest you want the feedback:

```json
{
  "brutality": "gordon-ramsay",
  "roast_level": "professional-chef",
  "ignore_patterns": ["legacy/*", "vendor/*"],
  "custom_insults": true
}
```

## Language Support

- Python ✅ (your FastAPI spaghetti)
- JavaScript ✅ (your React component soup)
- TypeScript ✅ (your over-engineered type gymnastics)
- Go ✅ (your "simple" microservice that imports 47 packages)
- More languages coming (unfortunately)

## FAQ

**Q: Is this just a joke?**
A: No. Your code genuinely needs help.

**Q: Why so aggressive?**
A: Because your linter has been lying to you. Someone has to tell the truth.

**Q: Can I disable the roasting?**
A: You can, but then you're just running a regular linter. Where's the fun in that?

**Q: Will this hurt my feelings?**
A: Probably. But your code will be better for it.

## Contributing

Found a new way code can be terrible? We'd love to hear about it.

1. Fork this repo
2. Add your horror stories to the detection engine
3. Submit a PR
4. Watch other developers suffer

## Roadmap

- [ ] Integration with popular IDEs (so you can be roasted in real-time)
- [ ] Team dashboard (shame your colleagues publicly)
- [ ] AI-generated refactoring suggestions (because apparently you need help)
- [ ] Slack integration (get roasted in meetings)
- [ ] Custom personality modes (Gordon Ramsay, Disappointed Parent, etc.)

## License

MIT - Because even terrible code deserves freedom

---

**Remember: The first step to writing better code is admitting your current code is shit.**

*Built with ❤️ and a concerning amount of coffee by [@iteebz](https://github.com/iteebz)*

---

⭐ **Star this repo if you're brave enough to face the truth about your 💩 code**
