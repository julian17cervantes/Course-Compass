import { useCallback, useEffect, useRef, useState } from "react";
import AuthForm from "./AuthForm";
import CourseForm from "./CourseForm";
import CourseTable from "./CourseTable";
import GoalPlanner from "./GoalPlanner";
import GpaSummary from "./GpaSummary";
import { GRADES } from "./grades";
import {
  createCourse,
  deleteCourse,
  getGoalPlan,
  getGpa,
  getToken,
  listCourses,
  logout,
  setGoal,
  updateCourse,
} from "./api";

export default function App() {
  const [signedIn, setSignedIn] = useState(Boolean(getToken()));
  const [courses, setCourses] = useState(null);
  const [gpa, setGpa] = useState(null);
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState("");
  const latestSummary = useRef(0);

  const refreshSummary = useCallback(async () => {
    const id = ++latestSummary.current;
    try {
      const [gpaData, planData] = await Promise.all([getGpa(), getGoalPlan()]);
      if (id !== latestSummary.current) return; // a newer request has started
      setGpa(gpaData);
      setPlan(planData);
    } catch (err) {
      if (id === latestSummary.current) setError(err.message);
    }
  }, []);

  const reset = useCallback(() => {
    latestSummary.current += 1; // ignore any request still in flight
    setSignedIn(false);
    setCourses(null);
    setGpa(null);
    setPlan(null);
    setError("");
  }, []);

  useEffect(() => {
    window.addEventListener("cc-logout", reset);
    return () => window.removeEventListener("cc-logout", reset);
  }, [reset]);

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
    refreshSummary();
    return () => {
      cancelled = true;
    };
  }, [signedIn, refreshSummary]);

  if (!signedIn) return <AuthForm onSuccess={() => setSignedIn(true)} />;

  const sorted = courses ? [...courses].sort((a, b) => a.id - b.id) : [];
  const semesters = [...new Set(sorted.map((c) => c.semester))];
  const gradedSemesters = new Set(
    sorted.filter((c) => GRADES.includes(c.grade)).map((c) => c.semester),
  );

  async function handleAdd(course) {
    const created = await createCourse(course);
    setCourses((list) => [...list, created]);
    refreshSummary();
  }

  async function handleGrade(course, grade) {
    setError("");
    try {
      const updated = await updateCourse(course.id, { grade });
      setCourses((list) => list.map((c) => (c.id === updated.id ? updated : c)));
      refreshSummary();
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
      refreshSummary();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleGoal(goal) {
    await setGoal(goal);
    await refreshSummary();
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
            reset();
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

      <div className="panels">
        <section>
          <h2>Your GPA</h2>
          <GpaSummary gpa={gpa} gradedSemesters={gradedSemesters} />
        </section>
        <section>
          <h2>Goal planner</h2>
          <GoalPlanner plan={plan} loaded={gpa !== null} onSave={handleGoal} />
        </section>
      </div>

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