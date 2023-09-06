CREATE TABLE bloginfo (
    unique_id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    link VARCHAR(255),
    blog_text TEXT,
    blog_name VARCHAR(255),
    published DATE,
    timestamp TIMESTAMP
);

CREATE TABLE blog_summaries (
    summary_id SERIAL PRIMARY KEY,
    unique_id VARCHAR(255) REFERENCES bloginfo(unique_id),
    translated_title VARCHAR(255),
    summary TEXT,
    type_of_summary VARCHAR(255) DEFAULT 'DefaultSummaryType',
    CONSTRAINT unique_summary_per_type UNIQUE (unique_id, type_of_summary)
);

SELECT bi.*
FROM bloginfo bi
LEFT JOIN blog_summaries bs ON bi.unique_id = bs.unique_id
WHERE bs.unique_id IS NULL
ORDER BY bi.timestamp DESC;