import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { getApiBaseUrl } from '../../shared/services/api-base-url';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private apiUrl = getApiBaseUrl();

  constructor(private http: HttpClient) {}

  getDashboardData(): Observable<any> {
    return this.http.get(`${this.apiUrl}/dashboard`);
  }
}
