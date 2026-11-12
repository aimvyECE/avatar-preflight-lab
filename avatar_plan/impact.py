"""Conservative review invalidation, not a proof of safe execution.

The graph represents review dependencies, not model performance. Unknown fields
invalidate all reviews. No media, identity information or changed values appear.
"""
REVIEWS = ('consent', 'licensing', 'runtime', 'voice', 'lipsync', 'human_qa', 'disclosure')
DEPENDENTS = {
    'consent': ('voice', 'lipsync'),
    'licensing': ('voice', 'lipsync'),
    'runtime': ('voice', 'lipsync'),
    'voice': ('lipsync',),
    'lipsync': ('human_qa',),
    'human_qa': ('disclosure',),
    'disclosure': (),
}


def _roots(path):
    # Broad buckets intentionally favor extra review over a missed dependency.
    if path == '/subject/synthetic_disclosure':
        return ('disclosure',)
    if path == '/subject' or path.startswith('/subject/'):
        return ('consent',)
    if path == '/runtime' or path.startswith('/runtime/'):
        return ('runtime',)
    if path == '/components' or path.startswith('/components/'):
        return ('licensing', 'runtime', 'voice')
    if path == '/media/reference_video':
        return ('consent', 'lipsync')
    if path in ('/media/audio', '/media/audio_origin'):
        return ('consent', 'voice')
    if path == '/media/duration_seconds':
        return ('runtime', 'voice')
    return REVIEWS


def review_impact(paths):
    """Map changed JSON Pointers to reviews that must be repeated.

    Deterministic conservative policy v1. A review unaffected by these paths is
    not thereby approved; existing declarations still need ordinary validation.
    """
    reasons = {review: set() for review in REVIEWS}
    for path in sorted(set(paths)):
        pending = list(_roots(path))
        visited = set()
        while pending:
            review = pending.pop()
            if review in visited:
                continue
            visited.add(review)
            reasons[review].add(path)
            pending.extend(DEPENDENTS[review])
    invalidated = [review for review in REVIEWS if reasons[review]]
    return {
        'policy': 'conservative-review-dependencies-v1',
        'invalidated_reviews': invalidated,
        'reasons': {review: sorted(reasons[review]) for review in invalidated},
        'unaffected_reviews': [review for review in REVIEWS if not reasons[review]],
        'meaning': 'Review guidance only. Unaffected does not mean approved; no prior approvals are stored or verified.',
    }
