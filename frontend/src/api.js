const TOKEN_KEY = "cc_token";

export const getToken = () => sessionStorage.getItem(TOKEN_KEY);
const setToken = (token) => sessionStorage.setItem(TOKEN_KEY, token);
const clearToken = () => sessionStorage.removeItem(TOKEN_KEY);

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

async function request(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(path, { ...options, headers });

  if (response.status === 401 && token) {
    // The token expired or was rejected, so sign the user out
    clearToken();
    window.dispatchEvent(new Event("cc-logout"));
  }
  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    if (response.status === 422) detail = "Please check what you entered.";
    try {
      const body = await response.json();
      if (typeof body.detail === "string") detail = body.detail;
    } catch {
      // the response had no JSON body
    }
    throw new ApiError(response.status, detail);
  }
  if (response.status === 204) return null;
  return response.json();
}

export function signup(email, password) {
  return request("/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
}

export async function login(email, password) {
  const data = await request("/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username: email, password }),
  });
  setToken(data.access_token);
}

export const logout = () => clearToken();

export const listCourses = () => request("/courses");