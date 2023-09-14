// Run this in terminal with 'node generateJsonData.js'

// Workaround to generate js file from json files to display on dashboard
// This will be changed in the future when we set up a proper database

// IMPORTANT!
// The 'fs' module is a built-in Node.js module and is not available in standard web browsers.
// 'fs' is only intended for server-side file system operations!
// If we try to use 'fs' in a browser-based JavaScript script, it won't work!!
// So we gotta call this function somewhere else (maybe through python??), or entirely change it.
// IF we decide to rewrite it, we could use Fetch API instead.
// https://www.w3schools.com/jsref/api_fetch.asp

const fs = require('fs');
const path = require('path');

function aggregateArticles(dirPath) {
  const startTime = new Date();

  const jsonData = [];

  console.log(`Aggregating articles from ${dirPath}`);

  fs.readdirSync(dirPath)
    .map((file) => {
      const filePath = path.join(dirPath, file);
      const fileData = fs.readFileSync(filePath, 'utf-8');
      const parsedData = JSON.parse(fileData);
      return { filePath, parsedData };
    })
    .sort((a, b) => new Date(b.parsedData.published) - new Date(a.parsedData.published))
    .slice(0, 15)
    .forEach(({ parsedData }) => {
      jsonData.push(parsedData);
    });

  const endTime = new Date();
  const timeForFunctionToComplete = endTime - startTime;

  const generatedContent = `// File generated with app/src/generateJsonData.js\nexport default ${JSON.stringify(jsonData, null, 2)};`;
  fs.writeFileSync('aggregated_articles.js', generatedContent);

  console.log(`Done in ${timeForFunctionToComplete} ms`);

}

const dirPath = '../../../data/data_warehouse/mit/articles';

aggregateArticles(dirPath);