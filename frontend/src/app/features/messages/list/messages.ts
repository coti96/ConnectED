import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MessageService } from '../message.service';
import { AuthService } from '../../../shared/services/auth';

@Component({
  selector: 'app-messages',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './messages.html',
  styleUrls: ['./messages.scss']
})
export class MessagesComponent implements OnInit {
  conversations: any[] = [];
  loading = true;

  constructor(
    private messageService: MessageService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
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
