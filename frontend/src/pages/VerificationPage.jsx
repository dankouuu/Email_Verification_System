

/**
 * Email verification page component.
 * Handles verifying the token from the URL, displays loading, error, and success states,
 * and provides navigation after successful verification.
 */
export default function VerificationPage() {
	// State variables for loading, result, error, and network error
	const [loading, setLoading] = useState(true);
	const [result, setResult] = useState('');
	const [error, setError] = useState('');
	const [networkError, setNetworkError] = useState(false);
	const navigate = useNavigate();

	/**
	 * Attempts to verify the token from the URL by making a POST request to the backend.
	 * Handles loading, error, and network error states.
	 */
	const verifyToken = () => {
		setLoading(true);
		setResult('');
		setError('');
		setNetworkError(false);
		const params = new URLSearchParams(window.location.search);
		const token = params.get('token');
		if (!token) {
			setError('No token provided.');
			setLoading(false);
			return;
		}
		fetch(`${API_BASE_URL}/verification/verify/`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ token }),
		})
			.then(res => res.json().then(data => ({ ok: res.ok, data })))
			.then(({ ok, data }) => {
				if (ok) setResult(data.detail);
				else setError(data.detail || 'Verification failed.');
			})
			.catch(() => {
				setError('Network error. Please try again.');
				setNetworkError(true);
			})
			.finally(() => setLoading(false));
	};

	// On mount, attempt to verify the token
	useEffect(() => {
		verifyToken();
		// eslint-disable-next-line
	}, []);

	// Redirect to home after successful verification (2.5s delay)
	useEffect(() => {
		if (result) {
			const timeout = setTimeout(() => {
				navigate('/');
			}, 2500);
			return () => clearTimeout(timeout);
		}
	}, [result, navigate]);

	// Render UI: loading spinner, result, error, and navigation options
	return (
		<div style={{ padding: 32 }}>
			<h2>Email Verification</h2>
			{/* Loading spinner */}
			{loading && (
				<div role="status" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
					<span className="spinner" style={{ width: 18, height: 18, border: '3px solid #ccc', borderTop: '3px solid #333', borderRadius: '50%', display: 'inline-block', animation: 'spin 1s linear infinite' }} />
					Prebieha overovanie…
				</div>
			)}
			{/* Success message and navigation */}
			{!loading && result && (
				<>
					<p style={{ color: 'green' }} role="status">{result}</p>
					<button onClick={() => navigate('/')} style={{ marginTop: 12 }}>Go Home</button>
					<div style={{ fontSize: 12, color: '#555', marginTop: 4 }}>
						You will be redirected automatically.
					</div>
				</>
			)}
			{/* Error message and retry option */}
			{!loading && error && (
				<>
					<p style={{ color: 'red' }} role="alert">{error}</p>
					{networkError && (
						<button onClick={verifyToken} style={{ marginTop: 8 }}>Retry</button>
					)}
				</>
			)}
			{/* Spinner animation style */}
			<style>{`
				@keyframes spin {
					0% { transform: rotate(0deg); }
					100% { transform: rotate(360deg); }
				}
			`}</style>
		</div>
	);
}
