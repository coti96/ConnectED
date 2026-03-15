import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ApplicationService } from '../application.service';
import { ProjectService } from '../project.service';
import { IconComponent } from '../../../shared/icon/icon';
import { Neo4jDatePipe } from '../../../shared/pipes/neo4j-date.pipe';
import { catchError, finalize, forkJoin, of, timeout } from 'rxjs';

@Component({
  selector: 'app-manage-candidates',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, IconComponent, Neo4jDatePipe],
  templateUrl: './manage-candidates.html',
  styleUrls: ['./manage-candidates.scss']
})
export class ManageCandidatesComponent implements OnInit {
  applications: any[] = [];
  project: any;
  loading = true;
  projectId: string = '';
  errorMessage = '';
  statusFilter: 'ALL' | 'PENDING' | 'ACCEPTED' | 'REJECTED' = 'ALL';
  search = '';
  busyEmails = new Set<string>();
  private hardLoadingTimer: any = null;

  constructor(
    private route: ActivatedRoute,
    private appService: ApplicationService,
    private projectService: ProjectService
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.projectId = params.get('id') || '';
      if (!this.projectId) {
        this.loading = false;
        this.errorMessage = 'Projet introuvable.';
        return;
      }
      this.loadData();
    });
  }

  loadData(): void {
    this.loading = true;
    this.errorMessage = '';

    if (this.hardLoadingTimer) clearTimeout(this.hardLoadingTimer);
    this.hardLoadingTimer = setTimeout(() => {
      if (!this.loading) return;
      this.loading = false;
      if (!this.errorMessage) {
        this.errorMessage = "Le chargement est bloqué. Vérifiez votre connexion ou reconnectez-vous.";
      }
    }, 10000);

    let appsError: any = null;

    forkJoin({
      projectRes: this.projectService.getProjectById(this.projectId).pipe(
        timeout(15000),
        catchError(() => of(null))
      ),
      appsRes: this.appService.getProjectApplications(this.projectId).pipe(
        timeout(15000),
        catchError(err => {
          appsError = err;
          return of({ applications: [] });
        })
      )
    })
      .pipe(
        finalize(() => {
          if (this.hardLoadingTimer) clearTimeout(this.hardLoadingTimer);
          this.loading = false;
        })
      )
      .subscribe(({ projectRes, appsRes }: any) => {
        this.project = projectRes?.project || null;
        const rawApps = Array.isArray(appsRes?.applications) ? appsRes.applications : [];
        this.applications = rawApps.filter((a: any) => a && typeof a === 'object');

        if (appsError) {
          if (appsError?.status === 401 || appsError?.status === 422) {
            this.errorMessage = 'Session expirée. Veuillez vous reconnecter.';
          } else if (appsError?.name === 'TimeoutError') {
            this.errorMessage = "Le serveur met trop de temps à répondre. Réessayez dans un instant.";
          } else if (appsError?.status === 0) {
            this.errorMessage = "Impossible de joindre le serveur. Vérifiez que le backend tourne bien.";
          } else {
            this.errorMessage =
              appsError?.error?.error ||
              appsError?.error?.message ||
              'Impossible de charger les candidatures.';
          }
        }
      });
  }

  setFilter(filter: 'ALL' | 'PENDING' | 'ACCEPTED' | 'REJECTED'): void {
    this.statusFilter = filter;
  }

  get filteredApplications(): any[] {
    const normalizedSearch = (this.search || '').trim().toLowerCase();
    return (this.applications || [])
      .filter(app => {
        if (this.statusFilter === 'ALL') return true;
        return app?.status === this.statusFilter;
      })
      .filter(app => {
        if (!normalizedSearch) return true;
        const applicant = app?.applicant || {};
        const techs = Array.isArray(applicant.technologies) ? applicant.technologies : [];
        const haystack = [
          applicant.prenom,
          applicant.nom,
          applicant.email,
          applicant.role,
          ...techs
        ]
          .filter(Boolean)
          .join(' ')
          .toLowerCase();
        return haystack.includes(normalizedSearch);
      })
      .slice()
      .sort((a, b) => {
        const da = Date.parse(a?.date || '') || 0;
        const db = Date.parse(b?.date || '') || 0;
        return db - da;
      });
  }

  updateStatus(applicantEmail: string, status: string): void {
    if (!applicantEmail || this.busyEmails.has(applicantEmail)) return;
    this.busyEmails.add(applicantEmail);
    this.appService.updateApplicationStatus(this.projectId, applicantEmail, status).subscribe({
      next: () => {
        // Mettre à jour localement
        const app = this.applications.find(a => a?.applicant?.email === applicantEmail);
        if (app) app.status = status;
        this.busyEmails.delete(applicantEmail);
      },
      error: (err) => {
        this.busyEmails.delete(applicantEmail);
        if (err?.status === 401 || err?.status === 422) {
          this.errorMessage = 'Session expirée. Veuillez vous reconnecter.';
          return;
        }
        this.errorMessage = err?.error?.error || err?.error?.message || 'Erreur lors de la mise à jour du statut.';
      }
    });
  }

  getCount(status: string): number {
    return this.applications.filter(app => app?.status === status).length;
  }

  getRoleLabel(role: string): string {
    if (role === 'etudiant') return 'Étudiant';
    if (role === 'professionnel') return 'Professionnel';
    if (role === 'encadrant') return 'Encadrant';
    return role || 'Utilisateur';
  }

  getRoleIcon(role: string): any {
    if (role === 'etudiant') return 'graduationCap';
    if (role === 'professionnel') return 'projects';
    if (role === 'encadrant') return 'badge';
    return 'profile';
  }

  get acceptedCount(): number {
    return this.getCount('ACCEPTED');
  }
}
