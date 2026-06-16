# Data model v0.2

This document describes the conceptual data model for `music-production-data-lab`.

Version 1 uses CSV files only. Later versions can transform these CSV files into a relational SQLite database.

## Core idea

The project models a music production setup as a set of related entities:

    equipment
    -> music references
    -> soundchains
    -> soundchain items
    -> boards and workflows
    -> analyses and dashboards

## Current CSV entities

Version 1 uses three public-safe CSV files:

    data/public/equipment_public.csv
    data/public/music_references_public.csv
    data/public/soundchains_public.csv

These files are sample datasets. They are not the full private inventory.

## Entity: equipment

`equipment_public.csv` stores public-safe equipment items.

Examples:

- instrument
- effect
- amplifier
- cabinet
- recording hardware
- software
- MIDI controller
- utility
- monitoring

The table uses `equipment_id` as a stable identifier.

Example identifier:

    EQP-0001

## Entity: music_references

`music_references_public.csv` stores public-safe reference artists, bands or sound concepts.

These entries are used to connect learning goals, sound design ideas and gear/workflow decisions.

The table uses `reference_id` as a stable identifier.

Example identifier:

    REF-0001

## Entity: soundchains

`soundchains_public.csv` stores public-safe workflow or signal-chain concepts.

A soundchain is not just a list of devices. It describes a target sound or workflow such as:

    guitar
    -> distortion
    -> chorus
    -> amp platform

The table uses `soundchain_id` as a stable identifier.

Example identifier:

    SC-0001

## Future relational model

Later versions should split the project into normalized relational tables.

Possible future tables:

    equipment
    equipment_categories
    pedals
    instruments
    amps_cabs
    recording_hardware
    software_tools
    midi_controllers
    music_references
    sound_axes
    soundchains
    soundchain_items
    boards
    board_items
    data_quality_checks

## Important relationships

### Equipment and soundchains

One soundchain can use multiple equipment items.

One equipment item can appear in multiple soundchains.

This is a many-to-many relationship.

Future table:

    soundchain_items

Possible fields:

    soundchain_id
    equipment_id
    position_in_chain
    role_in_chain
    required_or_optional

### Boards and equipment

One board can contain multiple equipment items.

One equipment item can appear on multiple boards or in multiple board concepts.

Future table:

    board_items

Possible fields:

    board_id
    equipment_id
    fixed_or_swap
    role_on_board
    power_source

### Music references and soundchains

One music reference can inform multiple soundchains.

One soundchain can be inspired by multiple references.

Future table:

    reference_soundchain_links

Possible fields:

    reference_id
    soundchain_id
    relevance
    learning_focus

## Version 1 design decision

Version 1 intentionally avoids building the database too early.

The current goal is to make the source data understandable first:

    CSV structure
    -> field names
    -> identifiers
    -> public/private boundaries
    -> documentation
    -> later database schema

Only after that should the relational database schema be created.
