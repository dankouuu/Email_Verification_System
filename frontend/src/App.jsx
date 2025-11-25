import React from 'react';
import { Link } from 'react-router-dom';

export default function App() {
	return (
		<div style={{ padding: 32 }}>
			<h1>Email Verification Showcase</h1>
			<nav>
				<Link to="/send">Send Verification Email</Link> |{' '}
				<Link to="/verify">Verify Email</Link>
			</nav>
		</div>
	);
}
