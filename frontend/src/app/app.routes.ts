import { Routes } from '@angular/router';
import { LandingComponent } from './features/landing/landing';
import { LoginComponent } from './features/auth/login/login';
import { RegisterComponent } from './features/auth/register/register';
import { ProfileComponent } from './features/profile/profile';
import { ProjectListComponent } from './features/projects/list/project-list';
import { CreateProjectComponent } from './features/projects/create/create-project';
import { RecommendedProjectsComponent } from './features/projects/recommended/recommended';

import { ProjectDetailComponent } from './features/projects/detail/project-detail';
import { MyApplicationsComponent } from './features/projects/applications/my-applications';
import { ManageCandidatesComponent } from './features/projects/manage/manage-candidates';
import { MessagesComponent } from './features/messages/list/messages';
import { ChatComponent } from './features/messages/chat/chat';
import { DashboardComponent } from './features/dashboard/dashboard';

export const routes: Routes = [
  { path: '', component: LandingComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'messages', component: MessagesComponent },
  { path: 'messages/:email', component: ChatComponent },
  { path: 'projects', component: ProjectListComponent },
  { path: 'projects/create', component: CreateProjectComponent },
  { path: 'projects/my-applications', component: MyApplicationsComponent }, // AVANT :id
  { path: 'projects/:id', component: ProjectDetailComponent },
  { path: 'projects/:id/manage', component: ManageCandidatesComponent },
  { path: 'recommended', component: RecommendedProjectsComponent },
  // Rediriger /about vers l'accueil pour éviter l'erreur
  { path: 'about', redirectTo: '', pathMatch: 'full' },
  // Wildcard route pour attraper toutes les URLs inconnues
  { path: '**', redirectTo: '' }
];
