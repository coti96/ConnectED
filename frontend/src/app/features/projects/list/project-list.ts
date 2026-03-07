import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProjectService } from '../project.service';
import { AuthService } from '../../../shared/services/auth';

@Component({
  selector: 'app-project-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './project-list.html',
  styleUrls: ['./project-list.scss']
})
export class ProjectListComponent implements OnInit {
  projects: any[] = [];
  loading: boolean = true;

  constructor(
    private projectService: ProjectService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.projectService.getProjects().subscribe({
      next: (res: any) => {
        this.projects = res.projects;
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Erreur chargement projets', err);
        this.loading = false;
      }
    });
  }
}
