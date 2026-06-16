# Product video → Vancouver shopping research

Use this reference when Sir asks to extract products from a short video/reel and then find buying links/prices for Vancouver, BC.

## Proven workflow

1. Extract the video metadata/content first.
   - Facebook share links may redirect to `/reel/<id>/` and only expose caption text via basic extraction.
   - If needed, use `yt-dlp` in a temporary venv to download public reels for frame review.
2. Sample frames for visual product ID.
   - `ffmpeg -i video.mp4 -vf "fps=1/1,scale=540:-1" frames/frame_%03d.jpg`
   - Build contact sheets, then run vision on contact sheets and key frames for labels.
3. For prices, default to **Vancouver BC** even if the active travel context is elsewhere.
   - The user explicitly clarified: “Remember that we live in Vancouver BC.”
   - If using Instacart pages, append `&zipcode=V6B1A1` or another Vancouver postal code; otherwise Instacart may silently use a stale/travel/default postal code.
4. Prefer verified local/Canadian purchase links and say when exact products are not found.
   - Do not substitute a close product without labeling it as a substitute.
   - Include retailer, price, size, URL, and note shipping/local availability or uncertainty.
5. For US-only direct-to-consumer products, provide official link and USD price; convert only if a current exchange-rate lookup succeeds, and label conversion approximate.

## Session examples

- Nordic Naturals Children’s DHA Liquid Strawberry 119 mL / 4 fl oz: Well.ca product page was verifiable and Canadian.
- Mama Bird Kids Liquid Multi+: product JSON endpoint `https://www.lovemamabird.com/products/kids-liquid-multi.js` exposed title, availability, and USD price when the normal HTML page was blocked.
- Instacart Vancouver search pages produced embedded product data with `name`, `size`, `evergreenUrl`, and `priceString`; direct links can be formed as `https://www.instacart.ca/products/<evergreenUrl>`.
- Exact matches may not exist in Canada/Vancouver: e.g. Once Upon a Farm Apple-Berry Avocado Oat Milk Smoothie and Organic Valley Pasture-Raised Ghee were not verified locally; local substitutes were reported separately.
