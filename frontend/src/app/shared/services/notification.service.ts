import { Injectable, effect, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from './auth';
import { getApiBaseUrl } from './api-base-url';

export type AppNotification = {
  id: string;
  type: string;
  message: string;
  read: boolean;
  created_at?: string;
  data?: Record<string, unknown>;
};

@Injectable({ providedIn: 'root' })
export class NotificationService {
  private apiUrl = getApiBaseUrl();
  notifications = signal<AppNotification[]>([]);
  unread = signal<number>(0);

  private pollTimer: number | null = null;

  constructor(
    private http: HttpClient,
    private auth: AuthService
  ) {
    effect(() => {
      const loggedIn = this.auth.isLoggedIn();
      if (loggedIn) {
        this.startPolling();
        this.refresh();
      } else {
        this.stopPolling();
        this.notifications.set([]);
        this.unread.set(0);
      }
    });
  }

  refresh(): void {
    this.http.get<any>(`${this.apiUrl}/notifications?limit=20`).subscribe({
      next: (res) => {
        this.notifications.set(Array.isArray(res?.notifications) ? res.notifications : []);
        this.unread.set(typeof res?.unread === 'number' ? res.unread : 0);
      }
    });
  }

  markRead(id: string): void {
    this.http.put(`${this.apiUrl}/notifications/${id}/read`, {}).subscribe({
      next: () => this.refresh()
    });
  }

  private startPolling(): void {
    if (this.pollTimer != null) return;
    this.pollTimer = window.setInterval(() => this.refresh(), 15000);
  }

  private stopPolling(): void {
    if (this.pollTimer == null) return;
    window.clearInterval(this.pollTimer);
    this.pollTimer = null;
  }
}

