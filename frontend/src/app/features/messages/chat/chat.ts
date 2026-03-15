import { Component, OnInit, OnDestroy, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MessageService } from '../message.service';
import { AuthService } from '../../../shared/services/auth';
import { Neo4jDatePipe } from '../../../shared/pipes/neo4j-date.pipe';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Neo4jDatePipe],
  templateUrl: './chat.html',
  styleUrls: ['../list/messages.scss', './chat.scss'] // Réutiliser le style de la liste
})
export class ChatComponent implements OnInit, OnDestroy {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;
  
  messages: any[] = [];
  newMessage = '';
  otherEmail = '';
  loading = true;
  currentUserEmail = '';
  loadingOlder = false;

  private pollTimer: number | null = null;
  private oldestTimestamp: string | null = null;
  private lastTimestamp: string | null = null;
  private readonly pageSize = 50;

  constructor(
    private route: ActivatedRoute,
    private messageService: MessageService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.currentUserEmail = this.auth.currentUser()?.email || '';
    this.route.paramMap.subscribe(params => {
      this.otherEmail = params.get('email') || '';
      if (this.otherEmail) {
        this.loadMessages();
        this.startPolling();
      }
    });
  }

  ngOnDestroy(): void {
    this.stopPolling();
  }

  scrollToBottom(): void {
    try {
      this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
    } catch(err) { }
  }

  private isNearBottom(): boolean {
    try {
      const el = this.scrollContainer.nativeElement;
      return el.scrollHeight - el.scrollTop - el.clientHeight < 80;
    } catch {
      return true;
    }
  }

  loadMessages(): void {
    this.loading = true;
    this.messageService.getMessages(this.otherEmail, { limit: this.pageSize }).subscribe({
      next: (res: any) => {
        this.messages = Array.isArray(res.messages) ? res.messages : [];
        this.oldestTimestamp = this.messages.length ? this.messages[0]?.timestamp : null;
        this.lastTimestamp = this.messages.length ? this.messages[this.messages.length - 1]?.timestamp : null;
        this.loading = false;
        setTimeout(() => this.scrollToBottom(), 0);
      },
      error: (err) => {
        console.error('Erreur chargement messages', err);
        this.loading = false;
      }
    });
  }

  loadOlder(): void {
    if (!this.oldestTimestamp || this.loadingOlder) return;
    this.loadingOlder = true;
    this.messageService.getMessages(this.otherEmail, { limit: this.pageSize, before: this.oldestTimestamp, markRead: false }).subscribe({
      next: (res: any) => {
        const older = Array.isArray(res.messages) ? res.messages : [];
        if (older.length) {
          this.messages = [...older, ...this.messages];
          this.oldestTimestamp = this.messages[0]?.timestamp || this.oldestTimestamp;
        }
        this.loadingOlder = false;
      },
      error: () => {
        this.loadingOlder = false;
      }
    });
  }

  private startPolling(): void {
    this.stopPolling();
    this.pollTimer = window.setInterval(() => this.pollNewMessages(), 4000);
  }

  private stopPolling(): void {
    if (this.pollTimer == null) return;
    window.clearInterval(this.pollTimer);
    this.pollTimer = null;
  }

  private pollNewMessages(): void {
    if (!this.otherEmail || !this.lastTimestamp) return;
    this.messageService.getMessages(this.otherEmail, { since: this.lastTimestamp }).subscribe({
      next: (res: any) => {
        const incoming = Array.isArray(res.messages) ? res.messages : [];
        if (!incoming.length) return;

        const shouldScroll = this.isNearBottom();
        const existingKeys = new Set(this.messages.map((m: any) => `${m.sender_email}|${m.timestamp}|${m.content}`));
        for (const msg of incoming) {
          const k = `${msg.sender_email}|${msg.timestamp}|${msg.content}`;
          if (!existingKeys.has(k)) this.messages.push(msg);
        }
        this.lastTimestamp = this.messages[this.messages.length - 1]?.timestamp || this.lastTimestamp;
        if (shouldScroll) setTimeout(() => this.scrollToBottom(), 0);
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
        this.lastTimestamp = this.messages[this.messages.length - 1]?.timestamp || this.lastTimestamp;
        this.newMessage = '';
        setTimeout(() => this.scrollToBottom(), 0);
      },
      error: (err) => alert("Erreur d'envoi")
    });
  }
}
