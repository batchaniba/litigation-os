import React, { useState } from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { Modal } from './Modal';

describe('Modal', () => {
  it('provides dialog semantics and closes with Escape', async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();
    render(
      <Modal isOpen onClose={onClose} title="Deadline details">
        <a href="#filing">View filing</a>
      </Modal>,
    );

    expect(screen.getByRole('dialog', { name: 'Deadline details' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Close' })).toHaveFocus();
    await user.keyboard('{Escape}');
    expect(onClose).toHaveBeenCalledOnce();
  });

  it('traps keyboard focus and restores it after closing', async () => {
    const user = userEvent.setup();

    function Harness() {
      const [open, setOpen] = useState(false);
      return (
        <>
          <button onClick={() => setOpen(true)}>Open details</button>
          <Modal isOpen={open} onClose={() => setOpen(false)} title="Details">
            <button>First action</button>
          </Modal>
        </>
      );
    }

    render(<Harness />);
    const trigger = screen.getByRole('button', { name: 'Open details' });
    await user.click(trigger);
    const close = screen.getByRole('button', { name: 'Close' });
    const action = screen.getByRole('button', { name: 'First action' });
    expect(close).toHaveFocus();
    await user.tab({ shift: true });
    expect(action).toHaveFocus();
    await user.tab();
    expect(close).toHaveFocus();
    await user.click(close);
    expect(trigger).toHaveFocus();
  });

  it('is absent from the accessibility tree when closed', () => {
    render(<Modal isOpen={false} onClose={vi.fn()} title="Hidden" />);
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});