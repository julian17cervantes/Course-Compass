import { GRADES } from "./grades";

export default function CourseTable({ courses, onGrade, onDelete }) {
  if (courses.length === 0) {
    return <p className="muted">No courses yet. Add one above.</p>;
  }
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Course</th>
            <th>Semester</th>
            <th>Units</th>
            <th>Grade</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {courses.map((course) => (
            <tr key={course.id}>
              <td>
                <strong>{course.code}</strong>
                <br />
                <span className="muted">{course.name}</span>
              </td>
              <td>{course.semester}</td>
              <td>{course.units}</td>
              <td>
                <select
                  aria-label={`Grade for ${course.code}`}
                  value={course.grade ?? ""}
                  onChange={(event) => onGrade(course, event.target.value || null)}
                >
                  <option value="">Not graded</option>
                  {GRADES.map((g) => (
                    <option key={g} value={g}>
                      {g}
                    </option>
                  ))}
                  {course.grade && !GRADES.includes(course.grade) && (
                    <option value={course.grade}>{course.grade}</option>
                  )}
                </select>
              </td>
              <td>
                <button
                  type="button"
                  className="danger"
                  aria-label={`Delete ${course.code}`}
                  onClick={() => onDelete(course)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}