# Data dictionary and controlled values

This document defines the current public schema and the controlled values enforced by Python and SQLite.

## Identifiers

| Prefix | Entity | Example |
|---|---|---|
| `EQP` | equipment | `EQP-0001` |
| `REF` | music reference | `REF-0001` |
| `SC` | soundchain | `SC-0001` |

Identifiers are stable public keys. They do not encode private purchase or location information.

## `equipment`

Primary key: `equipment_id`

Controlled values:

| Column | Allowed values |
|---|---|
| `category` | `instrument`, `effect`, `amplification`, `recording_hardware`, `midi_controller`, `software`, `power_utility` |
| `status_public` | `available`, `planned`, `reference` |
| `is_hardware` | `true`, `false` |
| `is_software` | `true`, `false` |
| `analog_digital` | `analog`, `digital`, `hybrid`, `not_applicable` |
| `mono_stereo` | `mono`, `stereo`, `both`, `not_applicable` |
| `data_quality_status` | `sample`, `verified`, `needs_verification` |
| `privacy_level` | `public_sample` |

Exactly one of `is_hardware` and `is_software` must be true.

## `music_references`

Primary key: `reference_id`

| Column | Allowed values |
|---|---|
| `importance_public` | `core`, `context` |
| `reference_role` | `playing_reference`, `sound_design_reference`, `songwriting_reference`, `rhythm_reference`, `production_reference` |
| `data_quality_status` | `sample`, `verified`, `needs_verification` |
| `privacy_level` | `public_sample` |

## `soundchains`

Primary key: `soundchain_id`

| Column | Allowed values |
|---|---|
| `workflow_type` | `guitar_signal_chain`, `recording_workflow` |
| `complexity_level` | `basic`, `intermediate`, `advanced` |
| `status_public` | `draft_public_sample`, `verified_public_sample` |
| `privacy_level` | `public_sample` |

Foreign keys:

- `primary_reference_id -> music_references.reference_id`
- `primary_instrument_id -> equipment.equipment_id`
- `output_equipment_id -> equipment.equipment_id`

## `soundchain_equipment`

Primary key: `soundchain_id + position_in_chain`

| Column | Allowed values |
|---|---|
| `required_or_optional` | `required`, `optional`, `swap_candidate` |
| `sequence_group` | `input`, `input_output`, `gain_stage`, `modulation`, `midi`, `software`, `output` |

`position_in_chain` must be a positive integer and unique within each soundchain.

## Public-data rules

Public CSV files may contain only reviewed sample fields. The workflow rejects selected forbidden column names, sensitive terms, currency-like values, serial-like values and any privacy classification other than `public_sample`.

Automated checks reduce accidental exposure but do not replace human review.
