import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SendEmailPage from './SendEmailPage';

beforeEach(() => {
  global.fetch = jest.fn();
});
afterEach(() => {
  jest.resetAllMocks();
});

describe('SendEmailPage', () => {
  it('shows error for invalid email', () => {
    render(<SendEmailPage />);
    fireEvent.change(screen.getByPlaceholderText(/enter your email/i), {
      target: { value: 'notanemail' },
    });
    fireEvent.click(screen.getByText(/send/i));
    expect(screen.getByText(/please enter a valid email/i)).toBeInTheDocument();
  });

  it('shows loading and success message', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });
    render(<SendEmailPage />);
    fireEvent.change(screen.getByPlaceholderText(/enter your email/i), {
      target: { value: 'user@example.com' },
    });
    fireEvent.click(screen.getByText(/send/i));
    expect(screen.getByText(/sending/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/verification link was sent/i)).toBeInTheDocument());
  });

  it('shows network error and retry button', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));
    render(<SendEmailPage />);
    fireEvent.change(screen.getByPlaceholderText(/enter your email/i), {
      target: { value: 'user@example.com' },
    });
    fireEvent.click(screen.getByText(/send/i));
    await waitFor(() => expect(screen.getByText(/network error/i)).toBeInTheDocument());
    expect(screen.getByText(/retry/i)).toBeInTheDocument();
  });
});
