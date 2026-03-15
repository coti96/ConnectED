import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { LandingComponent } from '../landing/landing';
import { AuthService } from '../../shared/services/auth';
import { DashboardService } from '../dashboard/dashboard.service';
import { ProjectService } from '../projects/project.service';
import { IconComponent } from '../../shared/icon/icon';
import { Neo4jDatePipe } from '../../shared/pipes/neo4j-date.pipe';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, LandingComponent, IconComponent, Neo4jDatePipe],
  templateUrl: './home.html',
  styleUrls: ['./home.scss']
})
export class HomeComponent implements OnInit {
  dashboard: any = null;
  recommendations: any[] = [];
  loading = false;
  error = '';

  constructor(
    public auth: AuthService,
    private router: Router,
    private dashboardService: DashboardService,
    private projectService: ProjectService
  ) {}

  ngOnInit(): void {
    if (!this.auth.isLoggedIn()) return;
    this.loading = true;

    this.dashboardService.getDashboardData().subscribe({
      next: (res: any) => {
        this.dashboard = res;
        this.loading = false;
      },
      error: (err: any) => {
        if (err?.status === 401 || err?.status === 422) {
          this.auth.logout();
          this.router.navigate(['/login']);
          return;
        }
        this.error = 'Impossible de charger votre accueil.';
        this.loading = false;
      }
    });

    this.projectService.getRecommendedProjects().subscribe({
      next: (res: any) => {
        this.recommendations = res.recommendations || [];
      },
      error: () => {
        this.recommendations = [];
      }
    });
  }

  initial(): string {
    const user = this.auth.currentUser();
    const source = user?.prenom || user?.email || 'U';
    return String(source).charAt(0).toUpperCase();
  }
}
