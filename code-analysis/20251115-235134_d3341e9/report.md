# Code Analysis Report

*Generated: 2025-11-15 23:51:34*

**Commit:** [`d3341e9`](https://github.com/Kynlos/CI-CD-Monitor-Test/commit/d3341e92c44b19336e5b422f5342d89caa89bf61)

## 📊 Overall Statistics

- **Files Analyzed:** 1
- **Average Quality Score:** 55.0/100
- **Security Vulnerabilities:** 0
- **Performance Issues:** 3

## 📈 Quality Scores

| File | Score | Grade | Doc | Complexity | Maint |
|------|-------|-------|-----|------------|-------|
| pages-manager.py | 55/100 | C | 15/30 | 15/30 | 25/40 |

## 🐌 Performance Issues

### pages-manager.py

**LOW** - Line 89: Large function "make_intelligent_decision" (107 lines) may impact performance
*Suggestion: Consider breaking into smaller functions*

**LOW** - Line 367: Large function "generate_index_page" (139 lines) may impact performance
*Suggestion: Consider breaking into smaller functions*

**LOW** - Line 506: Large function "process_docs_to_pages" (111 lines) may impact performance
*Suggestion: Consider breaking into smaller functions*


## 💡 Recommendations

- 📝 **Improve documentation coverage** - Add comments explaining complex logic
- ⚡ **Optimize 3 performance issues** - Consider algorithmic improvements
