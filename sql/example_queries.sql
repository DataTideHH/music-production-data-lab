-- music-production-data-lab
-- Analytical queries for the expanded public-safe relational sample.

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

-- 5. Equipment reuse and coverage classification
SELECT
    equipment_id,
    public_name,
    category,
    soundchain_usage_count,
    coverage_status
FROM vw_equipment_usage
ORDER BY soundchain_usage_count DESC, public_name;

-- 6. Required, optional and swap-candidate usage
SELECT
    required_or_optional,
    COUNT(*) AS usage_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM soundchain_equipment), 1) AS usage_share_percent
FROM soundchain_equipment
GROUP BY required_or_optional
ORDER BY usage_count DESC;

-- 7. Sound axes represented in the workflow sample
SELECT sound_axis, COUNT(*) AS soundchain_count
FROM soundchains
GROUP BY sound_axis
ORDER BY soundchain_count DESC, sound_axis;

-- 8. References grouped for reporting
SELECT dashboard_group, COUNT(*) AS reference_count
FROM music_references
GROUP BY dashboard_group
ORDER BY reference_count DESC, dashboard_group;

-- 9. Soundchain complexity and dependency mix
SELECT *
FROM vw_soundchain_analysis
ORDER BY total_steps DESC, chain_name;

-- 10. Equipment not currently used in any workflow
SELECT
    equipment_id,
    public_name,
    category,
    status_public,
    data_quality_status
FROM vw_equipment_usage
WHERE coverage_status = 'unused'
ORDER BY category, public_name;

-- 11. Workflow coverage by equipment category
SELECT
    e.category,
    COUNT(DISTINCT e.equipment_id) AS equipment_items_used,
    COUNT(DISTINCT se.soundchain_id) AS soundchains_covered,
    COUNT(*) AS equipment_uses
FROM soundchain_equipment se
JOIN equipment e
    ON se.equipment_id = e.equipment_id
GROUP BY e.category
ORDER BY soundchains_covered DESC, equipment_uses DESC, e.category;

-- 12. Required single-use dependencies
SELECT
    e.equipment_id,
    e.public_name,
    sc.soundchain_id,
    sc.chain_name,
    se.role_in_chain
FROM soundchain_equipment se
JOIN equipment e
    ON se.equipment_id = e.equipment_id
JOIN soundchains sc
    ON se.soundchain_id = sc.soundchain_id
JOIN vw_equipment_usage usage
    ON e.equipment_id = usage.equipment_id
WHERE se.required_or_optional = 'required'
  AND usage.soundchain_usage_count = 1
ORDER BY sc.chain_name, e.public_name;

-- 13. Recording workflow profile
SELECT
    soundchain_id,
    chain_name,
    complexity_level,
    total_steps,
    required_steps,
    optional_steps,
    swap_candidate_steps
FROM vw_soundchain_analysis
WHERE workflow_type = 'recording_workflow'
ORDER BY total_steps DESC, chain_name;

-- 14. Data-quality status distribution
SELECT
    'equipment' AS entity,
    data_quality_status AS quality_status,
    COUNT(*) AS record_count
FROM equipment
GROUP BY data_quality_status
UNION ALL
SELECT
    'music_references',
    data_quality_status,
    COUNT(*)
FROM music_references
GROUP BY data_quality_status
UNION ALL
SELECT
    'soundchains',
    status_public,
    COUNT(*)
FROM soundchains
GROUP BY status_public
ORDER BY entity, quality_status;

-- 15. Workflow-type summary
SELECT
    workflow_type,
    COUNT(*) AS soundchain_count,
    SUM(total_steps) AS equipment_uses,
    ROUND(AVG(total_steps), 2) AS average_steps,
    MAX(total_steps) AS maximum_steps
FROM vw_soundchain_analysis
GROUP BY workflow_type
ORDER BY workflow_type;

-- 16. Most reusable platform items
SELECT
    equipment_id,
    public_name,
    category,
    soundchain_usage_count
FROM vw_equipment_usage
WHERE soundchain_usage_count >= 2
ORDER BY soundchain_usage_count DESC, public_name;
