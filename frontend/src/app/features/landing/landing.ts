import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../shared/services/auth';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './landing.html',
  styleUrls: ['./landing.scss'],
})
export class LandingComponent implements OnInit {

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Si l'utilisateur est déjà connecté, on le redirige vers le Dashboard
    if (this.auth.isLoggedIn()) {
      console.log('User logged in, redirecting to dashboard');
      this.router.navigate(['/dashboard']);
    }
  }

  goToLogin() {
    console.log('Navigating to login...');
    this.router.navigate(['/login']);
  }

  goToRegister() {
    console.log('Navigating to register...');
    this.router.navigate(['/register']);
  }
}