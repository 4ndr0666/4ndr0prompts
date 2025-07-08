# ADR-0001 – Minimal Slot-by-Slot Interactive Flow with Wayland-Only Clipboard

**Status:** Accepted
**Date:** 2024-01-01

## Context
This project focuses on a simple prompt builder using fzf and wl-copy on Wayland systems.

## Decision
Provide only an interactive mode where each slot is chosen sequentially. Clipboard support is limited to wl-copy.

## Consequences
- Simplifies maintenance.
- Limits compatibility to Wayland environments.
