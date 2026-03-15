import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { getApiBaseUrl } from '../../shared/services/api-base-url';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private apiUrl = `${getApiBaseUrl()}/projects`;
  private adminUrl = `${getApiBaseUrl()}/admin/projects`;

  constructor(private http: HttpClient) {}

  getProjects(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  getProjectById(id: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/${id}`);
  }
  
  getRecommendedProjects(): Observable<any> {
    return this.http.get(`${this.apiUrl}/recommended`);
  }

  createProject(projectData: any): Observable<any> {
    return this.http.post(this.apiUrl, projectData);
  }

  getAdminProjects(): Observable<any> {
    return this.http.get(this.adminUrl);
  }

  setAdminProjectStatus(projectId: string, status: 'en_cours' | 'ferme'): Observable<any> {
    return this.http.put(`${this.adminUrl}/${projectId}/status`, { status });
  }
}
