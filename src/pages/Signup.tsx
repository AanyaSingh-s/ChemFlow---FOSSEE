// src/pages/Signup.tsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authAPI } from "@/services/api";
// import Iridescence from "@/components/Iridescence";
import { Button } from "@/components/ui/button";
import { FlaskConical, ArrowLeft, Sun, Moon } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useTheme } from "@/components/theme-provider";

const Signup = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { theme, setTheme } = useTheme();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleToggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    toast({ title: `Theme: ${next[0].toUpperCase() + next.slice(1)}` });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      toast({
        title: "Error",
        description: "Passwords do not match",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      const data = await authAPI.register(username, email, password, confirmPassword);
      localStorage.setItem("user", JSON.stringify(data.user));
      localStorage.setItem("token", data.token);
      
      toast({
        title: "Success",
        description: "Account created successfully!",
      });
      
      navigate("/dashboard");
    } catch (error: any) {
      toast({
        title: "Registration Failed",
        description: error.response?.data?.error || "Registration failed. Backend may not be running.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center p-4 bg-background text-foreground">
      {/* <div className="fixed inset-0 -z-10 opacity-90">
        <Iridescence color={[0.35, 0.65, 0.95]} speed={0.4} amplitude={0.15} />
      </div> */}

      <div className="w-full max-w-md">
        <div className="mb-6">
          <div className="flex items-center justify-between">
            <Link 
              to="/" 
              className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to home
            </Link>
            <Button variant="ghost" onClick={handleToggleTheme} title={`Toggle theme (current: ${theme})`} aria-label="Toggle theme" className="text-muted-foreground hover:text-foreground">
              {theme === "dark" ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
            </Button>
          </div>
        </div>

        <div className="bg-background/90 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-border/50">
          <div className="flex items-center gap-3 mb-6">
            <div className="rounded-xl bg-primary/20 p-3">
              <FlaskConical className="h-6 w-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Create Account</h1>
              <p className="text-sm text-muted-foreground">Sign up to get started</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="signup-username" className="block text-sm font-medium mb-2">Username</label>
              <input
                id="signup-username"
                name="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-lg bg-background/50 focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                required
                placeholder="Choose a username"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-2">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-lg bg-background/50 focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                required
                placeholder="your.email@example.com"
              />
            </div>

            <div>
              <label htmlFor="signup-password" className="block text-sm font-medium mb-2">Password</label>
              <input
                id="signup-password"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-lg bg-background/50 focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                required
                placeholder="Create a password"
                minLength={8}
              />
            </div>

            <div>
              <label htmlFor="confirm-password" className="block text-sm font-medium mb-2">Confirm Password</label>
              <input
                id="confirm-password"
                name="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-lg bg-background/50 focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                required
                placeholder="Confirm your password"
                minLength={8}
              />
            </div>

            <Button
              type="submit"
              disabled={loading}
              className="w-full bg-primary text-primary-foreground hover:brightness-95"
            >
              {loading ? "Creating account..." : "Sign Up"}
            </Button>

            <p className="text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link to="/login" className="text-primary hover:underline">
                Log in
              </Link>
            </p>
          </form>

        
        </div>
      </div>
    </div>
  );
};

export default Signup;