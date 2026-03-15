import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ProjectService } from '../project.service';
import { IconComponent } from '../../../shared/icon/icon';

@Component({
  selector: 'app-create-project',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule, IconComponent],
  templateUrl: './create-project.html',
  styleUrls: ['../../auth/login/login.scss', './create-project.scss'] // Réutiliser le style des formulaires auth pour la cohérence
})
export class CreateProjectComponent {
  projectForm: FormGroup;
  technologies: string[] = [];
  message: string = '';
  descriptionMax = 1200;

  constructor(
    private fb: FormBuilder,
    private projectService: ProjectService,
    private router: Router
  ) {
    this.projectForm = this.fb.group({
      titre: ['', Validators.required],
      description: ['', [Validators.required, Validators.maxLength(this.descriptionMax)]],
      domaine: ['', Validators.required],
      nombre_places: [1, [Validators.required, Validators.min(1)]],
      deadline: ['', Validators.required]
    });
  }

  get descriptionLength(): number {
    const value = this.projectForm.get('description')?.value;
    return typeof value === 'string' ? value.length : 0;
  }

  addTech(event: any): void {
    const val = event.target.value.trim();
    if (val && !this.technologies.includes(val)) {
      this.technologies.push(val);
    }
    event.target.value = '';
  }

  removeTech(tech: string): void {
    this.technologies = this.technologies.filter(t => t !== tech);
  }

  onSubmit(): void {
    if (this.projectForm.valid) {
      const formValue = this.projectForm.value;
      
      // Convertir la date locale en ISO
      const deadlineDate = new Date(formValue.deadline);
      const isoDeadline = deadlineDate.toISOString().slice(0, 19); // YYYY-MM-DDTHH:mm:ss

      const projectData = {
        ...formValue,
        deadline: isoDeadline,
        technologies: this.technologies
      };

      this.projectService.createProject(projectData).subscribe({
        next: (res) => {
          const id = (res as any)?.id;
          this.router.navigate(id ? ['/projects', id] : ['/projects']);
        },
        error: (err) => {
          console.error('Erreur création projet', err);
          if (err?.status === 401) {
            this.message = 'Session expirée. Veuillez vous reconnecter.';
            return;
          }
          this.message = err?.error?.error || err?.error?.message || 'Erreur lors de la création du projet.';
        }
      });
    }
  }
}
