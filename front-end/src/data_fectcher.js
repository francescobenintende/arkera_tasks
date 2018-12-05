import data from './data.csv';

function readTextFile(file, callback) {
    const req = new XMLHttpRequest();
    req.open("GET", file, true);
    req.addEventListener('load', () => {
        if (req.readyState === 4) {
            if (req.status === 200 || req.status === 0) {
                const text = req.responseText;
                callback(text);
            }
        }
    });
    req.send();
}


function getHeaders(lines) {
    let newLineFound = false;
    let amInQuotes = false;
    let h = 0;

    while (!newLineFound) {
        const currentLine = lines[h];
        for (let i = 0; i < currentLine.length; i++) {
            const currentChar = currentLine[i];
            if (currentChar === '"' || currentChar === '\'') {
                amInQuotes = !amInQuotes;
            }
        }
        if (!amInQuotes) {
            newLineFound = true;
        }
        h++;
    }

    const headerRows = lines.splice(0, h);
    const headerRow = headerRows.join(' ');
    const headerRowWithoutQuotes = headerRow.replace(/"/g, '');
    const headers = headerRowWithoutQuotes.split(',');
    const cleanedHeaders = headers.map((header) => {
        return header.trim();
    });

    return cleanedHeaders;
}


function generateJSON(lines, headers) {
    const result = [];
    for (let i = 0; i < lines.length; i++) {
        const obj = {};
        const currentLine = lines[i].match(/(".*?"|[^",]+)(?=\s*,|\s*$)/g);

        for (let j = 0; j < headers.length; j++) {
            const currentString = currentLine[j].replace(/,|"/g, '');
            const numericValue = parseInt(currentString);
            if (isNaN(numericValue)) {
                obj[headers[j]] = currentString;
            } else {
                obj[headers[j]] = numericValue;
            }
        }
        result.push(obj);
    }
    return result;
}


function getColumnWidth (headerText, lines) {
    let max = 0;
    let min = 100;
    const padding = 10;


    for (let i = 0; i < lines.length; i++) {
        if (lines[i] !== undefined && lines[i][headerText] !== null) {
            if (JSON.stringify(lines[i][headerText]).length > max) {
                max = JSON.stringify(lines[i][headerText]).length;
            }
        }
    }

    return Math.max(min, Math.max(max, JSON.stringify(headerText).length ) * padding);
}


function getHeadersForTable(headers, lines) {
    const headersForTable = [];
    for (let i = 0; i < headers.length; i++) {
        const headerForTable = {
            Header: headers[i],
            accessor: headers[i],
            minWidth: getColumnWidth(headers[i], lines)
        };
        headersForTable.push(headerForTable);
    }
    return headersForTable;
}


function csvToJSON(csv, callback) {
    const lines = csv.split("\n");

    const headers = getHeaders(lines);
    const cities = generateJSON(lines, headers);

    const headersForTable = getHeadersForTable(headers, cities);

    callback(headersForTable, cities);
}


export function getCitiesData(callback) {
    readTextFile(data, (text) => {
        csvToJSON(text, (headers, json) => {
            callback(headers, json)
        });
    });
}
