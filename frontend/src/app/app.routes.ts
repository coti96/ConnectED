import { Routes } from '@angular/router';
import { LandingComponent } from './features/landing/landing';
import { LoginComponent } from './features/auth/login/login';
import { RegisterComponent } from './features/auth/register/register';
import { ProfileComponent } from './features/profile/profile';
import { ProjectListComponent } from './features/projects/list/project-list';
import { CreateProjectComponent } from './features/projects/create/create-project';
import { RecommendedProjectsComponent } from './features/projects/recommended/recommended';

export const routes: Routes = [
  { path: '', component: LandingComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'projects', component: ProjectListComponent },
  { path: 'projects/create', component: CreateProjectComponent },
  { path: 'recommended', component: RecommendedProjectsComponent }
];
