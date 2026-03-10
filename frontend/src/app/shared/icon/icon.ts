import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export type AppIconName =
  | 'home'
  | 'projects'
  | 'recommended'
  | 'messages'
  | 'applications'
  | 'profile'
  | 'logout'
  | 'back'
  | 'plus'
  | 'search'
  | 'calendar'
  | 'users'
  | 'mail'
  | 'info'
  | 'warning'
  | 'globe'
  | 'idea'
  | 'lock'
  | 'chevronDown'
  | 'pin'
  | 'bell'
  | 'puzzle'
  | 'graduationCap'
  | 'keyboard'
  | 'emptyInbox'
  | 'refresh'
  | 'check'
  | 'x'
  | 'activity'
  | 'badge';

@Component({
  selector: 'app-icon',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './icon.html',
  styleUrls: ['./icon.scss']
})
export class IconComponent {
  @Input({ required: true }) name!: AppIconName;
  @Input() size = 18;
}
