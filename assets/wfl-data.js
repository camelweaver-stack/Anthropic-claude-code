// West FW Living — single source of truth for tools, deals, quiz & charts.
// EDIT THIS FILE MONTHLY and every page that uses it updates itself.
// Append a new entry to index.history and each complex's priceHistory each month.
window.WFL = {
  verified: "July 2026",          // "last verified from public listings"
  reportMonth: "August 2026",     // current Concession Index month
  index: {
    current: 7.5,                 // avg advertised weeks free across tracked communities
    history: [
      { m: "Aug 2026", v: 7.5 }
    ]
  },
  mortgage: { note: "30-yr fixed near 6.75% \u00b7 5% down \u00b7 verified Jul 2026" },
  complexes: [
    {
      id: "olympus", name: "Olympus Willow Park", area: "Willow Park",
      url: "/complexes/olympus-willow-park", commuteUrl: "/commutes/olympus-willow-park",
      type: "apartment", label: "Apartments",
      beds: { "1": 1148, "2": 1319, "3": 2165 },
      headline: { bed: "1", rent: 1148 },
      weeksFree: 8, leaseMonths: 12, specialNote: "8 weeks free (verify current offer)",
      garage: false, yard: false, gated: false,
      isd: "Aledo / Weatherford ISD \u2014 zone depends on unit address; verify",
      isdConfirmed: false,
      pets: "Welcome \u2014 verify breed policy before applying",
      fees: {},
      priceHistory: [ { m: "Jul 2026", "1": 1148, "2": 1319 } ]
    },
    {
      id: "gates", name: "Gates at Meadow Place", area: "Willow Park",
      url: "/complexes/gates-at-meadow-place", commuteUrl: "/commutes/gates-at-meadow-place",
      type: "apartment", label: "Apartments",
      beds: { "1": 1239, "2": 1328 },
      headline: { bed: "2", rent: 1328 },
      weeksFree: 7, leaseMonths: 12, specialNote: "7 weeks free (verify current offer)",
      garage: false, yard: false, gated: false,
      isd: "Parker County \u2014 verify zoned campus with the district for your unit",
      isdConfirmed: false,
      pets: "Welcome \u2014 verify breed policy before applying",
      fees: {},
      priceHistory: [ { m: "Jul 2026", "1": 1239, "2": 1328 } ]
    },
    {
      id: "canvas", name: "Canvas at Willow Park", area: "Willow Park / Weatherford",
      url: "/complexes/canvas-at-willow-park", commuteUrl: "/commutes/canvas-at-willow-park",
      type: "house", label: "Build-to-rent houses",
      beds: { "2": 2299, "3": 2320, "4": 2799 },
      headline: { bed: "3", rent: 2349 },
      weeksFree: 8, leaseMonths: 14, specialNote: "Up to 8 weeks free \u2014 offers vary by plan & lease length; promo rates appear tied to 14+ month leases",
      garage: true, yard: true, gated: false,
      isd: "Aledo ISD", isdConfirmed: true,
      pets: "Allowed \u2014 $500 fee + $40/mo, 2-pet limit (verify)",
      fees: { app: 125, deposit: 250 },
      priceHistory: [ { m: "Jul 2026", "2": 2299, "3": 2320, "4": 2799 } ]
    },
    {
      id: "willowcrossing", name: "Willow Crossing Townhomes", area: "Willow Park / Aledo",
      url: "/complexes/willow-crossing-townhomes", commuteUrl: "/commutes/willow-crossing-townhomes",
      type: "townhome", label: "Gated townhomes",
      beds: { "3": 2129, "4": 2310 },
      headline: { bed: "3", rent: 2129 },
      weeksFree: 8, leaseMonths: 12, specialNote: "8 weeks free \u201cwhile supplies last\u201d \u2014 confirm the free weeks attach to YOUR unit",
      garage: true, yard: false, gated: true,
      isd: "Aledo ISD", isdConfirmed: true,
      pets: "Allowed \u2014 ~$35/mo pet rent seen in listings (verify)",
      fees: { app: 65, admin: 300 },
      priceHistory: [ { m: "Jul 2026", "3": 2129, "4": 2310 } ]
    }
  ]
};

// Net-effective math used across the site: (rent \u00d7 months \u2212 rent \u00d7 weeks/4.345) \u00f7 months
window.WFL.netEffective = function (rent, weeksFree, months) {
  var gross = rent * months;
  var concession = rent * (weeksFree / 4.345);
  return { gross: gross, concession: concession, effective: (gross - concession) / months, savings: concession };
};
window.WFL.money = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };
