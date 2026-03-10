import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../../shared/services/auth';

@Component({
  selector: 'app-projects-shell',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './projects-shell.html',
  styleUrls: ['./projects-shell.scss']
})
export class ProjectsShellComponent {
  constructor(public auth: AuthService) {}
}

