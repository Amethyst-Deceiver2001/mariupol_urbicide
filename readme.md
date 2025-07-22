# Mariupol Administrative Violence Documentation Project

## Self-Reported Urbicide: How Occupiers Document Their Own War Crimes

In an unprecedented documentation effort, this project tracks how Russian occupation authorities in Mariupol systematically record their own property seizures and demolitions - creating a comprehensive digital paper trail of administrative violence that continues long after the siege ended.

**The Innovation**: While most war crimes investigations struggle to find evidence, Russian bureaucrats are methodically publishing thousands of property seizure orders, demolition decrees, and redistribution documents on official websites. We've built an automated pipeline to collect, verify, and map this self-incriminating evidence according to international legal standards.

## The Problem: Lawfare After Kinetic Warfare

The destruction of Mariupol didn't end with military surrender. Russian authorities now deploy **administrative violence** - using legal procedures and bureaucratic processes as weapons to permanently dispossess Ukrainian survivors. Our investigation reveals two distinct pathways:

### Path 1: Strategic Demolition (Nakhimova 82 Case)
A damaged but structurally intact 3-story building was mysteriously demolished in late 2022 without explanation. A year later, luxury condos appeared on the same spot - but with a completely different address (Chernomorsky Lane 1B instead of Nakhimova Avenue 82). Original residents cannot prove ownership when the address itself has been erased from existence.

### Path 2: Mass Clearance (Left Bank Quarter)
An entire dense residential neighborhood between Azovstal'ska and Morskoy Boulevard - home to thousands - was bulldozed to empty ground after sustaining damage. The area remains vacant, with no reconstruction plans for displaced residents.

**Both pathways achieve the same goal**: permanent dispossession through administrative manipulation while maintaining a veneer of legal process.

## Methodology: AI-Powered Investigation with Legal-Grade Standards

### The Research Brain: Claude Opus 4.0
Strategic research, pattern recognition, and complex analysis of international law precedents, funding opportunities, and methodological frameworks. Claude handles the big-picture synthesis that would take weeks of manual research.

### The Development Brain: Windsurf + ChatGPT 4.1
Granular debugging, code optimization, and technical problem-solving. This combination eliminates the cyclical debugging issues that plague complex geospatial projects while maintaining rapid development velocity.

### The Evidence Pipeline: Python + Docker + PostgreSQL
```
Russian Official Websites → PyMuPDF/OCR → Address Extraction → 
Geospatial Matching → PostgreSQL Database → QGIS Visualization → 
Legal Documentation → Audit Trail Generation
```

**Core Technical Components:**
- **PyMuPDF + Tesseract**: Extract text from Russian-language property seizure PDFs
- **RapidFuzz**: 350x faster address matching for conflict zone data
- **PostgreSQL/PostGIS**: Spatial database for correlating addresses with satellite imagery
- **QGIS**: Professional cartographic visualization for legal presentations
- **Berkeley Protocol Compliance**: Every document cryptographically hashed and audit-trailed

### Data Sources Integration
- **Official occupation websites** (doc.dnronline.su, ginspadnr.ru): Source of self-incriminating evidence
- **UNOSAT damage datasets**: Authoritative building destruction verification
- **OpenStreetMap historical data**: Pre-war baseline for address validation
- **Sentinel-2 satellite imagery**: Zero-cost temporal analysis for construction monitoring

## Administrative Pathways: Visual Documentation

The following flowchart illustrates the two distinct pathways through which Russian occupation authorities systematically dispossess Ukrainian property owners while maintaining documentary evidence of their crimes:

```
ADMINISTRATIVE PATHWAYS OF PROPERTY DISPOSSESSION IN OCCUPIED MARIUPOL
═══════════════════════════════════════════════════════════════════════

             ┌─────────────────────────────────┐
             │   Damaged or Destroyed Building │
             │         (Post-Invasion)         │
             └────────────────┬────────────────┘
                              │
             ┌────────────────▼────────────────┐
             │  Administrative Assessment by   │
             │     Occupation Authorities      │
             └────────────────┬────────────────┘
                              │
           ┌──────────────────┴──────────────────┐
           │                                     │
PATH 1: SELECTIVE DEMOLITION          PATH 2: MASS CLEARANCE
(Nakhimova 82 Case)                   (Left Bank Quarter Case)
           │                                     │
┌──────────▼───────────┐             ┌───────────▼───────────┐
│ Damaged but intact   │             │ Dense residential     │
│ 3-story building     │             │ neighborhood with     │
│                      │             │ ~30 apartment blocks  │
└──────────┬───────────┘             └───────────┬───────────┘
           │                                     │
┌──────────▼───────────┐             ┌───────────▼───────────┐
│ Demolition decree    │             │ Systematic clearing   │
│ issued without       │             │ operations begin      │
│ explanation          │             │                       │
└──────────┬───────────┘             └───────────┬───────────┘
           │                                     │
┌──────────▼───────────┐             ┌───────────▼───────────┐
│ Building demolished  │             │ Complete bulldozing   │
│ (late 2022)          │             │ of all structures     │
│                      │             │                       │
└──────────┬───────────┘             └───────────┬───────────┘
           │                                     │
┌──────────▼───────────┐             ┌───────────▼───────────┐
│ New luxury condos    │             │ Area remains empty    │
│ built on same spot   │             │ cleared lot with      │
│                      │             │ no reconstruction     │
└──────────┬───────────┘             └───────────┬───────────┘
           │                                     │
┌──────────▼───────────┐             ┌───────────▼───────────┐
│ NEW ADDRESS:         │             │ MASS DISPLACEMENT:    │
│ Chernomorsky Lane 1B │             │ Hundreds of families  │
│ (not Nakhimova 82)   │             │ permanently displaced │
└──────────┬───────────┘             └───────────┬───────────┘
           │                                     │
           └──────────────────┬──────────────────┘
                              │
             ┌────────────────▼────────────────┐
             │          COMMON RESULT:         │
             │                                 │
             │   Original residents lose all   │
             │     property claims through     │
             │   administrative manipulation   │
             └─────────────────────────────────┘

KEY DISTINCTIONS:
─────────────────
PATH 1: Individual building → Strategic demolition → Premium redevelopment → Address change
PATH 2: Entire neighborhood → Mass destruction → Land banking → No reconstruction

LEGAL IMPLICATIONS:
──────────────────
• Both pathways constitute PILLAGE under Rome Statute Article 8(2)(b)(xvi)
• Both create systematic barriers to property restitution
• Both generate self-incriminating documentary evidence via official decrees
• Both demonstrate ADMINISTRATIVE VIOLENCE as continuation of kinetic warfare

EVIDENCE TRAIL:
──────────────
Each pathway generates traceable documentation on official occupation websites:
- Demolition orders with specific addresses and dates
- Property seizure notices with legal justifications  
- Construction permits showing new developments
- Address reassignment records severing legal continuity
```

## Key Findings: Systematic Documentation of Systematic Crimes

**Scale**: Over 12.000 documented property seizures with complete paper trails leading to specific Russian officials who signed each order.

**Geographic Patterns**: Premium locations (sea views, central districts) systematically targeted, suggesting economic rather than security motivations.

**Legal Innovation**: Each red dot on our maps corresponds to a specific war crime with a specific perpetrator - creating unprecedented command responsibility documentation.

**Temporal Evidence**: Multi-year timeline showing administrative violence continuing long after military operations, demonstrating systematic rather than opportunistic behavior.

## The Bureaucratic Paradox

The most fascinating aspect: **Russian authorities cannot stop documenting their crimes**. Bureaucratic systems require documentation to function, but this same documentation becomes the evidence for war crimes prosecution. From Nazi Holocaust records to contemporary digital surveillance, perpetrators consistently create comprehensive paper trails of their own atrocities.

This compulsion to document - what we call "administrative confabulation" - provides investigators with unprecedented evidence quality while revealing the psychological and structural forces that enable systematic violence through routine bureaucratic processes.

## Technical Innovation: Conflict-Zone Geocoding

Traditional geocoding fails in conflict zones where street names change, buildings are destroyed, and competing authorities maintain different address systems. Our solution:

- **Dual-temporal address databases**: Tracking both Ukrainian and Russian naming systems
- **Fuzzy matching algorithms**: Handling transliteration variations and systematic renaming
- **Confidence scoring**: Legal-grade validation for evidence admissibility
- **Memory-efficient processing**: Handling multi-gigabyte datasets on consumer hardware

## Scalability and Impact

**Immediate Applications:**
- International Criminal Court evidence submission
- Asset recovery for post-conflict reconstruction
- Documentation for 12+ other occupied Ukrainian cities
- Template for similar conflicts globally

**Methodological Contributions:**
- First automated pipeline for self-incriminating evidence collection
- Berkeley Protocol-compliant digital forensics for OSINT investigations  
- Address harmonization solutions for conflict zones
- Integration framework for AI-assisted legal documentation

## Future Development

**Technical Expansion:**
- Machine learning for automated property seizure detection
- Real-time monitoring of new seizure orders as they're published
- Integration with international sanctions databases

**Geographic Scaling:**
- Deployment across all Russian-occupied Ukrainian territories
- Adaptation for other conflict zones with similar administrative violence patterns
- Training materials for international human rights organizations

## Why This Matters

This project demonstrates how modern technology can pierce the veil of administrative violence that traditionally conceals systematic war crimes. By combining AI-assisted research, automated evidence collection, and legal-grade documentation standards, we're creating new accountability mechanisms for the digital age.

The methodology proves that perpetrators' own bureaucratic compulsions can become their greatest vulnerability - transforming the very systems they use to commit crimes into the instruments of their prosecution.

**The result**: An unprecedented database of war crimes evidence, collected in real-time as perpetrators document their own violations of international law.

---

*This project operates entirely with open-source tools and public data sources, ensuring reproducibility and enabling replication across other conflict zones. All evidence collection meets Berkeley Protocol standards for international legal proceedings.*

**For further inquiries or collaboration, please contact Alexey Kovalev at kovalever@gmail.com**
