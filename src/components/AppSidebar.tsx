import { Home, History, LogOut, PauseCircle, PlayCircle, Sun, Moon } from "lucide-react";
import { NavLink } from "@/components/NavLink";
import { useAuth } from "@/contexts/AuthContext";
import { useUploadHistory } from "@/contexts/UploadHistoryContext";
import { useToast } from "@/hooks/use-toast";
import { useTheme } from "@/components/theme-provider";
import { useNavigate } from "react-router-dom";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
  useSidebar,
} from "@/components/ui/sidebar";

const menuItems = [
  { title: "Dashboard", url: "/dashboard", icon: Home },
  { title: "History", url: "/history", icon: History },
];

export function AppSidebar() {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const { logout } = useAuth();
  const { paused, togglePause } = useUploadHistory();
  const { toast } = useToast();
  const { theme, setTheme } = useTheme();
  const navigate = useNavigate();

  const handleToggleHistory = () => {
    const nextPaused = !paused;
    togglePause();
    toast({
      title: nextPaused ? "History paused" : "History resumed",
      description: nextPaused ? "Uploads will not be saved until resumed." : "Uploads will now be captured again.",
    });
  };

  const handleSignOut = () => {
    // Clear client-side auth state and navigate to login
    logout();
    try {
      localStorage.removeItem("user");
      localStorage.removeItem("token");
    } catch (e) {
      // ignore
    }
    toast({ title: "Signed out", description: "You have been signed out." });
    navigate("/login");
  };

  const handleToggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    toast({ title: `Theme: ${next[0].toUpperCase() + next.slice(1)}` });
  };

  return (
    <Sidebar className={collapsed ? "w-14" : "w-60"}>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {menuItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <NavLink
                      to={item.url}
                      end
                      className="hover:bg-muted/50"
                      activeClassName="bg-muted text-primary font-medium"
                    >
                      <item.icon className="mr-2 h-4 w-4" />
                      {!collapsed && <span>{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Settings</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton onClick={handleToggleHistory}>
                  {paused ? (
                    <PlayCircle className="mr-2 h-4 w-4" />
                  ) : (
                    <PauseCircle className="mr-2 h-4 w-4" />
                  )}
                  {!collapsed && (
                    <span>{paused ? "Resume History" : "Pause History"}</span>
                  )}
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton onClick={handleToggleTheme} title={`Toggle theme (current: ${theme})`} aria-label="Toggle theme">
                  {theme === "dark" ? (
                    <Moon className="mr-2 h-4 w-4 text-foreground" />
                  ) : (
                    <Sun className="mr-2 h-4 w-4 text-foreground" />
                  )}
                  {!collapsed && <span className="text-foreground">{theme === "dark" ? "Dark" : "Light"}</span>}
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton onClick={handleSignOut}>
              <LogOut className="mr-2 h-4 w-4" />
              {!collapsed && <span>Sign Out</span>}
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
