import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApplicationService } from '../application.service';
import { IconComponent } from '../../../shared/icon/icon';

@Component({
  selector: 'app-my-applications',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent],
  templateUrl: './my-applications.html',
  styleUrls: ['../list/project-list.scss', './my-applications.scss'] // Réutiliser le style des projets
})
export class MyApplicationsComponent implements OnInit {
  applications: any[] = [];
  loading = true;

  constructor(private appService: ApplicationService) {}

  ngOnInit(): void {
    this.appService.getMyApplications().subscribe({
      next: (res: any) => {
        this.applications = res.applications;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur chargement candidatures', err);
        this.loading = false;
      }
    });
  }
}
