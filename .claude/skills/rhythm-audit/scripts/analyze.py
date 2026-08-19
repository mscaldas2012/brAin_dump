#!/usr/bin/env python3
"""
rhythm-audit: analyze.py
Computes prose rhythm metrics and outputs JSON.

Usage:
    python analyze.py <input_file>
    echo "text..." | python analyze.py -

Output: JSON to stdout
"""

import sys
import re
import json
import math
from collections import Counter


TRANSITION_WORDS = {
    # Heavy LLM transitions
    'moreover', 'furthermore', 'additionally', 'consequently', 'subsequently',
    'crucially', 'notably', 'importantly', 'undoubtedly', 'certainly',
    # Common but lighter
    'however', 'therefore', 'thus', 'hence', 'nevertheless', 'nonetheless',
    'meanwhile', 'likewise', 'similarly', 'conversely', 'alternatively',
    'specifically', 'particularly', 'essentially', 'ultimately', 'fundamentally',
}

SENTENCE_STARTERS_TO_WATCH = {
    'this', 'it', 'the', 'i', 'he', 'she', 'they', 'we', 'there',
}


def read_input(arg):
    if arg == '-':
        return sys.stdin.read()
    with open(arg, 'r', encoding='utf-8') as f:
        return f.read()


def split_sentences(text):
    """Split text into sentences."""
    # Split on sentence-ending punctuation followed by whitespace and a capital letter
    raw = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'])', text)
    sentences = [s.strip() for s in raw if s.strip()]
    return sentences


def split_paragraphs(text):
    """Split on blank lines."""
    paras = re.split(r'\n\s*\n', text.strip())
    return [p.strip() for p in paras if p.strip()]


def word_count(text):
    return len(text.split())


def is_fragment(sentence, threshold=4):
    """A stylistic fragment: a very short sentence (under threshold words) used as a beat."""
    return word_count(sentence) < threshold


def stats(values):
    if not values:
        return {'mean': 0, 'stddev': 0, 'min': 0, 'max': 0, 'median': 0}
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    stddev = math.sqrt(variance)
    sorted_v = sorted(values)
    median = sorted_v[n // 2] if n % 2 == 1 else (sorted_v[n//2 - 1] + sorted_v[n//2]) / 2
    return {
        'mean': round(mean, 1),
        'stddev': round(stddev, 1),
        'min': min(values),
        'max': max(values),
        'median': round(median, 1),
    }


def analyze(text):
    sentences = split_sentences(text)
    paragraphs = split_paragraphs(text)
    words = text.split()
    total_words = len(words)

    # --- Sentence metrics ---
    sent_lengths = [word_count(s) for s in sentences if word_count(s) > 0]
    sent_stats = stats(sent_lengths)

    # Fragment count (very short sentences used as stylistic beats)
    fragments = [s for s in sentences if is_fragment(s, threshold=6)]
    fragment_count = len(fragments)
    fragment_examples = fragments[:3]

    # Long sentence count (>35 words — potential overload)
    long_sentences = [s for s in sentences if word_count(s) > 35]

    # Sentence length distribution buckets
    buckets = {'short_1_8': 0, 'medium_9_20': 0, 'long_21_35': 0, 'very_long_36plus': 0}
    for l in sent_lengths:
        if l <= 8:
            buckets['short_1_8'] += 1
        elif l <= 20:
            buckets['medium_9_20'] += 1
        elif l <= 35:
            buckets['long_21_35'] += 1
        else:
            buckets['very_long_36plus'] += 1

    # --- Paragraph metrics ---
    para_lengths = [word_count(p) for p in paragraphs]
    para_stats = stats(para_lengths)

    # Paragraph length range as % of mean (uniformity signal)
    if para_stats['mean'] > 0:
        para_range_pct = round((para_stats['max'] - para_stats['min']) / para_stats['mean'] * 100, 1)
    else:
        para_range_pct = 0

    # --- Em-dash density ---
    em_dash_count = text.count('—') + text.count('--')
    em_dash_per_100_words = round(em_dash_count / total_words * 100, 2) if total_words else 0

    # --- Transition word density ---
    word_lower = [w.strip('.,;:!?"\'()[]').lower() for w in words]
    transition_hits = [(w, i) for i, w in enumerate(word_lower) if w in TRANSITION_WORDS]
    transition_count = len(transition_hits)
    transition_rate_per_100 = round(transition_count / total_words * 100, 2) if total_words else 0
    transition_examples = [words[i] for _, i in transition_hits[:5]]

    # --- Sentence opener analysis ---
    openers = []
    for s in sentences:
        first = s.split()[0].lower().strip('",\'') if s.split() else ''
        if first:
            openers.append(first)

    opener_freq = Counter(openers)
    # Flag openers appearing more than 2 times AND in the watch list, or >3 times any word
    repeated_openers = {
        word: count for word, count in opener_freq.items()
        if (word in SENTENCE_STARTERS_TO_WATCH and count > 2) or count > 3
    }

    # --- Rhythm signals ---
    # Coefficient of variation for sentence length (low = uniform = bad)
    cv = round(sent_stats['stddev'] / sent_stats['mean'] * 100, 1) if sent_stats['mean'] > 0 else 0

    # Consecutive similar-length check (runs of same bucket)
    bucket_sequence = []
    for l in sent_lengths:
        if l <= 8:
            bucket_sequence.append('S')
        elif l <= 20:
            bucket_sequence.append('M')
        elif l <= 35:
            bucket_sequence.append('L')
        else:
            bucket_sequence.append('XL')

    # Find runs of 4+ same-bucket sentences
    runs = []
    i = 0
    while i < len(bucket_sequence):
        j = i
        while j < len(bucket_sequence) and bucket_sequence[j] == bucket_sequence[i]:
            j += 1
        if j - i >= 4:
            runs.append({'bucket': bucket_sequence[i], 'length': j - i, 'start_sentence': i + 1})
        i = j

    # --- Compile flags ---
    flags = []

    if cv < 35 and len(sent_lengths) >= 5:
        flags.append({
            'type': 'low_sentence_variety',
            'severity': 'high' if cv < 20 else 'medium',
            'message': f'Sentence length variance is low (CV={cv}%). Sentences cluster around {sent_stats["mean"]} words. Prose may feel metronomic.',
        })

    if fragment_count == 0 and len(sentences) >= 5:
        flags.append({
            'type': 'no_fragments',
            'severity': 'low',
            'message': 'No sentence fragments detected. Writers use fragments for emphasis and pace — their complete absence can feel controlled or flat.',
        })

    if para_range_pct < 40 and len(paragraphs) >= 3:
        flags.append({
            'type': 'uniform_paragraphs',
            'severity': 'medium',
            'message': f'Paragraph lengths are uniform (range is only {para_range_pct}% of the mean). Real prose breathes — vary paragraph weight deliberately.',
        })

    if em_dash_per_100_words > 0.8:
        flags.append({
            'type': 'em_dash_density',
            'severity': 'medium' if em_dash_per_100_words < 1.5 else 'high',
            'message': f'High em-dash density: {em_dash_count} em-dash(es) per {total_words} words ({em_dash_per_100_words} per 100). LLMs overuse em-dashes as clause connectors.',
        })

    if transition_rate_per_100 > 1.5:
        flags.append({
            'type': 'transition_overload',
            'severity': 'medium' if transition_rate_per_100 < 3 else 'high',
            'message': f'Transition word density is high: {transition_count} instances ({transition_rate_per_100} per 100 words). Stacked transitions signal scaffolded rather than earned logic.',
        })

    if repeated_openers:
        top = sorted(repeated_openers.items(), key=lambda x: -x[1])
        examples = ', '.join(f'"{w}" ({c}x)' for w, c in top[:3])
        flags.append({
            'type': 'repeated_openers',
            'severity': 'medium',
            'message': f'Repeated sentence openers: {examples}. Monotone sentence openings reduce rhythmic variety.',
        })

    if runs:
        run_desc = ', '.join(f'{r["length"]} consecutive {r["bucket"]}-length sentences starting at sentence {r["start_sentence"]}' for r in runs[:2])
        flags.append({
            'type': 'length_run',
            'severity': 'low',
            'message': f'Runs of same-length sentences detected: {run_desc}.',
        })

    # --- Build output ---
    return {
        'total_words': total_words,
        'total_sentences': len(sentences),
        'total_paragraphs': len(paragraphs),
        'sentence_length': {
            **sent_stats,
            'distribution': buckets,
            'length_sequence': sent_lengths,
            'coefficient_of_variation_pct': cv,
            'long_sentence_count': len(long_sentences),
        },
        'paragraph_length': {
            **para_stats,
            'range_pct_of_mean': para_range_pct,
            'lengths': para_lengths,
        },
        'fragments': {
            'count': fragment_count,
            'examples': fragment_examples,
        },
        'em_dashes': {
            'count': em_dash_count,
            'per_100_words': em_dash_per_100_words,
        },
        'transitions': {
            'count': transition_count,
            'per_100_words': transition_rate_per_100,
            'examples': transition_examples,
        },
        'sentence_openers': {
            'repeated': repeated_openers,
        },
        'rhythm_runs': runs,
        'flags': flags,
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python analyze.py <file> or echo "text" | python analyze.py -', file=sys.stderr)
        sys.exit(1)

    text = read_input(sys.argv[1])
    result = analyze(text)
    print(json.dumps(result, indent=2))
