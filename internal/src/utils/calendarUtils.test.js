import { describe, expect, it } from 'vitest';
import {
  buildMonthGrid,
  dayKey,
  groundEventDate,
  groupEventsByDay,
  isGroundedDate,
  parseMatterNumbers,
} from './calendarUtils';

describe('calendar utilities', () => {
  it('accepts only dates that identify one calendar day', () => {
    expect(isGroundedDate('Mar. 27, 2026')).toBe(true);
    expect(isGroundedDate('~July 9, 2026')).toBe(true);
    expect(isGroundedDate('Jul. 9-10, 2026')).toBe(false);
    expect(isGroundedDate('Mid-2026')).toBe(false);
  });

  it('grounds exact portfolio dates to the expected day key', () => {
    expect(dayKey(groundEventDate('Mar. 27, 2026'))).toBe('2026-03-27');
    expect(groundEventDate('July 2026')).toBeNull();
  });

  it('builds a stable Sunday-first six-week month grid', () => {
    const grid = buildMonthGrid(2026, 2);
    expect(grid).toHaveLength(42);
    expect(grid[0]).toMatchObject({ key: '2026-03-01', inMonth: true });
    expect(grid[41]).toMatchObject({ key: '2026-04-11', inMonth: false });
  });

  it('groups exact dates and preserves ungroundable events', () => {
    const exact = { date: 'Mar. 27, 2026', event: 'Hearing' };
    const range = { date: 'Mar. 27-28, 2026', event: 'Trial range' };
    const result = groupEventsByDay([exact, range]);
    expect(result.byDay.get('2026-03-27')).toEqual([exact]);
    expect(result.ungrounded).toEqual([range]);
  });

  it('parses individual and portfolio-wide matter references', () => {
    expect(parseMatterNumbers('9, 6, bad, 15')).toEqual({
      all: false,
      numbers: [9, 6, 15],
      label: '9, 6, bad, 15',
    });
    expect(parseMatterNumbers('All CDCR')).toEqual({
      all: true,
      numbers: [],
      label: 'All CDCR',
    });
  });
});
