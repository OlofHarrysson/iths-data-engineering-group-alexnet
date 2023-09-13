import React, { useState, useEffect } from 'react';
import { Client } from 'pg';

function ArticleListComponent() {
  const [jsonData, setJsonData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const client = new Client({
        user: 'TODO',
        host: 'TODO',
        database: 'airflow',
        password: 'airflow',
        port: 5432,
      });

      try {
        await client.connect();

        // TODO: Add search query here

        // TODO: Update default query
        const query = 'SELECT * FROM articles ORDER BY published DESC LIMIT 15';

        const result = await client.query(query);

        const data = result.rows; // TODO: Make sure the table schema matches JSON structure
        setJsonData(data);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        await client.end();
      }
    }

    fetchData();
  }, []); // Empty dependency array to run the effect once on component mount

  return (
    <div className="card-space">
      {jsonData.map((item, index) => (
        <ArticleCard key={index} item={item} />
      ))}
    </div>
  );
}

export default ArticleListComponent;
