/**
 * LingoLearning - Authentication & Profile Service
 * Integrates with Supabase Auth or manages local guest/student/admin session
 */

import { supabaseManager } from '../supabaseClient.js';

class AuthService {
  constructor() {
    this.sessionKey = 'lingo_user_session_v2';
    this.listeners = [];
    this.currentUser = this.loadSession();
  }

  loadSession() {
    const raw = localStorage.getItem(this.sessionKey);
    if (raw) {
      try {
        const u = JSON.parse(raw);
        if (u && u.role) return u;
      } catch (e) {
        // invalid JSON
      }
    }

    // Default: Guest mode (unauthenticated visitor)
    return {
      id: 'guest',
      fullName: 'Khách (Guest)',
      email: '',
      role: 'guest',
      xp: 0,
      streak: 0,
      hearts: 5,
      isGuest: true,
      targetLevel: 'A1',
      currentLang: 'de'
    };
  }

  saveSession(user) {
    this.currentUser = user;
    localStorage.setItem(this.sessionKey, JSON.stringify(user));
    this.notifyListeners();
  }

  onAuthChange(callback) {
    if (typeof callback === 'function') {
      this.listeners.push(callback);
    }
  }

  notifyListeners() {
    this.listeners.forEach(cb => {
      try {
        cb(this.currentUser);
      } catch (e) {
        console.error('Error in auth listener:', e);
      }
    });
  }

  getUser() {
    return this.currentUser;
  }

  isLoggedIn() {
    return !!(this.currentUser && !this.currentUser.isGuest && this.currentUser.role !== 'guest');
  }

  isGuest() {
    return !this.isLoggedIn();
  }

  isAdmin() {
    return this.isLoggedIn() && this.currentUser.role === 'admin';
  }

  /**
   * Quick Login for testing & fast onboarding
   */
  quickLogin(role = 'student') {
    const user = {
      id: role === 'admin' ? 'usr-admin-default' : 'usr-student-01',
      email: role === 'admin' ? 'admin@lingolearning.de' : 'hocvien@lingolearning.de',
      fullName: role === 'admin' ? 'Quản Trị Viên (Admin)' : 'Học Viên Tiếng Đức',
      role: role === 'admin' ? 'admin' : 'student',
      xp: role === 'admin' ? 1000 : 250,
      streak: role === 'admin' ? 7 : 5,
      hearts: 5,
      isGuest: false,
      targetLevel: 'A1',
      currentLang: 'de'
    };
    this.saveSession(user);
    return user;
  }

  /**
   * Sign In (Supabase Auth or Local Mock)
   * Default admin account: username/email 'admin', password 'admin123'
   */
  async signIn(emailOrUsername, password) {
    const input = (emailOrUsername || '').trim();
    const pwd = (password || '').trim();

    // 1. Check Default Admin Account (admin / admin123)
    if ((input.toLowerCase() === 'admin' || input.toLowerCase() === 'admin@lingolearning.de') && pwd === 'admin123') {
      const adminUser = {
        id: 'usr-admin-default',
        email: 'admin@lingolearning.de',
        fullName: 'Quản Trị Viên (Admin)',
        role: 'admin',
        xp: 1000,
        streak: 7,
        hearts: 5,
        isGuest: false,
        targetLevel: 'A1',
        currentLang: 'de'
      };
      this.saveSession(adminUser);
      return adminUser;
    }

    // 2. Check Supabase Auth if connected and input is valid email
    if (supabaseManager.isConnected && supabaseManager.client && input.includes('@')) {
      try {
        const { data, error } = await supabaseManager.client.auth.signInWithPassword({ email: input, password: pwd });
        if (error) throw error;
        const isAdminRole = input.toLowerCase().includes('admin');
        const user = {
          id: data.user.id,
          email: data.user.email,
          fullName: data.user.user_metadata?.full_name || input.split('@')[0],
          role: isAdminRole ? 'admin' : 'student',
          xp: 150,
          streak: 2,
          hearts: 5,
          isGuest: false,
          targetLevel: 'A1',
          currentLang: 'de'
        };
        this.saveSession(user);
        return user;
      } catch (err) {
        console.warn('Supabase auth sign in error, fallback to local:', err);
      }
    }

    // 3. Local authentication fallback
    const isAdminRole = input.toLowerCase() === 'admin' || input.toLowerCase().includes('admin');
    const user = {
      id: 'usr-' + Date.now(),
      email: input.includes('@') ? input : `${input}@lingolearning.de`,
      fullName: input.includes('@') ? input.split('@')[0] : input,
      role: isAdminRole ? 'admin' : 'student',
      xp: isAdminRole ? 1000 : 150,
      streak: 2,
      hearts: 5,
      isGuest: false,
      targetLevel: 'A1',
      currentLang: 'de'
    };
    this.saveSession(user);
    return user;
  }

  /**
   * Sign Up (Register new account)
   */
  async signUp(email, password, fullName = '') {
    if (supabaseManager.isConnected && supabaseManager.client) {
      try {
        const { data, error } = await supabaseManager.client.auth.signUp({
          email,
          password,
          options: { data: { full_name: fullName } }
        });
        if (error) throw error;
        const user = {
          id: data.user?.id || 'usr-' + Date.now(),
          email,
          fullName: fullName || email.split('@')[0],
          role: 'student',
          xp: 50,
          streak: 1,
          hearts: 5,
          isGuest: false,
          targetLevel: 'A1',
          currentLang: 'de'
        };
        this.saveSession(user);
        return user;
      } catch (err) {
        console.warn('Supabase sign up error, fallback to local:', err);
      }
    }

    // Local registration fallback
    const user = {
      id: 'usr-' + Date.now(),
      email,
      fullName: fullName || email.split('@')[0],
      role: 'student',
      xp: 50,
      streak: 1,
      hearts: 5,
      isGuest: false,
      targetLevel: 'A1',
      currentLang: 'de'
    };
    this.saveSession(user);
    return user;
  }

  /**
   * Sign Out
   */
  async signOut() {
    if (supabaseManager.isConnected && supabaseManager.client) {
      try {
        await supabaseManager.client.auth.signOut();
      } catch {
        // ignore
      }
    }
    localStorage.removeItem(this.sessionKey);
    this.currentUser = this.loadSession();
    this.notifyListeners();
  }

  /**
   * Add XP Points
   */
  addXp(points = 10) {
    if (!this.currentUser) return;
    this.currentUser.xp = (this.currentUser.xp || 0) + points;
    this.saveSession(this.currentUser);
    return this.currentUser.xp;
  }

  loseHeart() {
    if (!this.currentUser) return;
    if (this.currentUser.hearts > 0) {
      this.currentUser.hearts -= 1;
      this.saveSession(this.currentUser);
    }
    return this.currentUser.hearts;
  }

  refillHearts() {
    if (!this.currentUser) return;
    this.currentUser.hearts = 5;
    this.saveSession(this.currentUser);
    return 5;
  }
}

export const authService = new AuthService();
