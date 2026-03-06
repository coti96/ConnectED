import { Component } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import {AuthService} from '../../../shared/services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.scss'],
})
export class LoginComponent {

  loginForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private auth: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }

  onSubmit(): void {
    console.log("SUBMIT déclenché ");
    if (this.loginForm.valid) {

      this.http.post('http://localhost:5000/login', this.loginForm.value)
        .subscribe({
          next: (res: any) => {
            console.log('Réponse backend :', res);

            // on simule un token pour l'instant
            this.auth.login('fake-token');

            // redirection vers home
            this.router.navigate(['/']);
          },
          error: (err) => {
            console.error('Erreur :', err);
          }
        });

    }
  }
  }
