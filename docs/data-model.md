# Data model v0.1

This document describes the first conceptual data model for music-production-data-lab.

Version 1 uses CSV files only. Later versions can transform these CSV files into a relational SQLite database.

## Core idea

The project models a music production setup as a set of related entities:

    equipment
    -> soundchains
    -> soundchain items
    -> boards / setups
    -> music references

## Main entities

### equipment

General inventory-like entity for public-safe equipment items.

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

In version 1, this is represented by:

    data/public/equipment_public.csv

### music_references

Reference artists, bands or sound axes used for learning, sound design and workflow planning.

In version 1, this is represented by:

    data/public/music_references_public.csv

### soundchains

A soundchain describes a practical signal or workflow concept.

Example:

    guitar
    -> distortion
    -> chorus
    -> amp platform

In version 1, this is represented by:

    data/public/soundchains_public.csv

## Future relational model

Later versions should split the data into normalized relational tables.

Possible future tables:

    equipment
    equipment_categories
    pedals
    instruments
    amps_cabs
    recording_tools
    software_tools
    music_references
    soundchains
    soundchain_items
    boards
    board_items

## Important relationships

### Equipment and soundchains

A soundchain can use multiple equipment items.

An equipment item can appear in multiple soundchains.

This is a many-to-many relationship.

Future relational table:

    soundchain_items

Possible fields:

    soundchain_id
    equipment_id
    position_in_chain
    role_in_chain
    required_or_optional

### Boards and equipment

A board can contain multiple equipment items.

An equipment item can appear in multiple boards or board concepts.

Future relational table:

    board_items

Possible fields:

    board_id
    equipment_id
    fixed_or_swap
    role_on_board
    power_source

## Version 1 design decision

Version 1 intentionally avoids building the database too early.

The goal is to make the source data understandable first:

    CSV structure
    -> field names
    -> public/private boundaries
    -> first documentation

Only after that should the relational database schema be created.
