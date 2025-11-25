
import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

function validateEmail(email) {
	return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
}


export default function SendEmailPage() {
	const [email, setEmail] = useState('');
	const [loading, setLoading] = useState(false);
	const [message, setMessage] = useState('');
	const [error, setError] = useState('');
	const [networkError, setNetworkError] = useState(false);

	const handleSubmit = async (e) => {
		e.preventDefault();
		setMessage('');
		setError('');
		setNetworkError(false);
		if (!validateEmail(email)) {
			setError('Please enter a valid email address.');
			return;
		}
		setLoading(true);
		try {
			const res = await fetch(`${API_BASE_URL}/verification/send/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email }),
			});
			const data = await res.json();
			if (res.ok) {
				setMessage('If the email exists, a verification link was sent.');
			} else {
				setError(data.detail || 'An error occurred.');
			}
		} catch {
			setError('Network error. Please try again.');
			setNetworkError(true);
		} finally {
			setLoading(false);
		}
	};

	return (
		<div style={{ padding: 32 }}>
			<h2>Send Verification Email</h2>
			<form onSubmit={handleSubmit} aria-label="Send verification email form">
				<label htmlFor="email-input">Email address</label>
				<input
					id="email-input"
					type="email"
					placeholder="Enter your email"
					value={email}
					onChange={e => setEmail(e.target.value)}
					required
					aria-required="true"
					aria-describedby={error ? "email-error" : undefined}
				/>
				<button type="submit" disabled={loading} style={{ marginLeft: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
					{loading && (
						<span className="spinner" style={{ width: 16, height: 16, border: '3px solid #ccc', borderTop: '3px solid #333', borderRadius: '50%', display: 'inline-block', animation: 'spin 1s linear infinite' }} />
					)}
					{loading ? 'Sending...' : 'Send'}
				</button>
			</form>
			{message && <p style={{ color: 'green', marginTop: 16 }} role="status">{message}</p>}
			{error && (
				<>
					<p id="email-error" style={{ color: 'red', marginTop: 16 }} role="alert">{error}</p>
					{networkError && (
						<button onClick={handleSubmit} style={{ marginTop: 8 }}>Retry</button>
					)}
				</>
			)}
			<style>{`
				@keyframes spin {
					0% { transform: rotate(0deg); }
					100% { transform: rotate(360deg); }
				}
			`}</style>
		</div>
	);
}
