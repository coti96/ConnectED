import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../shared/services/auth';
import { IconComponent } from '../icon/icon';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent],
  templateUrl: './header.html',
  styleUrls: ['./header.scss'],
})
export class HeaderComponent {

  constructor(public auth: AuthService) {}

}
