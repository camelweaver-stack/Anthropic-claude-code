// West FW Living — data engine v2.1 (adds weeksHistory, zip, expanded watchlist).
// Verified from public listings July 31, 2026. EDIT MONTHLY; append to histories.
window.WFL = {
 "verified": "July 31, 2026",
 "provenance": {
  "source": "public listings and property websites",
  "verified_date": "2026-07-31",
  "refresh_due": "2026-09-01",
  "confidence": "point-in-time; rents/concessions/fees change without notice",
  "scope": "advertised rent, weeks-free concessions, application/admin/pet fees, lease terms for all tracked communities in this file"
 },
 "reportMonth": "August 2026",
 "index": {
  "current": 7.5,
  "history": [
   {
    "m": "Aug 2026",
    "v": 7.5
   }
  ],
  "note": "Core-4 Willow Park index. Late-July re-verification shows concessions tightening at Canvas (8\u21926 wks on some sources) and Willow Crossing (8\u21924 wks); September captures the move. Expanded 11-community index debuts with the September report.",
  "expandedCurrent": 5.6,
  "expandedN": 11
 },
 "mortgage": {
  "note": "30-yr fixed near 6.75% \u00b7 5% down \u00b7 verified Jul 2026"
 },
 "bah": {
  "effective": "January 1, 2026",
  "mha": "Fort Worth, TX",
  "primary_source": "DoD/DTMO BAH tables (authoritative)",
  "source_url": "https://www.travel.dod.mil/Allowances/Basic-Allowance-for-Housing/BAH-Rate-Lookup/",
  "compiled_from": "public republications of the DTMO 2026 tables",
  "verified_against_primary": false,
  "provenance_note": "OPERATOR: re-check anchors against the DTMO lookup (blocked from build environment 2026-08-24); never extrapolate unlisted grades",
  "anchors": [
   {
    "grade": "E-1\u2013E-4",
    "dep": "without dependents",
    "amt": 1494
   },
   {
    "grade": "E-5",
    "dep": "with dependents",
    "amt": 2118
   },
   {
    "grade": "O-3",
    "dep": "with dependents",
    "amt": 2460
   },
   {
    "grade": "O-4",
    "dep": "with dependents",
    "amt": 2640
   },
   {
    "grade": "O-7+",
    "dep": "with dependents",
    "amt": 2832
   }
  ],
  "notes": "Rates rose 1.4% from 2025; with-dependents rates average ~25% above without. Confirm your exact rate at the DTMO BAH calculator."
 },
 "tax": {
  "year": "2024\u20132025 published rates",
  "rows": [
   {
    "place": "Willow Park (Aledo ISD)",
    "total": 2.091,
    "city": 0.4325,
    "isd": 1.2052,
    "countyEtc": 0.4752
   },
   {
    "place": "Weatherford (Weatherford ISD)",
    "total": 1.902,
    "city": 0.3984,
    "isd": 1.0342,
    "countyEtc": 0.4752
   },
   {
    "place": "Aledo (city, Aledo ISD)",
    "total": 2.056,
    "city": 0.3901,
    "isd": 1.2052,
    "countyEtc": 0.4752
   },
   {
    "place": "Fort Worth in Parker Co. (Aledo ISD)",
    "total": 2.353,
    "city": 0.6725,
    "isd": 1.2052,
    "countyEtc": 0.4752
   }
  ]
 },
 "complexes": [
  {
   "id": "olympus",
   "name": "Olympus Willow Park",
   "area": "Willow Park",
   "areaKey": "willowpark",
   "zip": "76087",
   "address": "180 Crown Pointe Blvd, Willow Park",
   "url": "/complexes/olympus-willow-park",
   "commuteUrl": "/commutes/olympus-willow-park",
   "type": "apartment",
   "label": "Apartments",
   "beds": {
    "1": 1264,
    "2": 1330,
    "3": 1843
   },
   "headline": {
    "bed": "1",
    "rent": 1264
   },
   "weeksFree": 8,
   "weeksHistory": [
    {
     "m": "Jul 2026",
     "v": 8
    },
    {
     "m": "Aug 2026",
     "v": 8
    }
   ],
   "leaseMonths": 12,
   "specialNote": "Listings simultaneously advertise 2\u20138 weeks free \u2014 offer varies by unit and source; get YOUR quote in writing",
   "garage": false,
   "yard": false,
   "gated": false,
   "senior": false,
   "isd": "Aledo / Weatherford ISD \u2014 zone depends on unit address; verify",
   "isdConfirmed": false,
   "pets": "Welcome \u2014 verify breed policy",
   "fees": {},
   "priceHistory": [
    {
     "m": "Jul 2026",
     "1": 1148,
     "2": 1319,
     "3": 2165
    },
    {
     "m": "Aug 2026",
     "1": 1264,
     "2": 1330,
     "3": 1843
    }
   ]
  },
  {
   "id": "gates",
   "name": "Gates at Meadow Place",
   "area": "Willow Park",
   "areaKey": "willowpark",
   "zip": "76087",
   "address": "451 Meadow Place Dr, Willow Park",
   "url": "/complexes/gates-at-meadow-place",
   "commuteUrl": "/commutes/gates-at-meadow-place",
   "type": "apartment",
   "label": "Apartments",
   "beds": {
    "1": 1331,
    "2": 1544,
    "3": 2005
   },
   "headline": {
    "bed": "1",
    "rent": 1331
   },
   "weeksFree": 7,
   "weeksHistory": [
    {
     "m": "Jul 2026",
     "v": 7
    },
    {
     "m": "Aug 2026",
     "v": 7
    }
   ],
   "leaseMonths": 12,
   "specialNote": "Advertised at 4\u20137 weeks free depending on listing source \u2014 confirm the live offer",
   "garage": false,
   "yard": false,
   "gated": false,
   "senior": false,
   "isd": "Parker County \u2014 verify zoned campus for your unit",
   "isdConfirmed": false,
   "pets": "Welcome \u2014 verify breed policy",
   "fees": {},
   "priceHistory": [
    {
     "m": "Jul 2026",
     "1": 1239,
     "2": 1328
    },
    {
     "m": "Aug 2026",
     "1": 1331,
     "2": 1544,
     "3": 2005
    }
   ]
  },
  {
   "id": "canvas",
   "name": "Canvas at Willow Park",
   "area": "Willow Park",
   "areaKey": "willowpark",
   "zip": "76087",
   "address": "300 Meadow Place Dr, Willow Park",
   "url": "/complexes/canvas-at-willow-park",
   "commuteUrl": "/commutes/canvas-at-willow-park",
   "type": "house",
   "label": "Build-to-rent houses",
   "beds": {
    "2": 2299,
    "3": 2321,
    "4": 2799
   },
   "headline": {
    "bed": "3",
    "rent": 2321
   },
   "weeksFree": 6,
   "weeksHistory": [
    {
     "m": "Jul 2026",
     "v": 8
    },
    {
     "m": "Aug 2026",
     "v": 6
    }
   ],
   "leaseMonths": 14,
   "specialNote": "Now advertising 6 weeks free (down from 8 in July) \u2014 promo rates appear tied to longer leases; verify",
   "garage": true,
   "yard": true,
   "gated": false,
   "senior": false,
   "isd": "Aledo ISD",
   "isdConfirmed": true,
   "pets": "Allowed \u2014 $500 fee + $40/mo, 2-pet limit (verify)",
   "fees": {
    "app": 125,
    "deposit": 250
   },
   "priceHistory": [
    {
     "m": "Jul 2026",
     "2": 2299,
     "3": 2320,
     "4": 2799
    },
    {
     "m": "Aug 2026",
     "2": 2299,
     "3": 2321,
     "4": 2799
    }
   ]
  },
  {
   "id": "willowcrossing",
   "name": "Willow Crossing Townhomes",
   "area": "Willow Park / Aledo",
   "areaKey": "willowpark",
   "zip": "76087",
   "address": "Willow Crossing E, Willow Park",
   "url": "/complexes/willow-crossing-townhomes",
   "commuteUrl": "/commutes/willow-crossing-townhomes",
   "type": "townhome",
   "label": "Gated townhomes",
   "beds": {
    "3": 2222,
    "4": 2302
   },
   "headline": {
    "bed": "3",
    "rent": 2222
   },
   "weeksFree": 4,
   "weeksHistory": [
    {
     "m": "Jul 2026",
     "v": 8
    },
    {
     "m": "Aug 2026",
     "v": 4
    }
   ],
   "leaseMonths": 12,
   "specialNote": "Now advertising 4 weeks free (down from 8 in July) \u2014 supply-limited offers shrink as units fill; confirm yours",
   "garage": true,
   "yard": false,
   "gated": true,
   "senior": false,
   "isd": "Aledo ISD",
   "isdConfirmed": true,
   "pets": "Allowed \u2014 ~$35/mo pet rent seen in listings (verify)",
   "fees": {
    "app": 65,
    "admin": 300
   },
   "priceHistory": [
    {
     "m": "Jul 2026",
     "3": 2129,
     "4": 2310
    },
    {
     "m": "Aug 2026",
     "3": 2222,
     "4": 2302
    }
   ]
  },
  {
   "id": "olympushudson",
   "name": "Olympus Hudson Oaks",
   "area": "Hudson Oaks",
   "areaKey": "hudsonoaks",
   "zip": "76087",
   "address": "900 Cinema Dr, Hudson Oaks",
   "url": "/complexes/olympus-hudson-oaks",
   "commuteUrl": "/commutes/olympus-hudson-oaks",
   "type": "apartment",
   "label": "Apartments",
   "beds": {
    "1": 1162,
    "2": 1423,
    "3": 1827
   },
   "headline": {
    "bed": "1",
    "rent": 1162
   },
   "weeksFree": 8,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 8
    }
   ],
   "leaseMonths": 12,
   "specialNote": "8 weeks free advertised \u2014 active lease-up; sibling community to Olympus Willow Park",
   "garage": false,
   "yard": false,
   "gated": false,
   "senior": false,
   "isd": "Verify zoned district and campus for your unit (Weatherford / Aledo ISD boundary area)",
   "isdConfirmed": false,
   "pets": "Welcome \u2014 verify breed policy",
   "fees": {},
   "priceHistory": [
    {
     "m": "Aug 2026",
     "1": 1162,
     "2": 1423,
     "3": 1827
    }
   ]
  },
  {
   "id": "birchway",
   "name": "Birchway Hudson Oaks",
   "area": "Hudson Oaks",
   "areaKey": "hudsonoaks",
   "zip": "76087",
   "address": "150 Inspiration Dr, Hudson Oaks",
   "url": "/complexes/birchway-hudson-oaks",
   "commuteUrl": "/commutes/birchway-hudson-oaks",
   "type": "apartment",
   "label": "Apartments",
   "beds": {
    "1": 1165,
    "2": 1497
   },
   "headline": {
    "bed": "1",
    "rent": 1165
   },
   "weeksFree": 8,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 8
    }
   ],
   "leaseMonths": 12,
   "specialNote": "8 weeks free advertised; listed 1BR pricing ranges $1,165\u2013$1,458 across sources \u2014 a fine-print flag: confirm the rate the special attaches to",
   "garage": false,
   "yard": false,
   "gated": false,
   "senior": false,
   "isd": "Verify zoned district and campus for your unit",
   "isdConfirmed": false,
   "pets": "Welcome \u2014 verify breed policy",
   "fees": {},
   "priceHistory": [
    {
     "m": "Aug 2026",
     "1": 1165,
     "2": 1497
    }
   ]
  },
  {
   "id": "oxford",
   "name": "Oxford at Weatherford",
   "area": "Weatherford",
   "areaKey": "weatherford",
   "zip": "76087",
   "address": "209 W Interstate 20, Weatherford",
   "url": "/complexes/oxford-at-weatherford",
   "commuteUrl": "/commutes/oxford-at-weatherford",
   "type": "apartment",
   "label": "Apartments",
   "beds": {
    "1": 1115
   },
   "headline": {
    "bed": "1",
    "rent": 1115
   },
   "weeksFree": 8.7,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 8.7
    }
   ],
   "leaseMonths": 12,
   "specialNote": "\u201c2 months free\u201d advertised \u2014 the deepest headline concession we track; confirm lease-length requirements and which months the free rent lands in",
   "garage": false,
   "yard": false,
   "gated": false,
   "senior": false,
   "isd": "Weatherford ISD area \u2014 verify campus",
   "isdConfirmed": false,
   "pets": "Verify pet policy",
   "fees": {},
   "priceHistory": [
    {
     "m": "Aug 2026",
     "1": 1115
    }
   ]
  },
  {
   "id": "collegepark",
   "name": "College Park",
   "area": "Weatherford",
   "areaKey": "weatherford",
   "zip": "76087",
   "address": "202 College Park Dr, Weatherford",
   "url": "/complexes/college-park-weatherford",
   "commuteUrl": "/commutes/college-park-weatherford",
   "type": "apartment",
   "label": "Apartments",
   "beds": {
    "1": 900,
    "2": 1200
   },
   "headline": {
    "bed": "1",
    "rent": 900
   },
   "weeksFree": 0,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 0
    }
   ],
   "leaseMonths": 12,
   "specialNote": "No weeks-free special advertised \u2014 competes on base rent instead; the lowest advertised 1BR we track",
   "garage": false,
   "yard": false,
   "gated": false,
   "senior": false,
   "isd": "Weatherford ISD area \u2014 verify campus",
   "isdConfirmed": false,
   "pets": "Verify pet policy",
   "fees": {},
   "priceHistory": [
    {
     "m": "Aug 2026",
     "1": 900,
     "2": 1200
    }
   ]
  },
  {
   "id": "preserve",
   "name": "Preserve at Willow Park (55+)",
   "area": "Willow Park",
   "areaKey": "willowpark",
   "zip": "76087",
   "address": "149 Mary Lou Dr, Willow Park",
   "url": "/complexes/preserve-at-willow-park",
   "commuteUrl": "/commutes/preserve-at-willow-park",
   "type": "apartment",
   "label": "Active 55+ apartments",
   "beds": {
    "1": 1444,
    "2": 2248
   },
   "headline": {
    "bed": "1",
    "rent": 1444
   },
   "weeksFree": 6,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 6
    }
   ],
   "leaseMonths": 12,
   "specialNote": "6 weeks free advertised \u2014 age-qualified community (55+); the only senior-living option we track in the pocket",
   "garage": false,
   "yard": false,
   "gated": false,
   "senior": true,
   "isd": "N/A (age-qualified community)",
   "isdConfirmed": false,
   "pets": "Verify pet policy",
   "fees": {},
   "priceHistory": [
    {
     "m": "Aug 2026",
     "1": 1444,
     "2": 2248
    }
   ]
  },
  {
   "id": "westpoint",
   "name": "Westpoint at Scenic Vista",
   "area": "West Fort Worth (76108)",
   "areaKey": "westfw",
   "zip": "76108",
   "address": "1200 Scenic Vista Dr, Fort Worth",
   "url": "/complexes/westpoint-at-scenic-vista",
   "commuteUrl": "/commutes/westpoint-at-scenic-vista",
   "type": "apartment",
   "label": "Apartments",
   "beds": {
    "1": 1191,
    "2": 1512
   },
   "headline": {
    "bed": "1",
    "rent": 1191
   },
   "weeksFree": 6,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 6
    }
   ],
   "leaseMonths": 12,
   "specialNote": "6 weeks free advertised \u2014 1,017 sq ft one-bedrooms are unusually large for the price; minutes from Lockheed and NAS JRB",
   "garage": false,
   "yard": false,
   "gated": false,
   "senior": false,
   "isd": "White Settlement ISD area \u2014 verify campus",
   "isdConfirmed": false,
   "pets": "Welcome \u2014 verify breed policy",
   "fees": {},
   "priceHistory": [
    {
     "m": "Aug 2026",
     "1": 1191,
     "2": 1512
    }
   ]
  },
  {
   "id": "chapelcreek",
   "name": "Chapel Creek Cottages",
   "area": "West Fort Worth",
   "areaKey": "westfw",
   "zip": "76108",
   "address": "Chapel Creek area, west Fort Worth",
   "url": "/complexes/chapel-creek-cottages",
   "commuteUrl": "/commutes/chapel-creek-cottages",
   "type": "cottage",
   "label": "Cottage rentals, gated",
   "beds": {
    "2": 2025,
    "3": 2285
   },
   "headline": {
    "bed": "2",
    "rent": 2025
   },
   "weeksFree": 0,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 0
    }
   ],
   "leaseMonths": 12,
   "specialNote": "No weeks-free special advertised \u2014 gated cottage-style community; the west-FW alternative to the Willow Park build-to-rent products",
   "garage": false,
   "yard": true,
   "gated": true,
   "senior": false,
   "isd": "Verify zoned district and campus for your unit",
   "isdConfirmed": false,
   "pets": "Verify pet policy",
   "fees": {},
   "priceHistory": [
    {
     "m": "Aug 2026",
     "2": 2025,
     "3": 2285
    }
   ]
  }
 ],
 "watchlist": [
  {
   "name": "Highland Terrace Apartments",
   "area": "Weatherford",
   "note": "2BR advertised from ~$995 in spring-2026 listings \u2014 re-verification pending"
  },
  {
   "name": "Lone Oak Apartments",
   "area": "Weatherford",
   "note": "1BR advertised from ~$1,105 in spring-2026 listings \u2014 re-verification pending"
  },
  {
   "name": "Stone Lake Townhomes",
   "area": "Weatherford",
   "note": "Townhomes advertised from ~$2,100 in spring-2026 listings \u2014 re-verification pending"
  },
  {
   "name": "The Residences of Holland Lake",
   "area": "Weatherford (76086)",
   "note": "1BR from ~$1,189, 2BR ~$1,399 in current listings \u2014 full verification pending"
  },
  {
   "name": "Fox Hollow Townhomes",
   "area": "Weatherford (76086)",
   "note": "3\u20134BR townhomes from ~$1,450 in current listings \u2014 the value townhome flag of the corridor; verification pending"
  },
  {
   "name": "Woodhaven Villas",
   "area": "Weatherford (76086)",
   "note": "3BR from ~$1,495 in current listings \u2014 verification pending"
  },
  {
   "name": "Cypress View Villas",
   "area": "Weatherford (76086)",
   "note": "2BR ~$1,282 / 3BR ~$1,446 in current listings \u2014 verification pending"
  },
  {
   "name": "Meadow Vista",
   "area": "Weatherford area",
   "note": "Spotted in proximity listings \u2014 verification pending"
  },
  {
   "name": "Residences at Holly Oaks",
   "area": "Weatherford area",
   "note": "Spotted in proximity listings \u2014 verification pending"
  }
 ]
};
window.WFL.netEffective=function(r,w,m){var g=r*m,c=r*(w/4.345);return{gross:g,concession:c,savings:c,effective:(g-c)/m};};
window.WFL.money=function(n){return "$"+Math.round(n).toLocaleString("en-US");};
