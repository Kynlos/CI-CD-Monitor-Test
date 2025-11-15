# Code Analysis Report

*Generated: 2025-11-15 23:03:21*

**Commit:** [`2a5ed6b`](https://github.com/Kynlos/CI-CD-Monitor-Test/commit/2a5ed6b959ca20d9d397a357b65dd984ac1c9ec0)

## 📊 Overall Statistics

- **Files Analyzed:** 2
- **Average Quality Score:** 55.0/100
- **Security Vulnerabilities:** 0
- **Performance Issues:** 3

## 📈 Quality Scores

| File | Score | Grade | Doc | Complexity | Maint |
|------|-------|-------|-----|------------|-------|
| pages-manager.py | 55/100 | C | 15/30 | 15/30 | 25/40 |
| wiki-manager.py | 55/100 | C | 15/30 | 15/30 | 25/40 |

## 🐌 Performance Issues

### pages-manager.py

**LOW** - Line 86: Large function "make_intelligent_decision" (107 lines) may impact performance
*Suggestion: Consider breaking into smaller functions*

**LOW** - Line 420: Large function "process_docs_to_pages" (111 lines) may impact performance
*Suggestion: Consider breaking into smaller functions*

### wiki-manager.py

**LOW** - Line 397: Large function "process_documentation_to_wiki" (126 lines) may impact performance
*Suggestion: Consider breaking into smaller functions*


## 💡 Recommendations

- 📝 **Improve documentation coverage** - Add comments explaining complex logic
- ⚡ **Optimize 3 performance issues** - Consider algorithmic improvements
