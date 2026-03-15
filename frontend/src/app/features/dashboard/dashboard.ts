import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DashboardService } from './dashboard.service';
import { AuthService } from '../../shared/services/auth';
import { IconComponent } from '../../shared/icon/icon';
import { Neo4jDatePipe } from '../../shared/pipes/neo4j-date.pipe';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent, Neo4jDatePipe],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class DashboardComponent implements OnInit {
  data: any = null;
  loading: boolean = true;

  constructor(
    private dashboardService: DashboardService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.dashboardService.getDashboardData().subscribe({
      next: (res: any) => {
        this.data = res;
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Erreur dashboard', err);
        this.loading = false;
      }
    });
  }
}
