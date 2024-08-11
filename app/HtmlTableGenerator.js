/**
 * HtmlTableGenerator.js
 * ------------------------------------------------
 * Author: William Richmond
 * Created on: 08 July 2024
 * File name: HtmlTableGenerator.js
 * Revised: [Add revised date]
 *
 * Description:
 * This module generates HTML tables from given columns and rows.
 * It includes methods to handle table generation, string escaping,
 * and applying functions to each element with their index.
 *
 * Usage:
 * Import this module and use the HtmlTableGenerator class to generate HTML tables.
 *
 * Example:
 * const HtmlTableGenerator = require('./HtmlTableGenerator');
 * const generator = new HtmlTableGenerator();
 * const tableHtml = generator.generateTable(columns, rows, formatter);
 * console.log(tableHtml);
 */

const winston = require('winston');

// Configure winston logger
const logger = winston.createLogger({
    level: 'error',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.printf(({ timestamp, level, message }) => `${timestamp} [${level}]: ${message}`)
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'errors.log' })
    ]
});

class HtmlTableGenerator {
    constructor(transposed = false) {
        this.OUT = {
            output: [],
            append: (str) => {
                this.OUT.output.push(str);
            },
            getOutput: () => {
                return this.OUT.output.join('');
            }
        };
        this.TRANSPOSED = transposed;
        this.NEWLINE = "\n";
    }

    // Apply a function to each element in an array with its index
    eachWithIdx(array, f) {
        try {
            array.forEach((item, idx) => f(item, idx));
        } catch (error) {
            logger.error(`Error in eachWithIdx: ${error.message}`);
        }
    }

    // Map each element in an array to a new array using a function
    mapEach(array, f) {
        try {
            return array.map(f);
        } catch (error) {
            logger.error(`Error in mapEach: ${error.message}`);
            return [];
        }
    }

    // Escape special characters in a string for HTML
    escape(str) {
        try {
            str = str.replace(/\t|\b|\f/g, "");
            str = str.replace(/&/g, "&amp;");
            str = str.replace(/</g, "&lt;");
            str = str.replace(/>/g, "&gt;");
            str = str.replace(/"/g, "&quot;");
            str = str.replace(/'/g, "&#039;");
            str = str.replace(/\r|\n|\r\n/g, "<br/>");
            return str;
        } catch (error) {
            logger.error(`Error in escape: ${error.message}`);
            return str;
        }
    }

    // Check if a string is an HTML tag
    isHTML(str) {
        return /^<.+>$/.test(str);
    }

    // Output arguments to the OUT object
    output(...args) {
        try {
            for (const arg of args) {
                this.OUT.append(arg);
            }
        } catch (error) {
            logger.error(`Error in output: ${error.message}`);
        }
    }

    // Output a row of items in a table with the specified tag
    outputRow(items, tag) {
        try {
            this.output("<tr>");
            items.forEach(item => {
                this.output(`<${tag}>`, this.isHTML(item) ? item : this.escape(item), `</${tag}>`);
            });
            this.output("</tr>", this.NEWLINE);
        } catch (error) {
            logger.error(`Error in outputRow: ${error.message}`);
        }
    }

    // Generate the HTML table
    generateTable(COLUMNS, ROWS, FORMATTER) {
        this.output(`<!DOCTYPE html>${this.NEWLINE}
<html lang="en">${this.NEWLINE}
<head>${this.NEWLINE}
<title></title>${this.NEWLINE}
<meta charset="UTF-8">${this.NEWLINE}
<style>${this.NEWLINE},
table { border-collapse: collapse; }${this.NEWLINE},
th, td { border: 1px solid black; }${this.NEWLINE}
</style>${this.NEWLINE}
</head>${this.NEWLINE}
<body>${this.NEWLINE}
<table>${this.NEWLINE}`);

        try {
            if (this.TRANSPOSED) {
                // Handle transposed table
                const values = this.mapEach(COLUMNS, col => [col.name()]);
                this.eachWithIdx(ROWS, (row) => {
                    this.eachWithIdx(COLUMNS, (col, i) => {
                        values[i].push(FORMATTER.format(row, col));
                    });
                });
                this.eachWithIdx(COLUMNS, (_, i) => {
                    this.outputRow(values[i], "td");
                });
            } else {
                // Handle regular table
                this.outputRow(this.mapEach(COLUMNS, col => col.name()), "th");
                this.eachWithIdx(ROWS, (row) => {
                    this.outputRow(this.mapEach(COLUMNS, col => FORMATTER.format(row, col)), "td");
                });
            }
        } catch (error) {
            logger.error(`Error in generating table rows: ${error.message}`);
        }

        this.output(`</table>${this.NEWLINE}
</body>${this.NEWLINE}
</html>${this.NEWLINE}`);

        return this.OUT.getOutput();
    }
}

module.exports = HtmlTableGenerator;
