import { createClient } from '@supabase/supabase-js';

const url = import.meta.env.VITE_SUPABASE_URL;
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const configured = Boolean(url && anonKey && !url.includes('TU-PROYECTO'));
export const supabase = configured ? createClient(url, anonKey) : null;
