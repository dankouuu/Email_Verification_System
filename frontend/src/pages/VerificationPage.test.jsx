import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import VerificationPage from './VerificationPage';

// Mock fetch globally
beforeEach(() => {
  global.fetch = jest.fn();
  window.history.pushState({}, '', '/verify?token=abc');
});
afterEach(() => {
  jest.resetAllMocks();
});

describe('VerificationPage', () => {
  it('shows loading and success message', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ detail: 'Email verified.' }),
    });
    render(<VerificationPage />);
    expect(screen.getByText(/prebieha overovanie/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/email verified/i)).toBeInTheDocument());
  });

  it('shows backend error', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Token expired.' }),
    });
    render(<VerificationPage />);
    await waitFor(() => expect(screen.getByText(/token expired/i)).toBeInTheDocument());
  });

  it('shows network error and retry button', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));
    render(<VerificationPage />);
    await waitFor(() => expect(screen.getByText(/network error/i)).toBeInTheDocument());
    expect(screen.getByText(/retry/i)).toBeInTheDocument();
    // Simulate retry
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ detail: 'Email verified.' }),
    });
    fireEvent.click(screen.getByText(/retry/i));
    await waitFor(() => expect(screen.getByText(/email verified/i)).toBeInTheDocument());
  });
});
