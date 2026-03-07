import { Component, OnInit, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MessageService } from '../message.service';
import { AuthService } from '../../../shared/services/auth';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './chat.html',
  styleUrls: ['./chat.scss']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;
  
  messages: any[] = [];
  newMessage = '';
  otherEmail = '';
  loading = true;
  currentUserEmail = '';

  constructor(
    private route: ActivatedRoute,
    private messageService: MessageService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.currentUserEmail = this.auth.currentUser().email;
    this.route.paramMap.subscribe(params => {
      this.otherEmail = params.get('email') || '';
      if (this.otherEmail) {
        this.loadMessages();
      }
    });
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
    } catch(err) { }
  }

  loadMessages(): void {
    this.loading = true;
    this.messageService.getMessages(this.otherEmail).subscribe({
      next: (res: any) => {
        this.messages = res.messages;
        this.loading = false;
        this.scrollToBottom();
      },
      error: (err) => {
        console.error('Erreur chargement messages', err);
        this.loading = false;
      }
    });
  }

  sendMessage(): void {
    if (!this.newMessage.trim()) return;

    this.messageService.sendMessage(this.otherEmail, this.newMessage).subscribe({
      next: () => {
        // Ajouter le message localement pour l'instantanéité
        this.messages.push({
          content: this.newMessage,
          sender_email: this.currentUserEmail,
          timestamp: new Date().toISOString()
        });
        this.newMessage = '';
        this.scrollToBottom();
      },
      error: (err) => alert("Erreur d'envoi")
    });
  }
}
