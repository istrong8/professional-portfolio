// Builds NSEN6684_Beyond_Six_Factor.pptx -- dark, modern 16:9 deck with
//   * speaker notes from ../narration/NSEN6684_Narration_Script.md
//   * clickable section navigation on every slide + clickable roadmap on the title slide
//   * fade transitions between slides
// Run from the repository root:   node presentation/build_deck.js
// Requires: npm install pptxgenjs jszip ; dark figures from
//   python code/run_analysis.py && python code/make_figures.py --dark && python code/make_diagrams.py --dark
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
let JSZip;
try { JSZip = require("jszip"); }
catch (e) { JSZip = require(require.resolve("jszip", { paths: [path.dirname(require.resolve("pptxgenjs"))] })); }

const ROOT = path.resolve(__dirname, "..");
const FIG = (n) => path.join(ROOT, "figures", "dark", n + ".png");
const OUT = path.join(__dirname, "NSEN6684_Beyond_Six_Factor.pptx");
const RES = JSON.parse(fs.readFileSync(path.join(ROOT, "results", "analysis_results.json"), "utf8"));
const AR = (n) => { const b = fs.readFileSync(FIG(n)); return b.readUInt32BE(16) / b.readUInt32BE(20); };

// ---------- narration -> notes ----------
const script = fs.readFileSync(path.join(ROOT, "narration", "NSEN6684_Narration_Script.md"), "utf8");
const notes = {};
script.split(/^## /m).slice(1).forEach((block) => {
  const [head, ...rest] = block.split("\n");
  const m = head.match(/^Slide (\d+) — (.*) \((\d+:\d+)\)/);
  if (m) notes[+m[1]] = `Slide ${m[1]} — ${m[2]}  [target ${m[3]}]\n\n` + rest.join("\n").trim();
});

// ---------- theme (dark) ----------
const THEME = {
  name: "Lunar Night",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "0B1220", lt1: "F4F6FA", dk2: "141D2E", lt2: "A9B4C6",
    accent1: "F28C38", accent2: "2EC4B6", accent3: "8FB3E0", accent4: "E06C55",
    accent5: "6B7891", accent6: "26324A", hlink: "2EC4B6", folHlink: "8FB3E0",
  },
};
const HEX = THEME.colors;
const CARD = HEX.dk2, LINE = HEX.accent6, BG = HEX.dk1;
const WARM = "2A1E16", COOL = "10292B";      // tinted cards

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "Irais Strong";
pres.company = "Idaho State University";
pres.title = "Beyond the Six-Factor Formula: Neutron Leakage, Spectral Effects, and Reactivity Feedback in Compact Space Fission Reactors";
pres.subject = "NSEN 6684";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const TXT = C.background1, MUTED = C.background2;
const SW = 13.333;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: BG },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.65, y: 1.1, w: 7.6, h: 0.8,
        fontSize: 38, bold: true, color: TXT, valign: "top", align: "left", fontFace: THEME.headFontFace, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.65, y: 3.2, w: 7.3, h: 1.35,
        fontSize: 15, color: MUTED, valign: "top", align: "left", italic: true, margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT_DARK",
  background: { color: BG },
  margin: [0.5, 0.5, 0.6, 0.5],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.62, w: 12.15, h: 0.75,
        fontSize: 30, bold: true, color: TXT, valign: "middle", align: "left", fontFace: THEME.headFontFace, margin: 0 }, text: "" } },
    { text: { text: "NSEN 6684  ·  Irais Strong  ·  Idaho State University",
        options: { x: 0.6, y: 7.12, w: 5, h: 0.26, fontSize: 9, color: C.accent5, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.12, w: 0.45, h: 0.26, fontSize: 9, color: C.accent5, align: "right" },
});

// ---------- navigation ----------
const SECTIONS = [
  ["Classical", 3], ["Eigenvalue", 4], ["Diffusion", 5], ["Leakage", 6],
  ["Transport", 8], ["Spectrum", 9], ["KRUSTY", 10], ["Findings", 12],
];
const sectionOf = (num) => { let cur = null; SECTIONS.forEach(([name, s]) => { if (num >= s) cur = name; }); return cur; };
function nav(slide, num) {
  const w = 0.95, gap = 0.05, x0 = SW - 0.58 - SECTIONS.length * w - (SECTIONS.length - 1) * gap;
  const here = sectionOf(num);
  SECTIONS.forEach(([name, target], i) => {
    const x = x0 + i * (w + gap), on = name === here;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 0.2, w, h: 0.3, rectRadius: 0.15,
      fill: { color: on ? "3A2614" : CARD }, line: { color: on ? HEX.accent1 : LINE, width: 0.75 }, objectName: "nav pill " + name });
    slide.addText(name, { x, y: 0.2, w, h: 0.3, fontSize: 9.5, bold: on, color: on ? C.accent1 : MUTED, align: "center", valign: "middle",
        margin: 0, isTextBox: true, objectName: "nav label " + name });
    linkOverlay(slide, x, 0.2, w, 0.3, target, "Go to " + name);
  });
}
function linkOverlay(slide, x, y, w, h, target, tip) {   // whole-pill click target, no underlined text
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: h / 2, fill: { color: BG, transparency: 100 },
    line: { color: BG, transparency: 100 }, hyperlink: { slide: target, tooltip: tip }, objectName: "link: " + tip });
}
function kicker(slide, num, label) {
  slide.addText(`${String(num).padStart(2, "0")}  ·  ${label.toUpperCase()}`, { x: 0.6, y: 0.22, w: 4.2, h: 0.28,
    fontSize: 10.5, bold: true, color: C.accent1, charSpacing: 2, margin: 0, isTextBox: true, objectName: "kicker" });
}
function contentSlide(num, label, title) {
  const s = pres.addSlide({ masterName: "CONTENT_DARK", sectionTitle: sectionOf(num) || "Introduction" });
  s.addText(title, { placeholder: "title" });
  kicker(s, num, label);
  nav(s, num);
  return s;
}

// ---------- helpers ----------
function source(slide, text) {
  slide.addText("Sources: " + text, { x: 0.6, y: 6.74, w: 12.15, h: 0.34, fontSize: 9.5, color: C.accent5,
    italic: true, margin: 0, valign: "bottom", isTextBox: true, objectName: "Source citation" });
}
function card(slide, x, y, w, h, fill, line, name) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1,
    fill: { color: fill || CARD }, line: { color: line || LINE, width: 0.75 }, objectName: name || "card" });
}
function figure(slide, name, x, y, w, alt) {        // figure on a matching card
  const h = w / AR(name), p = 0.1;
  card(slide, x - p, y - p, w + 2 * p, h + 2 * p, CARD, LINE, "figure card");
  slide.addImage({ path: FIG(name), x, y, w, h, altText: alt, objectName: name });
  return h;
}
function figureH(slide, name, x, y, h, alt) {
  const w = h * AR(name), p = 0.1;
  card(slide, x - p, y - p, w + 2 * p, h + 2 * p, CARD, LINE, "figure card");
  slide.addImage({ path: FIG(name), x, y, w, h, altText: alt, objectName: name });
  return w;
}
function stat(slide, x, y, w, big, small, color, size) {
  slide.addText(big, { x, y, w, h: 0.72, fontSize: size || 36, bold: true, color, margin: 0, isTextBox: true, objectName: "stat value" });
  slide.addText(small, { x, y: y + 0.74, w, h: 0.62, fontSize: 13.5, color: MUTED, margin: 0, valign: "top", isTextBox: true, objectName: "stat label" });
}
function glowRings(slide, cx, cy, r) {
  [[1.45, 94], [1.25, 90], [1.0, 80]].forEach(([k, t]) => {
    slide.addShape(pres.shapes.OVAL, { x: cx - r * k, y: cy - r * k, w: 2 * r * k, h: 2 * r * k,
      fill: { color: HEX.accent2, transparency: t }, line: { color: HEX.accent2, width: k === 1.0 ? 1.5 : 0, transparency: k === 1.0 ? 0 : 100 }, objectName: "reflector glow" });
  });
  const rc = r * 0.48;
  [[1.35, 85], [1.15, 70]].forEach(([k, t]) => {
    slide.addShape(pres.shapes.OVAL, { x: cx - rc * k, y: cy - rc * k, w: 2 * rc * k, h: 2 * rc * k,
      fill: { color: HEX.accent1, transparency: t }, line: { color: HEX.accent1, transparency: 100 }, objectName: "core glow" });
  });
  slide.addShape(pres.shapes.OVAL, { x: cx - rc, y: cy - rc, w: 2 * rc, h: 2 * rc, fill: { color: HEX.accent1 }, line: { color: "FFB36B", width: 1 }, objectName: "core" });
  slide.addShape(pres.shapes.OVAL, { x: cx - r * 1.75, y: cy - r * 1.75, w: 3.5 * r, h: 3.5 * r, fill: { color: BG, transparency: 100 },
    line: { color: HEX.accent5, width: 0.75, dashType: "dash" }, objectName: "leakage boundary" });
}
const th = { bold: true, color: "F4F6FA", fill: { color: "1F2B42" }, fontSize: 14.5 };
function darkTable(slide, rows, opts) {
  const body = rows.map((r, i) => i === 0 ? r : r.map((c) => (typeof c === "string" ? { text: c, options: { fill: { color: i % 2 ? CARD : "172235" } } } : c)));
  slide.addTable(body, Object.assign({ color: "E8ECF2", border: { type: "solid", pt: 0.75, color: LINE }, valign: "middle", fontFace: "Calibri" }, opts));
}
const sub = (t, o) => ({ text: t, options: Object.assign({ subscript: true }, o || {}) });
const sup = (t, o) => ({ text: t, options: Object.assign({ superscript: true }, o || {}) });
const n = (t, o) => ({ text: t, options: o || {} });
const f3 = (x) => x.toFixed(3);
const VER = RES.verification, SENS = RES.sensitivity, REFL = RES.reflector, SPEC = RES.spectral, FB = RES.feedback, CL = RES.classical;

// =============== 1 — Title
pres.addSection({ title: "Introduction" });
let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Introduction" });
s.addText("NSEN 6684  ·  REACTOR PHYSICS  ·  IDAHO STATE UNIVERSITY", { x: 0.65, y: 0.6, w: 7.5, h: 0.3, fontSize: 11, bold: true,
  color: C.accent1, charSpacing: 2, margin: 0, isTextBox: true, objectName: "kicker" });
s.addText("Beyond the Six-Factor Formula", { placeholder: "title" });
s.addText("Neutron Leakage, Spectral Effects, and Reactivity Feedback in Compact Space Fission Reactors",
  { x: 0.65, y: 1.95, w: 7.4, h: 1.0, fontSize: 21, color: C.accent3, margin: 0, valign: "top", isTextBox: true, objectName: "subtitle" });
s.addText("Thesis: classical life-cycle theory is the foundation for criticality, but compact fast-spectrum space reactors require transport, leakage, reflector and temperature-dependent reactivity analysis.", { placeholder: "body" });
s.addText([n("Irais Strong", { bold: true, fontSize: 18, color: TXT, breakLine: true }),
  n("Ph.D. in Nuclear Engineering  ·  Idaho State University", { fontSize: 13, color: MUTED })],
  { x: 0.65, y: 4.75, w: 7.2, h: 0.75, margin: 0, valign: "top", isTextBox: true, objectName: "author block" });
s.addText("ROADMAP  —  click to jump", { x: 0.65, y: 5.75, w: 4, h: 0.25, fontSize: 9.5, bold: true, color: C.accent5, charSpacing: 1.5, margin: 0, isTextBox: true });
const road = [["Eigenvalue", 4, HEX.accent3], ["Diffusion", 5, HEX.accent3], ["Leakage", 6, HEX.accent2], ["Reflectors", 7, HEX.accent2],
              ["Spectrum", 9, HEX.accent1], ["KRUSTY", 10, HEX.accent1], ["Findings", 12, HEX.accent4]];
road.forEach(([name, target, col], i) => {
  const x = 0.65 + i * 1.07;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 6.05, w: 1.0, h: 0.42, rectRadius: 0.21, fill: { color: CARD }, line: { color: col, width: 1 }, objectName: "roadmap chip" });
  s.addText(name, { x, y: 6.05, w: 1.0, h: 0.42, fontSize: 10.5, bold: true, color: TXT, align: "center", valign: "middle", margin: 0, isTextBox: true });
  linkOverlay(s, x, 6.05, 1.0, 0.42, target, "Jump to " + name);
});
s.addText("Academic coursework · public sources only · calculations use idealized benchmark constants", { x: 0.65, y: 6.9, w: 8, h: 0.26,
  fontSize: 9.5, italic: true, color: C.accent5, margin: 0, isTextBox: true });
glowRings(s, 10.85, 3.55, 1.5);
s.addText("core", { x: 10.35, y: 3.35, w: 1.0, h: 0.4, fontSize: 14, bold: true, color: "1B2430", align: "center", margin: 0, isTextBox: true });
s.addText("reflector", { x: 10.05, y: 2.3, w: 1.6, h: 0.32, fontSize: 12, color: TXT, align: "center", margin: 0, isTextBox: true });
s.addText("leakage", { x: 10.05, y: 5.95, w: 1.6, h: 0.32, fontSize: 12, color: MUTED, align: "center", margin: 0, isTextBox: true });
s.addNotes(notes[1]);

// =============== 2 — Why compact fast reactors are different
pres.addSection({ title: "Motivation" });
s = contentSlide(2, "Motivation", "Why Compact Fast Reactors Are Different");
[["~14 days", "lunar night at low latitude", C.accent3], ["≥ 354 h", "darkness Lunar Reactor-1 must ride through (draft, as reported)", C.accent2],
 ["11 × 25 cm", "KRUSTY HEU core: diameter × height", C.accent1]].forEach(([b, t, col], i) => {
  const x = 0.6 + i * 4.1; card(s, x, 1.6, 3.9, 1.5); stat(s, x + 0.25, 1.7, 3.45, b, t, col, 34);
});
darkTable(s, [
  [{ text: "", options: th }, { text: "Large thermal reactor", options: th }, { text: "Compact fast core", options: th }],
  [{ text: "Biggest neutron loss", options: { bold: true } }, "absorption outside fuel", "leakage (45–75 % in this study)"],
  [{ text: "Reactivity control", options: { bold: true } }, "absorber rods, soluble boron", "reflector position"],
  [{ text: "Main prompt feedback", options: { bold: true } }, "Doppler, moderator density", "fuel thermal expansion"],
], { x: 0.6, y: 3.4, w: 12.15, colW: [3.15, 4.5, 4.5], fontSize: 16, rowH: 0.62, objectName: "comparison table" });
s.addText("Leakage is not a correction factor here. It is the physics.", { x: 0.6, y: 6.05, w: 12.15, h: 0.45, fontSize: 18, bold: true, color: C.accent1, margin: 0, isTextBox: true });
source(s, "NASA & DOE (Jan. 2026); New Space Economy (Sep. 2026), reporting NASA draft LR-1 requirements; Sanchez et al., Nucl. Technol. 206 (2020) S56; this work (study 2).");
s.addNotes(notes[2]);

// =============== 3 — Classical life cycle in two minutes
pres.addSection({ title: "Classical" });
s = contentSlide(3, "Review", "The Classical Life Cycle in Two Minutes");
s.addText([n("k"), sub("eff"), n(" = η · ε · p · f · P"), sub("FNL"), n(" · P"), sub("TNL")], { x: 0.6, y: 1.55, w: 12.15, h: 0.6, fontSize: 26, bold: true, color: TXT, fontFace: "Cambria Math", margin: 0, isTextBox: true });
const chain = [["1000", "absorbed\nin fuel", HEX.accent3], ["× 1.84", "η", HEX.accent1], ["× 1.03", "ε", HEX.accent1], ["× 0.80", "P_FNL", HEX.accent4],
               ["× 0.78", "p", HEX.accent2], ["× 0.95", "P_TNL", HEX.accent4], ["× 0.90", "f", HEX.accent2], [`${CL.ledger[6].toFixed(0)}`, "next\ngeneration", HEX.accent3]];
chain.forEach(([v, l, col], i) => {
  const x = 0.6 + i * 1.53;
  card(s, x, 2.35, 1.4, 1.25, CARD, col, "chain " + l);
  s.addText([n(v, { bold: true, fontSize: 20, color: TXT, breakLine: true }), n(l, { fontSize: 13, color: MUTED })], { x, y: 2.35, w: 1.4, h: 1.25, align: "center", valign: "middle", margin: 0, isTextBox: true });
});
s.addText(`Assumed LWR-like factors → k_eff = ${CL.k_eff.toFixed(3)}`, { x: 0.6, y: 3.7, w: 8, h: 0.35, fontSize: 14, italic: true, color: MUTED, margin: 0, isTextBox: true });
s.addText("Where it breaks in a fast core", { x: 0.6, y: 4.2, w: 8, h: 0.4, fontSize: 18, bold: true, color: C.accent1, margin: 0, isTextBox: true });
[["No moderator", "p and f lose their meaning"], ["One overlapping spectrum", "no separate fast and thermal groups"], ["Leakage dominates", "not a correction factor"]].forEach(([h, t], i) => {
  const x = 0.6 + i * 4.1; card(s, x, 4.7, 3.9, 1.1, WARM, HEX.accent1);
  s.addText([n(h, { bold: true, fontSize: 17, color: TXT, breakLine: true }), n(t, { fontSize: 15, color: MUTED })], { x: x + 0.2, y: 4.7, w: 3.5, h: 1.1, valign: "middle", margin: 0, isTextBox: true });
});
s.addText([n("Use instead:  ", { color: MUTED }), n("k = production / (absorption + leakage)", { bold: true, color: TXT })], { x: 0.6, y: 6.0, w: 12.15, h: 0.45, fontSize: 18, margin: 0, isTextBox: true });
source(s, "Lamarsh & Baratta (2001) ch. 6; Duderstadt & Hamilton (1976). Factor values assumed for review.");
s.addNotes(notes[3]);

// =============== 4 — Eigenvalue problem
pres.addSection({ title: "Eigenvalue" });
s = contentSlide(4, "Theory", "Generalized Neutron Balance: the k-Eigenvalue Problem");
card(s, 0.6, 1.6, 5.75, 4.95, CARD, HEX.accent3, "equations");
s.addText([
  n("Transport equation", { bold: true, color: C.accent3, fontSize: 15, breakLine: true }),
  n("Ω·∇ψ + Σ", { fontSize: 19 }), sub("t", { fontSize: 19 }), n("ψ = scattering in + (1/k)·fission", { fontSize: 19, breakLine: true }),
  n(" ", { fontSize: 8, breakLine: true }),
  n("Operator form", { bold: true, color: C.accent3, fontSize: 15, breakLine: true }),
  n("L ψ = (1/k) F ψ", { fontSize: 30, bold: true, breakLine: true }),
  n("k_eff = dominant eigenvalue", { fontSize: 18, color: MUTED, breakLine: true }),
  n(" ", { fontSize: 8, breakLine: true }),
  n("Power iteration", { bold: true, color: C.accent3, fontSize: 15, breakLine: true }),
  n("source → transport one generation →", { fontSize: 18, breakLine: true }),
  n("new source;  k = new / old", { fontSize: 18, breakLine: true }),
  n(" ", { fontSize: 8, breakLine: true }),
  n("Six-factor = two-group, separable special case", { fontSize: 17, italic: true, color: C.accent1 }),
], { x: 0.85, y: 1.7, w: 5.3, h: 4.75, color: TXT, valign: "top", margin: 0, isTextBox: true, fontFace: "Calibri" });
figure(s, "fig_power_iteration", 6.75, 1.75, 5.9, "Monte Carlo power iteration converging to the exact eigenvalue k = 1 for the LA-13511 bare sphere");
s.addText(`My Monte Carlo code: k = ${VER["Ua-1-0-SP"].k_mc.toFixed(4)} ± ${VER["Ua-1-0-SP"].k_std.toFixed(4)} vs exact 1`, { x: 6.65, y: 5.55, w: 6.1, h: 0.4, fontSize: 15, bold: true, color: C.accent1, margin: 0, isTextBox: true });
source(s, "Bell & Glasstone (1970); Duderstadt & Hamilton (1976) ch. 4; benchmark: Sood, Forster & Parsons, LA-13511 (1999), problem Ua-1-0-SP.");
s.addNotes(notes[4]);

// =============== 5 — Diffusion derivation
pres.addSection({ title: "Diffusion" });
s = contentSlide(5, "Theory", "From Transport to One-Group Diffusion");
const steps = [
  ["1  Balance", "∇·J + Σ_a φ = (1/k) νΣ_f φ", "integrate over angle and energy"],
  ["2  Fick's law (P₁)", "J = −D ∇φ,   D = 1 / 3Σ_tr", "assume linearly anisotropic flux"],
  ["3  Helmholtz", "∇²φ + B²φ = 0", "B_g² = (π / R_e)²,  R_e = R + 0.71 λ_tr"],
  ["4  Criticality", "k = k∞ / (1 + L²B²)", "P_NL = 1 / (1 + L²B²),  L² = D / Σ_a"],
];
steps.forEach(([h, eq, t], i) => {
  const x = 0.6 + i * 3.08;
  card(s, x, 1.65, 2.9, 2.35, CARD, i === 3 ? HEX.accent1 : HEX.accent3, "step " + h);
  s.addText([n(h, { bold: true, fontSize: 16, color: C.accent3, breakLine: true }), n(" ", { fontSize: 6, breakLine: true }),
    n(eq, { bold: true, fontSize: 18, color: TXT, breakLine: true }), n(" ", { fontSize: 6, breakLine: true }), n(t, { fontSize: 15, color: MUTED })],
    { x: x + 0.18, y: 1.75, w: 2.55, h: 2.15, valign: "top", margin: 0, isTextBox: true });
  if (i < 3) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 2.92, y: 2.65, w: 0.15, h: 0.3, fill: { color: HEX.accent5 }, line: { color: HEX.accent5 } });
});
card(s, 0.6, 4.35, 12.15, 1.9, WARM, HEX.accent1, "validity");
s.addText([n("Diffusion is valid when  ", { bold: true, color: C.accent1 }), n("the flux varies slowly over a mean free path · absorption is weak · far from boundaries", { color: TXT, breakLine: true }),
  n(" ", { fontSize: 6, breakLine: true }),
  n("A compact fast core fails all three: R is only 2–3 λ_tr, and most neutrons see the surface.", { bold: true, color: TXT })],
  { x: 0.85, y: 4.4, w: 11.7, h: 1.8, fontSize: 18, valign: "middle", margin: 0, isTextBox: true });
source(s, "Duderstadt & Hamilton (1976) ch. 4–5; Stacey (2018); Lamarsh & Baratta (2001) ch. 5–6. 0.7104 λ_tr: Milne-problem extrapolation distance.");
s.addNotes(notes[5]);

// =============== 6 — Sensitivity study
pres.addSection({ title: "Leakage" });
s = contentSlide(6, "Calculation", "Sensitivity Study: k_eff vs Size and Leakage");
figure(s, "fig_k_vs_R", 0.7, 1.7, 6.4, "k-effective versus sphere radius: one-group diffusion curve and Monte Carlo transport points");
const pick = [4.0, 6.0, 7.428998, 9.0, 12.0, 14.0];
const srows = SENS.rows.filter((r) => pick.some((p) => Math.abs(r.R - p) < 1e-3));
darkTable(s, [
  [{ text: "R [cm]", options: th }, { text: "k transport", options: th }, { text: "k diffusion", options: th }, { text: "leakage", options: th }],
  ...srows.map((r) => [r.R.toFixed(2), r.k_mc.toFixed(3), r.k_diff.toFixed(3), (100 * r.leak_mc).toFixed(0) + " %"]),
], { x: 7.5, y: 1.65, w: 5.25, colW: [1.15, 1.4, 1.4, 1.3], fontSize: 15, rowH: 0.47, objectName: "sensitivity table" });
s.addText([n("Diffusion: ", { bold: true, color: C.accent3 }), n(`R_c is ${(100 * (SENS.rc_diff / SENS.rc_exact - 1)).toFixed(1)} % too large. k error shrinks from ${Math.abs(SENS.rows[0].err_pct).toFixed(1)} % (R = 1.3 λ_tr) to ${Math.abs(SENS.rows[SENS.rows.length - 1].err_pct).toFixed(1)} % (R = 4.6 λ_tr).`, { color: TXT })],
  { x: 7.5, y: 5.0, w: 5.25, h: 1.1, fontSize: 16, margin: 0, isTextBox: true });
s.addText("Idealized LA-13511 one-group constants · mathematical illustration, not a reactor calculation", { x: 0.6, y: 6.25, w: 12.15, h: 0.32, fontSize: 12, italic: true, color: C.accent5, margin: 0, isTextBox: true });
source(s, "This work (code/run_analysis.py, study 2); cross sections and exact R_c = 7.428998 cm from Sood et al., LA-13511 (1999).");
s.addNotes(notes[6]);

// =============== 7 — Reflectors from boundary conditions
s = contentSlide(7, "Calculation", "Reflectors from Boundary Conditions");
card(s, 0.6, 1.6, 5.85, 3.0, CARD, HEX.accent2, "interface conditions");
s.addText([
  n("Core:  ", { color: C.accent2, bold: true }), n("φ_c = A sin(Br) / r", { breakLine: true }),
  n("Reflector:  ", { color: C.accent2, bold: true }), n("φ_r = C sinh[κ(R+T_e−r)] / r", { breakLine: true }),
  n(" ", { fontSize: 6, breakLine: true }),
  n("At r = R:  ", { color: C.accent2, bold: true }), n("φ_c = φ_r,   D_c φ_c′ = D_r φ_r′", { breakLine: true }),
  n(" ", { fontSize: 6, breakLine: true }),
  n("Reflector savings  δ = R_c,bare − R_c,reflected", { bold: true }),
], { x: 0.85, y: 1.7, w: 5.45, h: 2.8, fontSize: 17, color: TXT, valign: "middle", margin: 0, isTextBox: true });
figure(s, "fig_reflector_savings", 6.95, 1.7, 5.7, "Critical core radius versus reflector thickness: Monte Carlo transport, two-region diffusion and slab formula");
const rr = REFL.rows;
[[`${rr[0].savings_mc.toFixed(1)}–${rr[2].savings_mc.toFixed(1)} cm`, "transport savings, 1–3 mfp", C.accent1],
 [`×${(rr[0].savings_slab / rr[0].savings_mc).toFixed(1)}–${(rr[2].savings_slab / rr[2].savings_mc).toFixed(1)}`, "slab-formula overestimate", C.accent4],
 [`${(100 * VER["Ub-H2O(1)-1-0-SP"].frac_fis_after_refl).toFixed(0)}–${(100 * VER["Ud-H2O(3)-1-0-SP"].frac_fis_after_refl).toFixed(0)} %`, "fissions by reflector-returned neutrons", C.accent2]].forEach(([b, t, col], i) => {
  const x = 0.6 + i * 1.98; card(s, x, 4.8, 1.88, 1.65); stat(s, x + 0.12, 4.88, 1.7, b, t, col, 22);
});
source(s, "This work (study 3); H₂O (c = 0.90) and U-235 one-group constants from LA-13511; slab formula: Lamarsh & Baratta (2001) §6.6.");
s.addNotes(notes[7]);

// =============== 8 — Transport check
pres.addSection({ title: "Transport" });
s = contentSlide(8, "Verification", "Transport Check: Where Diffusion Fails");
const vrow = (id, lbl) => [lbl, "1", `${VER[id].k_mc.toFixed(4)} ± ${VER[id].k_std.toFixed(4)}`, VER[id].k_diff.toFixed(3)];
darkTable(s, [
  [{ text: "LA-13511 problem", options: th }, { text: "exact", options: th }, { text: "Monte Carlo", options: th }, { text: "diffusion", options: th }],
  vrow("Ua-1-0-SP", "bare sphere"), vrow("Ub-H2O(1)-1-0-SP", "+1 mfp reflector"), vrow("Uc-H2O(2)-1-0-SP", "+2 mfp reflector"),
  vrow("Ud-H2O(3)-1-0-SP", "+3 mfp reflector"), vrow("U-2-0-SP", "two-group sphere"),
], { x: 0.6, y: 1.65, w: 6.3, colW: [2.2, 0.9, 1.95, 1.25], fontSize: 15, rowH: 0.5, objectName: "verification table" });
s.addText([n("Monte Carlo verified ", { bold: true, color: C.accent2 }), n("on all five exact solutions (within ≈1σ).", { color: TXT, breakLine: true }),
  n("Diffusion is 6–12 % low ", { bold: true, color: C.accent4 }), n("at the same critical configurations.", { color: TXT })],
  { x: 0.6, y: 4.85, w: 6.3, h: 1.0, fontSize: 16, margin: 0, isTextBox: true });
figure(s, "fig_flux_shape", 7.35, 1.7, 5.3, "Normalized flux in the bare critical sphere: exact transport, Monte Carlo and diffusion");
const fs_ = VER["flux_shape_norm_at_0.25"]["1.0"];
s.addText(`Surface flux: exact ${fs_.exact.toFixed(2)} · MC ${fs_.mc.toFixed(2)} · diffusion ${fs_.diffusion.toFixed(2)}`, { x: 7.25, y: 5.5, w: 5.5, h: 0.4, fontSize: 15, bold: true, color: C.accent1, margin: 0, isTextBox: true });
source(s, "This work (studies 1–2); exact solutions and flux ratios: Sood, Forster & Parsons, LA-13511 (1999), Tables 13–15, 35.");
s.addNotes(notes[8]);

// =============== 9 — Spectral effects
pres.addSection({ title: "Spectrum" });
s = contentSlide(9, "Calculation", "Spectral Effects: Leakage Hardens the Spectrum");
figure(s, "fig_fast_share", 0.7, 1.7, 4.6, "Fast-group share of infinite-medium flux, of leaking neutrons, and of fissions");
figure(s, "fig_spectral_index", 5.7, 1.7, 4.55, "Fast-to-slow flux ratio versus radius in the critical two-group sphere");
const ci = SPEC.collapse_inf, cl = SPEC.collapse_leak;
[[`${ci.err_mc_pct.toFixed(1)} %`, "R_c error, one-group collapse with infinite-medium spectrum", C.accent1],
 [`${cl.err_mc_pct.toFixed(1)} %`, "with leakage-weighted spectrum", C.accent2],
 [`+${(100 * (SPEC.rc_diff_2g / SPEC.rc_exact - 1)).toFixed(1)} %`, "two-group diffusion error (for scale)", C.accent4]].forEach(([b, t, col], i) => {
  const y = 1.6 + i * 1.6; card(s, 10.6, y, 2.15, 1.45); stat(s, 10.75, y + 0.08, 1.95, b, t, col, 24);
});
s.addText([n("KRUSTY (literature): ", { bold: true, color: C.accent1 }), n("BeO-moderated neutrons returning from the reflector peak fission at the fuel edge.", { color: TXT })],
  { x: 0.6, y: 5.75, w: 12.15, h: 0.45, fontSize: 16, margin: 0, isTextBox: true });
source(s, "This work (study 4) with LA-13511 two-group U-235 constants (Tables 33–35); Poston et al., KRUSTY Reactor Design, Nucl. Technol. 206 (2020) S13.");
s.addNotes(notes[9]);

// =============== 10 — KRUSTY reflector worth
pres.addSection({ title: "KRUSTY" });
s = contentSlide(10, "Experiment", "KRUSTY: Reflector Worth Is the Control");
figureH(s, "fig_krusty_schematic", 0.7, 1.7, 4.8, "Simplified KRUSTY schematic: HEU core, B4C rod, BeO reflectors lifted by the COMET platen");
const kx = 6.55;
[["10.7–12 ¢/mm", "platen (reflector) worth, measured", C.accent2], ["≈ 4 ¢/mm", "central B₄C rod — one-third as sensitive", C.accent3],
 ["1.42 $", "inserted to reach 800 °C", C.accent1], ["−148 ¢", "fuel temperature defect (design model)", C.accent4]].forEach(([b, t, col], i) => {
  const x = kx + (i % 2) * 3.13, y = 1.6 + Math.floor(i / 2) * 1.75;
  card(s, x, y, 3.0, 1.6); stat(s, x + 0.2, y + 0.1, 2.65, b, t, col, 25);
});
card(s, kx, 5.2, 6.13, 1.3, WARM, HEX.accent1, "inference");
s.addText([n("Inference:  ", { bold: true, color: C.accent1 }), n("the reactivity added by moving the reflector ≈ the reactivity removed by hot fuel. MCNP predicted the first critical within 30 ¢.", { color: TXT })],
  { x: kx + 0.2, y: 5.2, w: 5.75, h: 1.3, fontSize: 15, valign: "middle", margin: 0, isTextBox: true });
source(s, "Poston et al., Results of the KRUSTY Nuclear System Test (2020) S89; KRUSTY Reactor Design (2020) S13, Table II; Results of the KRUSTY Warm Critical Experiments (2020) S78.");
s.addNotes(notes[10]);

// =============== 11 — Feedback decomposition
s = contentSlide(11, "Experiment + calculation", "Decomposing KRUSTY's Negative Feedback");
figure(s, "fig_krusty_feedback", 0.7, 1.7, 6.0, "KRUSTY component temperature coefficients from the published design model");
figure(s, "fig_feedback_compare", 7.1, 1.7, 5.55, "Expansion feedback: idealized estimates from this work versus KRUSTY published and measured values");
[["≈ 95 %", "of net feedback from fuel heating"], ["90 / 10", "expansion / cross sections (incl. Doppler)"], ["+0.06 ¢/K", "BeO radial reflector at 343 K"]].forEach(([b, t], i) => {
  const x = 0.6 + i * 2.15; card(s, x, 5.1, 2.0, 1.4, CARD, HEX.accent2); stat(s, x + 0.15, 5.15, 1.75, b, t, C.accent2, 24);
});
s.addText([n("This work: ", { bold: true, color: C.accent1 }), n(`(dln k/dε)·α/β ≈ ${FB["bare sphere, whole core expands"].cents_per_K.toFixed(2)} to ${FB["reflected (Ub-H2O(1)), core only expands"].cents_per_K.toFixed(2)} ¢/K. Right sign and order of magnitude; ~2× KRUSTY. A consistency check, not a prediction.`, { color: TXT })],
  { x: 7.1, y: 5.15, w: 5.65, h: 1.3, fontSize: 15, valign: "middle", margin: 0, isTextBox: true });
source(s, "Poston et al., KRUSTY Reactor Design (2020), Table II and text; Results of the KRUSTY Nuclear System Test (2020); α: Burkes et al., INL/EXT-10-19373 (U-10Mo proxy); this work (study 5).");
s.addNotes(notes[11]);

// =============== 12 — Findings
pres.addSection({ title: "Findings" });
s = contentSlide(12, "Findings", "Findings: Calculated · Observed · Inferred");
const cols3 = [
  ["Calculated (this work)", HEX.accent1, ["Diffusion: k 6–12 % low, R_c +7 % in compact benchmarks", "Error is set by size in mean free paths", "Leakage removes fast neutrons; spectral collapse error ~1 %"]],
  ["Observed (KRUSTY test)", HEX.accent2, ["Reflector position was the reactivity control", "Feedback ≈ 0.2 ¢/°C near 800 °C", "Power followed load passively"]],
  ["Inferred (engineering)", HEX.accent3, ["Compact-core criticality is mostly geometry and leakage", "Feedback sign depends on which component heats", "Design conclusions need validated transport"]],
];
cols3.forEach(([h, col, items], i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.95, 3.95, CARD, col, "findings " + h);
  s.addText(h, { x: x + 0.22, y: 1.72, w: 3.55, h: 0.45, fontSize: 18, bold: true, color: col, margin: 0, isTextBox: true });
  s.addText(items.map((t, j) => ({ text: t, options: { bullet: { indent: 14 }, breakLine: j < items.length - 1, paraSpaceAfter: 10 } })),
    { x: x + 0.22, y: 2.3, w: 3.55, h: 3.1, fontSize: 16, color: TXT, valign: "top", margin: 0, isTextBox: true });
});
card(s, 0.6, 5.75, 12.15, 0.75, COOL, HEX.accent2, "next step");
s.addText([n("Next: ", { bold: true, color: C.accent2 }), n("continuous-energy OpenMC model, validated against the KRUSTY benchmarks (input provided, not yet run)", { color: TXT })],
  { x: 0.85, y: 5.75, w: 11.7, h: 0.75, fontSize: 16, valign: "middle", margin: 0, isTextBox: true });
source(s, "This work (studies 1–5); Poston et al. (2020) S89, S13; Stolte et al., Nucl. Technol. 208 (2022) 625; Romano et al., Ann. Nucl. Energy 82 (2015) 90.");
s.addNotes(notes[12]);

// =============== 13 — Conclusions
s = contentSlide(13, "Conclusions", "Conclusions");
[["1", "Six-factor is a special case", "of the k-eigenvalue problem: useful for thinking, not for small fast cores.", HEX.accent1],
 ["2", "Leakage, reflection and spectrum are coupled", "One-group diffusion misses them by 5–12 % in k: many dollars of reactivity.", HEX.accent2],
 ["3", "KRUSTY makes it real", "Reflector position controlled the reactor; fuel expansion stabilized it.", HEX.accent3]].forEach(([num, h, t, col], i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.95, 3.2, CARD, col, "conclusion card");
  s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: 1.85, w: 0.7, h: 0.7, fill: { color: col }, line: { color: col } });
  s.addText(num, { x: x + 0.3, y: 1.85, w: 0.7, h: 0.7, fontSize: 22, bold: true, color: "1B2430", align: "center", valign: "middle", isTextBox: true });
  s.addText([n(h, { bold: true, fontSize: 19, color: TXT, breakLine: true }), n(t, { fontSize: 16, color: MUTED })],
    { x: x + 0.3, y: 2.75, w: 3.4, h: 1.95, valign: "top", margin: 0, isTextBox: true, paraSpaceAfter: 6 });
});
s.addText("Classical theory is where the analysis starts. Validated transport is where design conclusions come from.",
  { x: 0.6, y: 5.05, w: 12.15, h: 0.75, fontSize: 20, italic: true, color: TXT, margin: 0, isTextBox: true });
[["↺  Back to title", 1], ["References", 14]].forEach(([t, target], i) => {
  const x = 0.6 + i * 2.1;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 6.05, w: 1.95, h: 0.42, rectRadius: 0.21, fill: { color: CARD }, line: { color: HEX.accent5, width: 0.75 }, objectName: "link chip" });
  s.addText(t, { x, y: 6.05, w: 1.95, h: 0.42, fontSize: 11.5, bold: true, color: TXT, align: "center", valign: "middle", margin: 0, isTextBox: true });
  linkOverlay(s, x, 6.05, 1.95, 0.42, target, t.replace("↺  ", ""));
});
s.addText("Slides, report and code: GitHub repository linked in the video description", { x: 4.9, y: 6.08, w: 7.85, h: 0.36, fontSize: 11.5, color: C.accent5, align: "right", margin: 0, isTextBox: true });
s.addNotes(notes[13]);

// =============== 14 — References
s = contentSlide(14, "References", "References");
const refsL = [
  "Bell, G. I., Glasstone, S. Nuclear Reactor Theory. Van Nostrand Reinhold, 1970.",
  "Duderstadt, J. J., Hamilton, L. J. Nuclear Reactor Analysis. Wiley, 1976.",
  "Lamarsh, J. R., Baratta, A. J. Introduction to Nuclear Engineering, 3rd ed. Prentice Hall, 2001.",
  "Stacey, W. M. Nuclear Reactor Physics, 3rd ed. Wiley-VCH, 2018.",
  "Sood, A., Forster, R. A., Parsons, D. K. Analytical Benchmark Test Set for Criticality Code Verification. LA-13511, LANL, 1999; Prog. Nucl. Energy 42, 55–106, 2003.",
  "Romano, P. K. et al. OpenMC: A state-of-the-art Monte Carlo code for research and development. Ann. Nucl. Energy 82, 90–97, 2015.",
  "Burkes, D. E., Mickum, G. S., Wachs, D. M. Thermophysical Properties of U-10Mo Alloy. INL/EXT-10-19373, 2010.",
];
const refsR = [
  "Poston, D. I. et al. KRUSTY Reactor Design. Nucl. Technol. 206 (sup1) S13–S30, 2020.",
  "Poston, D. I. et al. Results of the KRUSTY Warm Critical Experiments. Nucl. Technol. 206 (sup1) S78–S88, 2020.",
  "Poston, D. I. et al. Results of the KRUSTY Nuclear System Test. Nucl. Technol. 206 (sup1) S89–S117, 2020.",
  "Sanchez, R. et al. KRUSTY Component-Critical Experiments. Nucl. Technol. 206 (sup1) S56–S67, 2020.",
  "Stolte, K. N. et al. Benchmark of the KRUSTY Component Critical Configurations. Nucl. Technol. 208(4) 625–643, 2022.",
  "NASA & U.S. DOE. NASA, Department of Energy to Develop Lunar Surface Reactor by 2030. News release, 13 Jan. 2026.",
  "New Space Economy. What Does NASA's SPARC Lunar Reactor Procurement Reveal About Lunar Reactor-1? 1 Sep. 2026.",
];
[refsL, refsR].forEach((list, k) => {
  s.addText(list.map((r, i) => ({ text: r, options: { breakLine: i < list.length - 1, paraSpaceAfter: 7 } })),
    { x: 0.6 + k * 6.25, y: 1.6, w: 5.9, h: 4.95, fontSize: 14, color: MUTED, valign: "top", margin: 0, isTextBox: true });
});
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.8, y: 6.62, w: 1.95, h: 0.4, rectRadius: 0.2, fill: { color: CARD }, line: { color: HEX.accent5, width: 0.75 }, objectName: "link chip" });
s.addText("↺  Back to title", { x: 10.8, y: 6.62, w: 1.95, h: 0.4, fontSize: 11, bold: true, color: TXT, align: "center", valign: "middle", margin: 0, isTextBox: true });
linkOverlay(s, 10.8, 6.62, 1.95, 0.4, 1, "Back to title");
s.addNotes("References slide. Full bibliography with DOIs and URLs: report/references.bib and the PDF report.");

// ---------- write, theme, transitions ----------
async function addTransitions(file) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const slides = Object.keys(zip.files).filter((f) => /^ppt\/slides\/slide\d+\.xml$/.test(f));
  for (const f of slides) {
    let xml = await zip.file(f).async("string");
    if (xml.includes("<p:transition")) continue;
    const tr = '<p:transition spd="med"><p:fade/></p:transition>';
    if (xml.includes("</p:clrMapOvr>")) xml = xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + tr);
    else xml = xml.replace("</p:cSld>", "</p:cSld>" + tr);
    zip.file(f, xml);
  }
  const out = new JSZip();                       // copy files only: no folder entries in the package
  for (const f of Object.keys(zip.files)) {
    if (!zip.files[f].dir) out.file(f, await zip.file(f).async("nodebuffer"), { createFolders: false });
  }
  fs.writeFileSync(file, await out.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
  return slides.length;
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  const skillTheme = "/mnt/skills/public/pptx/scripts/apply_theme.js";
  const local = path.join(__dirname, "apply_theme.js");
  const mod = fs.existsSync(skillTheme) ? skillTheme : (fs.existsSync(local) ? local : null);
  if (mod) { const { applyTheme } = require(mod); await applyTheme(OUT, THEME); }
  else console.warn("apply_theme.js not found: theme colors fall back to Office defaults.");
  const k = await addTransitions(OUT);
  console.log(`Wrote ${OUT} (${k} slides, fade transitions)`);
})();
