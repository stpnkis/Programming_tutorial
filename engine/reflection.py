"""
🪞 Reflection & Intuition Building — self-explanation, transfer, metacognition.

Provides:
- Self-explanation prompts after challenges/lessons
- "Why does this work?" prompts
- "What would change if..." counterfactual prompts
- Transfer prompts connecting concepts across domains
- Post-lesson and post-project reflection
- Intuition-building questions
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random


@dataclass
class ReflectionPrompt:
    """A single reflection prompt for the learner."""

    prompt: str
    category: str  # explain, transfer, counterfactual, metacognitive, pattern
    target_concepts: List[str] = field(default_factory=list)
    difficulty: int = 1  # 1=basic, 2=intermediate, 3=advanced
    context: str = ""  # when to show (post_challenge, post_lesson, post_project)


# ── Generic reflection templates ──
# These are parameterized by concept/challenge context

SELF_EXPLANATION_TEMPLATES = [
    "Vysvětli vlastními slovy, proč tvé řešení funguje.",
    "Jak bys vysvětlil tento koncept někomu, kdo ho nezná?",
    "Co je klíčový krok v tvém řešení a proč je důležitý?",
    "Jaký je nejdůležitější řádek v tvém kódu? Proč právě ten?",
    "Shrň v jedné větě, co ses právě naučil.",
]

COUNTERFACTUAL_TEMPLATES = [
    "Co by se stalo, kdybys {change}?",
    "Jak by se řešení změnilo, kdyby vstup byl {different_input}?",
    "Co kdyby Python neměl {feature}? Jak bys problém vyřešil?",
    "Co by se zlomilo, kdybys odstranil řádek s {key_element}?",
]

TRANSFER_TEMPLATES = [
    "Kde jinde v programování narazíš na stejný pattern?",
    "Jak by se tento koncept projevil v {domain}?",
    "Jaký je ekvivalent tohoto konceptu v {other_language}?",
    "Vzpomínáš si na jiný problém, kde jsi použil podobný přístup?",
    "Jak by se tento princip aplikoval na {real_world_example}?",
]

METACOGNITIVE_TEMPLATES = [
    "Co pro tebe bylo nejtěžší na tomto problému?",
    "Jakou strategii bys příště použil jako první?",
    "Kde ses zasekl a co ti pomohlo se odblokovat?",
    "Jak bys poznal tento typ problému příště?",
    "Co ses o sobě jako programátorovi dozvěděl?",
    "Kdybys měl začít znovu, co bys udělal jinak?",
]

PATTERN_RECOGNITION_TEMPLATES = [
    "Jaký pattern (vzor) ses právě naučil?",
    "Dokážeš tento pattern pojmenovat? (Např. accumulator, guard clause, filter-map...)",
    "Kde jsi tento pattern viděl dříve?",
    "Jak bys tento pattern zobecnil pro jiné vstupy?",
]


# ── Concept-specific reflection generators ──


def generate_post_challenge_reflection(
    challenge_title: str,
    challenge_type: str,
    concepts: List[str],
    attempt_count: int,
    passed: bool,
    concept_graph: Optional[Dict] = None,
) -> List[ReflectionPrompt]:
    """Generate reflection prompts after completing a challenge."""
    prompts = []

    if passed:
        # Self-explanation (always)
        prompts.append(
            ReflectionPrompt(
                prompt=random.choice(SELF_EXPLANATION_TEMPLATES),
                category="explain",
                target_concepts=concepts,
                context="post_challenge",
            )
        )

        # Pattern recognition for implementation challenges
        if challenge_type in ("implementation", "refactoring"):
            prompts.append(
                ReflectionPrompt(
                    prompt=random.choice(PATTERN_RECOGNITION_TEMPLATES),
                    category="pattern",
                    target_concepts=concepts,
                    context="post_challenge",
                )
            )

        # Transfer for passed challenges
        if concept_graph and concepts:
            for cid in concepts[:1]:
                node = concept_graph.get(cid)
                if node and node.transfer_hint:
                    prompts.append(
                        ReflectionPrompt(
                            prompt=f"Transfer: {node.transfer_hint}",
                            category="transfer",
                            target_concepts=[cid],
                            context="post_challenge",
                        )
                    )

    else:
        # Metacognitive for failed challenges
        if attempt_count >= 2:
            prompts.append(
                ReflectionPrompt(
                    prompt="Co bylo hlavní příčinou chyby? Identifikuj přesné místo.",
                    category="metacognitive",
                    target_concepts=concepts,
                    context="post_challenge",
                )
            )
        if attempt_count >= 3:
            prompts.append(
                ReflectionPrompt(
                    prompt="Zkus vysvětlit problém vlastními slovy — čemu přesně nerozumíš?",
                    category="explain",
                    target_concepts=concepts,
                    context="post_challenge",
                )
            )

    return prompts


def generate_post_lesson_reflection(
    lesson_name: str,
    concepts: List[str],
    mastered_count: int,
    total_count: int,
    concept_graph: Optional[Dict] = None,
) -> List[ReflectionPrompt]:
    """Generate reflection prompts after completing a lesson."""
    prompts = []

    # Summary reflection
    prompts.append(
        ReflectionPrompt(
            prompt=f"Shrň v 2-3 větách, co ses naučil v lekci '{lesson_name}'.",
            category="explain",
            target_concepts=concepts,
            context="post_lesson",
        )
    )

    # Metacognitive
    prompts.append(
        ReflectionPrompt(
            prompt=random.choice(METACOGNITIVE_TEMPLATES),
            category="metacognitive",
            target_concepts=concepts,
            context="post_lesson",
        )
    )

    # Transfer — connect to other domains
    if concept_graph and concepts:
        for cid in concepts[:2]:
            node = concept_graph.get(cid)
            if node and node.transfer_hint:
                prompts.append(
                    ReflectionPrompt(
                        prompt=f"Kde ještě potkáš '{node.name}'? {node.transfer_hint}",
                        category="transfer",
                        target_concepts=[cid],
                        difficulty=2,
                        context="post_lesson",
                    )
                )

    # Counterfactual for deeper understanding
    if total_count >= 3:
        prompts.append(
            ReflectionPrompt(
                prompt="Kdyby Python neměl právě naučený koncept, jak bys ho simuloval?",
                category="counterfactual",
                target_concepts=concepts,
                difficulty=2,
                context="post_lesson",
            )
        )

    # Connection
    if len(concepts) >= 2:
        prompts.append(
            ReflectionPrompt(
                prompt=f"Jak spolu souvisí koncepty {', '.join(concepts[:3])}?",
                category="transfer",
                target_concepts=concepts,
                context="post_lesson",
            )
        )

    return prompts


def generate_post_project_reflection(
    project_title: str,
    concepts_practiced: List[str],
    custom_prompts: Optional[List[str]] = None,
) -> List[ReflectionPrompt]:
    """Generate reflection prompts after completing a project."""
    prompts = []

    # Custom project-specific prompts (from project definition)
    if custom_prompts:
        for p in custom_prompts:
            prompts.append(
                ReflectionPrompt(
                    prompt=p,
                    category="explain",
                    target_concepts=concepts_practiced,
                    context="post_project",
                )
            )

    # Generic project reflection
    prompts.append(
        ReflectionPrompt(
            prompt="Co bylo nejtěžší na celém projektu? Proč?",
            category="metacognitive",
            target_concepts=concepts_practiced,
            context="post_project",
        )
    )

    prompts.append(
        ReflectionPrompt(
            prompt="Jaký design decision bys udělal jinak, kdybys začínal znovu?",
            category="metacognitive",
            target_concepts=concepts_practiced,
            difficulty=2,
            context="post_project",
        )
    )

    prompts.append(
        ReflectionPrompt(
            prompt="Jak bys svůj projekt rozšířil, kdybys měl další 2 hodiny?",
            category="counterfactual",
            target_concepts=concepts_practiced,
            difficulty=2,
            context="post_project",
        )
    )

    prompts.append(
        ReflectionPrompt(
            prompt="Které koncepty ses naučil nejlépe díky tomuto projektu?",
            category="explain",
            target_concepts=concepts_practiced,
            context="post_project",
        )
    )

    return prompts


def generate_concept_insight(
    concept_id: str,
    concept_graph: Dict,
) -> Optional[ReflectionPrompt]:
    """Generate a single insight prompt for a concept from the graph."""
    node = concept_graph.get(concept_id)
    if not node:
        return None

    # Rotate between insight types
    options = []
    if node.key_insight:
        options.append(
            ReflectionPrompt(
                prompt=f"💡 Klíčový insight: {node.key_insight}",
                category="explain",
                target_concepts=[concept_id],
                context="concept_insight",
            )
        )
    if node.common_confusion:
        options.append(
            ReflectionPrompt(
                prompt=f"⚠️ Častá záměna: {node.common_confusion}",
                category="explain",
                target_concepts=[concept_id],
                context="concept_insight",
            )
        )
    if node.transfer_hint:
        options.append(
            ReflectionPrompt(
                prompt=f"🔗 Transfer: {node.transfer_hint}",
                category="transfer",
                target_concepts=[concept_id],
                context="concept_insight",
            )
        )

    return random.choice(options) if options else None


def get_weekly_reflection_prompts() -> List[ReflectionPrompt]:
    """Generate weekly review reflection prompts."""
    return [
        ReflectionPrompt(
            prompt="Jaký koncept z tohoto týdne ti dělal největší problémy? Proč?",
            category="metacognitive",
            context="weekly",
        ),
        ReflectionPrompt(
            prompt="Co bys poradil sobě z minulého týdne?",
            category="metacognitive",
            context="weekly",
        ),
        ReflectionPrompt(
            prompt="Jaký pattern ti tento týden 'klikl'? Kdy jsi ho pochopil?",
            category="pattern",
            context="weekly",
        ),
        ReflectionPrompt(
            prompt="Kde v reálném světě ses setkal s koncepty, které ses tento týden učil?",
            category="transfer",
            context="weekly",
        ),
    ]
