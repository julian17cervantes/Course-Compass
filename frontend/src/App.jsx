import { useEffect, useState } from "react";
import AuthForm from "./AuthForm";
import { getToken, listCourses, logout } from "./api";

export default function App() {
  const [signedIn, setSignedIn] = useState(Boolean(getToken()));
  const [courses, setCourses] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const onLogout = () => {
      setSignedIn(false);
      setCourses(null);
    };
    window.addEventListener("cc-logout", onLogout);
    return () => window.removeEventListener("cc-logout", onLogout);
  }, []);

  useEffect(() => {
    if (!signedIn) return;
    let cancelled = false;
    listCourses()
      .then((data) => {
        if (!cancelled) setCourses(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      });
    return () => {
      cancelled = true;
    };
  }, [signedIn]);

  if (!signedIn) return <AuthForm onSuccess={() => setSignedIn(true)} />;

  return (
    <main className="card">
      <h1>Course Compass</h1>
      <p>You're signed in.</p>
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
      <p className="muted">
        {courses === null ? "Loading your courses..." : `You have ${courses.length} course(s).`}
      </p>
      <button
        type="button"
        onClick={() => {
          logout();
          setSignedIn(false);
          setCourses(null);
          setError("");
        }}
      >
        Log out
      </button>
    </main>
  );
}