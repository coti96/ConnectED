import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router, NavigationEnd } from '@angular/router';
import { ProjectService } from '../project.service';
import { AuthService } from '../../../shared/services/auth';
import { Subscription, filter } from 'rxjs';

@Component({
  selector: 'app-project-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './project-list.html',
  styleUrls: ['./project-list.scss']
})
export class ProjectListComponent implements OnInit, OnDestroy {
  projects: any[] = [];
  filteredProjects: any[] = [];
  loading: boolean = true;
  searchTerm: string = '';
  selectedDomain: string = '';

  constructor(
    private projectService: ProjectService,
    public auth: AuthService,
    private router: Router,
    private cd: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadProjects();
  }

  ngOnDestroy(): void {
    // Nettoyage si nécessaire
  }

  loadProjects() {
    this.loading = true;
    console.log('Chargement des projets...');
    this.projectService.getProjects().subscribe({
      next: (res: any) => {
        console.log('Projets reçus:', res);
        this.projects = res.projects || [];
        this.filteredProjects = this.projects;
        this.loading = false;
        this.cd.detectChanges(); // Force la mise à jour de la vue
      },
      error: (err: any) => {
        console.error('Erreur chargement projets', err);
        this.loading = false;
        this.cd.detectChanges();
      }
    });
  }

  onSearch(event: any) {
    this.searchTerm = event.target.value.toLowerCase();
    this.applyFilters();
  }

  onFilterDomain(event: any) {
    this.selectedDomain = event.target.value;
    this.applyFilters();
  }

  applyFilters() {
    this.filteredProjects = this.projects.filter(project => {
      const matchesSearch = 
        project.titre.toLowerCase().includes(this.searchTerm) ||
        project.technologies.some((t: string) => t.toLowerCase().includes(this.searchTerm));
      
      const matchesDomain = 
        this.selectedDomain === '' || 
        project.domain === this.selectedDomain || 
        (project.domaine && project.domaine === this.selectedDomain); // Check both 'domain' and 'domaine'

      return matchesSearch && matchesDomain;
    });
  }

  contactCreator(project: any): void {
    if (!this.auth.isLoggedIn()) {
      alert('Veuillez vous connecter pour contacter le créateur.');
      this.router.navigate(['/login']);
      return;
    }
    
    // Correction: l'email du créateur est dans l'objet 'creator'
    const creatorEmail = project.creator?.email;
    if (creatorEmail) {
      this.router.navigate(['/messages'], { queryParams: { contact: creatorEmail } });
    } else {
      alert("Impossible de contacter le créateur de ce projet (email manquant).");
    }
  }
}
