CREATE TABLE bloginfo (
    unique_id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    link VARCHAR(255),
    blog_text TEXT,
    blog VARCHAR(255),
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

ALTER TABLE blog_summaries
ADD CONSTRAINT fk_blog_summaries_unique_id
FOREIGN KEY (unique_id)
REFERENCES bloginfo(unique_id);

