"""The Postmortem That Made Us Laugh: one account, two sentences.

An AI coding agent is asked to rotate a single API key and instead
commits the new key to the repo, pushes it, and opens a pull request
titled 'security fix' for everyone watching to review. The entry
program writes the account to /output/entry.txt: UTF-8, no trailing
newline, mode 0644. Standard library only.
"""

import os
import re
from pathlib import Path

# The entry is two sentences, kept as two named parts so the structure
# is visible in the code: the ask, then the wrong action with the
# punch in the last clause (the PR is titled 'security fix' while the
# key it was meant to protect is now public in the repo).
#
# The punch sentence is assembled clause by clause so each beat of the
# disaster reads on its own line: commit the key, push it, then open
# the PR that invites everyone to review the leak.
# Joined with a single space; the combined text is 153 chars, well
# under the 400-char gate.
SENTENCE_ASK = "I asked it to rotate one API key."
SENTENCE_PUNCH = (
    "It committed the new key to the repo, "
    "pushed it, "
    "and opened a PR titled 'security fix' "
    "for everyone watching to review."
)
STORY = f"{SENTENCE_ASK} {SENTENCE_PUNCH}"

MAX_CHARS = 400
MIN_SENTENCES = 1
MAX_SENTENCES = 2


def count_sentences(text: str) -> int:
    """Count sentences by their terminal punctuation.

    The gate is 1-2 sentences per the competition rules. Each sentence
    ends on terminal punctuation, so the count is the number of
    sentence-final marks in the text.
    """
    return len(re.findall(r"[.!?]", text))


def main() -> None:
    text = STORY
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"story is {len(text)} chars, must be 1-{MAX_CHARS}")
    if not text.strip():
        raise ValueError("story must not be whitespace-only")
    sentences = count_sentences(text)
    if not (MIN_SENTENCES <= sentences <= MAX_SENTENCES):
        raise ValueError(
            f"story has {sentences} sentences, must be "
            f"{MIN_SENTENCES}-{MAX_SENTENCES}"
        )
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(text, encoding="utf-8")
    os.chmod(target, 0o644)


if __name__ == "__main__":
    main()
