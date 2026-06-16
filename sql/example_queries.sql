-- music-production-data-lab
-- Version 2.0 example queries
-- Purpose: show useful analysis questions based on the relational model.

-- 1. Equipment overview by category
SELECT
    category,
    COUNT(*) AS item_count
FROM equipment
GROUP BY category
ORDER BY item_count DESC, category;

-- 2. Hardware vs. software distribution
SELECT
    is_hardware,
    is_software,
    COUNT(*) AS item_count
FROM equipment
GROUP BY is_hardware, is_software
ORDER BY item_count DESC;

-- 3. Soundchains with their primary reference and output context
SELECT
    sc.soundchain_id,
    sc.chain_name,
    sc.sound_axis,
    sc.workflow_type,
    mr.artist_or_band AS primary_reference,
    sc.output_context
FROM soundchains sc
LEFT JOIN music_references mr
    ON sc.primary_reference_id = mr.reference_id
ORDER BY sc.soundchain_id;

-- 4. Equipment used in each soundchain, ordered by signal/workflow position
SELECT
    sc.soundchain_id,
    sc.chain_name,
    se.position_in_chain,
    e.category,
    e.subcategory,
    e.public_name,
    se.role_in_chain,
    se.required_or_optional,
    se.sequence_group
FROM soundchains sc
JOIN soundchain_equipment se
    ON sc.soundchain_id = se.soundchain_id
JOIN equipment e
    ON se.equipment_id = e.equipment_id
ORDER BY sc.soundchain_id, se.position_in_chain;

-- 5. Most frequently used equipment items across soundchains
SELECT
    e.equipment_id,
    e.public_name,
    e.category,
    e.primary_role,
    COUNT(*) AS soundchain_usage_count
FROM equipment e
JOIN soundchain_equipment se
    ON e.equipment_id = se.equipment_id
GROUP BY
    e.equipment_id,
    e.public_name,
    e.category,
    e.primary_role
ORDER BY soundchain_usage_count DESC, e.public_name;

-- 6. Required vs. optional equipment usage
SELECT
    required_or_optional,
    COUNT(*) AS usage_count
FROM soundchain_equipment
GROUP BY required_or_optional
ORDER BY usage_count DESC;

-- 7. Sound axes represented in the sample data
SELECT
    sound_axis,
    COUNT(*) AS soundchain_count
FROM soundchains
GROUP BY sound_axis
ORDER BY soundchain_count DESC, sound_axis;

-- 8. References grouped for dashboard preparation
SELECT
    dashboard_group,
    COUNT(*) AS reference_count
FROM music_references
GROUP BY dashboard_group
ORDER BY reference_count DESC, dashboard_group;

-- 9. Guitar signal chains only
SELECT
    soundchain_id,
    chain_name,
    sound_axis,
    complexity_level,
    output_context
FROM soundchains
WHERE workflow_type = 'guitar_signal_chain'
ORDER BY complexity_level, chain_name;

-- 10. Recording or software-related equipment
SELECT
    equipment_id,
    public_name,
    category,
    subcategory,
    setup_domain,
    primary_role
FROM equipment
WHERE
    category = 'software'
    OR setup_domain = 'recording'
    OR is_software = 'true'
ORDER BY category, public_name;
