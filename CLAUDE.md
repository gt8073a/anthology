# Anthology — Project Instructions for Claude Code

## Core Design Principle

**Build things any capable AI can follow.**

All instructions, operator manuals, and game logic live in plain markdown and JSON.
No Claude-specific APIs. No tool-dependent logic. If it can't be read and followed by
any sufficiently capable AI with file access, it doesn't belong in the vault.

This keeps Anthology portable without slowing down development now.
