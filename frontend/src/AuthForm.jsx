import { useState } from "react";
import { login, signup } from "./api";

export default function AuthForm({ onSuccess }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const isSignup = mode === "signup";

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      if (isSignup) await signup(email.trim(), password);
      await login(email.trim(), password);
      onSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="card">
      <h1>Course Compass</h1>
      <p className="muted">Track your courses and plan your GPA.</p>
      <form onSubmit={handleSubmit}>
        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete={isSignup ? "new-password" : "current-password"}
            minLength={isSignup ? 8 : undefined}
            required
          />
        </label>
        {error && (
          <p className="error" role="alert">
            {error}
          </p>
        )}
        <button type="submit" disabled={busy}>
          {busy ? "Please wait..." : isSignup ? "Create account" : "Log in"}
        </button>
      </form>
      <button
        type="button"
        className="link"
        onClick={() => {
          setMode(isSignup ? "login" : "signup");
          setError("");
        }}
      >
        {isSignup ? "I already have an account" : "Create an account"}
      </button>
    </main>
  );
}