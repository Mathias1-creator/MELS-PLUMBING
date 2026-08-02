# Images — what's in the site now, and how to swap it

Every image on the site lives in `images/` and is referenced by a relative path
(`images/hero.jpg`). **Swapping an image is a straight file replacement:** keep
the filename, keep roughly the same shape, and nothing in the HTML or CSS needs
to change.

---

## Status: 7 of 10 are placeholders

**Update (Aug 2, 2026):** two slots now hold real client photos from the Drive
`MELS` folder — `service-remodel.jpg` (finished bathroom remodel) and
`service-maintenance.jpg` (water heater service). `service-repair.jpg` holds a
stock photo the client chose (Unsplash industrial pipework). The remaining
seven — hero and gallery 1–6 — still hold placeholders and are **not yet in the
Drive folder**; only the two client photos have been uploaded there so far.

The site was built inside a sandbox whose network policy blocks every stock
photo host (Unsplash, Pexels, Pixabay, Wikimedia — all refused at the proxy).
Rather than ship broken image slots, each remaining one holds a **generated
placeholder plate**: a technical line drawing of the right subject, in the site's own green
and silver palette, with the word `PLACEHOLDER` printed in the corner so nobody
mistakes it for a real project photo.

They are real, valid JPEGs at the correct dimensions, so layout, spacing and
load behaviour on the preview are exactly what you'll get with real photos.

**Two ways to get real images in:**

1. **Client photos (best).** Melvin's own job photos will always beat stock —
   they are the actual work, and they build more trust than a stock bathroom.
   Drop them in using the filenames below.
2. **Stock photos.** Run `bash tools/fetch-stock-images.sh` on any machine with
   normal internet access. It scrapes Unsplash search pages for genuine photo
   IDs, downloads one per slot, verifies each file is a real JPEG over 30KB,
   and backs up the placeholders it replaces.

---

## The 10 image slots

| File | Where it appears | What it should show | Current contents | Dimensions | Source |
|---|---|---|---|---|---|
| `images/hero.jpg` | Home — full-width hero behind the headline | Plumber at work, copper pipework, or a clean modern bathroom. Needs a calm left side: the headline sits over it and the green scrim darkens that half. | Generated plate — supply-line rough-in with gate valve and pressure gauge | 2000 × 1250 (16:10) | Generated locally, `tools/generate-placeholder-images.py` |
| `images/service-remodel.jpg` | Home service card + Services "Plumbing remodels" | ✔ Done — real client photo in place | Client photo — finished bathroom remodel: white subway tile, tub/shower, toilet, grey vanity | 1600 × 1200 (4:3) | Client photo from Drive `MELS/Plumbing remodels` (cropped from 4000×6000 portrait original) |
| `images/service-repair.jpg` | Home service card + Services "Plumbing repairs" | Hands-on repair: wrench on a fitting, leak under a sink — a real MELS repair photo would beat the current stock | Stock photo — steel pipework, valves and regulator on a brick wall (Unsplash ID 4CNNH2KEjhc, photographer "compagnons") | 1600 × 1200 (4:3) | Unsplash, uploaded by client |
| `images/service-maintenance.jpg` | Home service card + Services "Plumbing maintenance" | ✔ Done — real client photo in place | Client photo — pliers on a water heater supply connection, insulated hot line and brass valve, tank below | 1600 × 1200 (4:3) | Client photo from Drive `MELS/plumbing maintence` (top-aligned crop of 5894×5304 original) |
| `images/gallery-1.jpg` | Home teaser + Gallery (large tile, top-left) | Finished bathroom remodel — the best "after" shot available | Generated plate — finished bathroom with tile field | 1200 × 900 (4:3) | Generated locally |
| `images/gallery-2.jpg` | Home teaser + Gallery | Water heater installed, strapped and piped to code | Generated plate — water heater install with expansion tank | 1200 × 900 (4:3) | Generated locally |
| `images/gallery-3.jpg` | Home teaser + Gallery | Copper or PEX runs through studs — clean rough-in work | Generated plate — copper run through framing | 1200 × 900 (4:3) | Generated locally |
| `images/gallery-4.jpg` | Gallery | Modern kitchen or bath faucet, newly installed | Generated plate — gooseneck kitchen faucet | 1200 × 900 (4:3) | Generated locally |
| `images/gallery-5.jpg` | Gallery (large tile) | Drain or rooter work — cleared line, cable, floor drain | Generated plate — floor drain with rooter cable | 1200 × 900 (4:3) | Generated locally |
| `images/gallery-6.jpg` | Gallery | Finished kitchen or bath — wide "after" shot | Generated plate — kitchen sink with supply lines | 1200 × 900 (4:3) | Generated locally |

---

## Rules for replacement photos

- **Filenames must stay the same.** `gallery-3.jpg` has to stay `gallery-3.jpg`.
  If a client photo is a PNG or HEIC, convert it to JPEG first.
- **Shape matters more than exact pixels.** Everything except the hero is
  roughly 4:3 and gets cropped to fill its box, so keep the subject centred.
  The hero is wide (16:10) and its left third sits under the headline — pick
  something that isn't busy on that side.
- **Size:** aim for 1600px wide for the gallery and service images, 2000px for
  the hero. Keep files under ~400KB so the site stays fast; quality 80–85 in
  any image editor is plenty.
- **Landscape, not portrait.** Vertical phone photos get badly cropped in the
  grid.
- **Update the alt text too.** Each `<img>` has descriptive alt text written for
  the placeholder subject. When a photo changes what's actually pictured, edit
  the `alt` attribute in the HTML to match — it's what screen readers announce
  and what Google reads.

## After swapping

1. Open each page and check the crop: `index.html`, `services.html`, `gallery.html`.
2. On `gallery.html`, click a tile — the lightbox loads the same file at full size,
   so a low-resolution photo will show it there first.
3. Delete `images/_placeholders-backup/` once you're happy.
4. Update the "Current contents" and "Source" columns above so the next person
   knows where the photos came from.

## Regenerating the placeholders

If you ever need the plates back:

```bash
python3 tools/generate-placeholder-images.py   # needs Pillow + Chromium
```
