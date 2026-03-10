import { Component } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import {AuthService} from '../../../shared/services/auth';
import { CommonModule } from '@angular/common';
import { IconComponent } from '../../../shared/icon/icon';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, RouterModule, IconComponent],
  templateUrl: './register.html',
  styleUrls: ['../login/login.scss'], // Reuse login styles
})
export class RegisterComponent {

  registerForm!: FormGroup;
  errorMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router
  ) {
    this.registerForm = this.fb.group({
      nom: ['', Validators.required],
      prenom: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      role: ['etudiant', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.registerForm.valid) {
      this.errorMessage = '';
      
      this.auth.register(this.registerForm.value)
        .subscribe({
          next: (res: any) => {
            console.log('Inscription réussie', res);
            // Auto login or redirect to login
            this.router.navigate(['/login']);
          },
          error: (err) => {
            console.error('Erreur inscription:', err);
            this.errorMessage = err.error?.error || 'Erreur lors de l\'inscription';
          }
        });
    }
  }
}
