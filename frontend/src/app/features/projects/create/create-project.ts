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
  styleUrls: ['../../auth/login/login.scss'] // Réutiliser le style des formulaires auth pour la cohérence
})
export class CreateProjectComponent {
  projectForm: FormGroup;
  technologies: string[] = [];
  message: string = '';

  constructor(
    private fb: FormBuilder,
    private projectService: ProjectService,
    private router: Router
  ) {
    this.projectForm = this.fb.group({
      titre: ['', Validators.required],
      description: ['', Validators.required],
      domaine: ['', Validators.required],
      nombre_places: [1, [Validators.required, Validators.min(1)]],
      deadline: ['', Validators.required]
    });
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
          console.log('Projet créé', res);
          this.router.navigate(['/projects']);
        },
        error: (err) => {
          console.error('Erreur création projet', err);
          this.message = 'Erreur lors de la création du projet.';
        }
      });
    }
  }
}
