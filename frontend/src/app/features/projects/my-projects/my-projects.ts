import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProjectService } from '../project.service';
import { AuthService } from '../../../shared/services/auth';

@Component({
  selector: 'app-my-projects',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './my-projects.html',
  styleUrls: ['./my-projects.scss']
})
export class MyProjectsComponent implements OnInit {
  projects: any[] = [];
  loading = true;

  constructor(private projectService: ProjectService, public auth: AuthService) {}

  ngOnInit(): void {
    if (!this.auth.isLoggedIn()) {
      this.loading = false;
      return;
    }

    this.projectService.getProjects().subscribe({
      next: (res: any) => {
        const all = res.projects || [];
        const email = this.auth.currentUser()?.email;
        this.projects = all.filter((p: any) => p.creator?.email && p.creator.email === email);
        this.loading = false;
      },
      error: () => {
        this.projects = [];
        this.loading = false;
      }
    });
  }
}

