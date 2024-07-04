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
            append: function (str) {
                this.output.push(str);
            },
            getOutput: function () {
                return this.output.join('');
            }
        };
        this.TRANSPOSED = transposed;
        this.NEWLINE = "\n";
    }

    // Apply a function to each element in an iterable with its index
    eachWithIdx(iterable, f) {
        try {
            const i = iterable.iterator();
            let idx = 0;
            while (i.hasNext()) {
                f(i.next(), idx++);
            }
        } catch (error) {
            logger.error(`Error in eachWithIdx: ${error.message}`);
        }
    }

    // Map each element in an iterable to a new array using a function
    mapEach(iterable, f) {
        try {
            const vs = [];
            this.eachWithIdx(iterable, function (i) {
                vs.push(f(i));
            });
            return vs;
        } catch (error) {
            logger.error(`Error in mapEach: ${error.message}`);
            return [];
        }
    }

    // Escape special characters in a string for XML
    escape(str) {
        try {
            str = str.replace(/\t|\b|\f/g, "");
            str = com.intellij.openapi.util.text.StringUtil.escapeXml(str);
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
            for (const item of items) {
                this.output(`<${tag}>`, this.isHTML(item) ? item : this.escape(item), `</${tag}>`);
            }
            this.output("</tr>", this.NEWLINE);
        } catch (error) {
            logger.error(`Error in outputRow: ${error.message}`);
        }
    }

    // Generate the HTML table
    generateTable(COLUMNS, ROWS, FORMATTER) {
        this.output(`<!DOCTYPE html>${this.NEWLINE}
<html>${this.NEWLINE}
<head>${this.NEWLINE}
<title></title>${this.NEWLINE}
<meta charset="UTF-8">${this.NEWLINE}
</head>${this.NEWLINE}
<body>${this.NEWLINE}
<table border="1" style="border-collapse:collapse">${this.NEWLINE}`);

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
