CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, surname, phone
    FROM contacts
    WHERE name ILIKE '%' || pattern || '%'
       OR surname ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, surname, phone
    FROM contacts
    ORDER BY id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;