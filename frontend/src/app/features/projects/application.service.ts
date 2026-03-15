import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { getApiBaseUrl } from '../../shared/services/api-base-url';

@Injectable({
  providedIn: 'root'
})
export class ApplicationService {
  private apiUrl = getApiBaseUrl();

  constructor(private http: HttpClient) {}

  // Candidat : Postuler
  applyToProject(projectId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/projects/${projectId}/apply`, {});
  }

  cancelApplication(projectId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/projects/${projectId}/apply`);
  }

  // Candidat : Mes candidatures
  getMyApplications(): Observable<any> {
    return this.http.get(`${this.apiUrl}/my-applications`);
  }

  // Créateur : Voir les candidats
  getProjectApplications(projectId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/projects/${projectId}/applications`);
  }

  // Créateur : Accepter/Refuser
  updateApplicationStatus(projectId: string, applicantEmail: string, status: string): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/projects/${projectId}/applications/${applicantEmail}/status`,
      { status }
    );
  }
}
