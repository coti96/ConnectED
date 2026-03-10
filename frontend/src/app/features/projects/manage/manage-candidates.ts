import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ApplicationService } from '../application.service';
import { ProjectService } from '../project.service';
import { IconComponent } from '../../../shared/icon/icon';

@Component({
  selector: 'app-manage-candidates',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent],
  templateUrl: './manage-candidates.html',
  styleUrls: ['./manage-candidates.scss']
})
export class ManageCandidatesComponent implements OnInit {
  applications: any[] = [];
  project: any;
  loading = true;
  projectId: string = '';

  constructor(
    private route: ActivatedRoute,
    private appService: ApplicationService,
    private projectService: ProjectService
  ) {}

  ngOnInit(): void {
    this.projectId = this.route.snapshot.paramMap.get('id') || '';
    if (this.projectId) {
      this.loadData();
    }
  }

  loadData(): void {
    // 1. Charger les infos du projet
    this.projectService.getProjectById(this.projectId).subscribe((res: any) => {
      this.project = res.project;
    });

    // 2. Charger les candidatures
    this.appService.getProjectApplications(this.projectId).subscribe({
      next: (res: any) => {
        this.applications = res.applications;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur', err);
        this.loading = false;
      }
    });
  }

  updateStatus(applicantEmail: string, status: string): void {
    this.appService.updateApplicationStatus(this.projectId, applicantEmail, status).subscribe({
      next: () => {
        // Mettre à jour localement
        const app = this.applications.find(a => a.applicant.email === applicantEmail);
        if (app) app.status = status;
      },
      error: (err) => alert('Erreur mise à jour statut')
    });
  }

  getCount(status: string): number {
    return this.applications.filter(app => app.status === status).length;
  }
}
