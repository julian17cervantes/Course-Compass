export default function GpaSummary({ gpa, gradedSemesters }) {
  if (gpa === null) return <p className="muted">Calculating your GPA...</p>;

  const hasGrades = gradedSemesters.size > 0;
  const semesters = Object.entries(gpa.by_semester).filter(([name]) => gradedSemesters.has(name));

  return (
    <div>
      <div className="stat">
        <span className="stat-value">{hasGrades ? gpa.cumulative_gpa.toFixed(2) : "—"}</span>
        <span className="muted">Cumulative GPA</span>
      </div>
      {hasGrades ? (
        <ul className="semesters">
          {semesters.map(([name, value]) => (
            <li key={name}>
              <span>{name}</span>
              <strong>{value.toFixed(2)}</strong>
            </li>
          ))}
        </ul>
      ) : (
        <p className="muted">Add a graded course to see your GPA.</p>
      )}
    </div>
  );
}