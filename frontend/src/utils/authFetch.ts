import { getAuth } from "firebase/auth";

/**
 * A wrapper around fetch that automatically attaches the Firebase ID token
 * to the Authorization header if a user is logged in.
 */
export async function authFetch(
  input: RequestInfo | URL,
  init: RequestInit = {}
): Promise<Response> {
  const auth = getAuth();
  const user = auth.currentUser;

  if (user) {
    const token = await user.getIdToken();
    const existingHeaders = init.headers instanceof Headers
      ? Object.fromEntries(init.headers.entries())
      : init.headers || {};

    init.headers = {
      ...existingHeaders,
      Authorization: `Bearer ${token}`,
    };
  }

  return fetch(input, init);
}
