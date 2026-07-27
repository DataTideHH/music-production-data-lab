-- music-production-data-lab
-- Current SQLite schema for the public-safe analytical sample.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS vw_soundchain_analysis;
DROP VIEW IF EXISTS vw_equipment_usage;

DROP TABLE IF EXISTS soundchain_equipment;
DROP TABLE IF EXISTS soundchains;
DROP TABLE IF EXISTS music_references;
DROP TABLE IF EXISTS equipment;

CREATE TABLE equipment (
    equipment_id TEXT PRIMARY KEY,
    category TEXT NOT NULL CHECK (
        category IN (
            'instrument',
            'effect',
            'amplification',
            'recording_hardware',
            'midi_controller',
            'software',
            'power_utility'
        )
    ),
    subcategory TEXT,
    brand TEXT,
    model TEXT,
    public_name TEXT NOT NULL,
    status_public TEXT NOT NULL CHECK (
        status_public IN ('available', 'planned', 'reference')
    ),
    setup_domain TEXT,
    primary_role TEXT,
    is_hardware TEXT NOT NULL CHECK (is_hardware IN ('true', 'false')),
    is_software TEXT NOT NULL CHECK (is_software IN ('true', 'false')),
    analog_digital TEXT CHECK (
        analog_digital IN ('analog', 'digital', 'hybrid', 'not_applicable')
    ),
    mono_stereo TEXT CHECK (
        mono_stereo IN ('mono', 'stereo', 'both', 'not_applicable')
    ),
    power_category TEXT,
    power_notes_public TEXT,
    data_quality_status TEXT NOT NULL CHECK (
        data_quality_status IN ('sample', 'verified', 'needs_verification')
    ),
    privacy_level TEXT NOT NULL CHECK (privacy_level = 'public_sample'),
    public_notes TEXT,
    CHECK (
        (is_hardware = 'true' AND is_software = 'false')
        OR
        (is_hardware = 'false' AND is_software = 'true')
    )
);

CREATE TABLE music_references (
    reference_id TEXT PRIMARY KEY,
    artist_or_band TEXT NOT NULL,
    sound_axis TEXT NOT NULL,
    importance_public TEXT NOT NULL CHECK (
        importance_public IN ('core', 'context')
    ),
    reference_role TEXT NOT NULL CHECK (
        reference_role IN (
            'playing_reference',
            'sound_design_reference',
            'songwriting_reference',
            'rhythm_reference',
            'production_reference'
        )
    ),
    learning_focus TEXT,
    production_focus TEXT,
    gear_anchor_public TEXT,
    tuning_notes_public TEXT,
    dashboard_group TEXT,
    data_quality_status TEXT NOT NULL CHECK (
        data_quality_status IN ('sample', 'verified', 'needs_verification')
    ),
    privacy_level TEXT NOT NULL CHECK (privacy_level = 'public_sample'),
    public_notes TEXT
);

CREATE TABLE soundchains (
    soundchain_id TEXT PRIMARY KEY,
    chain_name TEXT NOT NULL,
    target_sound TEXT,
    sound_axis TEXT,
    workflow_type TEXT NOT NULL CHECK (
        workflow_type IN ('guitar_signal_chain', 'recording_workflow')
    ),
    tuning_context TEXT,
    primary_reference_id TEXT,
    primary_instrument_id TEXT,
    output_equipment_id TEXT,
    output_context TEXT,
    complexity_level TEXT NOT NULL CHECK (
        complexity_level IN ('basic', 'intermediate', 'advanced')
    ),
    status_public TEXT NOT NULL CHECK (
        status_public IN ('draft_public_sample', 'verified_public_sample')
    ),
    privacy_level TEXT NOT NULL CHECK (privacy_level = 'public_sample'),
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
    position_in_chain INTEGER NOT NULL CHECK (position_in_chain > 0),
    role_in_chain TEXT NOT NULL,
    required_or_optional TEXT NOT NULL CHECK (
        required_or_optional IN ('required', 'optional', 'swap_candidate')
    ),
    sequence_group TEXT NOT NULL CHECK (
        sequence_group IN (
            'input',
            'input_output',
            'gain_stage',
            'modulation',
            'midi',
            'software',
            'output'
        )
    ),
    public_notes TEXT,

    PRIMARY KEY (soundchain_id, position_in_chain),

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

CREATE VIEW vw_equipment_usage AS
SELECT
    e.equipment_id,
    e.public_name,
    e.category,
    e.subcategory,
    e.status_public,
    e.data_quality_status,
    COUNT(se.soundchain_id) AS soundchain_usage_count,
    CASE
        WHEN COUNT(se.soundchain_id) = 0 THEN 'unused'
        WHEN COUNT(se.soundchain_id) = 1 THEN 'single_use'
        ELSE 'reused'
    END AS coverage_status
FROM equipment e
LEFT JOIN soundchain_equipment se
    ON e.equipment_id = se.equipment_id
GROUP BY
    e.equipment_id,
    e.public_name,
    e.category,
    e.subcategory,
    e.status_public,
    e.data_quality_status;

CREATE VIEW vw_soundchain_analysis AS
SELECT
    sc.soundchain_id,
    sc.chain_name,
    sc.workflow_type,
    sc.sound_axis,
    sc.complexity_level,
    mr.artist_or_band AS primary_reference,
    COUNT(se.equipment_id) AS total_steps,
    SUM(CASE WHEN se.required_or_optional = 'required' THEN 1 ELSE 0 END) AS required_steps,
    SUM(CASE WHEN se.required_or_optional = 'optional' THEN 1 ELSE 0 END) AS optional_steps,
    SUM(CASE WHEN se.required_or_optional = 'swap_candidate' THEN 1 ELSE 0 END) AS swap_candidate_steps
FROM soundchains sc
LEFT JOIN music_references mr
    ON sc.primary_reference_id = mr.reference_id
LEFT JOIN soundchain_equipment se
    ON sc.soundchain_id = se.soundchain_id
GROUP BY
    sc.soundchain_id,
    sc.chain_name,
    sc.workflow_type,
    sc.sound_axis,
    sc.complexity_level,
    mr.artist_or_band;
