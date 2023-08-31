// Run in terminal with 'node generateJsonData.js'
// Workaround to generate js file from json files to display on dashboard
// This will be changed in the furutre when we set up a proper database

const fs = require('fs');
const path = require('path');

const dirPath = '../data/data_warehouse/mit/articles'
const jsonData = [];

fs.readdirSync(dirPath).forEach((file) => {
  const filePath = path.join(dirPath, file);
  const fileData = fs.readFileSync(filePath, 'utf-8');
  const parsedData = JSON.parse(fileData);
  jsonData.push(parsedData);
});

// We could also put this in data_warehouse
const generatedContent = `// File generated with app/src/generateJsonData.js\nexport default ${JSON.stringify(jsonData, null, 2)};`;
fs.writeFileSync('./src/aggregated_articles.js', generatedContent);