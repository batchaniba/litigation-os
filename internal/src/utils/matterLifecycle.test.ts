import { describe, expect, it } from 'vitest';
import type { MatterSummary } from '../types/portfolio';
import {
  archivedFromLifecycle,
  isArchivedMatter,
  isLiveLifecycle,
  isOpenLifecycle,
  isTerminalLifecycle,
  lifecycleLabel,
  MATTER_LIFECYCLES,
} from './matterLifecycle';

describe('matter lifecycle helpers', () => {
  it('classifies every supported lifecycle consistently', () => {
    expect(MATTER_LIFECYCLES).toHaveLength(6);
    expect(isOpenLifecycle('settled')).toBe(true);
    expect(isLiveLifecycle('settled')).toBe(false);
    expect(isLiveLifecycle('pre_filing')).toBe(true);
    expect(isTerminalLifecycle('dismissed')).toBe(true);
    expect(isOpenLifecycle(undefined)).toBe(false);
  });

  it('prefers lifecycle over the legacy archived flag', () => {
    expect(isArchivedMatter({ lifecycle: 'active', archived: true })).toBe(false);
    expect(isArchivedMatter({ lifecycle: 'closed', archived: false })).toBe(true);
    const legacyMatter = { archived: true } as Pick<MatterSummary, 'lifecycle' | 'archived'>;
    expect(isArchivedMatter(legacyMatter)).toBe(true);
  });

  it.each([
    ['active', 'Active', false],
    ['pre_filing', 'Pre-filing', false],
    ['settled', 'Settled', false],
    ['dismissed', 'Dismissed', true],
    ['abandoned', 'Abandoned', true],
    ['closed', 'Closed', true],
  ] as const)('labels and archives %s', (lifecycle, label, archived) => {
    expect(lifecycleLabel(lifecycle)).toBe(label);
    expect(archivedFromLifecycle(lifecycle)).toBe(archived);
  });
});
