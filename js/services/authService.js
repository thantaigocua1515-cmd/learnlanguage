/**
 * LingoLearning - Authentication & Profile Service
 * Integrates with Supabase Auth or manages local guest/admin session
 */

import { supabaseManager } from '../supabaseClient.js';

class AuthService {
  constructor() {
    this.sessionKey = 'lingo_user_session_v1';
    this.currentUser = this.loadSession();
  }

  loadSession() {
    const raw = localStorage.getItem(this.sessionKey);
    if (raw) {
      try {
        return JSON.parse(raw);
      } catch (e) {
        // invalid JSON
      }
    }

    // Default guest profile
    const defaultUser = {
      id: 'usr-guest-01',
      email: 'huan.nguyen@lingolearning.de',
      fullName: 'Học viên Tiếng Đức',
      role: 'student', // 'student' | 'admin'
      xp: 240,
      streak: 5,
      hearts: 5,
      targetLevel: 'A1',
      currentLang: 'de'
    };
    this.saveSession(defaultUser);
    return defaultUser;
  }

  saveSession(user) {
    this.currentUser = user;
    localStorage.setItem(this.sessionKey, JSON.stringify(user));
  }

  getUser() {
    return this.currentUser;
  }

  isAdmin() {
    return this.currentUser && this.currentUser.role === 'admin';
  }

  /**
   * Switch roles dynamically for rapid previewing (Student <-> Admin)
   */
  toggleRole() {
    const newRole = this.currentUser.role === 'admin' ? 'student' : 'admin';
    this.currentUser.role = newRole;
    this.saveSession(this.currentUser);
    return newRole;
  }

  /**
   * Add XP Points & update streaks
   */
  addXp(points = 10) {
    if (!this.currentUser) return;
    this.currentUser.xp = (this.currentUser.xp || 0) + points;
    this.saveSession(this.currentUser);
    return this.currentUser.xp;
  }

  /**
   * Decrement heart on wrong answer
   */
  loseHeart() {
    if (!this.currentUser) return;
    if (this.currentUser.hearts > 0) {
      this.currentUser.hearts -= 1;
      this.saveSession(this.currentUser);
    }
    return this.currentUser.hearts;
  }

  /**
   * Refill hearts
   */
  refillHearts() {
    if (!this.currentUser) return;
    this.currentUser.hearts = 5;
    this.saveSession(this.currentUser);
    return 5;
  }

  /**
   * Sign in with Supabase or Local
   */
  async signIn(email, password) {
    if (supabaseManager.isConnected && supabaseManager.client) {
      const { data, error } = await supabaseManager.client.auth.signInWithPassword({ email, password });
      if (error) throw error;
      const user = {
        id: data.user.id,
        email: data.user.email,
        fullName: data.user.user_metadata?.full_name || email.split('@')[0],
        role: email.includes('admin') ? 'admin' : 'student',
        xp: 100,
        streak: 1,
        hearts: 5,
        targetLevel: 'A1',
        currentLang: 'de'
      };
      this.saveSession(user);
      return user;
    }

    // Local authentication fallback
    const user = {
      id: 'usr-' + Date.now(),
      email,
      fullName: email.split('@')[0],
      role: email.toLowerCase().includes('admin') ? 'admin' : 'student',
      xp: 150,
      streak: 3,
      hearts: 5,
      targetLevel: 'A1',
      currentLang: 'de'
    };
    this.saveSession(user);
    return user;
  }

  async signOut() {
    if (supabaseManager.isConnected && supabaseManager.client) {
      await supabaseManager.client.auth.signOut();
    }
    localStorage.removeItem(this.sessionKey);
    this.currentUser = this.loadSession();
  }
}

export const authService = new AuthService();

