from __future__ import annotations
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

try:
    from guesslang import Guess
except Exception:
    Guess = None

try:
    from pygments.lexers import guess_lexer, guess_lexer_for_filename
except Exception:
    guess_lexer = None
    guess_lexer_for_filename = None


@dataclass
class DetectionResult:
    path: str
    is_text: bool
    is_code: bool
    document_type: str
    category: str
    language: str | None
    language_family: str | None
    variant: str | None
    frameworks: list[str] = field(default_factory=list)
    confidence: float = 0.0
    candidates: list[dict[str, Any]] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    line_count: int = 0
    encoding: str | None = None
    engines_used: list[str] = field(default_factory=list)


class SourceDetector:
    def __init__(self) -> None:
        self.guesslang = Guess() if Guess is not None else None
        self.framework_rules = [
            ("react", r"\bfrom\s+['\"]react['\"]|\buseState\b|\buseEffect\b|React\.createElement", 1.0),
            ("next.js", r"\bfrom\s+['\"]next/|\buse client\b|\bnext\.config\.(js|mjs|cjs|ts)\b", 1.4),
            ("vue", r"<template>|<script\s+setup|\bfrom\s+['\"]vue['\"]|\bdefineComponent\b", 1.0),
            ("angular", r"@Component\s*\(|@NgModule\s*\(|@Injectable\s*\(|['\"]@angular/", 1.1),
            ("svelte", r"\bfrom\s+['\"]svelte['\"]|\$:|onMount", 1.0),
            ("express", r"\bfrom\s+['\"]express['\"]|require\(['\"]express['\"]\)|\bexpress\(\)", 0.9),
            ("nest.js", r"@Module\s*\(|@Controller\s*\(|@Injectable\s*\(|['\"]@nestjs/", 1.2),
            ("django", r"\bfrom\s+django\b|\bmodels\.Model\b|\burlpatterns\b|\bINSTALLED_APPS\b", 1.2),
            ("flask", r"\bfrom\s+flask\s+import\b|\bFlask\(__name__\)|@app\.route", 1.0),
            ("fastapi", r"\bfrom\s+fastapi\s+import\b|\bFastAPI\(|@app\.(get|post|put|delete|patch)\b", 1.2),
            ("spring boot", r"@SpringBootApplication|@RestController|org\.springframework", 1.2),
            ("laravel", r"\buse\s+Illuminate\\|\bRoute::|artisan|blade", 1.1),
            ("tailwindcss", r"@tailwind\b|class(Name)?=.*\b(bg-|text-|flex|grid|px-|py-|mx-|my-|rounded|w-|h-)", 0.8),
            ("bootstrap", r"class(Name)?=.*\b(container|row|col-|btn|card|navbar|form-control)\b", 0.8),
            ("unity", r"\bMonoBehaviour\b|\bUnityEngine\b|\bStart\s*\(|\bUpdate\s*\(", 1.1),
            ("unreal engine", r"\bUCLASS\b|\bUPROPERTY\b|\bUE_LOG\b|\bGENERATED_BODY\b", 1.1),
        ]
        self.heuristics = {
            "html": [(r"<!doctype\s+html", 0.40, "doctype html"), (r"<html[\s>]", 0.20, "html tag"), (r"<(head|body|div|span|script|style|meta|link)[\s>]", 0.15, "common html tags")],
            "css": [(r"\b(color|margin|padding|display|position|font-size|background|border)\s*:", 0.30, "css properties"), (r"@media|@import|:root", 0.20, "css rules"), (r"--[a-zA-Z0-9_-]+\s*:", 0.10, "css vars"), (r"[.#]?[a-zA-Z0-9_\-\s,>:\[\]=\"'()]+\{[^}]+\}", 0.20, "css blocks")],
            "python": [(r"^\s*def\s+\w+\s*\(", 0.20, "python def"), (r"^\s*class\s+\w+[\(:]", 0.15, "python class"), (r"^\s*(import\s+\w+|from\s+\w+\s+import\s+)", 0.20, "python imports"), (r"if\s+__name__\s*==\s*['\"]__main__['\"]", 0.20, "main guard")],
            "javascript": [(r"\b(function|const|let|var|export|import|async|await)\b", 0.20, "js keywords"), (r"=>", 0.10, "arrow function"), (r"\b(document\.|window\.|console\.log|module\.exports|require\()", 0.20, "js runtime patterns")],
            "typescript": [(r"\binterface\s+\w+", 0.25, "ts interface"), (r"\btype\s+\w+\s*=", 0.15, "ts type alias"), (r":\s*(string|number|boolean|unknown|any|never|void)\b", 0.20, "ts type annotations"), (r"\bimplements\b|\benum\b|\bas\s+const\b", 0.10, "ts features")],
            "java": [(r"\bpackage\s+[a-zA-Z0-9_.]+\s*;", 0.15, "java package"), (r"\bpublic\s+class\s+\w+", 0.20, "java class"), (r"\bstatic\s+void\s+main\s*\(", 0.25, "java main")],
            "csharp": [(r"\busing\s+[A-Z][A-Za-z0-9_.]*\s*;", 0.20, "csharp using"), (r"\bnamespace\s+[A-Z][A-Za-z0-9_.]*", 0.15, "namespace"), (r"\basync\s+Task\b|\bTask<", 0.15, "task async"), (r"\bConsole\.Write(Line)?\b|\bget;\s*set;", 0.15, "csharp patterns")],
            "php": [(r"<\?php", 0.45, "php open tag"), (r"\$[A-Za-z_][A-Za-z0-9_]*", 0.10, "php var"), (r"\becho\b|\bnamespace\b|\buse\b", 0.10, "php keywords")],
            "c": [(r"#include\s*<([a-z]+)\.h>", 0.20, "c include"), (r"\bprintf\s*\(", 0.15, "printf"), (r"\bmalloc\s*\(", 0.10, "malloc"), (r"\btypedef\b|\bstruct\b", 0.10, "typedef struct")],
            "cpp": [(r"#include\s*<iostream>|#include\s*<vector>|#include\s*<string>", 0.20, "cpp include"), (r"\bstd::", 0.20, "std namespace"), (r"\btemplate\s*<", 0.15, "templates"), (r"cout\s*<<", 0.10, "cout")],
            "rust": [(r"\bfn\s+main\s*\(", 0.20, "rust main"), (r"\blet\s+mut\b", 0.10, "mut"), (r"\bimpl\b|\btrait\b|\bmatch\b", 0.15, "rust keywords")],
            "go": [(r"\bpackage\s+main\b", 0.20, "go package"), (r"\bfunc\s+main\s*\(", 0.20, "go main"), (r":=", 0.10, "short declaration")],
            "shell": [(r"^#!\s*/bin/(ba)?sh", 0.25, "shell shebang"), (r"\b(grep|sed|awk|chmod|find|echo|export)\b", 0.20, "shell commands")],
            "powershell": [(r"\bWrite-Host\b|\bGet-[A-Za-z]+\b|\bSet-[A-Za-z]+\b", 0.25, "powershell cmdlets"), (r"\bParam\s*\(", 0.15, "param block")],
            "sql": [(r"\bSELECT\b.*\bFROM\b", 0.30, "select from"), (r"\b(INSERT|UPDATE|DELETE|CREATE TABLE|ALTER TABLE|JOIN|WHERE)\b", 0.25, "sql statements")],
            "yaml": [(r"^\s*[A-Za-z0-9_-]+\s*:\s*.*$", 0.15, "yaml kv"), (r"^\s*-\s+.+$", 0.10, "yaml list")],
            "json": [(r"^\s*\{", 0.10, "json start"), (r"\"[A-Za-z0-9_ -]+\"\s*:\s*", 0.25, "json kv")],
        }
        self.name_map = {
            'c#': 'csharp', 'c++': 'cpp', 'js': 'javascript', 'ts': 'typescript', '.net': 'csharp',
            'shell': 'shell', 'bash': 'shell', 'html': 'html', 'xml': 'xml', 'json': 'json', 'yaml': 'yaml',
            'python': 'python', 'java': 'java', 'php': 'php', 'css': 'css', 'sql': 'sql', 'go': 'go', 'rust': 'rust',
            'powershell': 'powershell', 'c': 'c'
        }
        self.skip_dirs = {'.git', 'node_modules', '.next', 'dist', 'build', 'target', 'coverage', '__pycache__', '.venv', 'venv', '.idea', '.vscode'}
        self.manifest_names = {'package.json', 'requirements.txt', 'pyproject.toml', 'composer.json', 'pom.xml', 'build.gradle', 'Cargo.toml'}
        self.programming_languages = {'python', 'javascript', 'typescript', 'java', 'csharp', 'php', 'c', 'cpp', 'rust', 'go', 'shell', 'powershell'}

    def detect(self, file_path: str | Path) -> DetectionResult:
        path = Path(file_path)
        text, encoding, is_text = self._read_text(path)
        if not is_text or text is None:
            return DetectionResult(str(path), False, False, 'binary_or_unsupported', 'binary_files', None, None, None, [], 0.0, [], ['file is binary or unsupported text encoding'], 0, None, [])

        line_count = text.count('\n') + (1 if text else 0)
        document_type = self._document_type(text)
        category = self._category_from_document_type(document_type)
        engines_used = []
        aggregate: dict[str, dict[str, Any]] = {}

        heur = self._heuristic_candidates(text)
        if heur:
            engines_used.append('heuristics')
            self._merge_candidates(aggregate, heur, 'heuristics')

        pyg = self._pygments_candidates(path, text)
        if pyg:
            engines_used.append('pygments')
            self._merge_candidates(aggregate, pyg, 'pygments')

        gl = self._guesslang_candidates(text)
        if gl:
            engines_used.append('guesslang')
            self._merge_candidates(aggregate, gl, 'guesslang')

        candidates = self._finalize_candidates(aggregate)
        language = candidates[0]['language'] if candidates else None
        confidence = candidates[0]['score'] if candidates else 0.0
        language_family, variant = self._resolve_family_variant(language, text)
        frameworks = self._detect_frameworks(text, path)
        evidence = candidates[0]['evidence'] if candidates else []

        if document_type == 'code' and language not in self.programming_languages:
            category = 'text_files'
        elif document_type == 'text':
            category = 'text_files'
        elif document_type == 'markup':
            category = 'markup_files'
        elif document_type == 'style':
            category = 'style_files'
        elif document_type == 'config':
            category = 'config_files'
        elif document_type == 'data':
            category = 'data_files'
        elif document_type == 'code':
            category = 'source_code_files'

        is_code = category in {'source_code_files', 'markup_files', 'style_files', 'config_files', 'data_files'}

        return DetectionResult(
            path=str(path),
            is_text=True,
            is_code=is_code,
            document_type=document_type,
            category=category,
            language=language,
            language_family=language_family,
            variant=variant,
            frameworks=frameworks,
            confidence=round(confidence, 3),
            candidates=candidates[:5],
            evidence=evidence,
            line_count=line_count,
            encoding=encoding,
            engines_used=engines_used,
        )

    def analyze_repository(self, root: str | Path) -> dict[str, Any]:
        root = Path(root)
        file_results: list[dict[str, Any]] = []
        language_counter = Counter()
        programming_language_counter = Counter()
        variant_counter = Counter()
        framework_score = defaultdict(float)
        framework_files = defaultdict(set)
        manifest_hits = []
        category_counts = Counter()

        for path in self._iter_files(root):
            result = self.detect(path)
            result_dict = asdict(result)
            file_results.append(result_dict)
            category_counts[result.category] += 1

            if result.language:
                language_counter[result.language] += max(result.confidence, 0.1)
            if result.category == 'source_code_files' and result.language in self.programming_languages:
                programming_language_counter[result.language] += max(result.confidence, 0.1)
            if result.variant:
                variant_counter[result.variant] += max(result.confidence, 0.1)
            for fw in result.frameworks:
                boost = 1.0 + result.confidence
                if Path(result.path).name in self.manifest_names:
                    boost += 1.5
                    manifest_hits.append({'file': result.path, 'framework': fw})
                framework_score[fw] += boost
                framework_files[fw].add(result.path)

        top_languages = [
            {'language': lang, 'score': round(score, 3)}
            for lang, score in language_counter.most_common(10)
        ]
        top_programming_languages = [
            {'language': lang, 'score': round(score, 3)}
            for lang, score in programming_language_counter.most_common(10)
        ]
        top_variants = [
            {'variant': var, 'score': round(score, 3)}
            for var, score in variant_counter.most_common(10)
        ]
        total_code_like_files = sum(category_counts[c] for c in ['source_code_files', 'markup_files', 'style_files', 'config_files', 'data_files'])
        inferred_frameworks = self._infer_repository_frameworks(framework_score, framework_files, total_code_like_files)
        primary_language = top_languages[0]['language'] if top_languages else None
        primary_programming_language = top_programming_languages[0]['language'] if top_programming_languages else None
        primary_framework = inferred_frameworks[0]['framework'] if inferred_frameworks else None

        return {
            'root': str(root),
            'summary': {
                'files_scanned': len(file_results),
                'source_code_files': category_counts['source_code_files'],
                'markup_files': category_counts['markup_files'],
                'style_files': category_counts['style_files'],
                'config_files': category_counts['config_files'],
                'data_files': category_counts['data_files'],
                'text_files': category_counts['text_files'],
                'binary_files': category_counts['binary_files'],
                'code_like_files': total_code_like_files,
                'primary_language': primary_language,
                'primary_programming_language': primary_programming_language,
                'primary_framework': primary_framework,
            },
            'top_languages': top_languages,
            'top_programming_languages': top_programming_languages,
            'top_variants': top_variants,
            'framework_ranking': inferred_frameworks,
            'manifest_hits': manifest_hits,
            'files': file_results,
        }

    def _category_from_document_type(self, document_type: str) -> str:
        mapping = {
            'binary_or_unsupported': 'binary_files',
            'markup': 'markup_files',
            'style': 'style_files',
            'config': 'config_files',
            'data': 'data_files',
            'text': 'text_files',
            'code': 'source_code_files',
        }
        return mapping.get(document_type, 'text_files')

    def _infer_repository_frameworks(self, framework_score, framework_files, total_code_like_files):
        ranked = []
        for fw, score in framework_score.items():
            file_count = len(framework_files[fw])
            density = (file_count / total_code_like_files) if total_code_like_files else 0.0
            final_score = min(0.99, 0.15 + (score / max(total_code_like_files, 1)) + density)
            ranked.append({
                'framework': fw,
                'score': round(final_score, 3),
                'matched_files': file_count,
                'sample_files': sorted(list(framework_files[fw]))[:5],
            })
        ranked.sort(key=lambda x: (x['score'], x['matched_files']), reverse=True)
        return ranked[:10]

    def _iter_files(self, root: Path):
        for path in root.rglob('*'):
            if not path.is_file():
                continue
            if any(part in self.skip_dirs for part in path.parts):
                continue
            yield path

    def _read_text(self, path: Path, max_bytes: int = 500_000):
        data = path.read_bytes()[:max_bytes]
        if self._is_probably_binary(data):
            return None, None, False
        for enc in ('utf-8', 'utf-8-sig', 'latin-1'):
            try:
                return data.decode(enc), enc, True
            except UnicodeDecodeError:
                continue
        return None, None, False

    def _is_probably_binary(self, data: bytes) -> bool:
        if not data:
            return False
        if b'\x00' in data:
            return True
        textish = sum(1 for b in data if b in b'\n\r\t\f\b' or 32 <= b <= 126 or 128 <= b <= 255)
        return (textish / len(data)) < 0.85

    def _document_type(self, text: str) -> str:
        t = text[:5000]
        if re.search(r'<!doctype\s+html|<html[\s>]', t, re.I):
            return 'markup'
        if re.search(r'\b(color|margin|padding|display|font-size|background)\s*:', t) and re.search(r'\{[^}]+\}', t, re.S):
            return 'style'
        if re.search(r'\bSELECT\b.*\bFROM\b', t, re.I | re.S) or re.search(r'^\s*\{\s*\"', t):
            return 'data'
        if re.search(r'^\s*[A-Za-z0-9_-]+\s*:\s*.*$', t, re.M) and not re.search(r';', t):
            return 'config'
        if re.search(r'\b(function|class|def|import|public\s+class|#include|fn\s+main|package\s+main)\b', t, re.I):
            return 'code'
        return 'text'

    def _heuristic_candidates(self, text: str):
        out = []
        sample = text[:30000]
        for lang, patterns in self.heuristics.items():
            score = 0.0
            ev = []
            for pat, weight, note in patterns:
                if re.search(pat, sample, re.I | re.M | re.S):
                    score += weight
                    ev.append(f'heuristic:{note}')
            if score > 0:
                out.append({'language': lang, 'score': min(score, 0.82), 'evidence': ev})
        return out

    def _pygments_candidates(self, path: Path, text: str):
        if guess_lexer is None:
            return []
        out = []
        try:
            lexer = guess_lexer_for_filename(path.name, text) if guess_lexer_for_filename is not None else guess_lexer(text)
            aliases = getattr(lexer, 'aliases', []) or []
            name = (aliases[0] if aliases else getattr(lexer, 'name', '')).lower()
            mapped = self.name_map.get(name, name)
            out.append({'language': mapped, 'score': 0.72, 'evidence': [f'pygments:{getattr(lexer, "name", mapped)}']})
        except Exception:
            try:
                lexer = guess_lexer(text)
                aliases = getattr(lexer, 'aliases', []) or []
                name = (aliases[0] if aliases else getattr(lexer, 'name', '')).lower()
                mapped = self.name_map.get(name, name)
                out.append({'language': mapped, 'score': 0.65, 'evidence': [f'pygments:{getattr(lexer, "name", mapped)}']})
            except Exception:
                pass
        return out

    def _guesslang_candidates(self, text: str):
        if self.guesslang is None:
            return []
        out = []
        try:
            probs = self.guesslang.probabilities(text)
            for item in probs[:5]:
                lang = self.name_map.get(item['language_name'].lower(), item['language_name'].lower())
                score = float(item['probability'])
                out.append({'language': lang, 'score': min(max(score, 0.0), 0.99), 'evidence': [f"guesslang:{item['language_name']}={score:.3f}"]})
        except Exception:
            try:
                lang = self.guesslang.language_name(text)
                mapped = self.name_map.get(lang.lower(), lang.lower())
                out.append({'language': mapped, 'score': 0.75, 'evidence': [f'guesslang:{lang}']})
            except Exception:
                pass
        return out

    def _merge_candidates(self, aggregate: dict[str, dict[str, Any]], items: list[dict[str, Any]], engine: str):
        weights = {'heuristics': 0.9, 'pygments': 1.0, 'guesslang': 1.15}
        for item in items:
            lang = item['language']
            if lang not in aggregate:
                aggregate[lang] = {'language': lang, 'raw': 0.0, 'votes': 0, 'evidence': []}
            aggregate[lang]['raw'] += item['score'] * weights.get(engine, 1.0)
            aggregate[lang]['votes'] += 1
            aggregate[lang]['evidence'].extend(item.get('evidence', []))

    def _finalize_candidates(self, aggregate: dict[str, dict[str, Any]]):
        items = []
        for lang, data in aggregate.items():
            raw = data['raw']
            votes = data['votes']
            score = min(0.99, 0.22 * votes + (raw / 3.0))
            items.append({'language': lang, 'score': round(score, 3), 'votes': votes, 'evidence': data['evidence'][:8]})
        items.sort(key=lambda x: (x['score'], x['votes']), reverse=True)
        return items

    def _resolve_family_variant(self, language: str | None, text: str):
        if language is None:
            return None, None
        if language in {'html', 'xml'}:
            return 'web-markup', language
        if language == 'css':
            return 'web-style', 'css'
        if language in {'python', 'java', 'php', 'sql', 'yaml', 'json', 'shell', 'powershell', 'go', 'rust'}:
            family = {'python': 'python', 'java': 'jvm', 'php': 'php', 'sql': 'data', 'yaml': 'config', 'json': 'data', 'shell': 'scripting', 'powershell': 'scripting', 'go': 'native', 'rust': 'native'}[language]
            return family, language
        if language in {'c', 'cpp', 'csharp'}:
            family = {'c': 'c-family', 'cpp': 'c-family', 'csharp': '.net'}[language]
            return family, language
        if language in {'javascript', 'typescript'}:
            if re.search(r'<([A-Z][A-Za-z0-9]*|div|span|main|section|button)[^>]*>|return\s*\(\s*<', text, re.M | re.S):
                if re.search(r'\binterface\b|:\s*(string|number|boolean|unknown|any|never|void)\b', text):
                    return 'javascript', 'tsx'
                return 'javascript', 'jsx'
            if re.search(r'\binterface\s+\w+|\btype\s+\w+\s*=|:\s*(string|number|boolean|unknown|any|never|void)\b', text, re.M):
                return 'javascript', 'typescript'
            if re.search(r'\brequire\(|module\.exports|process\.', text):
                return 'javascript', 'nodejs'
            return 'javascript', 'javascript'
        return language, language

    def _detect_frameworks(self, text: str, path: Path):
        scores = defaultdict(float)
        sample = text[:80000]
        for name, pattern, weight in self.framework_rules:
            if re.search(pattern, sample, re.I | re.M | re.S):
                scores[name] += weight
        if path.name == 'package.json':
            for fw in self._frameworks_from_package_json(text):
                scores[fw] += 2.0
        elif path.name in {'pyproject.toml', 'requirements.txt'}:
            for fw in self._frameworks_from_python_manifest(text):
                scores[fw] += 2.0
        return [fw for fw, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]

    def _frameworks_from_package_json(self, text: str):
        result = []
        try:
            data = json.loads(text)
            deps = {}
            deps.update(data.get('dependencies', {}))
            deps.update(data.get('devDependencies', {}))
            mapping = {'react': 'react', 'next': 'next.js', 'vue': 'vue', '@angular/core': 'angular', 'svelte': 'svelte', 'express': 'express', '@nestjs/core': 'nest.js', 'tailwindcss': 'tailwindcss', 'bootstrap': 'bootstrap'}
            for pkg, name in mapping.items():
                if pkg in deps:
                    result.append(name)
        except Exception:
            pass
        return result

    def _frameworks_from_python_manifest(self, text: str):
        sample = text.lower()
        mapping = {'django': 'django', 'flask': 'flask', 'fastapi': 'fastapi', 'pydantic': 'pydantic', 'sqlalchemy': 'sqlalchemy', 'pytest': 'pytest'}
        return [name for key, name in mapping.items() if key in sample]


def analyze_repository_to_json(root: str | Path) -> str:
    detector = SourceDetector()
    result = detector.analyze_repository(root)
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Scan a repository and infer language/framework profile with explicit categories')
    parser.add_argument('path', help='Path to file or repository root')
    args = parser.parse_args()
    detector = SourceDetector()
    p = Path(args.path)
    if p.is_dir():
        print(json.dumps(detector.analyze_repository(p), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(asdict(detector.detect(p)), ensure_ascii=False, indent=2))
