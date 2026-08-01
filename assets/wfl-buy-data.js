// West FW Living — buyer-side data engine v1 (sibling to wfl-data.js).
// Verified from builder pages, official community docs & industry tracking, July 31, 2026.
// UPDATE MONTHLY with each Builder Report: rates, incentives, append to index.history.
window.WFLBUY = {
 "verified": "July 31, 2026",
 "rates": {
  "resale30": 6.75,
  "resaleNote": "30-yr fixed, Freddie Mac PMMS range, verified Jul 2026 \u2014 update monthly with the Builder Report",
  "builderAdvertised": 4.99,
  "builderNote": "Lowest widely-advertised builder buydown rates in the corridor, spring\u2013summer 2026, via builders' preferred lenders; terms and qualification vary"
 },
 "insuranceMonthlyPer100k": 60,
 "index": {
  "current": 32500,
  "pctOfBase": 4.5,
  "history": [
   {
    "m": "Aug 2026",
    "v": 32500
   }
  ],
  "note": "Debut reading. Anchored on Walsh's advertised $25K\u2013$40K flex-cash range (midpoint $32,500, \u22484.5% of a midpoint base price); corridor-wide evidence base runs $10K\u2013$40K, and roughly 70% of DFW new-home sales now include structured incentives per industry tracking. The tracked-community set expands as more builders publish hard numbers."
 },
 "communities": [
  {
   "id": "walsh",
   "name": "Walsh",
   "area": "Fort Worth (Aledo ISD)",
   "url": "/buy/new-construction/walsh",
   "priceLow": 550000,
   "priceHigh": 950000,
   "priceNote": "production homes; custom/estate $1M+",
   "taxRate": 2.689,
   "taxNote": "Official published total incl. PID; PID assessment \u2248$0.36/$100 (planning areas 1\u20133 \u2248$0.18) \u2014 the PID rate doubled from $0.18 in 2026",
   "pid": true,
   "isd": "Aledo ISD",
   "city": "Fort Worth city limits (Tarrant & Parker counties)",
   "hoaNote": "HOA + lifestyle program \u2014 verify current dues",
   "incentive": {
    "low": 25000,
    "high": 40000,
    "note": "\u201cFlex cash\u201d $25K\u2013$40K advertised spring 2026 \u2014 usable toward rate buydown, closing costs, or design credits; typically requires builder's preferred lender"
   }
  },
  {
   "id": "morningstar",
   "name": "Morningstar",
   "area": "Aledo (Aledo ISD)",
   "url": "/buy/new-construction/aledo",
   "priceLow": 360990,
   "priceHigh": 547255,
   "priceNote": "multi-builder: D.R. Horton from $360,990; Riverside $420K\u2013$547K; Trophy Signature also active; community median \u2248$443K",
   "taxRate": 2.06,
   "taxNote": "Aledo-area combined rate basis \u2014 portions of the community may differ; verify the exact taxing units for a specific lot",
   "pid": false,
   "isd": "Aledo ISD (listings cite Lynn McKinney Elem \u2192 McAnally \u2192 Aledo HS \u2014 verify per lot)",
   "city": "Aledo / Parker County",
   "hoaNote": "HOA with amenity center \u2014 verify current dues",
   "incentive": {
    "low": null,
    "high": null,
    "note": "National-builder rate promotions advertised (D.R. Horton financing promos running through 2026); hard dollar values not published \u2014 ask each builder for the current package in writing"
   }
  },
  {
   "id": "parksofaledo",
   "name": "Parks of Aledo",
   "area": "Aledo (Aledo ISD)",
   "url": "/buy/new-construction/aledo",
   "priceLow": null,
   "priceHigh": null,
   "priceNote": "Active phases (Parks of Aledo, Bluffs) \u2014 phase pricing varies; verify current releases",
   "taxRate": 2.06,
   "taxNote": "Aledo-area basis \u2014 verify per lot",
   "pid": false,
   "isd": "Aledo ISD",
   "city": "Aledo / Parker County",
   "hoaNote": "Verify current dues",
   "incentive": {
    "low": null,
    "high": null,
    "note": "Varies by builder and phase \u2014 request in writing"
   }
  },
  {
   "id": "wpho",
   "name": "Willow Park / Hudson Oaks actives",
   "area": "Parker County I-20 corridor",
   "url": "/buy/new-construction/willow-park-hudson-oaks",
   "priceLow": null,
   "priceHigh": null,
   "priceNote": "Smaller actives (e.g., Bear Creek Estates by Remington in the Aledo 76008 area) plus the permit pipeline \u2014 see the tracker",
   "taxRate": 2.09,
   "taxNote": "Willow Park\u2013Aledo ISD basis where applicable \u2014 verify per address",
   "pid": false,
   "isd": "Aledo / Weatherford ISD by location",
   "city": "Willow Park / Hudson Oaks",
   "hoaNote": "Varies",
   "incentive": {
    "low": null,
    "high": null,
    "note": "Smaller builders negotiate case-by-case \u2014 which cuts both ways"
   }
  }
 ]
};
window.WFLBUY.piti=function(price,ratePct,downPct,taxRatePct,insPer100k,hoaMo){
 var loan=price*(1-downPct/100), r=ratePct/100/12, n=360;
 var pi=r>0? loan*r/(1-Math.pow(1+r,-n)) : loan/n;
 var tax=price*taxRatePct/100/12, ins=price/100000*insPer100k;
 return {pi:pi,tax:tax,ins:ins,hoa:hoaMo||0,total:pi+tax+ins+(hoaMo||0),loan:loan};};
