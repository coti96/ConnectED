import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home';
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
import { ProjectsShellComponent } from './features/projects/shell/projects-shell';
import { MyProjectsComponent } from './features/projects/my-projects/my-projects';
import { authGuard } from './shared/guards/auth.guard';
import { adminGuard } from './shared/guards/admin.guard';
import { AdminProjectsComponent } from './features/admin/projects/admin-projects';
import { HelpComponent } from './features/help/help';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'admin', component: AdminProjectsComponent, canActivate: [authGuard, adminGuard] },
  { path: 'help', component: HelpComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] },
  { path: 'profile', component: ProfileComponent, canActivate: [authGuard] },
  { path: 'messages', component: MessagesComponent, canActivate: [authGuard] },
  { path: 'messages/:email', component: ChatComponent, canActivate: [authGuard] },
  {
    path: 'projects',
    component: ProjectsShellComponent,
    children: [
      { path: '', component: ProjectListComponent },
      { path: 'recommended', component: RecommendedProjectsComponent, canActivate: [authGuard] },
      { path: 'my-applications', component: MyApplicationsComponent, canActivate: [authGuard] },
      { path: 'my-projects', component: MyProjectsComponent, canActivate: [authGuard] },
      { path: 'create', component: CreateProjectComponent, canActivate: [authGuard] },
      { path: ':id/manage', component: ManageCandidatesComponent, canActivate: [authGuard] },
      { path: ':id', component: ProjectDetailComponent }
    ]
  },
  { path: 'recommended', redirectTo: 'projects/recommended', pathMatch: 'full' },
  // Rediriger /about vers l'accueil pour éviter l'erreur
  { path: 'about', redirectTo: '', pathMatch: 'full' },
  // Wildcard route pour attraper toutes les URLs inconnues
  { path: '**', redirectTo: '' }
];
