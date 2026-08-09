// West FW Living — decision-engine match data, built for /where-to-live.html.
// Sourced from the site's own verified commute tables (commutes/*.html), tax/price
// posture (assets/wfl-compare-data.js) and hard new-construction pricing
// (assets/wfl-buy-data.js) where those exist. Fields marked "est." below were not
// published elsewhere on the site and are editorial estimates derived from the
// site's existing descriptive copy (e.g. "12-20 min to the plant", "add ~5 min vs
// Willow Park") — verify against current listings/mapping before this goes live,
// and re-check lifestyle scores (1-5, subjective) against local knowledge.
window.WFL_MATCH = {
 communities: [
  {
   name: "Willow Park",
   url: "/buy/rent-or-buy-willow-park",
   note: "The corridor's newest retail center plus a full medical cluster — a small city that added a downtown in one stroke.",
   priceLow: 350000, priceHigh: 500000,
   school: "aledo",
   homeTypes: ["new", "resale"],
   commute: { lockheed: 22, nas: 24, downtown: 30, medical: 26 }, // lockheed/nas/downtown sourced from commutes/olympus-willow-park.html; medical est.
   trails: 2, pool: 3, retail: 5, space: 2, value: 3, lowTax: 2, smallTown: 2
  },
  {
   name: "Hudson Oaks",
   url: "/buy/new-construction/willow-park-hudson-oaks",
   note: "The no-frills, low-tax retail spine just west of Willow Park — commercial corridor up front, quiet streets behind it.",
   priceLow: 325000, priceHigh: 475000, // est. — compare-data.js: "often undercuts Willow Park like-for-like"
   school: "weatherford",
   homeTypes: ["resale", "new"],
   commute: { lockheed: 24, nas: 26, downtown: 32, medical: 28 }, // lockheed/nas/downtown sourced from commutes/olympus-hudson-oaks.html; medical est.
   trails: 2, pool: 2, retail: 4, space: 2, value: 4, lowTax: 5, smallTown: 3
  },
  {
   name: "Aledo",
   url: "/guides/living-in-aledo",
   note: "The small-town-with-the-schools identity — Aledo ISD throughout, and Friday nights are a civic event.",
   priceLow: 350000, priceHigh: 500000,
   school: "aledo",
   homeTypes: ["new", "resale"],
   commute: { lockheed: 27, nas: 29, downtown: 30, medical: 27 }, // downtown sourced from guides/living-in-aledo.html FAQ (25-35 min); lockheed/nas/medical est. from "+5 min vs Willow Park"
   trails: 4, pool: 2, retail: 3, space: 3, value: 3, lowTax: 3, smallTown: 5
  },
  {
   name: "Weatherford",
   url: "/buy/rent-or-buy-weatherford",
   note: "A real county-seat city — full services, history, and the price relief that distance buys.",
   priceLow: 275000, priceHigh: 500000, // est. — compare-data.js: "corridor's lowest entry prices; full spread from historic to new"
   school: "weatherford",
   homeTypes: ["new", "resale"],
   commute: { lockheed: 29, nas: 31, downtown: 36, medical: 33 }, // lockheed/nas/downtown sourced from commutes/oxford-at-weatherford.html; medical est.
   trails: 2, pool: 2, retail: 3, space: 4, value: 5, lowTax: 5, smallTown: 4
  },
  {
   name: "Benbrook",
   url: "/areas/benbrook",
   note: "The lake-country value case: Fort Worth proximity without Fort Worth pricing.",
   priceLow: 325000, priceHigh: 550000, // est. — compare-data.js: "value play ... under comparable FW neighborhoods"
   school: "other",
   homeTypes: ["resale"],
   commute: { lockheed: 16, nas: 19, downtown: 20, medical: 15 }, // lockheed sourced from areas/benbrook.html (12-20 min); nas/downtown/medical est. ("shortest FW commutes on this list")
   trails: 5, pool: 2, retail: 2, space: 3, value: 4, lowTax: 3, smallTown: 3
  },
  {
   name: "Walsh",
   url: "/guides/living-in-walsh",
   note: "The full-ecosystem flagship — the plan IS the product. Highest tax stack on this list; the amenities are what it buys.",
   priceLow: 550000, priceHigh: 950000,
   school: "aledo",
   homeTypes: ["new"],
   commute: { lockheed: 20, nas: 22, downtown: 28, medical: 22 }, // medical (Clearfork) sourced from guides/living-in-walsh.html (20-25 min); lockheed/nas/downtown est. from "best-positioned master plan for FW jobs"
   trails: 3, pool: 5, retail: 5, space: 2, value: 1, lowTax: 1, smallTown: 2
  },
  {
   name: "Morningstar",
   url: "/neighborhoods/morningstar",
   note: "The established, resale-deep alternative to Walsh — less spectacle, more house per dollar.",
   priceLow: 360990, priceHigh: 547255,
   school: "aledo",
   homeTypes: ["new", "resale"],
   commute: { lockheed: 24, nas: 26, downtown: 32, medical: 28 }, // est. — "north of I-20", ~10 min to both Willow Park's District and Aledo's core
   trails: 2, pool: 3, retail: 2, space: 3, value: 4, lowTax: 3, smallTown: 3
  },
  {
   name: "Parks of Aledo",
   url: "/neighborhoods/parks-of-aledo",
   note: "The trails-first plan — about six miles of maintained greenbelt trails, real infrastructure with its own constituency.",
   priceLow: 350000, priceHigh: 500000, // est. — wfl-buy-data.js lists this community's own pricing as null ("phase pricing varies"); using in-town Aledo new-construction band
   school: "aledo",
   homeTypes: ["new", "resale"],
   commute: { lockheed: 27, nas: 29, downtown: 30, medical: 27 }, // est. — "in-town Aledo" per compare-data.js, treated as equivalent to Aledo
   trails: 5, pool: 2, retail: 2, space: 2, value: 3, lowTax: 3, smallTown: 4
  }
 ]
};
