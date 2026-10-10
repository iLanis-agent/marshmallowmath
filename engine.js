// Marshmallow math engine - pure arithmetic, shared by the page and the tests.
// Every borrowed number is a labeled kitchen norm, not a rule.
(function (root) {
"use strict";

// Labeled norms:
// - Powder gelatin envelope: 7 g.
// - Sheet gelatin weights (labeled, common reference): bronze 3.3 g, silver 2.5 g, gold 2.0 g, platinum 1.7 g. Bloom strengths vary by brand.
// - Aerated marshmallow slab density: about 0.5 g per ml.
// - Base batch ratios by mass (labeled home-kitchen reference, sums to 891 g): sugar 300, corn syrup 330, water 240, gelatin 21.
// - Dusting mix: 2 g per piece, 50/50 cornstarch and powdered sugar.
var SHEETS = { bronze: 3.3, silver: 2.5, gold: 2.0, platinum: 1.7 };
var RATIO = { sugar: 300 / 891, syrup: 330 / 891, water: 240 / 891, gelatin: 21 / 891 };
var DENSITY = 0.5;

function r1(x) { return Math.round(x * 10) / 10; }
function positive() {
  for (var i = 0; i < arguments.length; i++) {
    var v = arguments[i];
    if (typeof v !== "number" || !isFinite(v) || v <= 0) return false;
  }
  return true;
}

function gelatinConvert(powderG, sheetType) {
  if (!positive(powderG)) return { error: "gelatin must be positive" };
  var sw = SHEETS[sheetType];
  if (!sw) return { error: "unknown sheet type" };
  return {
    powderG: r1(powderG),
    sheetType: sheetType,
    sheetW: sw,
    envelopes: r1(powderG / 7),
    sheets: r1(powderG / sw)
  };
}

function renderGelatin(r) {
  if (r.error) return r.error;
  return r.powderG + " g of powder = " + r.envelopes + " envelopes (7 g each) = " + r.sheets + " " + r.sheetType +
    " sheets (" + r.sheetW + " g each) - labeled sheet weights, bloom strengths vary by brand.";
}

function panFill(w, l, h) {
  if (!positive(w, l, h)) return { error: "pan dimensions must be positive" };
  var vol = w * l * h;
  var batch = r1(vol * DENSITY);
  return {
    vol: r1(vol),
    batch: batch,
    sugar: r1(batch * RATIO.sugar),
    syrup: r1(batch * RATIO.syrup),
    water: r1(batch * RATIO.water),
    gelatin: r1(batch * RATIO.gelatin)
  };
}

function renderPan(r) {
  if (r.error) return r.error;
  return r.vol + " ml of pan holds about " + r.batch + " g of batch: sugar " + r.sugar + " g, corn syrup " + r.syrup +
    " g, water " + r.water + " g, gelatin " + r.gelatin + " g (labeled base ratios).";
}

function cutYield(w, l, piece) {
  if (!positive(w, l, piece)) return { error: "sizes must be positive" };
  var cols = Math.floor(w / piece);
  var rows = Math.floor(l / piece);
  if (cols < 1 || rows < 1) return { error: "piece size is bigger than the pan" };
  var pieces = cols * rows;
  var dust = r1(pieces * 2);
  return {
    cols: cols,
    rows: rows,
    pieces: pieces,
    dust: dust,
    cornstarch: r1(dust / 2),
    powderedSugar: r1(dust / 2)
  };
}

function renderCut(r) {
  if (r.error) return r.error;
  return r.cols + " x " + r.rows + " grid = " + r.pieces + " pieces; dusting " + r.dust + " g - " + r.cornstarch +
    " g cornstarch + " + r.powderedSugar + " g powdered sugar (labeled 2 g per piece).";
}

var api = {
  gelatinConvert: gelatinConvert,
  panFill: panFill,
  cutYield: cutYield,
  renderGelatin: renderGelatin,
  renderPan: renderPan,
  renderCut: renderCut
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.MarshmallowMath = api;
})(typeof window !== "undefined" ? window : globalThis);
