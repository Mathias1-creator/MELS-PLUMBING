# Images — what's on the site, and how to swap it

Every image lives in `images/` and is referenced by a relative path
(`images/gallery-1.jpg`). **Swapping one is a straight file replacement:** keep
the filename, keep roughly the same shape, and nothing in the HTML or CSS has
to change — only the `alt` text, which should describe what the new photo
actually shows.

---

## Status: no placeholders left

Every image on the site is now a real photograph. Seven of the eight are
Melvin's own job photos; one is stock.

The home hero and all four interior page heroes use **no photo at all** — they
are solid green gradients, by client request.

---

## The eight image slots

| File | Where it appears | What it shows | Dimensions | Source |
|---|---|---|---|---|
| `images/service-remodel.jpg` | Home services card + Services "Plumbing remodels" | Finished bathroom remodel — white subway tile, new tub and shower valve, toilet, grey vanity | 1600 × 1200 (4:3) | Client photo, Drive `MELS` folder |
| `images/service-repair.jpg` | Home services card + Services "Plumbing repairs" | **Stock, not Melvin's work** — steel pipework, valves and a regulator on a brick wall | 1600 × 1200 (4:3) | Unsplash (photo ID `4CNNH2KEjhc`), chosen by the client |
| `images/service-maintenance.jpg` | Home services card + Services "Plumbing maintenance" | Pliers on a water heater supply connection, insulated hot line and brass valve | 1600 × 1200 (4:3) | Client photo, Drive `MELS` folder |
| `images/gallery-1.jpg` | Gallery (large tile) + home teaser | Stone vessel sink on a live-edge wood vanity, black iron P-trap and supply lines | 1200 × 1600 (3:4) | Client photo `1000008076.jpg` |
| `images/gallery-2.jpg` | Gallery (large tile) + home teaser | Tankless water heater, copper lines, gas flex connector, shut-off valves | 1200 × 1600 (3:4) | Client photo `1000008070.jpg` |
| `images/gallery-3.jpg` | Gallery + home teaser | Scaled-up water heater element beside its clean replacement | 900 × 1200 (3:4) | Client photo `1000008069.jpg` |
| `images/gallery-4.jpg` | Gallery | Black iron pipe run with a shut-off valve, through an attic beside ductwork | 900 × 1200 (3:4) | Client photo `1000008071.jpg` |
| `images/gallery-5.jpg` | Gallery | Finished bathroom corner, stone vessel sink on a live-edge counter | 900 × 1200 (3:4) | Client photo `1000006731.jpg` |

---

## The one thing still worth replacing

`images/service-repair.jpg` is a stock photo of commercial gas equipment — not
Melvin's work, and not really a plumbing repair. The site's whole pitch is
honesty first, so a real repair photo (even a phone shot of a water heater swap
or a leak under a sink) would serve it better. Same filename, roughly 4:3
landscape, and update the `alt` text on `index.html` and `services.html`.

---

## Rules for replacement photos

- **Keep the filename.** `gallery-3.jpg` has to stay `gallery-3.jpg`. Convert
  HEIC or PNG to JPEG first.
- **Shape matters more than exact pixels.** Gallery tiles are 3:4 portrait —
  phone photos held upright fit with no cropping. The three service images are
  4:3 landscape.
- **Size:** 900–1200px on the long edge is plenty. Keep files under ~400KB so
  the site stays fast; quality 80 in any image editor gets you there.
- **Update the alt text.** Each `<img>` has alt text written for the specific
  photo in that slot. It is what screen readers announce and what Google reads,
  so it has to match whatever picture is actually there.
- **Watch out for Android motion photos.** The client's phone saves a JPEG with
  a video clip appended. They decode fine but some tools choke; re-saving them
  as a plain JPEG (which the crop step does) strips the extra data.

## Adding a sixth gallery tile

The gallery grid is built for exactly five tiles — two half-width on top, three
thirds below, so both rows fill with no gap. Adding a sixth means editing the
`nth-child` rules under `.gallery-grid` in `css/styles.css`, or the last row
will come out ragged.

## About the scripts in `tools/`

Both are **deliberately switched off** — their slot lists are empty.

They were used to build the placeholder art the site launched with. Now that
every slot holds a real photo, running either one with its old list would
overwrite the client's photographs. `generate-placeholder-images.py` did
exactly that once and had to be undone from git. Leave them empty unless a
genuinely new, photo-less slot is added.
