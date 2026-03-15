import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../shared/services/auth';
import { IconComponent } from '../icon/icon';
import { NotificationService } from '../services/notification.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent],
  templateUrl: './header.html',
  styleUrls: ['./header.scss'],
})
export class HeaderComponent {
  showNotifications = false;

  constructor(
    public auth: AuthService,
    public notifications: NotificationService
  ) {}

  toggleNotifications(): void {
    this.showNotifications = !this.showNotifications;
    if (this.showNotifications) this.notifications.refresh();
  }

}
