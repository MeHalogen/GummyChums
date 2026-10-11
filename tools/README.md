# tools

## visual-baseline.mjs

Captures the home and product pages in real Safari at phone and desktop widths,
so a refactor can be checked against "nothing moved".

    node tools/visual-baseline.mjs capture before
    node tools/visual-baseline.mjs capture after
    node tools/visual-baseline.mjs compare before after

**It compares PNG bytes, not pixels.** Byte-identical is a strong pass. Anything
else only means "look at these two images" — antialiasing, a cursor, a lazy image
arriving a frame later, and font rasterisation all change bytes without changing
the design. Treat a DIFFERS result as a prompt to open both files, never as proof
of a regression.

Requires `shopify theme dev` on port 9292 and `safaridriver -p 4712`.
