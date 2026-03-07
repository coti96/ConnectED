import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MessageService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  getConversations(): Observable<any> {
    return this.http.get(`${this.apiUrl}/conversations`, { headers: this.getHeaders() });
  }

  getMessages(otherEmail: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/messages/${otherEmail}`, { headers: this.getHeaders() });
  }

  sendMessage(receiverEmail: string, content: string): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/messages`,
      { receiver_email: receiverEmail, content },
      { headers: this.getHeaders() }
    );
  }
}
