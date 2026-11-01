import { useState } from "react";
import { GRADES } from "./grades";

const EMPTY = { name: "", code: "", units: "3", semester: "", grade: "" };

export default function CourseForm({ onAdd, semesters }) {
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const set = (field) => (event) => {
    const value = event.target.value;
    setForm((current) => ({ ...current, [field]: value }));
  };

  async function handleSubmit(event) {
    event.preventDefault();
    const name = form.name.trim();
    const code = form.code.trim();
    const semester = form.semester.trim();
    const units = Number(form.units);
    if (!name || !code || !semester) {
      setError("Name, code, and semester are required.");
      return;
    }
    if (!Number.isFinite(units) || units <= 0) {
      setError("Units must be a number greater than 0.");
      return;
    }
    setError("");
    setBusy(true);
    try {
      await onAdd({ name, code, units, semester, grade: form.grade || null });
      setForm({ ...EMPTY, semester }); // keep the semester, so adding several courses is quick
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="course-form" onSubmit={handleSubmit}>
      <label>
        Code
        <input value={form.code} onChange={set("code")} placeholder="CS101" required />
      </label>
      <label>
        Name
        <input value={form.name} onChange={set("name")} placeholder="Intro to Programming" required />
      </label>
      <label>
        Semester
        <input
          value={form.semester}
          onChange={set("semester")}
          list="semester-options"
          placeholder="Fall 2025"
          required
        />
        <datalist id="semester-options">
          {semesters.map((s) => (
            <option key={s} value={s} />
          ))}
        </datalist>
      </label>
      <label>
        Units
        <input type="number" min="0.5" step="0.5" value={form.units} onChange={set("units")} required />
      </label>
      <label>
        Grade
        <select value={form.grade} onChange={set("grade")}>
          <option value="">Not graded yet</option>
          {GRADES.map((g) => (
            <option key={g} value={g}>
              {g}
            </option>
          ))}
        </select>
      </label>
      <button type="submit" disabled={busy}>
        {busy ? "Adding..." : "Add course"}
      </button>
      {error && (
        <p className="error full" role="alert">
          {error}
        </p>
      )}
    </form>
  );
}