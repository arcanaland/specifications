// SPDX-FileCopyrightText: 2026 Adam Fidel
// SPDX-License-Identifier: MIT
//
// Pandoc Typst template for the Arcana Land specifications.

$if(highlighting-definitions)$
$highlighting-definitions$

$endif$

#let draft = sys.inputs.at("draft", default: "true") != "false"

#let serif = ("Libertinus Serif", "New Computer Modern", "Noto Serif", "Liberation Serif")
#let mono = ("DejaVu Sans Mono", "JetBrainsMono NF", "Liberation Mono")

#let ink = luma(0)
#let faint = luma(120)
#let rule-thin = 0.5pt + luma(150)

#set page(
  paper: "us-letter",
  margin: (x: 1in, y: 1in),
  background: if draft {
    align(center + horizon, rotate(45deg, reflow: false,
      text(size: 120pt, fill: rgb(0, 0, 0, 8), weight: "bold")[DRAFT]))
  },
  footer: context {
    set text(size: 8pt, fill: faint, font: serif)
    grid(
      columns: (1fr, auto, 1fr),
      align: (left + horizon, center + horizon, right + horizon),
$if(provenance)$
      [$provenance$],
$else$
      [],
$endif$
      counter(page).display("1"),
      if draft [Draft] else [],
    )
  },
)

#set document(
  title: "$title$",
  author: "Arcana Land",
)

// --- text --------------------------------------------------------------------

#set text(font: serif, size: 10.5pt, lang: "$if(lang)$$lang$$else$en$endif$", hyphenate: true)
#set par(justify: true, leading: 0.62em, spacing: 1.1em)

#let linkcolor = rgb("#1a4f8a")
#show link: set text(fill: linkcolor)

#show heading: set text(font: serif, weight: "bold")
#show heading: set block(sticky: true, above: 1.4em, below: 0.7em)
#show heading.where(level: 1): set text(size: 17pt)
#show heading.where(level: 2): set text(size: 13pt)
#show heading.where(level: 3): set text(size: 11.5pt)
#show heading.where(level: 4): set text(size: 10.5pt)

// --- code --------------------------------------------------------------------

#show raw: set text(font: mono, size: 8.8pt)
#show raw.where(block: true): it => block(
  width: 100%,
  fill: luma(248),
  stroke: (left: 2pt + luma(210)),
  inset: (x: 8pt, y: 7pt),
  above: 1.1em,
  below: 1.1em,
  it,
)

// --- tables ------------------------------------------------------------------

#show figure: set block(breakable: true)
#show figure: set align(left)
#show figure.where(kind: table): set figure.caption(position: top)
#show figure.where(kind: image): set figure.caption(position: bottom)

#set table(
  inset: (x: 6pt, y: 5pt),
  stroke: (x, y) => if y == 0 { (bottom: rule-thin) },
)
#show table.cell.where(y: 0): set text(weight: "bold")
#show table.cell: it => {
  set align(left + top)
  it
}
#show table: set text(size: 9.5pt)
#show table: set par(justify: false)

// --- pandoc's own defaults ----------------------------------------------------

#let horizontalrule = line(start: (25%, 0%), end: (75%, 0%))

#show terms.item: it => block(breakable: false)[
  #text(weight: "bold")[#it.term]
  #block(inset: (left: 1.5em, top: -0.4em))[#it.description]
]

$if(smart)$
$else$
#set smartquote(enabled: false)

$endif$
$for(header-includes)$
$header-includes$

$endfor$
// --- title block --------------------------------------------------------------

#block(above: 0pt, below: 2.2em)[
  #text(size: 22pt, weight: "bold")[$title$]
$if(subtitle)$
  #linebreak()
  #v(0.5em, weak: true)
  #text(size: 13pt, fill: faint)[$subtitle$]
$endif$
  #v(0.9em, weak: true)
  #line(length: 100%, stroke: rule-thin)
$if(date)$
  #v(0.4em, weak: true)
  #text(size: 9pt, fill: faint)[Built $date$$if(provenance)$ from $provenance$$endif$]
$endif$
]

$for(include-before)$
$include-before$

$endfor$
$if(toc)$
#outline(title: auto, depth: $toc-depth$)
$endif$

$body$

$for(include-after)$
$include-after$

$endfor$
