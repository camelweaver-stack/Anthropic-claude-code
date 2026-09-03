// West FW Living — data engine v2.1 (adds weeksHistory, zip, expanded watchlist).
// Verified from public listings September 3, 2026. EDIT MONTHLY; append to histories.
window.WFL = {
 "verified": "September 3, 2026",
 "provenance": {
  "source": "public listings and property websites",
  "verified_date": "2026-09-03",
  "refresh_due": "2026-10-01",
  "confidence": "point-in-time; rents/concessions/fees change without notice",
  "scope": "advertised rent, weeks-free concessions, application/admin/pet fees, lease terms for all tracked communities in this file"
 },
 "reportMonth": "September 2026",
 "index": {
  "current": 4.0,
  "history": [
   {
    "m": "Aug 2026",
    "v": 7.5
   },
   {
    "m": "Sep 2026",
    "v": 4.0
   }
  ],
  "note": "Core-4 Willow Park index fell 7.5\u21924.0 in one month \u2014 Olympus cut 8\u21922 weeks, Gates 7\u21924, and Oxford's \u201c2 months free\u201d vanished entirely. The deep offers migrated west: Birchway and Chapel Creek Cottages now carry the 8-week flags. Expanded 11-community index debuts this month at 4.4.",
  "expandedCurrent": 4.4,
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
    "1": 1425,
    "2": 1579
   },
   "headline": {
    "bed": "1",
    "rent": 1425
   },
   "weeksFree": 2,
   "weeksHistory": [
    {
     "m": "Jul 2026",
     "v": 8
    },
    {
     "m": "Aug 2026",
     "v": 8
    },
    {
     "m": "Sep 2026",
     "v": 2
    }
   ],
   "leaseMonths": 12,
   "specialNote": "Sept re-verification: \u201c2 Weeks Free on Select Units\u201d on the price-verified listing (Sep 3), while stale search snippets still say \u201cup to 8 weeks\u201d \u2014 the deep-offer era here looks over; get YOUR quote in writing. 3BR pricing not listed this cycle",
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
    },
    {
     "m": "Sep 2026",
     "1": 1425,
     "2": 1579
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
    "1": 1412
   },
   "headline": {
    "bed": "1",
    "rent": 1412
   },
   "weeksFree": 4,
   "weeksHistory": [
    {
     "m": "Jul 2026",
     "v": 7
    },
    {
     "m": "Aug 2026",
     "v": 7
    },
    {
     "m": "Sep 2026",
     "v": 4
    }
   ],
   "leaseMonths": 12,
   "specialNote": "4 weeks free on select units per current listings (down from 7 in Aug); the property's own site shows no banner \u2014 confirm the live offer. 2\u20133BR pricing not re-verified this cycle",
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
    },
    {
     "m": "Sep 2026",
     "1": 1412
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
    "2": 2299
   },
   "headline": {
    "bed": "2",
    "rent": 2299
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
    },
    {
     "m": "Sep 2026",
     "v": 6
    }
   ],
   "leaseMonths": 14,
   "specialNote": "Up to 6 weeks free on 13\u201315 month leases; offers vary by floor plan. 8 homes listed $2,299\u2013$2,699 (2\u20134BR); per-plan pricing beyond the $2,299 start not broken out this cycle",
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
    },
    {
     "m": "Sep 2026",
     "2": 2299
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
    "3": 2475
   },
   "headline": {
    "bed": "3",
    "rent": 2475
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
    },
    {
     "m": "Sep 2026",
     "v": 4
    }
   ],
   "leaseMonths": 12,
   "specialNote": "\u201cUp to 4 weeks free \u2014 restrictions apply\u201d (price-verified Sep 3). Rents jumped: 3BR now from $2,475 vs $2,222 in Aug; one stale listing still shows 8 weeks \u2014 trust the dated quote. Range $2,475\u2013$2,627 across 3\u20134BR",
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
    },
    {
     "m": "Sep 2026",
     "3": 2475
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
    "1": 1267,
    "2": 1594
   },
   "headline": {
    "bed": "1",
    "rent": 1267
   },
   "weeksFree": 6,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 8
    },
    {
     "m": "Sep 2026",
     "v": 6
    }
   ],
   "leaseMonths": 12,
   "specialNote": "\u201cUp to 6 Weeks Free on Select Units\u201d (down from 8 in Aug), price-verified Sep 3. 3BR pricing not listed this cycle",
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
    },
    {
     "m": "Sep 2026",
     "1": 1267,
     "2": 1594
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
    "1": 1378,
    "2": 1708
   },
   "headline": {
    "bed": "1",
    "rent": 1378
   },
   "weeksFree": 8,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 8
    },
    {
     "m": "Sep 2026",
     "v": 8
    }
   ],
   "leaseMonths": 12,
   "specialNote": "\u201cUp to 8 Weeks Base Rent Free!\u201d \u2014 now the deepest advertised offer we track; price-verified Sep 3. Stickers rose with it ($1,378 1BR / $1,708 2BR vs $1,165/$1,497 in Aug) \u2014 run the effective-rent math, not the banner",
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
    },
    {
     "m": "Sep 2026",
     "1": 1378,
     "2": 1708
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
    "1": 1284,
    "2": 1647
   },
   "headline": {
    "bed": "1",
    "rent": 1284
   },
   "weeksFree": 0,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 8.7
    },
    {
     "m": "Sep 2026",
     "v": 0
    }
   ],
   "leaseMonths": 12,
   "specialNote": "No rent specials advertised as of Sep 3 \u2014 August's \u201c2 months free\u201d is gone and the 1BR sticker rose $169. If you toured in August, requote everything before signing",
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
    },
    {
     "m": "Sep 2026",
     "1": 1284,
     "2": 1647
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
    "2": 1200
   },
   "headline": {
    "bed": "2",
    "rent": 1200
   },
   "weeksFree": 0,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 0
    },
    {
     "m": "Sep 2026",
     "v": 0
    }
   ],
   "leaseMonths": 12,
   "specialNote": "No specials \u2014 competes on base rent: 2BR from $1,200 standard / $1,300 remodeled (price-verified Sep 3); 1BR pricing not listed this cycle. 3.5x income requirement; 6\u201313 month leases (short terms may carry fees)",
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
    },
    {
     "m": "Sep 2026",
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
    "1": 1255
   },
   "headline": {
    "bed": "1",
    "rent": 1255
   },
   "weeksFree": 4.3,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 6
    },
    {
     "m": "Sep 2026",
     "v": 4.3
    }
   ],
   "leaseMonths": 12,
   "specialNote": "\u201c1 Month Free for eligible applicants\u201d (\u22484.3 wks); units from $1,255 \u2014 listed starting rent down from $1,444 in Aug. Age-qualified 55+ community; 2BR pricing not re-verified this cycle",
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
    },
    {
     "m": "Sep 2026",
     "1": 1255
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
    "1": 1299
   },
   "headline": {
    "bed": "1",
    "rent": 1299
   },
   "weeksFree": 6,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 6
    },
    {
     "m": "Sep 2026",
     "v": 6
    }
   ],
   "leaseMonths": 12,
   "specialNote": "6 weeks free PLUS no application fee (one source frames it as a \u201cLook & Lease\u201d prorated on 12-month terms); the property's own specials page confirms active offers Sep 3 but posts details as images \u2014 call for exact terms. Listed range $1,299\u2013$1,649 (1\u20132BR)",
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
    },
    {
     "m": "Sep 2026",
     "1": 1299
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
    "1": 1530
   },
   "headline": {
    "bed": "1",
    "rent": 1530
   },
   "weeksFree": 8,
   "weeksHistory": [
    {
     "m": "Aug 2026",
     "v": 0
    },
    {
     "m": "Sep 2026",
     "v": 8
    }
   ],
   "leaseMonths": 12,
   "specialNote": "NEW: \u201cGet Up to 8 Weeks FREE \u2014 restrictions apply\u201d \u2014 this community advertised no concession in August; the deep-offer cluster has moved west. Listed range $1,530\u2013$1,999 across 1\u20133BR floor plans ($1,530 is the range floor); per-plan pricing not broken out this cycle",
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
    },
    {
     "m": "Sep 2026",
     "1": 1530
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
