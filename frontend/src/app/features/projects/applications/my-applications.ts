import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApplicationService } from '../application.service';
import { IconComponent } from '../../../shared/icon/icon';
import { Neo4jDatePipe } from '../../../shared/pipes/neo4j-date.pipe';

@Component({
  selector: 'app-my-applications',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent, Neo4jDatePipe],
  templateUrl: './my-applications.html',
  styleUrls: ['../list/project-list.scss', './my-applications.scss'] // Réutiliser le style des projets
})
export class MyApplicationsComponent implements OnInit {
  applications: any[] = [];
  loading = true;
  message = '';

  constructor(private appService: ApplicationService) {}

  ngOnInit(): void {
    this.refresh();
  }

  refresh(): void {
    this.loading = true;
    this.appService.getMyApplications().subscribe({
      next: (res: any) => {
        this.applications = Array.isArray(res.applications) ? res.applications : [];
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur chargement candidatures', err);
        this.loading = false;
      }
    });
  }

  cancel(projectId: string): void {
    if (!confirm('Annuler cette candidature ?')) return;
    this.appService.cancelApplication(projectId).subscribe({
      next: () => {
        this.message = 'Candidature annulée.';
        this.refresh();
        setTimeout(() => (this.message = ''), 3000);
      },
      error: (err) => {
        this.message = '';
        alert(err?.error?.error || "Impossible d'annuler la candidature.");
      }
    });
  }
}
