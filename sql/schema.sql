-- music-production-data-lab
-- Version 2.0 SQLite schema
-- Purpose: relational model derived from public-safe CSV sample data.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS soundchain_equipment;
DROP TABLE IF EXISTS soundchains;
DROP TABLE IF EXISTS music_references;
DROP TABLE IF EXISTS equipment;

CREATE TABLE equipment (
    equipment_id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    subcategory TEXT,
    brand TEXT,
    model TEXT,
    public_name TEXT NOT NULL,
    status_public TEXT,
    setup_domain TEXT,
    primary_role TEXT,
    is_hardware TEXT CHECK (is_hardware IN ('true', 'false')),
    is_software TEXT CHECK (is_software IN ('true', 'false')),
    analog_digital TEXT,
    mono_stereo TEXT,
    power_category TEXT,
    power_notes_public TEXT,
    data_quality_status TEXT,
    privacy_level TEXT,
    public_notes TEXT
);

CREATE TABLE music_references (
    reference_id TEXT PRIMARY KEY,
    artist_or_band TEXT NOT NULL,
    sound_axis TEXT NOT NULL,
    importance_public TEXT,
    reference_role TEXT,
    learning_focus TEXT,
    production_focus TEXT,
    gear_anchor_public TEXT,
    tuning_notes_public TEXT,
    dashboard_group TEXT,
    data_quality_status TEXT,
    privacy_level TEXT,
    public_notes TEXT
);

CREATE TABLE soundchains (
    soundchain_id TEXT PRIMARY KEY,
    chain_name TEXT NOT NULL,
    target_sound TEXT,
    sound_axis TEXT,
    workflow_type TEXT,
    tuning_context TEXT,
    primary_reference_id TEXT,
    primary_instrument_id TEXT,
    output_equipment_id TEXT,
    output_context TEXT,
    complexity_level TEXT,
    status_public TEXT,
    privacy_level TEXT,
    public_description TEXT,

    FOREIGN KEY (primary_reference_id)
        REFERENCES music_references(reference_id),

    FOREIGN KEY (primary_instrument_id)
        REFERENCES equipment(equipment_id),

    FOREIGN KEY (output_equipment_id)
        REFERENCES equipment(equipment_id)
);

CREATE TABLE soundchain_equipment (
    soundchain_id TEXT NOT NULL,
    equipment_id TEXT NOT NULL,
    position_in_chain INTEGER NOT NULL,
    role_in_chain TEXT,
    required_or_optional TEXT,
    sequence_group TEXT,
    public_notes TEXT,

    PRIMARY KEY (soundchain_id, equipment_id, position_in_chain),

    FOREIGN KEY (soundchain_id)
        REFERENCES soundchains(soundchain_id),

    FOREIGN KEY (equipment_id)
        REFERENCES equipment(equipment_id)
);

CREATE INDEX idx_equipment_category
    ON equipment(category);

CREATE INDEX idx_equipment_setup_domain
    ON equipment(setup_domain);

CREATE INDEX idx_music_references_sound_axis
    ON music_references(sound_axis);

CREATE INDEX idx_soundchains_sound_axis
    ON soundchains(sound_axis);

CREATE INDEX idx_soundchains_workflow_type
    ON soundchains(workflow_type);

CREATE INDEX idx_soundchain_equipment_equipment_id
    ON soundchain_equipment(equipment_id);

CREATE INDEX idx_soundchain_equipment_soundchain_id
    ON soundchain_equipment(soundchain_id);
