import { Component } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import {AuthService} from '../../../shared/services/auth';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, RouterModule],
  templateUrl: './login.html',
  styleUrls: ['./login.scss'],
})
export class LoginComponent {

  loginForm!: FormGroup;
  errorMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.errorMessage = '';
      
      this.auth.login(this.loginForm.value)
        .subscribe({
          next: (res: any) => {
            console.log('Connexion réussie', res);
            // Redirection vers le Dashboard après connexion
            this.router.navigate(['/dashboard']);
          },
          error: (err) => {
            console.error('Erreur connexion:', err);
            this.errorMessage = err.error?.error || 'Erreur de connexion';
          }
        });
    }
  }
}
