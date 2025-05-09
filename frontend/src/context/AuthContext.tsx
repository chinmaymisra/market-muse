import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { onAuthStateChanged, User } from "firebase/auth";
import { auth } from "../firebase";

// Type definition for AuthContext
interface AuthContextType {
  user: User | null;       // Firebase authenticated user object (null if not logged in)
  loading: boolean;        // Whether the authentication state is still loading
}

// Create context with default state
const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
});

// Context provider that wraps the entire app
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);    // Stores current Firebase user
  const [loading, setLoading] = useState(true);           // Tracks loading state

  // Listen to auth state changes on mount
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
      setLoading(false);
    });

    return () => unsubscribe(); // Clean up on unmount
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to consume auth context easily
export const useAuth = () => useContext(AuthContext);
