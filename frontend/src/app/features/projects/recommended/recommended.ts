import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
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
  styleUrls: ['../list/project-list.scss', './recommended.scss']
})
export class RecommendedProjectsComponent implements OnInit {
  projects: any[] = [];
  loading: boolean = true;

  constructor(
    private projectService: ProjectService,
    public auth: AuthService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.projectService.getRecommendedProjects().subscribe({
      next: (res: any) => {
        this.projects = res.recommendations;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Erreur:', err);
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }
}