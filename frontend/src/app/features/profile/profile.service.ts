import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { getApiBaseUrl } from '../../shared/services/api-base-url';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  private apiUrl = `${getApiBaseUrl()}/profile`;

  constructor(private http: HttpClient) {}

  getProfile(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  updateProfile(data: any): Observable<any> {
    return this.http.put(this.apiUrl, data);
  }

  updatePassword(currentPassword: string, newPassword: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/password`, {
      current_password: currentPassword,
      new_password: newPassword
    });
  }
}
