deal_date_create_SQL_SCRIPT = '''
CREATE TABLE bitrix.deals_on_datecreated (
    deal_id BIGINT PRIMARY KEY,
    contact_id BIGINT,
    stage_id TEXT,
    close_date DATE,
    date_create DATE,
    date_modify DATE,
    category_id INTEGER,
    source_id TEXT,
    semantic_id TEXT,
    created_by_id BIGINT,
    blank_url TEXT,
    department_id BIGINT
);
'''