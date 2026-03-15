import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router, NavigationEnd } from '@angular/router';
import { ProjectService } from '../project.service';
import { AuthService } from '../../../shared/services/auth';
import { Subscription, filter } from 'rxjs';
import { IconComponent } from '../../../shared/icon/icon';
import { Neo4jDatePipe } from '../../../shared/pipes/neo4j-date.pipe';

@Component({
  selector: 'app-project-list',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent, Neo4jDatePipe],
  templateUrl: './project-list.html',
  styleUrls: ['./project-list.scss']
})
export class ProjectListComponent implements OnInit, OnDestroy {
  projects: any[] = [];
  filteredProjects: any[] = [];
  loading: boolean = true;
  searchTerm: string = '';
  selectedDomain: string = '';
  sortBy: 'deadline_asc' | 'deadline_desc' | 'title_asc' = 'deadline_asc';
  onlyOpen = true;

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
    this.projectService.getProjects().subscribe({
      next: (res: any) => {
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

  onSort(event: any) {
    this.sortBy = event.target.value;
    this.applyFilters();
  }

  toggleOnlyOpen(event: any) {
    this.onlyOpen = !!event.target.checked;
    this.applyFilters();
  }

  applyFilters() {
    const filtered = this.projects.filter(project => {
      const title = (project?.titre || '').toString().toLowerCase();
      const technologies = Array.isArray(project?.technologies) ? project.technologies : [];
      const matchesSearch = 
        title.includes(this.searchTerm) ||
        technologies.some((t: string) => (t || '').toString().toLowerCase().includes(this.searchTerm));
      
      const matchesDomain = 
        this.selectedDomain === '' || 
        project?.domain === this.selectedDomain || 
        (project?.domaine && project.domaine === this.selectedDomain); // Check both 'domain' and 'domaine'

      const matchesOpen = !this.onlyOpen || project?.statut === 'en_cours' || !project?.statut;

      return matchesSearch && matchesDomain && matchesOpen;
    });

    this.filteredProjects = filtered.sort((a: any, b: any) => {
      if (this.sortBy === 'title_asc') {
        return String(a?.titre || '').localeCompare(String(b?.titre || ''), 'fr');
      }

      const aDeadline = new Date(String(a?.deadline || '')).getTime();
      const bDeadline = new Date(String(b?.deadline || '')).getTime();
      const safeA = Number.isFinite(aDeadline) ? aDeadline : 0;
      const safeB = Number.isFinite(bDeadline) ? bDeadline : 0;
      return this.sortBy === 'deadline_desc' ? safeB - safeA : safeA - safeB;
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
