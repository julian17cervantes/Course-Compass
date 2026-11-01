import { useEffect, useState } from "react";
import AuthForm from "./AuthForm";
import CourseForm from "./CourseForm";
import CourseTable from "./CourseTable";
import { createCourse, deleteCourse, getToken, listCourses, logout, updateCourse } from "./api";

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

  const sorted = courses ? [...courses].sort((a, b) => a.id - b.id) : [];
  const semesters = [...new Set(sorted.map((c) => c.semester))];

  async function handleAdd(course) {
    const created = await createCourse(course);
    setCourses((list) => [...list, created]);
  }

  async function handleGrade(course, grade) {
    setError("");
    try {
      const updated = await updateCourse(course.id, { grade });
      setCourses((list) => list.map((c) => (c.id === updated.id ? updated : c)));
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(course) {
    if (!window.confirm(`Delete ${course.code}?`)) return;
    setError("");
    try {
      await deleteCourse(course.id);
      setCourses((list) => list.filter((c) => c.id !== course.id));
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="card wide">
      <div className="header">
        <h1>Course Compass</h1>
        <button
          type="button"
          className="secondary"
          onClick={() => {
            logout();
            setSignedIn(false);
            setCourses(null);
            setError("");
          }}
        >
          Log out
        </button>
      </div>
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
      <h2>Add a course</h2>
      <CourseForm onAdd={handleAdd} semesters={semesters} />
      <h2>Your courses</h2>
      {courses === null ? (
        <p className="muted">Loading your courses...</p>
      ) : (
        <CourseTable courses={sorted} onGrade={handleGrade} onDelete={handleDelete} />
      )}
    </main>
  );
}