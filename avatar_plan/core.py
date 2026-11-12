"""Deterministic preflight checks for an experimental talking-avatar workflow.

Checks declarations, not their truth: consent, licensing and actual media still
require human review. No network, subprocess, model imports or media execution.
"""
from dataclasses import dataclass
from math import isfinite
from pathlib import PurePosixPath
from typing import Any


@dataclass(frozen=True)
class Issue:
    field: str
    message: str


ROOT_FIELDS = {"schema_version", "purpose", "subject", "media", "runtime", "components"}


def finite_number(value: Any) -> bool:
    return type(value) is int or (type(value) is float and isfinite(value))


def validate(data: Any) -> list[Issue]:
    issues: list[Issue] = []

    def problem(field: str, message: str) -> None:
        issues.append(Issue(field, message))

    def object_at(value: Any, field: str, fields: set[str]) -> dict:
        if not isinstance(value, dict):
            problem(field, "must be an object")
            return {}
        for key in sorted(set(value) - fields):
            problem(f"{field}.{key}", "unknown field")
        for key in sorted(fields - set(value)):
            problem(f"{field}.{key}", "required field")
        return value

    def positive(value: Any, field: str, cap: float | None = None) -> None:
        if not finite_number(value) or value <= 0:
            problem(field, "must be a finite positive number")
        elif cap is not None and value > cap:
            problem(field, f"prototype cap is {cap:g}; split the test clip")

    def local_path(value: Any, field: str) -> None:
        # Conservative portable subset. These checks are NOT a file access sandbox.
        if (not isinstance(value, str) or not value.strip() or
                '\\' in value or ':' in value or value.startswith('/') or
                any(c in value for c in ('\x00', '\n', '\r')) or
                any(part in ('', '.', '..') for part in value.split('/'))):
            problem(field, "must be a relative POSIX path without traversal or URLs")
        elif not PurePosixPath(value).suffix:
            problem(field, "must include a file extension")

    root = object_at(data, "manifest", ROOT_FIELDS)
    if type(root.get("schema_version")) is not int or root.get("schema_version") != 1:
        problem("schema_version", "only integer schema version 1 is supported")
    if root.get("purpose") not in ("personal", "commercial"):
        problem("purpose", "must be personal or commercial")

    subject = object_at(root.get("subject"), "subject", {"consent_record", "consent_reviewed", "synthetic_disclosure"})
    local_path(subject.get("consent_record"), "subject.consent_record")
    for key in ("consent_reviewed", "synthetic_disclosure"):
        if subject.get(key) is not True:
            problem(f"subject.{key}", "must explicitly be true")

    media = object_at(root.get("media"), "media", {"reference_video", "audio", "duration_seconds", "audio_origin"})
    for key in ("reference_video", "audio"):
        local_path(media.get(key), f"media.{key}")
    positive(media.get("duration_seconds"), "media.duration_seconds", 30)
    if media.get("audio_origin") not in ("recorded", "generated"):
        problem("media.audio_origin", "must be recorded or generated")

    runtime = object_at(root.get("runtime"), "runtime", {"network_allowed", "gpu_memory_gib"})
    if runtime.get("network_allowed") is not False:
        problem("runtime.network_allowed", "this prototype supports offline plans only")
    positive(runtime.get("gpu_memory_gib"), "runtime.gpu_memory_gib")

    components = root.get("components")
    if not isinstance(components, list) or not components:
        problem("components", "must be a nonempty list")
        return issues
    roles: list[str] = []
    for index, component in enumerate(components):
        prefix = f"components[{index}]"
        obj = object_at(component, prefix, {"role", "name", "revision", "license_reviewed", "commercial_use_allowed", "model_path", "tested_gpu_memory_gib"})
        role = obj.get("role")
        if role not in ("voice", "lipsync"):
            problem(prefix + ".role", "must be voice or lipsync")
        else:
            roles.append(role)
        for key in ("name", "revision"):
            if not isinstance(obj.get(key), str) or not obj.get(key, "").strip():
                problem(prefix + "." + key, "must be a nonempty string")
        if obj.get("revision") in ("main", "latest", "master"):
            problem(prefix + ".revision", "pin a specific reviewed revision, not a moving branch")
        local_path(obj.get("model_path"), prefix + ".model_path")
        if obj.get("license_reviewed") is not True:
            problem(prefix + ".license_reviewed", "code, weights and dependencies must be reviewed")
        if type(obj.get("commercial_use_allowed")) is not bool:
            problem(prefix + ".commercial_use_allowed", "must be boolean")
        elif root.get("purpose") == "commercial" and not obj["commercial_use_allowed"]:
            problem(prefix + ".commercial_use_allowed", "commercial use not declared allowed")
        memory = obj.get("tested_gpu_memory_gib")
        positive(memory, prefix + ".tested_gpu_memory_gib")
        available = runtime.get("gpu_memory_gib")
        if (finite_number(memory) and finite_number(available) and memory > available):
            problem(prefix + ".tested_gpu_memory_gib", "exceeds declared GPU memory")
    expected = ["lipsync"] + (["voice"] if media.get("audio_origin") == "generated" else [])
    if sorted(roles) != sorted(expected):
        problem("components", f"exactly these roles required: {', '.join(expected)}")
    return issues


def plan(data: Any) -> dict:
    issues = validate(data)
    if issues:
        return {"status": "blocked", "issues": [vars(issue) for issue in issues], "steps": []}
    steps = ["Review consent, identity, licenses and media manually"]
    if data["media"]["audio_origin"] == "generated":
        steps.append("Generate audio using a separately implemented and audited adapter")
    steps.extend(["Run a separately implemented lip-sync adapter", "Review identity, pronunciation, sync and artifacts", "Add synthetic-media disclosure and export after approval"])
    return {
        "status": "declarations_valid",
        "issues": [],
        "steps": steps,
        "warning": "No generation performed. Declarations and GPU numbers are not independently verified.",
        "clip_seconds": data["media"]["duration_seconds"],
    }
