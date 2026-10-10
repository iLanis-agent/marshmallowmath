#!/usr/bin/env python3
"""Independent oracle for Marshmallow math. Mirrors engine.js float ops exactly."""
import json, math

SHEETS = {"bronze": 3.3, "silver": 2.5, "gold": 2.0, "platinum": 1.7}
RATIO = {"sugar": 300 / 891, "syrup": 330 / 891, "water": 240 / 891, "gelatin": 21 / 891}
DENSITY = 0.5

def r1(x):
    return math.floor(x * 10 + 0.5) / 10

def num(x):
    # JS number-to-string for the values this engine produces (matches %g)
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)

def gelatin_convert(powder_g, sheet_type):
    if not (isinstance(powder_g, (int, float)) and math.isfinite(powder_g) and powder_g > 0):
        return {"error": "gelatin must be positive"}
    sw = SHEETS.get(sheet_type)
    if sw is None:
        return {"error": "unknown sheet type"}
    return {
        "powderG": r1(powder_g),
        "sheetType": sheet_type,
        "sheetW": sw,
        "envelopes": r1(powder_g / 7),
        "sheets": r1(powder_g / sw),
    }

def render_gelatin(r):
    if "error" in r: return r["error"]
    return (f"{num(r['powderG'])} g of powder = {num(r['envelopes'])} envelopes (7 g each) = "
            f"{num(r['sheets'])} {r['sheetType']} sheets ({num(r['sheetW'])} g each) - "
            "labeled sheet weights, bloom strengths vary by brand.")

def pan_fill(w, l, h):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (w, l, h)):
        return {"error": "pan dimensions must be positive"}
    vol = w * l * h
    batch = r1(vol * DENSITY)
    return {
        "vol": r1(vol),
        "batch": batch,
        "sugar": r1(batch * RATIO["sugar"]),
        "syrup": r1(batch * RATIO["syrup"]),
        "water": r1(batch * RATIO["water"]),
        "gelatin": r1(batch * RATIO["gelatin"]),
    }

def render_pan(r):
    if "error" in r: return r["error"]
    return (f"{num(r['vol'])} ml of pan holds about {num(r['batch'])} g of batch: sugar {num(r['sugar'])} g, "
            f"corn syrup {num(r['syrup'])} g, water {num(r['water'])} g, gelatin {num(r['gelatin'])} g "
            "(labeled base ratios).")

def cut_yield(w, l, piece):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (w, l, piece)):
        return {"error": "sizes must be positive"}
    cols = math.floor(w / piece)
    rows = math.floor(l / piece)
    if cols < 1 or rows < 1:
        return {"error": "piece size is bigger than the pan"}
    pieces = cols * rows
    dust = r1(pieces * 2)
    return {"cols": cols, "rows": rows, "pieces": pieces, "dust": dust,
            "cornstarch": r1(dust / 2), "powderedSugar": r1(dust / 2)}

def render_cut(r):
    if "error" in r: return r["error"]
    return (f"{r['cols']} x {r['rows']} grid = {r['pieces']} pieces; dusting {num(r['dust'])} g - "
            f"{num(r['cornstarch'])} g cornstarch + {num(r['powderedSugar'])} g powdered sugar "
            "(labeled 2 g per piece).")

cases = []
for pw, st in [(21, "silver"), (10, "bronze"), (7, "gold"), (14, "platinum"), (3.5, "silver"),
               (28, "bronze"), (50, "gold"), (2, "platinum"), (100, "silver"), (12.25, "gold"),
               (0, "silver"), (-5, "bronze"), (21, "unobtanium"), (8, "silver")]:
    res = gelatin_convert(pw, st)
    cases.append({"fn": "gelatinConvert", "args": [pw, st], "result": res, "render": render_gelatin(res)})
for w, l, h in [(23, 33, 2.5), (20, 20, 4), (13, 13, 5), (30, 40, 3), (10, 10, 2),
                (17.5, 25.5, 3.2), (9, 9, 9), (50, 70, 6), (0, 20, 4), (20, -3, 4),
                (15, 15, 0), (22.2, 33.3, 4.4)]:
    res = pan_fill(w, l, h)
    cases.append({"fn": "panFill", "args": [w, l, h], "result": res, "render": render_pan(res)})
for w, l, p in [(23, 33, 5), (20, 30, 5), (20, 20, 4), (10, 10, 2.5), (33, 23, 4.5),
                (4, 10, 5), (10, 4, 5), (15, 15, 7.5), (40, 25, 3), (0, 10, 5),
                (10, 10, -2), (9.9, 20, 5), (100, 60, 7)]:
    res = cut_yield(w, l, p)
    cases.append({"fn": "cutYield", "args": [w, l, p], "result": res, "render": render_cut(res)})

with open("expected.json", "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print(len(cases), "cases written")
