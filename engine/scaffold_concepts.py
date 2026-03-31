"""
🏗️ Concept Coverage Scaffold — auto-suggest concept tags for lesson.yaml files.

Usage:
    python -m engine.scaffold_concepts [--apply] [--section NUM]

Reads each lesson.yaml, analyses existing tags, and suggests matching
concept IDs from concept_graph.yaml.  With --apply, writes the suggested
`concepts:` field into the YAML files.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List, Set, Tuple

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from engine.concepts import load_concept_graph, ConceptNode


def _build_tag_to_concepts(graph: Dict[str, ConceptNode]) -> Dict[str, List[str]]:
    """Build reverse lookup: lowercase tag → list of concept IDs."""
    lookup: Dict[str, List[str]] = {}

    for cid, node in graph.items():
        # Map by concept ID parts
        parts = cid.split(".")
        for part in parts:
            lookup.setdefault(part.lower(), []).append(cid)

        # Map by category
        lookup.setdefault(node.category.lower(), []).append(cid)

    # Common aliases
    aliases = {
        "basics": ["python.variables", "python.types", "python.operators"],
        "fundamentals": [
            "python.variables",
            "python.types",
            "python.conditions",
            "python.loops",
        ],
        "functions": ["python.functions", "python.function_params"],
        "strings": ["python.strings", "python.string_methods"],
        "formatting": ["python.fstrings"],
        "lists": ["python.lists", "python.list_indexing", "python.list_methods"],
        "comprehensions": ["python.list_comprehensions"],
        "dictionaries": ["python.dicts", "python.dict_methods"],
        "dict": ["python.dicts"],
        "sets": ["python.sets"],
        "tuples": ["python.tuples"],
        "loops": ["python.loops", "python.loop_control"],
        "conditions": ["python.conditions"],
        "boolean": ["python.boolean_logic"],
        "files": ["python.file_io"],
        "exceptions": ["python.exceptions"],
        "classes": ["oop.classes", "oop.init"],
        "inheritance": ["oop.inheritance"],
        "polymorphism": ["oop.polymorphism"],
        "encapsulation": ["oop.encapsulation"],
        "abstract": ["oop.abstract_classes"],
        "dataclass": ["oop.dataclasses"],
        "decorator": ["python.decorators"],
        "generator": ["python.generators"],
        "sorting": ["ds.sorting"],
        "searching": ["ds.searching"],
        "recursion": ["ds.recursion"],
        "trees": ["ds.trees"],
        "graphs": ["ds.graphs"],
        "stacks": ["ds.stacks_queues"],
        "queues": ["ds.stacks_queues"],
        "linked": ["ds.linked_lists"],
        "hash": ["ds.hash_tables"],
        "dynamic": ["ds.dynamic_programming"],
        "big-o": ["ds.big_o"],
    }
    for tag, concepts in aliases.items():
        existing = lookup.get(tag, [])
        for cid in concepts:
            if cid not in existing and cid in graph:
                existing.append(cid)
        lookup[tag] = existing

    return lookup


def suggest_concepts_for_lesson(
    yaml_path: str, graph: Dict[str, ConceptNode], lookup: Dict[str, List[str]]
) -> Tuple[List[str], List[str]]:
    """Suggest concept IDs based on lesson tags and name.

    Returns (existing_concepts, suggested_concepts).
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    existing = data.get("concepts", []) or []
    tags = [t.lower() for t in (data.get("tags", []) or [])]
    name = (data.get("name", "") or "").lower()

    candidates: Set[str] = set()
    for tag in tags:
        for cid in lookup.get(tag, []):
            candidates.add(cid)
    # Also check name words
    for word in name.replace("-", " ").replace("_", " ").split():
        for cid in lookup.get(word, []):
            candidates.add(cid)

    suggested = sorted(candidates - set(existing))
    return existing, suggested


def find_all_lesson_yamls(section_filter: str = "") -> List[str]:
    """Find all lesson.yaml files, optionally filtered by section number."""
    yamls = []
    for dirpath, _, filenames in os.walk(ROOT):
        if "lesson.yaml" in filenames:
            full = os.path.join(dirpath, "lesson.yaml")
            if section_filter:
                rel = os.path.relpath(dirpath, ROOT)
                if not rel.startswith(f"{section_filter}_"):
                    continue
            yamls.append(full)
    return sorted(yamls)


def scaffold(section_filter: str = "", apply: bool = False) -> Dict[str, dict]:
    """Run scaffold across all lessons. Returns report dict."""
    graph = load_concept_graph()
    lookup = _build_tag_to_concepts(graph)
    report: Dict[str, dict] = {}

    for yaml_path in find_all_lesson_yamls(section_filter):
        rel = os.path.relpath(yaml_path, ROOT)
        existing, suggested = suggest_concepts_for_lesson(yaml_path, graph, lookup)

        entry = {
            "existing": existing,
            "suggested": suggested,
            "applied": False,
        }

        if apply and suggested:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            merged = sorted(set((existing or []) + suggested))
            data["concepts"] = merged

            with open(yaml_path, "w", encoding="utf-8") as f:
                yaml.dump(
                    data,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                )
            entry["applied"] = True
            entry["final"] = merged

        report[rel] = entry

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold concept tags for lesson.yaml files"
    )
    parser.add_argument(
        "--apply", action="store_true", help="Write suggested concepts to YAML files"
    )
    parser.add_argument(
        "--section", default="", help="Filter by section number (e.g. '01')"
    )
    args = parser.parse_args()

    report = scaffold(section_filter=args.section, apply=args.apply)

    total = len(report)
    has_concepts = sum(1 for v in report.values() if v["existing"])
    new_suggestions = sum(1 for v in report.values() if v["suggested"])
    applied = sum(1 for v in report.values() if v.get("applied"))

    print(f"\n📊 Concept Coverage Report")
    print(f"{'=' * 50}")
    print(f"Total lessons scanned: {total}")
    print(f"Already have concepts: {has_concepts}")
    print(f"New suggestions:       {new_suggestions}")
    if args.apply:
        print(f"Applied:               {applied}")

    print(f"\n{'─' * 50}")
    for path, info in report.items():
        status = "✅" if info["existing"] else "⬜"
        if info["suggested"]:
            status = "🆕" if not info.get("applied") else "✏️"
        print(f"{status} {path}")
        if info["existing"]:
            print(f"   existing: {', '.join(info['existing'])}")
        if info["suggested"]:
            print(f"   suggest:  {', '.join(info['suggested'])}")


if __name__ == "__main__":
    main()
