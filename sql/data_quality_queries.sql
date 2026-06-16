-- music-production-data-lab
-- Version 2.0 data-quality queries
-- Purpose: SQL checks for IDs, relationships, required fields and public-safe sample data.

-- 1. Duplicate equipment IDs
SELECT
    equipment_id,
    COUNT(*) AS duplicate_count
FROM equipment
GROUP BY equipment_id
HAVING COUNT(*) > 1;

-- 2. Duplicate music reference IDs
SELECT
    reference_id,
    COUNT(*) AS duplicate_count
FROM music_references
GROUP BY reference_id
HAVING COUNT(*) > 1;

-- 3. Duplicate soundchain IDs
SELECT
    soundchain_id,
    COUNT(*) AS duplicate_count
FROM soundchains
GROUP BY soundchain_id
HAVING COUNT(*) > 1;

-- 4. Missing required equipment fields
SELECT *
FROM equipment
WHERE
    equipment_id IS NULL
    OR equipment_id = ''
    OR category IS NULL
    OR category = ''
    OR public_name IS NULL
    OR public_name = '';

-- 5. Missing required music reference fields
SELECT *
FROM music_references
WHERE
    reference_id IS NULL
    OR reference_id = ''
    OR artist_or_band IS NULL
    OR artist_or_band = ''
    OR sound_axis IS NULL
    OR sound_axis = '';

-- 6. Missing required soundchain fields
SELECT *
FROM soundchains
WHERE
    soundchain_id IS NULL
    OR soundchain_id = ''
    OR chain_name IS NULL
    OR chain_name = '';

-- 7. Orphan primary reference links in soundchains
SELECT
    sc.soundchain_id,
    sc.chain_name,
    sc.primary_reference_id
FROM soundchains sc
LEFT JOIN music_references mr
    ON sc.primary_reference_id = mr.reference_id
WHERE
    sc.primary_reference_id IS NOT NULL
    AND sc.primary_reference_id <> 'not_applicable'
    AND mr.reference_id IS NULL;

-- 8. Orphan primary instrument links in soundchains
SELECT
    sc.soundchain_id,
    sc.chain_name,
    sc.primary_instrument_id
FROM soundchains sc
LEFT JOIN equipment e
    ON sc.primary_instrument_id = e.equipment_id
WHERE
    sc.primary_instrument_id IS NOT NULL
    AND sc.primary_instrument_id <> 'not_applicable'
    AND e.equipment_id IS NULL;

-- 9. Orphan output equipment links in soundchains
SELECT
    sc.soundchain_id,
    sc.chain_name,
    sc.output_equipment_id
FROM soundchains sc
LEFT JOIN equipment e
    ON sc.output_equipment_id = e.equipment_id
WHERE
    sc.output_equipment_id IS NOT NULL
    AND sc.output_equipment_id <> 'not_applicable'
    AND e.equipment_id IS NULL;

-- 10. Orphan soundchain-equipment links
SELECT
    se.soundchain_id,
    se.equipment_id
FROM soundchain_equipment se
LEFT JOIN soundchains sc
    ON se.soundchain_id = sc.soundchain_id
LEFT JOIN equipment e
    ON se.equipment_id = e.equipment_id
WHERE
    sc.soundchain_id IS NULL
    OR e.equipment_id IS NULL;

-- 11. Duplicate position within the same soundchain
SELECT
    soundchain_id,
    position_in_chain,
    COUNT(*) AS duplicate_position_count
FROM soundchain_equipment
GROUP BY soundchain_id, position_in_chain
HAVING COUNT(*) > 1;

-- 12. Public sample privacy check
SELECT
    'equipment' AS table_name,
    equipment_id AS item_id,
    privacy_level
FROM equipment
WHERE privacy_level <> 'public_sample'

UNION ALL

SELECT
    'music_references' AS table_name,
    reference_id AS item_id,
    privacy_level
FROM music_references
WHERE privacy_level <> 'public_sample'

UNION ALL

SELECT
    'soundchains' AS table_name,
    soundchain_id AS item_id,
    privacy_level
FROM soundchains
WHERE privacy_level <> 'public_sample';
