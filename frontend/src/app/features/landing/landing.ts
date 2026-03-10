import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../shared/services/auth';
import { CommonModule } from '@angular/common';
import { IconComponent } from '../../shared/icon/icon';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [RouterModule, CommonModule, IconComponent],
  templateUrl: './landing.html',
  styleUrls: ['./landing.scss'],
  encapsulation: ViewEncapsulation.None
})
export class LandingComponent implements OnInit {

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // On ne redirige plus automatiquement vers le dashboard
    // L'utilisateur doit pouvoir voir la landing page même s'il est connecté
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
