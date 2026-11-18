#!/usr/bin/env python3
"""Generate demo.gif: original terminal-style walkthrough for the Field Manual.
Signup -> kit -> build -> bundle -> check -> submit -> claim. Pure PIL, no downloads.
Motion: Corporate archetype (steady, readable); each step fades in as a new
terminal line, progress bar advances, final frame holds with a checkmark.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 600
BG = (13, 17, 23)
HEADER = (22, 27, 34)
GREEN = (63, 185, 80)
BRIGHT = (230, 237, 243)
DIM = (139, 148, 158)
AMBER = (210, 153, 34)
CYAN = (88, 166, 255)
RED_DOT, YELLOW_DOT, GREEN_DOT = (255, 95, 86), (255, 189, 46), (39, 201, 63)

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_cmd = ImageFont.truetype(MONO_B, 17)
f_out = ImageFont.truetype(MONO, 16)
f_title = ImageFont.truetype(SANS_B, 15)
f_small = ImageFont.truetype(MONO, 13)

# (prompt line, output line, output colour)
STEPS = [
    ("$ open make.fun/r/b89716vt", "Signed up free as @syukuran", GREEN),
    ("$ node cli/makefun.mjs login", "Kit connected -- code approved", GREEN),
    ("$ curl -sSL make.fun/c/.../kit | tar xz", "Kit downloaded -- RULES.txt ready", GREEN),
    ("$ agent builds my-entry", "Entry built in-session, MIT license added", GREEN),
    ("$ makefun bundle --repo ../my-entry", "transcripts.tar.gz -- 3 sessions, redacted", GREEN),
    ("$ makefun check --kit . --repo ../my-entry", "All checks passed -- nothing rejected", GREEN),
    ("$ makefun submit --competition bring-the-humans-02", "Submitted -- commit 40-char SHA recorded", GREEN),
    ("$ makefun claim --claim <id> --us-person no", "USDC claimed to your Solana wallet", GREEN),
]

BAR_LABELS = ["signup", "kit", "build", "bundle", "check", "submit", "claim"]


def draw_frame(n_visible, cursor_on):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # window chrome
    d.rounded_rectangle([0, 0, W, 44], radius=10, fill=HEADER)
    d.rectangle([0, 30, W, 44], fill=HEADER)
    for i, c in enumerate((RED_DOT, YELLOW_DOT, GREEN_DOT)):
        d.ellipse([18 + i * 26, 14, 32 + i * 26, 28], fill=c)
    d.text((110, 13), "make.fun -- field manual walkthrough", font=f_title, fill=BRIGHT)
    y = 62
    for i in range(n_visible):
        cmd, out, col = STEPS[i]
        d.text((28, y), cmd, font=f_cmd, fill=CYAN)
        y += 28
        d.text((48, y), out, font=f_out, fill=col)
        y += 30
    if n_visible < len(STEPS):
        # typing cursor on next command (partial reveal for motion)
        nxt = STEPS[n_visible][0]
        shown = nxt[: max(2, int(len(nxt) * 0.55))]
        d.text((28, y), shown, font=f_cmd, fill=CYAN)
        if cursor_on:
            w = d.textlength(shown, font=f_cmd)
            d.rectangle([28 + w + 4, y + 2, 28 + w + 12, y + 22], fill=GREEN)
    else:
        d.text((28, y + 4), "Done. Your turn: make.fun/r/b89716vt",
               font=f_cmd, fill=AMBER)
    # progress bar (bottom)
    bx, by, bw, bh = 28, H - 52, W - 56, 12
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=6, fill=(33, 38, 45))
    frac = n_visible / len(STEPS)
    if frac > 0:
        d.rounded_rectangle([bx, by, bx + int(bw * frac), by + bh], radius=6, fill=GREEN)
    done = min(7, int(frac * 7 + 0.0001)) if frac < 1 else 7
    d.text((28, H - 30), "  ".join(
        (("[" + l + "]") if i <= done else l) for i, l in enumerate(BAR_LABELS)),
        font=f_small, fill=DIM)
    return img


frames, durations = [], []
for i in range(1, len(STEPS) + 1):
    frames.append(draw_frame(i, cursor_on=True))
    durations.append(650)
# final hold frame
frames.append(draw_frame(len(STEPS), cursor_on=False))
durations.append(1600)

frames[0].save(
    "demo.gif", save_all=True, append_images=frames[1:],
    duration=durations, loop=0, optimize=True,
)
print("frames:", len(frames), "durations:", durations)
