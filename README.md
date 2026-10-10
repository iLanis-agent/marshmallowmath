# Marshmallow math

Homemade marshmallow planning. A static site with three calculators:

- **Gelatin converter** - powder grams become envelopes and bronze, silver, gold or platinum sheets, with labeled sheet weights and a bloom-strength caveat.
- **Pan fill** - pan dimensions and slab height become the batch size and its ingredient split from a labeled base ratio.
- **Cut yield** - pan and piece size become the grid, the piece count and the dusting mix.

Live site: https://ilanis-agent.github.io/marshmallowmath/

## Labeled norms

Labeled kitchen references - your recipe and your labels win:

- Powder envelope 7 g. Sheet weights: bronze 3.3 g, silver 2.5 g, gold 2.0 g, platinum 1.7 g. Bloom strengths vary by brand.
- Aerated slab density about 0.5 g per ml.
- Base batch by mass per 891 g: sugar 300, corn syrup 330, water 240, gelatin 21.
- Dusting 2 g per piece, 50/50 cornstarch and powdered sugar.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 39 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 117 checks, 0 failures
```
