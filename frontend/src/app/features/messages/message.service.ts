import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { getApiBaseUrl } from '../../shared/services/api-base-url';

@Injectable({
  providedIn: 'root'
})
export class MessageService {
  private apiUrl = getApiBaseUrl();

  constructor(private http: HttpClient) {}

  getConversations(): Observable<any> {
    return this.http.get(`${this.apiUrl}/conversations`);
  }

  getMessages(
    otherEmail: string,
    opts?: { limit?: number; before?: string; since?: string; markRead?: boolean }
  ): Observable<any> {
    const params: Record<string, string> = {};
    if (opts?.limit != null) params['limit'] = String(opts.limit);
    if (opts?.before) params['before'] = opts.before;
    if (opts?.since) params['since'] = opts.since;
    if (opts?.markRead === false) params['mark_read'] = '0';
    return this.http.get(`${this.apiUrl}/messages/${otherEmail}`, { params });
  }

  sendMessage(receiverEmail: string, content: string): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/messages`,
      { receiver_email: receiverEmail, content }
    );
  }
}
