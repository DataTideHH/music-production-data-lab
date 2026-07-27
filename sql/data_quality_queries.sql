-- music-production-data-lab
-- Data-quality queries. Every statement must return zero rows.

-- 1. Missing required equipment fields
SELECT *
FROM equipment
WHERE TRIM(equipment_id) = '' OR TRIM(category) = '' OR TRIM(public_name) = '';

-- 2. Missing required music-reference fields
SELECT *
FROM music_references
WHERE TRIM(reference_id) = '' OR TRIM(artist_or_band) = '' OR TRIM(sound_axis) = '';

-- 3. Missing required soundchain fields
SELECT *
FROM soundchains
WHERE TRIM(soundchain_id) = '' OR TRIM(chain_name) = '' OR TRIM(workflow_type) = '';

-- 4. Orphan primary-reference links
SELECT sc.soundchain_id, sc.primary_reference_id
FROM soundchains sc
LEFT JOIN music_references mr
    ON sc.primary_reference_id = mr.reference_id
WHERE sc.primary_reference_id IS NOT NULL
  AND sc.primary_reference_id <> ''
  AND mr.reference_id IS NULL;

-- 5. Orphan primary-instrument links
SELECT sc.soundchain_id, sc.primary_instrument_id
FROM soundchains sc
LEFT JOIN equipment e
    ON sc.primary_instrument_id = e.equipment_id
WHERE sc.primary_instrument_id IS NOT NULL
  AND sc.primary_instrument_id <> ''
  AND e.equipment_id IS NULL;

-- 6. Orphan output-equipment links
SELECT sc.soundchain_id, sc.output_equipment_id
FROM soundchains sc
LEFT JOIN equipment e
    ON sc.output_equipment_id = e.equipment_id
WHERE sc.output_equipment_id IS NOT NULL
  AND sc.output_equipment_id <> ''
  AND e.equipment_id IS NULL;

-- 7. Orphan bridge-table links
SELECT se.soundchain_id, se.equipment_id
FROM soundchain_equipment se
LEFT JOIN soundchains sc
    ON se.soundchain_id = sc.soundchain_id
LEFT JOIN equipment e
    ON se.equipment_id = e.equipment_id
WHERE sc.soundchain_id IS NULL OR e.equipment_id IS NULL;

-- 8. Duplicate positions within a soundchain
SELECT soundchain_id, position_in_chain, COUNT(*) AS duplicate_position_count
FROM soundchain_equipment
GROUP BY soundchain_id, position_in_chain
HAVING COUNT(*) > 1;

-- 9. Non-public records in public source tables
SELECT 'equipment' AS table_name, equipment_id AS item_id, privacy_level
FROM equipment
WHERE privacy_level <> 'public_sample'
UNION ALL
SELECT 'music_references', reference_id, privacy_level
FROM music_references
WHERE privacy_level <> 'public_sample'
UNION ALL
SELECT 'soundchains', soundchain_id, privacy_level
FROM soundchains
WHERE privacy_level <> 'public_sample';

-- 10. Invalid hardware/software classification
SELECT equipment_id, is_hardware, is_software
FROM equipment
WHERE NOT (
    (is_hardware = 'true' AND is_software = 'false')
    OR
    (is_hardware = 'false' AND is_software = 'true')
);

-- 11. Non-positive chain positions
SELECT *
FROM soundchain_equipment
WHERE position_in_chain <= 0;

-- 12. Soundchains without any bridge-table item
SELECT sc.soundchain_id, sc.chain_name
FROM soundchains sc
LEFT JOIN soundchain_equipment se
    ON sc.soundchain_id = se.soundchain_id
GROUP BY sc.soundchain_id, sc.chain_name
HAVING COUNT(se.equipment_id) = 0;
