# Candidate components, not integrated models

The following are upstream references to assess before an implementation. Names,
capabilities and licenses can change. Pin and review the actual artifact version,
weights, training-data restrictions and transitive dependencies separately.

| Candidate | Possible role | Review boundary |
|---|---|---|
| [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) | French speech / optional voice cloning | Distinguish Base cloning from CustomVoice controls; inspect the selected model card and consent requirements. |
| [MuseTalk](https://github.com/TMElyralab/MuseTalk) | Modify lip movement in a reference video | Review code, weights and dependencies separately; mouth edits do not generate a whole expressive performance. |
| [HeyGen TAVR](https://github.com/heygen-com/TAVR) | Research video-reference avatar generation | Not the commercial Avatar V service; upstream hardware and dependency requirements may be substantial. |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | Video composition and captions | Composition is not voice cloning or face animation. |

No candidate is bundled, installed, tested or endorsed by this project. There is no
claim that any candidate equals the quality of a commercial product. Real recorded
audio is also a valid starting point, requiring no voice synthesis model.

## Selection checklist

1. Record repository URL, exact revision and weight checksum.
2. Read separate code, weight and third-party licenses; record commercial limits.
3. Review model card, intended uses and known failures.
4. Test one consenting subject with a short clip and local storage.
5. Measure total time per accepted output, including retries and cleanup.
6. Document errors and do not extrapolate a benchmark from another GPU.
