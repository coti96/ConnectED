import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ProjectService } from '../project.service';
import { ApplicationService } from '../application.service';
import { AuthService } from '../../../shared/services/auth';
import { IconComponent } from '../../../shared/icon/icon';

@Component({
  selector: 'app-project-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent],
  templateUrl: './project-detail.html',
  styleUrls: ['./project-detail.scss']
})
export class ProjectDetailComponent implements OnInit {
  project: any;
  isCreator = false;
  hasApplied = false;
  message = '';
  error = '';

  constructor(
    private route: ActivatedRoute,
    private projectService: ProjectService,
    private appService: ApplicationService,
    public auth: AuthService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadProject(id);
    }
  }

  loadProject(id: string): void {
    this.projectService.getProjectById(id).subscribe({
      next: (res: any) => {
        this.project = res.project;
        console.log('Projet chargé:', this.project);
        this.cdr.detectChanges();
        console.log('Détails du projet:', this.project);
        if (this.auth.isLoggedIn()) {
          const user = this.auth.currentUser();
          // Vérification si créateur (objet creator)
          this.isCreator = this.project.creator?.email === user.email;
          
          if (!this.isCreator) {
            this.checkIfApplied();
          }
        }
      },
      error: (err) => {
        console.error('Erreur chargement projet', err);
        this.error = 'Impossible de charger le projet.';
        this.cdr.detectChanges();
      }
    });
  }

  checkIfApplied(): void {
    this.appService.getMyApplications().subscribe({
      next: (res: any) => {
        // On vérifie si une candidature existe pour ce projet
        if (res.applications && Array.isArray(res.applications)) {
          this.hasApplied = res.applications.some((app: any) => app?.project?.id === this.project.id);
        }
      },
      error: (err) => console.error(err)
    });
  }

  apply(): void {
    if (!confirm('Voulez-vous vraiment postuler à ce projet ?')) return;

    this.appService.applyToProject(this.project.id).subscribe({
      next: () => {
        this.message = 'Candidature envoyée avec succès !';
        this.hasApplied = true;
      },
      error: (err) => {
        this.message = '';
        this.error = err.error?.error || 'Erreur lors de la candidature';
      }
    });
  }
}
