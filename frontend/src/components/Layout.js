import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { 
  Home, User, TrendingUp, BarChart3, MessageSquare, 
  LogOut, Sun, Moon, Menu, Shield, Users, Search, Bell, ChevronLeft, Sparkles,
  CheckCircle, AlertTriangle, Info, X
} from 'lucide-react';
import './Layout.css';

const Layout = () => {
  const { user, student, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const location = useLocation();
  const navigate = useNavigate();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [notificationList, setNotificationList] = useState([
    { id: 1, type: 'success', title: 'Welcome!', message: 'Your account is ready to use', time: '2 min ago', read: false },
    { id: 2, type: 'warning', title: 'Low Attendance Alert', message: 'Your attendance is below 75% in Database Management', time: '1 hour ago', read: false },
    { id: 3, type: 'info', title: 'New Feature', message: 'AI Career Recommendations are now available', time: '1 day ago', read: false },
  ]);

  const unreadCount = notificationList.filter(n => !n.read).length;

  const markAsRead = (id) => {
    setNotificationList(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
  };

  const clearNotification = (id) => {
    setNotificationList(prev => prev.filter(n => n.id !== id));
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success': return <CheckCircle size={16} className="notif-icon success" />;
      case 'warning': return <AlertTriangle size={16} className="notif-icon warning" />;
      case 'info': return <Info size={16} className="notif-icon info" />;
      default: return <Info size={16} className="notif-icon" />;
    }
  };

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: Home },
    { path: '/profile', label: 'Profile', icon: User },
    { path: '/predictions', label: 'AI Predictions', icon: TrendingUp },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/chatbot', label: 'AI Mentor', icon: MessageSquare },
  ];

  if (user?.role === 'admin' || user?.role === 'faculty') {
    menuItems.push({ path: '/students', label: 'All Students', icon: Users });
    menuItems.push({ path: '/admin', label: 'Admin Panel', icon: Shield });
  }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="layout">
      {/* Modern Sidebar */}
      <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar-inner">
          {/* Logo */}
          <div className="sidebar-header">
            <Link to="/dashboard" className="logo-link">
              <div className="logo-icon">
                <Sparkles size={24} />
              </div>
              {!sidebarCollapsed && <span className="logo-text">AcademicAI</span>}
            </Link>
            <button 
              className="collapse-btn"
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              aria-label="Toggle sidebar"
            >
              <ChevronLeft size={18} className={`collapse-icon ${sidebarCollapsed ? 'rotated' : ''}`} />
            </button>
          </div>

          {/* Navigation */}
          <nav className="sidebar-nav">
            <div className="nav-section">
              {!sidebarCollapsed && <span className="nav-label">Menu</span>}
              {menuItems.map((item, index) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`nav-item ${isActive ? 'active' : ''}`}
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <div className={`nav-icon-wrapper ${isActive ? 'active' : ''}`}>
                      <Icon size={20} />
                    </div>
                    {!sidebarCollapsed && <span className="nav-text">{item.label}</span>}
                    {isActive && <div className="nav-indicator" />}
                  </Link>
                );
              })}
            </div>
          </nav>

          {/* Footer */}
          <div className="sidebar-footer">
            <button className="nav-item" onClick={toggleTheme}>
              <div className="nav-icon-wrapper">
                {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
              </div>
              {!sidebarCollapsed && <span className="nav-text">Toggle Theme</span>}
            </button>
            <button className="nav-item logout" onClick={handleLogout}>
              <div className="nav-icon-wrapper">
                <LogOut size={20} />
              </div>
              {!sidebarCollapsed && <span className="nav-text">Logout</span>}
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className={`main-wrapper ${sidebarCollapsed ? 'expanded' : ''}`}>
        {/* Top Navbar */}
        <header className="top-navbar">
          <div className="navbar-left">
            <button className="mobile-menu-btn" onClick={() => setSidebarCollapsed(!sidebarCollapsed)}>
              <Menu size={20} />
            </button>
            <div className="search-wrapper">
              <Search size={18} className="search-icon" />
              <input 
                type="text" 
                placeholder="Search anything..." 
                className="search-input"
              />
              <span className="search-shortcut">⌘K</span>
            </div>
          </div>

          <div className="navbar-right">
            {/* Notifications */}
            <div className="notification-wrapper">
              <button 
                className="navbar-btn notification-btn"
                onClick={() => {
                  setShowNotifications(!showNotifications);
                  setShowProfileMenu(false);
                }}
              >
                <Bell size={20} />
                {unreadCount > 0 && (
                  <span className="notification-badge">{unreadCount}</span>
                )}
              </button>

              {showNotifications && (
                <div className="notification-dropdown">
                  <div className="notification-header">
                    <h4>Notifications</h4>
                    {unreadCount > 0 && (
                      <button 
                        className="mark-all-read"
                        onClick={() => setNotificationList(prev => prev.map(n => ({ ...n, read: true })))}
                      >
                        Mark all read
                      </button>
                    )}
                  </div>
                  <div className="notification-list">
                    {notificationList.length > 0 ? (
                      notificationList.map(notif => (
                        <div 
                          key={notif.id} 
                          className={`notification-item ${notif.read ? 'read' : 'unread'}`}
                          onClick={() => markAsRead(notif.id)}
                        >
                          {getNotificationIcon(notif.type)}
                          <div className="notification-content">
                            <span className="notification-title">{notif.title}</span>
                            <span className="notification-message">{notif.message}</span>
                            <span className="notification-time">{notif.time}</span>
                          </div>
                          <button 
                            className="notification-close"
                            onClick={(e) => { e.stopPropagation(); clearNotification(notif.id); }}
                          >
                            <X size={14} />
                          </button>
                        </div>
                      ))
                    ) : (
                      <div className="no-notifications">
                        <Bell size={32} />
                        <p>No notifications</p>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Profile */}
            <div className="profile-menu-wrapper">
              <button 
                className="profile-btn"
                onClick={() => setShowProfileMenu(!showProfileMenu)}
              >
                <div className="profile-avatar">
                  {student?.first_name?.charAt(0) || user?.username?.charAt(0) || 'U'}
                </div>
                {!sidebarCollapsed && (
                  <div className="profile-info">
                    <span className="profile-name">{user?.username}</span>
                    <span className="profile-role">{user?.role}</span>
                  </div>
                )}
              </button>

              {showProfileMenu && (
                <div className="profile-dropdown">
                  <Link to="/profile" className="dropdown-item" onClick={() => setShowProfileMenu(false)}>
                    <User size={16} />
                    <span>View Profile</span>
                  </Link>
                  <button className="dropdown-item" onClick={handleLogout}>
                    <LogOut size={16} />
                    <span>Logout</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="page-content">
          <Outlet />
        </main>
      </div>

      {/* Floating AI Chat Button */}
      <Link to="/chatbot" className="floating-ai-btn">
        <Sparkles size={24} />
        <span className="floating-btn-text">AI Mentor</span>
      </Link>
    </div>
  );
};

export default Layout;
