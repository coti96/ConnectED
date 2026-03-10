import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProjectService } from '../project.service';
import { AuthService } from '../../../shared/services/auth';
import { IconComponent } from '../../../shared/icon/icon';

@Component({
  selector: 'app-recommended-projects',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent],
  templateUrl: './recommended.html',
  styleUrls: ['../list/project-list.scss', './recommended.scss'] // Réutiliser le style + custom
})
export class RecommendedProjectsComponent implements OnInit {
  projects: any[] = [];
  loading: boolean = true;

  constructor(
    private projectService: ProjectService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.projectService.getRecommendedProjects().subscribe({
      next: (res: any) => {
        this.projects = res.recommendations;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur chargement recommandations', err);
        this.loading = false;
      }
    });
  }
}
