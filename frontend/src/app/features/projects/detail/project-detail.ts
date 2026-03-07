import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ProjectService } from '../project.service';
import { ApplicationService } from '../application.service';
import { AuthService } from '../../../shared/services/auth';

@Component({
  selector: 'app-project-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './project-detail.html',
  styleUrls: ['../list/project-list.scss', './project-detail.scss']
})
export class ProjectDetailComponent implements OnInit {
  project: any;
  loading = true;
  isCreator = false;
  hasApplied = false;
  message = '';

  constructor(
    private route: ActivatedRoute,
    private projectService: ProjectService,
    private appService: ApplicationService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadProject(id);
    }
  }

  loadProject(id: string): void {
    this.projectService.getProjects().subscribe((res: any) => {
      // Note: Idéalement on aurait une route GET /projects/:id spécifique
      this.project = res.projects.find((p: any) => p.id === id);
      
      if (this.project && this.auth.currentUser()) {
        this.isCreator = this.project.creator?.email === this.auth.currentUser().email;
        this.checkIfApplied();
      }
      this.loading = false;
    });
  }

  checkIfApplied(): void {
    this.appService.getMyApplications().subscribe((res: any) => {
      this.hasApplied = res.applications.some((app: any) => app.project.id === this.project.id);
    });
  }

  apply(): void {
    if (!confirm('Voulez-vous vraiment postuler à ce projet ?')) return;

    this.appService.applyToProject(this.project.id).subscribe({
      next: () => {
        this.message = 'Candidature envoyée !';
        this.hasApplied = true;
      },
      error: (err) => {
        this.message = err.error.error || 'Erreur lors de la candidature';
      }
    });
  }
}
