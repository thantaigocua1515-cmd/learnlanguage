/**
 * LingoLearning - Supabase Client Bridge
 * Wraps @supabase/supabase-js with fallback to resilient Local Persistence
 */

import { CONFIG } from './config.js';

class SupabaseManager {
  constructor() {
    this.client = null;
    this.isConnected = false;
    this.init();
  }

  init() {
    const url = CONFIG.SUPABASE.URL;
    const key = CONFIG.SUPABASE.ANON_KEY;

    if (window.supabase && url && url !== 'https://xyzcompany.supabase.co' && key) {
      try {
        this.client = window.supabase.createClient(url, key);
        this.isConnected = true;
        console.log('✅ Supabase Client connected successfully to:', url);
      } catch (err) {
        console.warn('⚠️ Supabase initialization failed, running in resilient Local Mode:', err);
        this.client = null;
        this.isConnected = false;
      }
    } else {
      console.info('ℹ️ Supabase credentials not configured yet. Operating with Local Storage & In-Memory Store.');
      this.isConnected = false;
    }
  }

  updateCredentials(url, key) {
    localStorage.setItem('lingo_supabase_url', url);
    localStorage.setItem('lingo_supabase_key', key);
    CONFIG.SUPABASE.URL = url;
    CONFIG.SUPABASE.ANON_KEY = key;
    this.init();
  }
}

export const supabaseManager = new SupabaseManager();
export const supabase = supabaseManager.client;

