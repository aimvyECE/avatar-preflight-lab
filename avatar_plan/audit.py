"""Deterministic, offline provenance for declarations; never reads media files."""
import hashlib
import json
from .core import plan


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON object key')
        result[key] = value
    return result


def fingerprint(data):
    """SHA-256 of sorted compact UTF-8 JSON, not a signature or identity proof."""
    payload = json.dumps(data, sort_keys=True, separators=(',', ':'),
                         ensure_ascii=False, allow_nan=False).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def changed_paths(before, after, path=''):
    """Return JSON Pointer paths only, never changed values. Lists are positional."""
    if type(before) is not type(after):
        return [path]
    if isinstance(before, dict):
        result = []
        for key in sorted(before.keys() | after.keys()):
            pointer = path + '/' + key.replace('~', '~0').replace('/', '~1')
            if key not in before or key not in after:
                result.append(pointer)
            else:
                result.extend(changed_paths(before[key], after[key], pointer))
        return result
    if isinstance(before, list):
        result = []
        for index in range(max(len(before), len(after))):
            pointer = path + '/' + str(index)
            if index >= len(before) or index >= len(after):
                result.append(pointer)
            else:
                result.extend(changed_paths(before[index], after[index], pointer))
        return result
    return [] if before == after else [path]


def audit(data, previous=None):
    result = plan(data)
    result['provenance'] = {'format': 'avatar-preflight-audit-v1',
                            'manifest_sha256': fingerprint(data),
                            'meaning': 'Content fingerprint only; not proof of consent, identity or authenticity.'}
    if previous is not None:
        paths = changed_paths(previous, data)
        result['comparison'] = {'previous_sha256': fingerprint(previous),
                                'changed_paths': paths,
                                'review_required': bool(paths),
                                'previous_status': plan(previous)['status']}
    return result
