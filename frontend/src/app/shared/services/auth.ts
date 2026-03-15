import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { getApiBaseUrl } from './api-base-url';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = getApiBaseUrl();

  isLoggedIn = signal<boolean>(!!localStorage.getItem('token'));
  currentUser = signal<any>(JSON.parse(localStorage.getItem('user') || 'null'));

  constructor(private http: HttpClient) {}

  private normalizeRole(role: unknown): string {
    const raw = String(role || '').trim().toLowerCase();
    if (!raw) return raw;
    if (raw === 'student') return 'etudiant';
    if (raw === 'professional') return 'professionnel';
    if (raw === 'creator') return 'professionnel';
    if (raw === 'encadrant') return 'encadrant';
    if (raw === 'etudiant' || raw === 'professionnel' || raw === 'admin') return raw;
    return raw;
  }

  login(credentials: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, credentials).pipe(
      tap((response: any) => {
        if (response.token) {
          if (response.user) {
            response.user = { ...response.user, role: this.normalizeRole(response.user.role) };
          }
          localStorage.setItem('token', response.token);
          localStorage.setItem('user', JSON.stringify(response.user));
          this.isLoggedIn.set(true);
          this.currentUser.set(response.user);
        }
      })
    );
  }

  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, userData);
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    this.isLoggedIn.set(false);
    this.currentUser.set(null);
  }
}
