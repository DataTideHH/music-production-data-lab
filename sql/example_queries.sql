-- music-production-data-lab
-- Analytical queries for the public-safe relational sample.

-- 1. Equipment overview by category
SELECT category, COUNT(*) AS item_count
FROM equipment
GROUP BY category
ORDER BY item_count DESC, category;

-- 2. Hardware versus software distribution
SELECT is_hardware, is_software, COUNT(*) AS item_count
FROM equipment
GROUP BY is_hardware, is_software
ORDER BY item_count DESC;

-- 3. Soundchains with primary reference and output context
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

-- 4. Ordered equipment used in each soundchain
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

-- 5. Most frequently reused equipment
SELECT
    e.equipment_id,
    e.public_name,
    e.category,
    e.primary_role,
    COUNT(*) AS soundchain_usage_count
FROM equipment e
JOIN soundchain_equipment se
    ON e.equipment_id = se.equipment_id
GROUP BY e.equipment_id, e.public_name, e.category, e.primary_role
ORDER BY soundchain_usage_count DESC, e.public_name;

-- 6. Required versus optional equipment usage
SELECT required_or_optional, COUNT(*) AS usage_count
FROM soundchain_equipment
GROUP BY required_or_optional
ORDER BY usage_count DESC;

-- 7. Sound axes represented in the sample
SELECT sound_axis, COUNT(*) AS soundchain_count
FROM soundchains
GROUP BY sound_axis
ORDER BY soundchain_count DESC, sound_axis;

-- 8. References grouped for reporting
SELECT dashboard_group, COUNT(*) AS reference_count
FROM music_references
GROUP BY dashboard_group
ORDER BY reference_count DESC, dashboard_group;

-- 9. Soundchain complexity and item counts
SELECT
    sc.soundchain_id,
    sc.chain_name,
    sc.complexity_level,
    COUNT(se.equipment_id) AS equipment_steps,
    SUM(CASE WHEN se.required_or_optional = 'optional' THEN 1 ELSE 0 END) AS optional_steps
FROM soundchains sc
LEFT JOIN soundchain_equipment se
    ON sc.soundchain_id = se.soundchain_id
GROUP BY sc.soundchain_id, sc.chain_name, sc.complexity_level
ORDER BY equipment_steps DESC, sc.chain_name;

-- 10. Equipment not currently used in any soundchain
SELECT e.equipment_id, e.public_name, e.category
FROM equipment e
LEFT JOIN soundchain_equipment se
    ON e.equipment_id = se.equipment_id
WHERE se.equipment_id IS NULL
ORDER BY e.category, e.public_name;
