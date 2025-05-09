import { useNavigate } from "react-router-dom";
import { auth, provider } from "../firebase";
import { signInWithPopup } from "firebase/auth";
import { authFetch } from "@/utils/authFetch";

// Login button component using Firebase Google Sign-In
export const LoginButton = () => {
  const navigate = useNavigate();

  // Handles user login via Google popup and backend sync
  const handleLogin = async () => {
    try {
      // Firebase Google OAuth popup
      const result = await signInWithPopup(auth, provider);
      const user = result.user;

      // Get Firebase ID token for backend authentication
      const idToken = await user.getIdToken();

      // Optional: Log token for debugging only on your own account
      if (user.email === "misrachinmay@gmail.com") {
        console.log("🪪 Firebase ID Token:", idToken);
      }

      // Call backend /users/me to ensure user is stored in DB
      const res = await authFetch("https://api.marketmuse.chinmaymisra.com/users/me", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${idToken}`,
        },
      });

      const data = await res.json();
      console.log("✅ /users/me response:", data);

      // Redirect to home page
      navigate("/");
    } catch (err) {
      console.error("❌ Login failed or backend error:", err);
    }
  };

  return (
    <button
      onClick={handleLogin}
      className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      Sign in with Google
    </button>
  );
};
