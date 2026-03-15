import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ProjectService } from '../project.service';
import { ApplicationService } from '../application.service';
import { AuthService } from '../../../shared/services/auth';
import { IconComponent } from '../../../shared/icon/icon';
import { Neo4jDatePipe } from '../../../shared/pipes/neo4j-date.pipe';

@Component({
  selector: 'app-project-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent, Neo4jDatePipe],
  templateUrl: './project-detail.html',
  styleUrls: ['./project-detail.scss']
})
export class ProjectDetailComponent implements OnInit {
  project: any;
  isCreator = false;
  hasApplied = false;
  applicationStatus: string = '';
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
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (!id) return;
      this.loadProject(id);
    });
  }

  loadProject(id: string): void {
    this.project = null;
    this.error = '';
    this.message = '';
    this.hasApplied = false;
    this.isCreator = false;
    this.applicationStatus = '';
    this.projectService.getProjectById(id).subscribe({
      next: (res: any) => {
        this.project = res.project;
        this.cdr.detectChanges();
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

  get acceptedCount(): number {
    const v = this.project?.accepted_count;
    return Number.isFinite(Number(v)) ? Number(v) : 0;
  }

  get capacity(): number {
    const v = this.project?.nombre_places;
    return Number.isFinite(Number(v)) ? Number(v) : 0;
  }

  get placesRemaining(): number {
    const remaining = this.capacity - this.acceptedCount;
    return remaining < 0 ? 0 : remaining;
  }

  get isFull(): boolean {
    return this.capacity > 0 && this.placesRemaining <= 0;
  }

  checkIfApplied(): void {
    this.appService.getMyApplications().subscribe({
      next: (res: any) => {
        // On vérifie si une candidature existe pour ce projet
        if (res.applications && Array.isArray(res.applications)) {
          const found = res.applications.find((app: any) => app?.project?.id === this.project.id);
          this.hasApplied = !!found;
          this.applicationStatus = found?.status || '';
        }
      },
      error: (err) => {
        if (err?.status === 401) {
          this.error = 'Session expirée. Veuillez vous reconnecter.';
          return;
        }
        console.error(err);
      }
    });
  }

  apply(): void {
    if (this.isFull) {
      this.message = '';
      this.error = 'Ce projet est complet.';
      return;
    }
    if (!confirm('Voulez-vous vraiment postuler à ce projet ?')) return;

    this.appService.applyToProject(this.project.id).subscribe({
      next: () => {
        this.message = 'Candidature envoyée avec succès !';
        this.hasApplied = true;
        this.applicationStatus = 'PENDING';
      },
      error: (err) => {
        this.message = '';
        if (err?.status === 401) {
          this.error = 'Session expirée. Veuillez vous reconnecter.';
          return;
        }
        this.error = err.error?.error || 'Erreur lors de la candidature';
      }
    });
  }

  cancel(): void {
    if (!confirm('Annuler cette candidature ?')) return;
    this.appService.cancelApplication(this.project.id).subscribe({
      next: () => {
        this.message = 'Candidature annulée.';
        this.hasApplied = false;
        this.applicationStatus = '';
      },
      error: (err) => {
        this.message = '';
        this.error = err?.error?.error || "Impossible d'annuler la candidature.";
      }
    });
  }
}
