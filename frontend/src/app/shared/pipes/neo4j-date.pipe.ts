import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'neo4jDate',
  standalone: true
})
export class Neo4jDatePipe implements PipeTransform {
  transform(value: unknown): Date | null {
    if (value == null) return null;
    if (value instanceof Date) return value;
    if (typeof value !== 'string') return null;

    const input = value.trim();
    if (!input) return null;

    const match = input.match(
      /^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(\.\d+)?(Z|[+-]\d{2}:\d{2})?$/
    );

    if (!match) {
      const parsed = Date.parse(input);
      return Number.isNaN(parsed) ? null : new Date(parsed);
    }

    const base = match[1];
    const fraction = match[2] || '';
    const tz = match[3] || 'Z';

    let milliseconds = '';
    if (fraction) {
      const digits = fraction.slice(1);
      const ms = (digits + '000').slice(0, 3);
      milliseconds = `.${ms}`;
    }

    const normalized = `${base}${milliseconds}${tz}`;
    const parsed = Date.parse(normalized);
    return Number.isNaN(parsed) ? null : new Date(parsed);
  }
}

