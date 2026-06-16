# CSV schema v0.2

This document describes the current public CSV files.

The files in `data/public/` are public-safe sample datasets. They are intentionally smaller than the private working data.

## File: equipment_public.csv

Purpose: public-safe equipment sample data.

Primary key:

    equipment_id

Columns:

| Column | Meaning |
|---|---|
| equipment_id | Stable item identifier such as EQP-0001 |
| category | High-level equipment category |
| subcategory | More specific type within the category |
| brand | Public brand or manufacturer name |
| model | Public model name |
| public_name | Public-safe display name |
| status_public | Public-safe status such as available or planned |
| setup_domain | Main domain such as guitar_effect or recording |
| primary_role | Main practical role in the setup |
| is_hardware | Boolean-like value: true or false |
| is_software | Boolean-like value: true or false |
| analog_digital | Analog or digital where applicable |
| mono_stereo | Mono, stereo or not_applicable |
| power_category | Coarse power classification |
| power_notes_public | Public-safe power notes without private details |
| data_quality_status | Status such as sample or needs_verification |
| privacy_level | Public-safe classification |
| public_notes | Short public-safe note |

## File: music_references_public.csv

Purpose: public-safe reference data for musical learning and sound design.

Primary key:

    reference_id

Columns:

| Column | Meaning |
|---|---|
| reference_id | Stable reference identifier such as REF-0001 |
| artist_or_band | Public artist or band name |
| sound_axis | Public sound axis |
| importance_public | Public relevance level such as core or context |
| reference_role | Public role of the reference |
| learning_focus | What can be learned from the reference |
| production_focus | Production or arrangement angle |
| gear_anchor_public | Public-safe gear or workflow anchor |
| tuning_notes_public | Public-safe tuning notes |
| dashboard_group | Coarse grouping for later BI use |
| data_quality_status | Status such as sample or needs_verification |
| privacy_level | Public-safe classification |
| public_notes | Short public-safe note |

## File: soundchains_public.csv

Purpose: public-safe soundchain and workflow sample data.

Primary key:

    soundchain_id

Columns:

| Column | Meaning |
|---|---|
| soundchain_id | Stable soundchain identifier such as SC-0001 |
| chain_name | Public name of the soundchain |
| target_sound | Short target sound description |
| sound_axis | Public sound axis or analysis category |
| workflow_type | Type such as guitar_signal_chain or recording_workflow |
| tuning_context | Public-safe tuning context |
| primary_reference_id | Optional link to music_references_public.csv |
| primary_instrument_id | Optional link to equipment_public.csv |
| output_equipment_id | Optional output or platform link |
| output_context | Amp, DAW, interface or other output context |
| complexity_level | Coarse level for later analysis |
| status_public | Public-safe status |
| privacy_level | Public-safe classification |
| public_description | Short public-safe description |

## File: soundchain_equipment_public.csv

Purpose: relationship table between soundchains and equipment items.

Composite key candidate:

    soundchain_id + equipment_id + position_in_chain

Columns:

| Column | Meaning |
|---|---|
| soundchain_id | Link to soundchains_public.csv |
| equipment_id | Link to equipment_public.csv |
| position_in_chain | Numeric order inside the chain or workflow |
| role_in_chain | Functional role of the item |
| required_or_optional | required, optional or swap_candidate |
| sequence_group | Coarse grouping such as front_end, gain_stage or output |
| public_notes | Short public-safe note |

## Naming rules

Current identifier prefixes:

| Prefix | Meaning |
|---|---|
| EQP | Equipment |
| REF | Music reference |
| SC | Soundchain |

Example:

    EQP-0001
    REF-0001
    SC-0001

## Public data rules

Public CSV files must not contain:

- serial numbers
- invoices
- purchase prices
- private condition notes
- private storage information
- full private inventory exports
- original Word source material
- long copied manufacturer descriptions
- copyrighted manuals or images
