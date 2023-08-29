// testing json batch reading
const fs = require('fs');
const path = require('path');

function readJSONFilesFromDir(dirPath) {
  const files = fs.readdirSync(dirPath);
  const jsonData = [];

  files.forEach((file) => {
    const filePath = path.join(dirPath, file);
    const fileData = fs.readFileSync(filePath, 'utf-8');
    const parsedData = JSON.parse(fileData);
    jsonData.push(parsedData);
  });

  return jsonData;
}

module.exports = readJSONFilesFromDir;
