import { Routes } from '@angular/router';
import { LandingComponent } from './features/landing/landing';
import { LoginComponent } from './features/auth/login/login';

export const routes: Routes = [
  { path: '', component: LandingComponent },
  { path: 'login', component: LoginComponent }
];
