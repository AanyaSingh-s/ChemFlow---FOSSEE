// src/pages/Login.tsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authAPI } from "@/services/api";
// import Iridescence from "@/components/Iridescence";
import { Button } from "@/components/ui/button";
import { FlaskConical, ArrowLeft, Sun, Moon } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useTheme } from "@/components/theme-provider";

const Login = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { theme, setTheme } = useTheme();

  const handleToggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    toast({ title: `Theme: ${next[0].toUpperCase() + next.slice(1)}` });
  };
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = await authAPI.login(username, password);
      localStorage.setItem("user", JSON.stringify(data.user));
      localStorage.setItem("token", data.token);
      
      toast({
        title: "Success",
        description: "Logged in successfully!",
      });
      
      navigate("/dashboard");
    } catch (error: any) {
      toast({
        title: "Login Failed",
        description: error.response?.data?.error || "Invalid credentials. Backend may not be running.",
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
              <h1 className="text-2xl font-bold">Welcome Back</h1>
              <p className="text-sm text-muted-foreground">Log in to your account</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium mb-2">Username</label>
              <input
                id="username"
                name="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-lg bg-background/50 focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                required
                placeholder="Enter your username"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium mb-2">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-lg bg-background/50 focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                required
                placeholder="Enter your password"
              />
            </div>

            <Button
              type="submit"
              disabled={loading}
              className="w-full bg-primary text-primary-foreground hover:brightness-95"
            >
              {loading ? "Logging in..." : "Log In"}
            </Button>

            <p className="text-center text-sm text-muted-foreground">
              Don't have an account?{" "}
              <Link to="/signup" className="text-primary hover:underline">
                Sign up
              </Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;


