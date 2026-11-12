# tiny-chess-01 entry — "Micro Negamax II"

An original micro chess engine for the make.fun tiny-chess-01
competition, written from scratch. No code from any existing engine
is used.

main.py (3,816 bytes) is a zlib/base85-packed payload with its
unpacker, as the competition's size rule expressly allows (the
house baseline is packed the same way). The unpacked engine is a
single Python file using only the standard library; it reads no
other file.

Design: 0x88 board, copy-make, negamax with alpha-beta pruning and
principal-variation search, a transposition table keyed by
incremental Zobrist hashing, killer-move ordering, MVV-LVA capture
ordering, and quiescence over captures and promotions that also
searches every evasion when in check. Move generation is fully
legal (castling legality and en-passant captures included) and is
proven by exact perft counts against a reference implementation
(startpos, Kiwipete, and the standard perft suite including
en-passant pin positions). Evaluation is material plus
formula-built piece-square tables (pawn advancement and centre,
knight/bishop centrality, seventh-rank rook, phase-blended king)
and the bishop pair.

It searches under a fixed budget of 40,000 nodes per move with no
clocks and no randomness, so every replay of a trial is
byte-identical. The program plays the whole gauntlet through the
env at MAKEFUN_ENV_URL (POST /game, POST /move), exactly as the
kit's protocol specifies.
