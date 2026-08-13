#!/usr/bin/env python3
"""Generate the animated SVG assets for the GitHub profile README."""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)

BG0, BG1, BG2 = "#070B16", "#0E1428", "#161E3A"
CYAN, VIOLET, EMERALD, AMBER = "#22D3EE", "#A78BFA", "#34D399", "#FBBF24"
TEXT, MUTED = "#E8EEF7", "#94A3B8"

SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','Cascadia Code','Fira Code',Menlo,Consolas,monospace"


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(body)
    print(f"wrote {path} ({len(body)} bytes)")


# --------------------------------------------------------------------------
# header.svg  -- name, title, typewriter tagline, live attention-map animation
# --------------------------------------------------------------------------
def header():
    W, H = 900, 270
    p = []
    a = p.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
      f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
      f'aria-label="Asik Ifthaker Hamim, Associate AI Engineer">')

    # ---- defs
    a("<defs>")
    a(f'<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0%" stop-color="{BG0}"/><stop offset="55%" stop-color="{BG1}"/>'
      f'<stop offset="100%" stop-color="{BG2}"/></linearGradient>')
    a(f'<linearGradient id="name" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0%" stop-color="#FFFFFF"/><stop offset="55%" stop-color="{CYAN}"/>'
      f'<stop offset="100%" stop-color="{VIOLET}"/></linearGradient>')
    a(f'<radialGradient id="halo" cx="50%" cy="50%" r="50%">'
      f'<stop offset="0%" stop-color="{VIOLET}" stop-opacity="0.40"/>'
      f'<stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>')
    a(f'<radialGradient id="halo2" cx="50%" cy="50%" r="50%">'
      f'<stop offset="0%" stop-color="{CYAN}" stop-opacity="0.32"/>'
      f'<stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>')
    a('<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">'
      '<feGaussianBlur stdDeviation="3.2" result="b"/>'
      '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a('<filter id="soft" x="-60%" y="-60%" width="220%" height="220%">'
      '<feGaussianBlur stdDeviation="1.6" result="b"/>'
      '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a(f'<clipPath id="panelclip"><rect x="0" y="0" width="{W}" height="{H}" rx="18"/></clipPath>')

    # typewriter clip rects, one per phrase
    phrases = [
        "building LLM agents that survive production",
        "LangGraph  .  RAG  .  evals  .  tool use",
        "python, prompts and a lot of measurement",
    ]
    CH = 8.42          # advance width of the mono face at 14px
    TX, TY = 62, 196   # baseline origin of the typed line
    for i, s in enumerate(phrases):
        a(f'<clipPath id="tc{i}"><rect id="tr{i}" x="{TX}" y="{TY-16}" width="0" height="24"/></clipPath>')
    a("</defs>")

    # ---- style
    a("<style>")
    a(f".n{{font-family:{SANS};}} .m{{font-family:{MONO};}}")
    a("@keyframes cell{0%,100%{opacity:.08}45%{opacity:1}}")
    a("@keyframes drift{0%{transform:translateY(0)}100%{transform:translateY(-16px)}}")
    a("@keyframes sweep{0%{opacity:0}12%{opacity:.55}60%{opacity:0}100%{opacity:0}}")
    a("@keyframes barp{0%,100%{transform:scaleY(.35)}50%{transform:scaleY(1)}}")
    a(".cell{animation:cell 3.4s ease-in-out infinite;}")
    a(".dot{animation:drift 4.2s ease-in-out infinite alternate;}")
    a(".bar{transform-box:fill-box;transform-origin:50% 100%;animation:barp 2.4s ease-in-out infinite;}")
    a("</style>")

    a('<g clip-path="url(#panelclip)">')
    a(f'<rect width="{W}" height="{H}" fill="url(#panel)"/>')
    a(f'<circle cx="770" cy="60" r="230" fill="url(#halo)"/>')
    a(f'<circle cx="120" cy="250" r="200" fill="url(#halo2)"/>')

    # faint grid
    for x in range(0, W, 30):
        a(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{CYAN}" stroke-opacity="0.045"/>')
    for y in range(0, H, 30):
        a(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{CYAN}" stroke-opacity="0.045"/>')

    # floating particles
    rnd = random.Random(7)
    for i in range(22):
        cx = rnd.uniform(20, W - 20)
        cy = rnd.uniform(20, H - 20)
        r = rnd.uniform(0.9, 2.2)
        col = rnd.choice([CYAN, VIOLET, EMERALD])
        d = rnd.uniform(3.2, 6.5)
        a(f'<circle class="dot" cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.1f}" fill="{col}" '
          f'opacity="{rnd.uniform(.25,.7):.2f}" style="animation-duration:{d:.1f}s;'
          f'animation-delay:-{rnd.uniform(0,4):.1f}s"/>')

    # ---- attention map, 9x9, diagonal wave
    GX, GY, CS, GAP = 660, 52, 15, 4
    N = 9
    a(f'<g>')
    for r in range(N):
        for c in range(N):
            x = GX + c * (CS + GAP)
            y = GY + r * (CS + GAP)
            # value falls off from the diagonal, like a causal attention band
            band = math.exp(-((r - c) ** 2) / 7.0)
            col = CYAN if band > 0.55 else (VIOLET if band > 0.18 else EMERALD)
            base = 0.16 + 0.84 * band
            delay = (r + c) * 0.085
            a(f'<rect class="cell" x="{x}" y="{y}" width="{CS}" height="{CS}" rx="3.5" '
              f'fill="{col}" style="animation-delay:-{delay:.2f}s;opacity:{base:.2f}"/>')
    a("</g>")
    # scan line over the map
    grid_w = N * (CS + GAP) - GAP
    a(f'<rect x="{GX}" y="{GY}" width="{grid_w}" height="3" fill="{TEXT}" opacity="0" '
      f'filter="url(#soft)">'
      f'<animate attributeName="y" values="{GY};{GY+grid_w-3};{GY}" dur="6s" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="0;.65;0;0" keyTimes="0;.25;.5;1" dur="6s" '
      f'repeatCount="indefinite"/></rect>')
    a(f'<text class="m" x="{GX}" y="{GY + grid_w + 20}" font-size="10.5" fill="{MUTED}" '
      f'letter-spacing="2.4">ATTENTION</text>')

    # equaliser bars, left of the map, like live token throughput
    for i in range(5):
        bx = 600 + i * 11
        a(f'<rect class="bar" x="{bx}" y="{GY+60}" width="5" height="{grid_w-60}" rx="2.5" '
          f'fill="{VIOLET}" opacity="0.5" style="animation-delay:-{i*0.31:.2f}s"/>')

    # ---- text block
    a(f'<text class="n" x="60" y="104" font-size="42" font-weight="700" fill="url(#name)" '
      f'filter="url(#glow)">Asik Ifthaker Hamim</text>')

    a(f'<rect x="60" y="124" width="34" height="2.5" rx="1.25" fill="{CYAN}">'
      f'<animate attributeName="width" values="34;220;34" dur="5s" repeatCount="indefinite" '
      f'calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" keyTimes="0;0.5;1"/></rect>')

    a(f'<text class="n" x="60" y="154" font-size="16.5" font-weight="600" fill="{TEXT}" '
      f'letter-spacing="4.2">ASSOCIATE AI ENGINEER</text>')
    a(f'<text class="n" x="384" y="154" font-size="16.5" fill="{MUTED}" letter-spacing="1">'
      f'@ Liberate Labs</text>')

    # typed line
    a(f'<text class="m" x="{TX-22}" y="{TY}" font-size="14" fill="{EMERALD}">&gt;</text>')
    cycle = 13.5
    slot = cycle / len(phrases)
    for i, s in enumerate(phrases):
        w = len(s) * CH
        start = i * slot
        k = lambda t: round(t / cycle, 4)
        # 0 -> full over 1.5s, hold 2.4s, back to 0
        kt = [0, k(start), k(start + 1.5), k(start + 3.9), k(start + 4.05), 1]
        vals = [0, 0, w, w, 0, 0]
        if i == 0:  # first phrase starts at t=0, no leading hold
            kt = [0, k(1.5), k(3.9), k(4.05), 1]
            vals = [0, w, w, 0, 0]
        a(f'<g clip-path="url(#tc{i})"><text class="m" x="{TX}" y="{TY}" font-size="14" '
          f'fill="{TEXT}" xml:space="preserve">{s}</text></g>')
        a(f'<animate xlink:href="#tr{i}" attributeName="width" dur="{cycle}s" '
          f'repeatCount="indefinite" calcMode="linear" '
          f'keyTimes="{";".join(str(x) for x in kt)}" values="{";".join(str(v) for v in vals)}"/>')

    # blinking caret that rides the reveal edge
    a(f'<rect id="caret" x="{TX}" y="{TY-12}" width="8.4" height="16" fill="{CYAN}" opacity="0.9">')
    ckt, cvals = [0.0], [TX]
    for i, s in enumerate(phrases):
        w = len(s) * CH
        start = i * slot
        k = lambda t: round(t / cycle, 4)
        ckt += [k(start + 1.5), k(start + 3.9), k(start + 4.02)]
        cvals += [TX + w, TX + w, TX]
    ckt.append(1.0)
    cvals.append(TX)
    a(f'<animate attributeName="x" dur="{cycle}s" repeatCount="indefinite" calcMode="linear" '
      f'keyTimes="{";".join(str(round(x,4)) for x in ckt)}" '
      f'values="{";".join(str(round(v,1)) for v in cvals)}"/>')
    a('<animate attributeName="opacity" values="0.95;0.95;0;0" keyTimes="0;0.5;0.51;1" '
      'dur="1.05s" repeatCount="indefinite"/>')
    a("</rect>")

    # bottom accent rail
    a(f'<rect x="0" y="{H-4}" width="{W}" height="4" fill="{BG0}"/>')
    a(f'<rect x="0" y="{H-4}" width="240" height="4" fill="{CYAN}" opacity="0.9">'
      f'<animate attributeName="x" values="-240;{W};-240" dur="7s" repeatCount="indefinite"/></rect>')
    a(f'<rect x="0" y="{H-4}" width="140" height="4" fill="{VIOLET}" opacity="0.85">'
      f'<animate attributeName="x" values="{W};-140;{W}" dur="9s" repeatCount="indefinite"/></rect>')

    a("</g>")
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" '
      f'stroke="{CYAN}" stroke-opacity="0.22"/>')
    a("</svg>")
    write("header.svg", "".join(p))


# --------------------------------------------------------------------------
# loop.svg -- the agent loop, with a signal travelling the circuit
# --------------------------------------------------------------------------
def loop():
    W, H = 900, 210
    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="img" aria-label="The agent loop: prompt, reason, tool call, observe">')

    a("<defs>")
    a(f'<linearGradient id="lp" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0%" stop-color="{BG0}"/><stop offset="100%" stop-color="{BG2}"/></linearGradient>')
    a('<filter id="g2" x="-70%" y="-70%" width="240%" height="240%">'
      '<feGaussianBlur stdDeviation="4" result="b"/>'
      '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a(f'<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
      f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{CYAN}" opacity="0.75"/></marker>')
    a(f'<clipPath id="lc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    a("</defs>")

    a("<style>")
    a(f".n{{font-family:{SANS};}} .m{{font-family:{MONO};}}")
    a("@keyframes lit{0%,100%{opacity:.30}8%{opacity:1}26%{opacity:.30}}")
    a(".stage{animation:lit 6s linear infinite;}")
    a("</style>")

    a('<g clip-path="url(#lc)">')
    a(f'<rect width="{W}" height="{H}" fill="url(#lp)"/>')
    for x in range(0, W, 30):
        a(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{CYAN}" stroke-opacity="0.04"/>')
    for y in range(0, H, 30):
        a(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{CYAN}" stroke-opacity="0.04"/>')

    BW, BH, BY = 186, 66, 34
    xs = [38, 262, 486, 710]
    labels = [
        ("PROMPT", "what you actually asked", CYAN),
        ("REASON", "plan the next step", VIOLET),
        ("TOOL CALL", "search, run, fetch", EMERALD),
        ("OBSERVE", "did it work, or retry", AMBER),
    ]
    cy = BY + BH / 2

    # circuit path: left to right, then loop back under to REASON
    path_d = (f"M {xs[0]+8} {cy} H 838 Q 862 {cy} 862 {cy+26} V 150 Q 862 172 838 172 "
              f"H {xs[1]+BW/2+22} Q {xs[1]+BW/2} 172 {xs[1]+BW/2} 150 V {BY+BH+4}")
    a(f'<path id="circuit" d="{path_d}" fill="none" stroke="{CYAN}" stroke-opacity="0.30" '
      f'stroke-width="1.6" marker-end="url(#ah)"/>')
    a(f'<path d="{path_d}" fill="none" stroke="{CYAN}" stroke-opacity="0.85" stroke-width="1.6" '
      f'stroke-dasharray="10 14"><animate attributeName="stroke-dashoffset" values="0;-480" '
      f'dur="6s" repeatCount="indefinite"/></path>')

    # stage boxes
    for i, (x, (title, sub, col)) in enumerate(zip(xs, labels)):
        delay = -6 + i * 1.42
        a(f'<g class="stage" style="animation-delay:{delay:.2f}s">'
          f'<rect x="{x}" y="{BY}" width="{BW}" height="{BH}" rx="12" fill="{col}" opacity="0.10"/>'
          f'<rect x="{x}" y="{BY}" width="{BW}" height="{BH}" rx="12" fill="none" stroke="{col}" '
          f'stroke-width="1.6" filter="url(#g2)"/></g>')
        a(f'<rect x="{x}" y="{BY}" width="{BW}" height="{BH}" rx="12" fill="{BG0}" opacity="0.86"/>')
        a(f'<rect x="{x}" y="{BY}" width="{BW}" height="{BH}" rx="12" fill="none" stroke="{col}" '
          f'stroke-opacity="0.45" stroke-width="1.2"/>')
        a(f'<circle cx="{x+18}" cy="{BY+24}" r="4" fill="{col}"/>')
        a(f'<text class="n" x="{x+32}" y="{BY+28}" font-size="14.5" font-weight="700" '
          f'fill="{TEXT}" letter-spacing="1.6">{title}</text>')
        a(f'<text class="m" x="{x+18}" y="{BY+50}" font-size="10.5" fill="{MUTED}">{sub}</text>')

    # travelling signal
    a(f'<circle r="6" fill="{TEXT}" filter="url(#g2)">'
      f'<animateMotion dur="6s" repeatCount="indefinite" rotate="auto">'
      f'<mpath href="#circuit"/></animateMotion></circle>')
    a(f'<circle r="12" fill="{CYAN}" opacity="0.35" filter="url(#g2)">'
      f'<animateMotion dur="6s" repeatCount="indefinite" begin="-0.08s">'
      f'<mpath href="#circuit"/></animateMotion></circle>')

    a(f'<text class="m" x="38" y="{H-16}" font-size="11" fill="{MUTED}" letter-spacing="1.6">'
      f'the loop I spend my days making faster, cheaper and harder to break</text>')

    a("</g>")
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{CYAN}" '
      f'stroke-opacity="0.20"/>')
    a("</svg>")
    write("loop.svg", "".join(p))


# --------------------------------------------------------------------------
# divider.svg -- slim animated rule
# --------------------------------------------------------------------------
def divider():
    W, H = 900, 8
    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="presentation">')
    a("<defs>")
    a(f'<linearGradient id="dv" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0%" stop-color="{CYAN}" stop-opacity="0"/>'
      f'<stop offset="50%" stop-color="{VIOLET}" stop-opacity="0.85"/>'
      f'<stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>')
    a("</defs>")
    a(f'<rect x="0" y="3" width="{W}" height="2" rx="1" fill="url(#dv)"/>')
    a(f'<circle cy="4" r="3" fill="{CYAN}"><animate attributeName="cx" values="0;{W};0" '
      f'dur="8s" repeatCount="indefinite"/><animate attributeName="opacity" '
      f'values="0;1;1;0" keyTimes="0;.1;.9;1" dur="8s" repeatCount="indefinite"/></circle>')
    a("</svg>")
    write("divider.svg", "".join(p))


if __name__ == "__main__":
    header()
    loop()
    divider()


# --------------------------------------------------------------------------
# stack.svg -- the toolkit, as animated chips (no third-party badge service)
# --------------------------------------------------------------------------
def stack():
    ROWS = [
        ("CORE", CYAN, ["Python", "Jupyter", "pandas", "NumPy", "Bash"]),
        ("AGENTS", VIOLET, ["LangGraph", "LangChain", "LangSmith", "Claude", "OpenAI",
                            "Groq", "MCP", "RAG"]),
        ("SPEECH", EMERALD, ["AssemblyAI", "Deepgram", "Whisper", "WER / CER evals"]),
        ("TOOLING", AMBER, ["Playwright", "Pydantic", "pytest", "uv", "Git", "GitHub Actions"]),
    ]
    LBL_X, CHIP_X = 34, 152
    CH, ROW_H, PAD, GAP = 6.75, 40, 15, 9
    CHIP_H = 27
    W = 900
    top = 26
    H = top + len(ROWS) * ROW_H + 14

    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}" role="img" aria-label="Toolkit">')
    a("<defs>")
    a(f'<linearGradient id="sp" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0%" stop-color="{BG0}"/><stop offset="100%" stop-color="{BG2}"/></linearGradient>')
    a(f'<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>'
      f'<stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.13"/>'
      f'<stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')
    a(f'<clipPath id="sc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    a("</defs>")
    a("<style>")
    a(f".n{{font-family:{SANS};}} .m{{font-family:{MONO};}}")
    # no entrance animation: the resting state must be the visible one, so that any
    # renderer that only paints the first frame still shows a full panel
    a("@keyframes breathe{0%,100%{opacity:.34}50%{opacity:.85}}")
    a(".ring{animation:breathe 4.2s ease-in-out infinite;}")
    a("</style>")

    a('<g clip-path="url(#sc)">')
    a(f'<rect width="{W}" height="{H}" fill="url(#sp)"/>')
    for x in range(0, W, 30):
        a(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{CYAN}" stroke-opacity="0.04"/>')
    for y in range(0, H, 30):
        a(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{CYAN}" stroke-opacity="0.04"/>')

    idx = 0
    for r, (label, col, items) in enumerate(ROWS):
        cy = top + r * ROW_H + CHIP_H / 2
        a(f'<text class="m" x="{LBL_X}" y="{cy+4}" font-size="10.5" fill="{col}" '
          f'letter-spacing="2.6" opacity="0.95">{label}</text>')
        a(f'<line x1="{LBL_X}" y1="{cy+12}" x2="{CHIP_X-22}" y2="{cy+12}" stroke="{col}" '
          f'stroke-opacity="0.28"/>')
        x = CHIP_X
        for item in items:
            w = round(len(item) * CH + PAD * 2 + 12)
            a(f'<g>')
            a(f'<rect x="{x}" y="{cy-CHIP_H/2}" width="{w}" height="{CHIP_H}" rx="{CHIP_H/2}" '
              f'fill="{col}" fill-opacity="0.10"/>')
            a(f'<rect class="ring" x="{x}" y="{cy-CHIP_H/2}" width="{w}" height="{CHIP_H}" '
              f'rx="{CHIP_H/2}" fill="none" stroke="{col}" stroke-opacity="0.42" '
              f'style="animation-delay:-{idx*0.21:.2f}s"/>')
            a(f'<circle cx="{x+PAD}" cy="{cy}" r="3" fill="{col}">'
              f'<animate attributeName="opacity" values="1;0.35;1" dur="2.6s" '
              f'begin="-{idx*0.17:.2f}s" repeatCount="indefinite"/></circle>')
            a(f'<text class="m" x="{x+PAD+11}" y="{cy+4}" font-size="11.5" fill="{TEXT}" '
              f'xml:space="preserve">{item.replace("&", "&amp;")}</text>')
            a("</g>")
            x += w + GAP
            idx += 1

    a(f'<rect x="0" y="0" width="200" height="{H}" fill="url(#shine)" transform="skewX(-18)">'
      f'<animate attributeName="x" values="-260;{W+120};-260" dur="9s" repeatCount="indefinite"/>'
      f'</rect>')
    a("</g>")
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{CYAN}" '
      f'stroke-opacity="0.20"/>')
    a("</svg>")
    write("stack.svg", "".join(p))


stack()
