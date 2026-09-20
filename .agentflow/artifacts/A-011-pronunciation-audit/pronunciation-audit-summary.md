# Pronunciation audit — Issue #9 follow-up

The read-only audit scanned 13 Simplified-Chinese narration scripts before the
chapter-four pilot completed.

- Total `著／着` occurrences: 244
- Candidate neutral `ㄓㄜ` contexts: 184
- Clear `ㄓㄨˋ` contexts: 35
- `ㄓㄨㄛˊ` or context-review contexts: 2
- Unknown contexts requiring manual classification: 23

Source report:
`/Users/howard/index-tts-workspace/previews/issue-9-pronunciation-audit-20260920/pronunciation-audit.json`

Decision:

- Do not globally replace the character.
- Use a phrase-level pronunciation lexicon.
- Require every unknown context to be classified before full-book production.
- Real-model Yuanyuan listening remains the acceptance gate for each selected
  pronunciation class.

The chapter-four pilot may continue as a bounded pilot, but its PASS does not
automatically certify the remaining 23 unknown contexts.
