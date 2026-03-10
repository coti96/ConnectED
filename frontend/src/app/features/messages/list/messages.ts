import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { MessageService } from '../message.service';
import { AuthService } from '../../../shared/services/auth';
import { IconComponent } from '../../../shared/icon/icon';

@Component({
  selector: 'app-messages',
  standalone: true,
  imports: [CommonModule, RouterModule, IconComponent],
  templateUrl: './messages.html',
  styleUrls: ['./messages.scss']
})
export class MessagesComponent implements OnInit {
  conversations: any[] = [];
  loading = true;

  constructor(
    private messageService: MessageService,
    public auth: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Vérifier si un contact est demandé via queryParams
    this.route.queryParams.subscribe(params => {
      const contactEmail = params['contact'];
      if (contactEmail) {
        // Rediriger directement vers le chat avec cet utilisateur
        this.router.navigate(['/messages', contactEmail]);
      } else {
        // Sinon charger la liste
        this.loadConversations();
      }
    });
  }

  loadConversations() {
    this.loading = true;
    this.messageService.getConversations().subscribe({
      next: (res: any) => {
        this.conversations = res.conversations;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur chargement conversations', err);
        this.loading = false;
      }
    });
  }
}
