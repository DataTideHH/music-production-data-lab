# Data model v0.3

This document describes the conceptual data model for `music-production-data-lab`.

Version 1 uses CSV files only. Later versions can transform these CSV files into a relational SQLite database.

## Core idea

The project models a music production setup as a set of related entities:

    equipment
    -> music references
    -> soundchains
    -> soundchain equipment links
    -> boards and workflows
    -> analyses and dashboards

## Current CSV entities

Version 1.2 uses four public-safe CSV files:

    data/public/equipment_public.csv
    data/public/music_references_public.csv
    data/public/soundchains_public.csv
    data/public/soundchain_equipment_public.csv

These files are sample datasets. They are not the full private inventory.

## Entity: equipment

`equipment_public.csv` stores public-safe equipment items.

Examples:

- instrument
- effect
- amplification
- recording hardware
- software
- MIDI controller
- power utility

Primary key:

    equipment_id

SQLite preparation:

    equipment_id TEXT PRIMARY KEY
    category TEXT NOT NULL
    subcategory TEXT
    brand TEXT
    model TEXT
    public_name TEXT NOT NULL
    status_public TEXT
    is_hardware INTEGER
    is_software INTEGER

## Entity: music_references

`music_references_public.csv` stores public-safe reference artists, bands or sound concepts.

These entries connect learning goals, sound design ideas and workflow decisions.

Primary key:

    reference_id

SQLite preparation:

    reference_id TEXT PRIMARY KEY
    artist_or_band TEXT NOT NULL
    sound_axis TEXT NOT NULL
    importance_public TEXT
    reference_role TEXT

## Entity: soundchains

`soundchains_public.csv` stores public-safe workflow or signal-chain concepts.

A soundchain is not just a list of devices. It describes a target sound or workflow.

Primary key:

    soundchain_id

SQLite preparation:

    soundchain_id TEXT PRIMARY KEY
    chain_name TEXT NOT NULL
    target_sound TEXT
    sound_axis TEXT
    workflow_type TEXT
    primary_reference_id TEXT
    output_context TEXT

## Relationship: soundchain_equipment

`soundchain_equipment_public.csv` connects soundchains and equipment items.

This is the first actual relationship table in the project.

One soundchain can contain multiple equipment items.

One equipment item can appear in multiple soundchains.

Primary key candidate:

    soundchain_id + equipment_id + position_in_chain

SQLite preparation:

    soundchain_id TEXT NOT NULL
    equipment_id TEXT NOT NULL
    position_in_chain INTEGER NOT NULL
    role_in_chain TEXT
    required_or_optional TEXT

Future foreign keys:

    soundchain_id -> soundchains.soundchain_id
    equipment_id -> equipment.equipment_id

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

## Power BI preparation

The current CSV structure is designed to support later Power BI modeling.

Potential relationships:

    soundchains_public[soundchain_id]
    -> soundchain_equipment_public[soundchain_id]

    equipment_public[equipment_id]
    -> soundchain_equipment_public[equipment_id]

    music_references_public[reference_id]
    -> soundchains_public[primary_reference_id]

This makes it possible to analyze:

- equipment usage per soundchain
- most frequently used equipment categories
- sound axes by reference and workflow type
- hardware versus software distribution
- sample data quality and privacy status

## Version 1.2 design decision

Version 1.2 still avoids building the database too early.

The current goal is to make the data structure realistic enough for later SQLite and Power BI work:

    CSV structure
    -> stable IDs
    -> relationship table
    -> public/private boundaries
    -> data-quality fields
    -> later database schema
