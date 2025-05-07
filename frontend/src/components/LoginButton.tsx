import { useNavigate } from "react-router-dom";
import { auth, provider } from "../firebase";
import { signInWithPopup } from "firebase/auth";

export const LoginButton = () => {
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const user = result.user;
      const idToken = await user.getIdToken();

      // 🛡️ Log token only if it's your account
      if (user.email === "misrachinmay@gmail.com") {
        console.log("🪪 Firebase ID Token:", idToken);
      }

      // 🔁 Send token to backend to persist the user
      const res = await fetch("https://api.marketmuse.chinmaymisra.com/users/me", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${idToken}`,
        },
      });

      const data = await res.json();
      console.log("✅ /users/me response:", data);

      // ✅ Redirect to dashboard
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
