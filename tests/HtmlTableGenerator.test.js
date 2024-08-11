/**
 * Unit tests for the HtmlTableGenerator class.
 *
 * These tests verify that the HtmlTableGenerator correctly generates tables
 * with the appropriate headers and data, handles empty columns and rows gracefully,
 * and logs errors when the eachWithIdx method fails.
 */

import { expect } from 'chai';
import sinon from 'sinon';
import HtmlTableGenerator from '../app/HtmlTableGenerator.js';  // Adjust the path as necessary

/**
 * Unit tests for the HtmlTableGenerator class.
 */
describe('HtmlTableGenerator', function () {
    let tableGenerator;
    let COLUMNS;
    let ROWS;
    let FORMATTER;

    beforeEach(function () {
        tableGenerator = new HtmlTableGenerator(false);

        // Mock data for COLUMNS, ROWS, and FORMATTER
        COLUMNS = [
            { name: () => 'Column1' },
            { name: () => 'Column2' }
        ];
        ROWS = [
            { data: 'Row1' },
            { data: 'Row2' }
        ];
        FORMATTER = {
            format: (row, col) => `${row.data}-${col.name()}`
        };
    });

    /**
     * Test that the table generator creates correct headers.
     */
    it('should generate a table with correct headers', function () {
        const output = tableGenerator.generateTable(COLUMNS, ROWS, FORMATTER);
        expect(output).to.include('<th>Column1</th>');
        expect(output).to.include('<th>Column2</th>');
    });

    /**
     * Test that the table generator creates correct data cells.
     */
    it('should generate a table with correct data', function () {
        const output = tableGenerator.generateTable(COLUMNS, ROWS, FORMATTER);
        expect(output).to.include('<td>Row1-Column1</td>');
        expect(output).to.include('<td>Row2-Column2</td>');
    });

    /**
     * Test that the table generator handles empty columns and rows gracefully.
     */
    it('should handle empty columns and rows gracefully', function () {
        const output = tableGenerator.generateTable([], [], FORMATTER);
        expect(output).to.include('<table');
        expect(output).to.include('</table>');
    });

    /**
     * Test that the table generator logs an error if eachWithIdx fails.
     */
    it('should log an error if eachWithIdx fails', function () {
        const spy = sinon.spy(console, 'error');
        tableGenerator.eachWithIdx(null, () => {});
        expect(spy.calledOnce).to.be.true;
        spy.restore();
    });
});
