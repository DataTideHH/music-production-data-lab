# Analysis Findings and Interpretation

The findings below are derived from the committed public-safe sample and the generated reporting outputs. They describe the sample model, not a complete private inventory.

## 1. The sample is large enough to show real relational behaviour

The analytical layer now contains:

- 30 equipment records
- 12 music references
- 12 soundchains
- 53 ordered equipment uses

The bridge table is no longer a minimal demonstration. It now supports reuse, dependency, coverage and complexity analysis across both guitar signal chains and recording workflows.

## 2. Workflow coverage is high without implying completeness

Twenty-four of 30 equipment records are used in at least one workflow, producing an 80% coverage rate. Six records remain unused in the current workflow sample.

This is useful portfolio evidence because the model distinguishes between:

- items actively used in workflows
- records retained for comparison or future modelling
- planned or reference-only records

Unused records are therefore visible analytical information, not automatically data-quality failures.

## 3. Reusable platform items emerge clearly

The most reused records are:

| Equipment | Soundchain uses |
|---|---:|
| SD-1 Super OverDrive | 5 |
| UR22C | 5 |
| Ableton Live 12 Intro | 4 |
| SE Standard 24-08 | 4 |
| DL4 MkII | 3 |

The pattern shows that common platform components create more cross-workflow leverage than highly specialized items. The interface and DAW connect several recording workflows, while the overdrive and versatile guitar recur across multiple sound-design goals.

## 4. Recording workflows are fewer but structurally larger

Four of the 12 workflows are recording workflows. The two largest chains are:

- Stereo Ambient Recording: 7 steps
- Layered Delay Recording: 6 steps

Recording workflows combine input, processing, interface and software roles, so they tend to create more ordered relationships than compact amplifier-based workflows. This demonstrates why workflow type should be analysed separately from sound style.

## 5. Required versus optional roles make the model operational

Of 53 equipment uses:

- 39 are required
- 11 are optional
- 3 are swap candidates

The distinction prevents the bridge table from becoming a simple list. It supports questions about minimum viable setups, extension options and substitutions—concepts that transfer directly to process modelling and dependency analysis.

## 6. Data quality is explicit rather than implied

Nineteen equipment records are marked verified, ten remain sample-level records and one planned record needs verification. Every soundchain is marked as a verified public sample.

The quality status is intentionally visible in the reporting layer. This is preferable to treating all records as equally certain and supports a basic governance narrative for Data/BI roles.

## Portfolio interpretation

The project now demonstrates:

- domain discovery and public-safe curation
- normalized entity and bridge-table modelling
- controlled values and relationship validation
- SQL reporting views and analytical queries
- reproducible generated reporting datasets
- Power BI semantic-model and DAX documentation
- interpretation of findings for a non-specialist reviewer
