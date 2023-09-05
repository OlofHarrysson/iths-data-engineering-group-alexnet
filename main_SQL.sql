CREATE TABLE bloginfo (
    unique_id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    link VARCHAR(255),
    blog_text TEXT,
    published DATE,
    timestamp TIMESTAMP
);

CREATE TABLE blog_summaries (
    unique_id VARCHAR(255) PRIMARY KEY,
    translated_title VARCHAR(255),
    summary TEXT,
    type_of_summary VARCHAR(255) DEFAULT 'DefaultSummaryType'
);

