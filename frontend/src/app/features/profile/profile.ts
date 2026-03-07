import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ProfileService } from './profile.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './profile.html',
  styleUrls: ['./profile.scss']
})
export class ProfileComponent implements OnInit {
  profileForm: FormGroup;
  technologies: string[] = [];
  userRole: string = '';
  isEditing = false;
  message = '';

  constructor(
    private fb: FormBuilder,
    private profileService: ProfileService,
    private router: Router
  ) {
    this.profileForm = this.fb.group({
      nom: ['', Validators.required],
      prenom: ['', Validators.required],
      email: [{value: '', disabled: true}],
      ville: [''],
      bio_courte: [''],
      ecole: [''],
      filiere: [''],
      entreprise: [''],
      fonction: ['']
    });
  }

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile(): void {
    const token = localStorage.getItem('token');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }

    this.profileService.getProfile().subscribe({
      next: (data: any) => {
        console.log('Profil chargé:', data);
        this.userRole = data.role;
        this.technologies = data.technologies || [];
        
        this.profileForm.patchValue({
          nom: data.nom,
          prenom: data.prenom,
          email: data.email,
          ville: data.ville,
          bio_courte: data.bio_courte,
          ecole: data.ecole,
          filiere: data.filiere,
          entreprise: data.entreprise,
          fonction: data.fonction
        });

        if (!this.isEditing) {
          this.profileForm.disable();
        }
      },
      error: (err) => {
        console.error('Erreur chargement profil', err);
        if (err.status === 401) {
          localStorage.removeItem('token');
          this.router.navigate(['/login']);
        }
      }
    });
  }

  toggleEdit(): void {
    this.isEditing = !this.isEditing;
    if (this.isEditing) {
      this.profileForm.enable();
      this.profileForm.get('email')?.disable(); // Email reste toujours bloqué
    } else {
      this.profileForm.disable();
      this.loadProfile(); // Annuler les changements
    }
  }

  addTech(event: any): void {
    const val = event.target.value.trim();
    if (val && !this.technologies.includes(val)) {
      this.technologies.push(val);
    }
    event.target.value = '';
  }

  removeTech(tech: string): void {
    if (this.isEditing) {
      this.technologies = this.technologies.filter(t => t !== tech);
    }
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      const formData = {
        ...this.profileForm.getRawValue(),
        technologies: this.technologies
      };

      this.profileService.updateProfile(formData).subscribe({
        next: () => {
          this.message = 'Profil mis à jour avec succès !';
          this.isEditing = false;
          this.profileForm.disable();
          setTimeout(() => this.message = '', 3000);
        },
        error: (err) => {
          console.error('Erreur mise à jour', err);
          this.message = 'Erreur lors de la mise à jour.';
        }
      });
    }
  }
}
