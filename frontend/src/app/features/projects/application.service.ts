import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApplicationService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  // Candidat : Postuler
  applyToProject(projectId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/projects/${projectId}/apply`, {}, { headers: this.getHeaders() });
  }

  // Candidat : Mes candidatures
  getMyApplications(): Observable<any> {
    return this.http.get(`${this.apiUrl}/my-applications`, { headers: this.getHeaders() });
  }

  // Créateur : Voir les candidats
  getProjectApplications(projectId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/projects/${projectId}/applications`, { headers: this.getHeaders() });
  }

  // Créateur : Accepter/Refuser
  updateApplicationStatus(projectId: string, applicantEmail: string, status: string): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/projects/${projectId}/applications/${applicantEmail}/status`,
      { status },
      { headers: this.getHeaders() }
    );
  }
}
