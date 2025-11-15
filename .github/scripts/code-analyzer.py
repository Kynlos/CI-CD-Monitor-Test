#!/usr/bin/env python3
"""
Advanced Code Analyzer
Includes: Quality scoring, Security scanning, Performance regression detection
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Language-specific patterns
LANGUAGE_PATTERNS = {
    'python': {
        'function': r'def\s+(\w+)\s*\(',
        'class': r'class\s+(\w+)',
        'complexity_keywords': ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'with'],
    },
    'javascript': {
        'function': r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\()',
        'class': r'class\s+(\w+)',
        'complexity_keywords': ['if', 'else', 'for', 'while', 'switch', 'catch', 'case'],
    },
    'typescript': {
        'function': r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\()',
        'class': r'class\s+(\w+)',
        'complexity_keywords': ['if', 'else', 'for', 'while', 'switch', 'catch', 'case'],
    },
    'go': {
        'function': r'func\s+(\w+)\s*\(',
        'struct': r'type\s+(\w+)\s+struct',
        'complexity_keywords': ['if', 'else', 'for', 'switch', 'case', 'select'],
    },
    'rust': {
        'function': r'fn\s+(\w+)\s*\(',
        'struct': r'struct\s+(\w+)',
        'complexity_keywords': ['if', 'else', 'for', 'while', 'match', 'loop'],
    },
    'java': {
        'function': r'(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)?(\w+)\s*\(',
        'class': r'(?:public\s+)?class\s+(\w+)',
        'complexity_keywords': ['if', 'else', 'for', 'while', 'switch', 'catch', 'case'],
    },
    'cpp': {
        'function': r'(?:\w+\s+)?(\w+)\s*\([^)]*\)\s*{',
        'class': r'class\s+(\w+)',
        'complexity_keywords': ['if', 'else', 'for', 'while', 'switch', 'catch', 'case'],
    }
}

# Security vulnerability patterns
SECURITY_PATTERNS = {
    'hardcoded_secret': [
        (r'password\s*=\s*["\'](?!{{)[^"\']{8,}["\']', 'Hardcoded password detected'),
        (r'api[_-]?key\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded API key detected'),
        (r'secret\s*=\s*["\'][^"\']{16,}["\']', 'Hardcoded secret detected'),
        (r'token\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded token detected'),
    ],
    'sql_injection': [
        (r'execute\s*\(\s*["\'].*\+.*["\']', 'Possible SQL injection (string concatenation)'),
        (r'query\s*\(\s*f["\'].*{.*}.*["\']', 'Possible SQL injection (f-string formatting)'),
        (r'SELECT.*\+\s*\w+', 'Possible SQL injection in query'),
    ],
    'xss': [
        (r'innerHTML\s*=\s*\w+', 'Possible XSS via innerHTML'),
        (r'dangerouslySetInnerHTML', 'Dangerous HTML injection'),
        (r'eval\s*\(', 'Dangerous use of eval()'),
    ],
    'path_traversal': [
        (r'open\s*\([^)]*\+.*\)', 'Possible path traversal in file operations'),
        (r'File\s*\([^)]*\+.*\)', 'Possible path traversal in file creation'),
    ],
    'command_injection': [
        (r'exec\s*\(', 'Dangerous use of exec()'),
        (r'os\.system\s*\(', 'Dangerous use of os.system()'),
        (r'subprocess\..*shell\s*=\s*True', 'Dangerous shell=True in subprocess'),
    ]
}

# Performance anti-patterns
PERFORMANCE_PATTERNS = {
    'nested_loops': r'for\s+.*:\s*\n\s*for\s+',
    'n_squared': r'for\s+\w+\s+in\s+(\w+):.*for\s+\w+\s+in\s+\1',
    'repeated_computation': r'for\s+.*:\s*\n.*\.(\w+)\(',
}


class CodeAnalyzer:
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content
        self.language = self._detect_language()
        self.lines = content.split('\n')
        
    def _detect_language(self) -> str:
        """Detect programming language from file extension"""
        ext = Path(self.file_path).suffix.lower()
        mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.c': 'cpp',
            '.h': 'cpp',
            '.hpp': 'cpp',
        }
        return mapping.get(ext, 'unknown')
    
    def calculate_quality_score(self) -> Dict:
        """Calculate comprehensive quality score"""
        scores = {
            'total': 0,
            'documentation': 0,
            'complexity': 0,
            'maintainability': 0,
            'breakdown': {}
        }
        
        # Documentation score (0-30 points)
        doc_score = self._calculate_documentation_score()
        scores['documentation'] = doc_score
        scores['breakdown']['documentation'] = {
            'score': doc_score,
            'max': 30,
            'details': self._get_documentation_details()
        }
        
        # Complexity score (0-30 points)
        complexity_score = self._calculate_complexity_score()
        scores['complexity'] = complexity_score
        scores['breakdown']['complexity'] = {
            'score': complexity_score,
            'max': 30,
            'details': self._get_complexity_details()
        }
        
        # Maintainability score (0-40 points)
        maint_score = self._calculate_maintainability_score()
        scores['maintainability'] = maint_score
        scores['breakdown']['maintainability'] = {
            'score': maint_score,
            'max': 40,
            'details': self._get_maintainability_details()
        }
        
        scores['total'] = doc_score + complexity_score + maint_score
        scores['grade'] = self._get_grade(scores['total'])
        
        return scores
    
    def _calculate_documentation_score(self) -> int:
        """Score based on documentation coverage"""
        total_lines = len(self.lines)
        comment_lines = sum(1 for line in self.lines if line.strip().startswith(('#', '//', '/*', '*', '///')))
        
        if total_lines == 0:
            return 0
        
        coverage = (comment_lines / total_lines) * 100
        
        # Score based on coverage
        if coverage >= 20:
            return 30
        elif coverage >= 15:
            return 25
        elif coverage >= 10:
            return 20
        elif coverage >= 5:
            return 15
        else:
            return int(coverage * 2)  # 0-10 points for <5%
    
    def _calculate_complexity_score(self) -> int:
        """Score based on cyclomatic complexity"""
        if self.language not in LANGUAGE_PATTERNS:
            return 15  # Default mid-score for unknown languages
        
        keywords = LANGUAGE_PATTERNS[self.language].get('complexity_keywords', [])
        complexity_count = sum(
            sum(1 for _ in re.finditer(rf'\b{kw}\b', self.content)) 
            for kw in keywords
        )
        
        lines = len(self.lines)
        if lines == 0:
            return 15
        
        complexity_per_line = complexity_count / lines
        
        # Lower complexity = higher score
        if complexity_per_line <= 0.05:
            return 30
        elif complexity_per_line <= 0.10:
            return 25
        elif complexity_per_line <= 0.15:
            return 20
        elif complexity_per_line <= 0.20:
            return 15
        else:
            return 10
    
    def _calculate_maintainability_score(self) -> int:
        """Score based on maintainability factors"""
        score = 40
        
        # Line length penalty
        long_lines = sum(1 for line in self.lines if len(line) > 120)
        if long_lines > len(self.lines) * 0.2:
            score -= 10
        elif long_lines > len(self.lines) * 0.1:
            score -= 5
        
        # Function length penalty
        avg_function_length = self._get_average_function_length()
        if avg_function_length > 50:
            score -= 10
        elif avg_function_length > 30:
            score -= 5
        
        # Nesting depth penalty
        max_nesting = self._get_max_nesting_depth()
        if max_nesting > 5:
            score -= 10
        elif max_nesting > 3:
            score -= 5
        
        return max(0, score)
    
    def _get_average_function_length(self) -> float:
        """Calculate average function length"""
        if self.language not in LANGUAGE_PATTERNS:
            return 0
        
        pattern = LANGUAGE_PATTERNS[self.language].get('function', '')
        if not pattern:
            return 0
        
        function_starts = [m.start() for m in re.finditer(pattern, self.content)]
        if not function_starts:
            return 0
        
        # Estimate function lengths (rough approximation)
        lengths = []
        for i, start in enumerate(function_starts):
            end = function_starts[i + 1] if i + 1 < len(function_starts) else len(self.content)
            length = self.content[start:end].count('\n')
            lengths.append(length)
        
        return sum(lengths) / len(lengths) if lengths else 0
    
    def _get_max_nesting_depth(self) -> int:
        """Calculate maximum nesting depth"""
        max_depth = 0
        current_depth = 0
        
        for line in self.lines:
            stripped = line.strip()
            # Count opening braces/keywords
            if self.language in ['python']:
                if stripped.endswith(':') and any(kw in stripped for kw in ['if', 'for', 'while', 'def', 'class', 'with', 'try']):
                    current_depth += 1
                    max_depth = max(max_depth, current_depth)
                elif stripped and not stripped.startswith('#'):
                    # Dedent detection (rough)
                    if len(line) - len(line.lstrip()) == 0 and current_depth > 0:
                        current_depth = max(0, current_depth - 1)
            else:
                current_depth += line.count('{') - line.count('}')
                max_depth = max(max_depth, current_depth)
        
        return max_depth
    
    def _get_grade(self, score: int) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        else:
            return 'D'
    
    def _get_documentation_details(self) -> str:
        """Get documentation details"""
        total_lines = len(self.lines)
        comment_lines = sum(1 for line in self.lines if line.strip().startswith(('#', '//', '/*', '*', '///')))
        coverage = (comment_lines / total_lines * 100) if total_lines > 0 else 0
        return f"{coverage:.1f}% documentation coverage ({comment_lines}/{total_lines} lines)"
    
    def _get_complexity_details(self) -> str:
        """Get complexity details"""
        if self.language not in LANGUAGE_PATTERNS:
            return "Language not supported for complexity analysis"
        
        keywords = LANGUAGE_PATTERNS[self.language].get('complexity_keywords', [])
        complexity_count = sum(
            sum(1 for _ in re.finditer(rf'\b{kw}\b', self.content)) 
            for kw in keywords
        )
        return f"{complexity_count} decision points"
    
    def _get_maintainability_details(self) -> str:
        """Get maintainability details"""
        long_lines = sum(1 for line in self.lines if len(line) > 120)
        avg_func_len = self._get_average_function_length()
        max_nesting = self._get_max_nesting_depth()
        return f"{long_lines} long lines, avg function: {avg_func_len:.0f} lines, max nesting: {max_nesting}"
    
    def scan_security_vulnerabilities(self) -> List[Dict]:
        """Scan for common security vulnerabilities"""
        vulnerabilities = []
        
        for category, patterns in SECURITY_PATTERNS.items():
            for pattern, description in patterns:
                for match in re.finditer(pattern, self.content, re.IGNORECASE | re.MULTILINE):
                    line_num = self.content[:match.start()].count('\n') + 1
                    vulnerabilities.append({
                        'category': category,
                        'severity': 'HIGH' if category in ['sql_injection', 'command_injection'] else 'MEDIUM',
                        'description': description,
                        'line': line_num,
                        'code': self.lines[line_num - 1].strip() if line_num <= len(self.lines) else ''
                    })
        
        return vulnerabilities
    
    def detect_performance_issues(self) -> List[Dict]:
        """Detect potential performance regressions"""
        issues = []
        
        # Nested loops (O(n²))
        for match in re.finditer(PERFORMANCE_PATTERNS['nested_loops'], self.content, re.MULTILINE):
            line_num = self.content[:match.start()].count('\n') + 1
            issues.append({
                'type': 'nested_loops',
                'severity': 'MEDIUM',
                'description': 'Nested loops detected - possible O(n²) complexity',
                'line': line_num,
                'suggestion': 'Consider using hash maps or optimizing the algorithm'
            })
        
        # N² pattern (iterating same collection twice nested)
        for match in re.finditer(PERFORMANCE_PATTERNS['n_squared'], self.content, re.MULTILINE):
            line_num = self.content[:match.start()].count('\n') + 1
            issues.append({
                'type': 'n_squared_iteration',
                'severity': 'HIGH',
                'description': 'O(n²) pattern detected - iterating same collection in nested loops',
                'line': line_num,
                'suggestion': 'Use hash set/map for O(n) lookup instead'
            })
        
        # Large functions (>100 lines)
        if self.language in LANGUAGE_PATTERNS:
            pattern = LANGUAGE_PATTERNS[self.language].get('function', '')
            if pattern:
                function_starts = [(m.start(), m.group(1) or m.group(2)) for m in re.finditer(pattern, self.content)]
                for i, (start, name) in enumerate(function_starts):
                    end = function_starts[i + 1][0] if i + 1 < len(function_starts) else len(self.content)
                    length = self.content[start:end].count('\n')
                    if length > 100:
                        line_num = self.content[:start].count('\n') + 1
                        issues.append({
                            'type': 'large_function',
                            'severity': 'LOW',
                            'description': f'Large function "{name}" ({length} lines) may impact performance',
                            'line': line_num,
                            'suggestion': 'Consider breaking into smaller functions'
                        })
        
        return issues


def analyze_file(file_path: str) -> Dict:
    """Analyze a single file"""
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
    
    analyzer = CodeAnalyzer(file_path, content)
    
    return {
        'file': file_path,
        'language': analyzer.language,
        'quality_score': analyzer.calculate_quality_score(),
        'security_vulnerabilities': analyzer.scan_security_vulnerabilities(),
        'performance_issues': analyzer.detect_performance_issues()
    }


def main():
    print("="*80)
    print("ADVANCED CODE ANALYZER")
    print("="*80)
    
    # Get commit info
    commit_sha = os.environ.get('GITHUB_SHA', 'unknown')[:7]
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Create analysis directory with commit info
    analysis_dir = Path('code-analysis') / f"{timestamp}_{commit_sha}"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Analysis directory: {analysis_dir}\n")
    
    # Read changed files
    if not os.path.exists('changed_files.txt'):
        print("No changed files detected")
        sys.exit(0)
    
    with open('changed_files.txt', 'r') as f:
        changed_files = [line.strip() for line in f if line.strip()]
    
    code_extensions = {'.ts', '.js', '.tsx', '.jsx', '.py', '.go', '.rs', '.java', '.cpp', '.cc', '.c', '.h', '.hpp'}
    code_files = [f for f in changed_files if Path(f).suffix in code_extensions]
    
    if not code_files:
        print("No code files to analyze")
        sys.exit(0)
    
    print(f"Analyzing {len(code_files)} files...\n")
    
    results = []
    total_vulns = 0
    total_perf_issues = 0
    
    for file_path in code_files:
        print(f"📊 Analyzing: {file_path}")
        result = analyze_file(file_path)
        
        if result:
            results.append(result)
            
            # Print quality score
            score = result['quality_score']
            print(f"   Quality: {score['total']}/100 ({score['grade']})")
            print(f"   - Documentation: {score['documentation']}/30")
            print(f"   - Complexity: {score['complexity']}/30")
            print(f"   - Maintainability: {score['maintainability']}/40")
            
            # Print vulnerabilities
            vulns = result['security_vulnerabilities']
            if vulns:
                print(f"   ⚠️  {len(vulns)} security issue(s) found")
                total_vulns += len(vulns)
            
            # Print performance issues
            perf = result['performance_issues']
            if perf:
                print(f"   🐌 {len(perf)} performance issue(s) found")
                total_perf_issues += len(perf)
            
            print()
    
    # Save results to timestamped directory
    results_file = analysis_dir / 'results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate summary report in timestamped directory
    report_file = analysis_dir / 'report.md'
    generate_summary_report(results, report_file)
    
    # Create symlinks/copies for easy access (for notifications)
    latest_report = Path('analysis_report.md')
    latest_results = Path('analysis_results.json')
    
    # Copy to root for backward compatibility
    import shutil
    shutil.copy(report_file, latest_report)
    shutil.copy(results_file, latest_results)
    
    print("="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"✓ {len(results)} files analyzed")
    print(f"⚠️  {total_vulns} security vulnerabilities found")
    print(f"🐌 {total_perf_issues} performance issues found")
    print(f"📂 Analysis saved to: {analysis_dir}")
    print(f"📄 Report: {report_file}")
    print(f"📊 Data: {results_file}")


def generate_summary_report(results: List[Dict], output_file: Path):
    """Generate markdown summary report"""
    commit_sha = os.environ.get('GITHUB_SHA', 'unknown')[:7]
    commit_url = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', '')}/commit/{os.environ.get('GITHUB_SHA', '')}"
    
    report = "# Code Analysis Report\n\n"
    report += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    report += f"**Commit:** [`{commit_sha}`]({commit_url})\n\n"
    
    # Overall statistics
    avg_score = sum(r['quality_score']['total'] for r in results) / len(results) if results else 0
    total_vulns = sum(len(r['security_vulnerabilities']) for r in results)
    total_perf = sum(len(r['performance_issues']) for r in results)
    
    report += "## 📊 Overall Statistics\n\n"
    report += f"- **Files Analyzed:** {len(results)}\n"
    report += f"- **Average Quality Score:** {avg_score:.1f}/100\n"
    report += f"- **Security Vulnerabilities:** {total_vulns}\n"
    report += f"- **Performance Issues:** {total_perf}\n\n"
    
    # Quality scores by file
    report += "## 📈 Quality Scores\n\n"
    report += "| File | Score | Grade | Doc | Complexity | Maint |\n"
    report += "|------|-------|-------|-----|------------|-------|\n"
    
    for result in sorted(results, key=lambda x: x['quality_score']['total'], reverse=True):
        score = result['quality_score']
        name = Path(result['file']).name
        report += f"| {name} | {score['total']}/100 | {score['grade']} | {score['documentation']}/30 | {score['complexity']}/30 | {score['maintainability']}/40 |\n"
    
    # Security vulnerabilities
    if total_vulns > 0:
        report += "\n## 🚨 Security Vulnerabilities\n\n"
        for result in results:
            vulns = result['security_vulnerabilities']
            if vulns:
                report += f"### {Path(result['file']).name}\n\n"
                for vuln in vulns:
                    report += f"**{vuln['severity']}** - Line {vuln['line']}: {vuln['description']}\n"
                    report += f"```\n{vuln['code']}\n```\n\n"
    
    # Performance issues
    if total_perf > 0:
        report += "\n## 🐌 Performance Issues\n\n"
        for result in results:
            perf = result['performance_issues']
            if perf:
                report += f"### {Path(result['file']).name}\n\n"
                for issue in perf:
                    report += f"**{issue['severity']}** - Line {issue['line']}: {issue['description']}\n"
                    report += f"*Suggestion: {issue['suggestion']}*\n\n"
    
    # Recommendations
    report += "\n## 💡 Recommendations\n\n"
    
    if avg_score < 70:
        report += "- 📝 **Improve documentation coverage** - Add comments explaining complex logic\n"
    
    if total_vulns > 0:
        report += f"- 🔒 **Address {total_vulns} security vulnerabilities** - Review flagged issues\n"
    
    if total_perf > 0:
        report += f"- ⚡ **Optimize {total_perf} performance issues** - Consider algorithmic improvements\n"
    
    # Save report to specified file
    with open(output_file, 'w') as f:
        f.write(report)


if __name__ == '__main__':
    from datetime import datetime
    main()
