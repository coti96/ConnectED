import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProjectService } from '../../projects/project.service';

@Component({
  selector: 'app-admin-projects',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-projects.html',
  styleUrls: ['./admin-projects.scss']
})
export class AdminProjectsComponent implements OnInit {
  loading = true;
  projects: any[] = [];
  message = '';

  constructor(private projectsService: ProjectService) {}

  ngOnInit(): void {
    this.refresh();
  }

  refresh(): void {
    this.loading = true;
    this.projectsService.getAdminProjects().subscribe({
      next: (res: any) => {
        this.projects = Array.isArray(res?.projects) ? res.projects : [];
        this.loading = false;
      },
      error: () => {
        this.projects = [];
        this.loading = false;
      }
    });
  }

  setStatus(projectId: string, status: 'en_cours' | 'ferme'): void {
    this.projectsService.setAdminProjectStatus(projectId, status).subscribe({
      next: () => {
        this.message = 'Mise à jour effectuée.';
        this.refresh();
        setTimeout(() => (this.message = ''), 2000);
      }
    });
  }
}

