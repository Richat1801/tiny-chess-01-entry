# tiny-chess-01 entry — "Micro Negamax"

An original micro chess engine in a single Python file (4,096 bytes),
written from scratch for the make.fun tiny-chess-01 competition.
No code from any existing engine is used.

Design: 0x88 board, copy-make, negamax with alpha-beta pruning,
quiescence search over captures, MVV-LVA-style move ordering, and a
material + positional evaluation (piece centrality, pawn advancement,
phase-aware king placement). It searches under a fixed node budget
(24,000 nodes per move) with no clocks and no randomness, so every
replay of a trial is byte-identical.

The program plays the whole gauntlet through the env at
MAKEFUN_ENV_URL (POST /game, POST /move), exactly as the kit's
protocol specifies. Python 3.13 standard library only; main.py reads
no other file.
