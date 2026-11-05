import { useState } from "react";

function describe(plan) {
  const goal = plan.goal_gpa.toFixed(2);
  const units = plan.upcoming_units;
  switch (plan.status) {
    case "achievable":
      return `To finish at ${goal}, you need about a ${plan.required_average.toFixed(2)} average across your ${units} upcoming units. Earning at least ${plan.minimum_letter} in each would get you there.`;
    case "already_met":
      return `Your ${goal} goal is already secured, whatever you earn in your ${units} upcoming units.`;
    case "impossible":
      return `A ${goal} is out of reach: it would take an average above 4.0 across your ${units} upcoming units.`;
    default:
      return "Add a course without a grade to see what you need to reach this goal.";
  }
}

export default function GoalPlanner({ plan, loaded, onSave }) {
  const [value, setValue] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    const goal = Number(value);
    if (value.trim() === "" || !Number.isFinite(goal) || goal < 0 || goal > 4) {
      setError("Enter a goal between 0.0 and 4.0.");
      return;
    }
    setError("");
    setBusy(true);
    try {
      await onSave(goal);
      setValue("");
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <form className="goal-form" onSubmit={handleSubmit}>
        <label>
          Goal GPA
          <input
            type="number"
            min="0"
            max="4"
            step="0.01"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder={plan ? plan.goal_gpa.toFixed(2) : "3.50"}
          />
        </label>
        <button type="submit" disabled={busy}>
          {busy ? "Saving..." : plan ? "Update goal" : "Set goal"}
        </button>
      </form>
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
      <p aria-live="polite" className={plan ? "" : "muted"}>
        {!loaded
          ? "Loading your goal..."
          : plan
            ? describe(plan)
            : "Set a goal GPA to see what grades you need."}
      </p>
    </div>
  );
}