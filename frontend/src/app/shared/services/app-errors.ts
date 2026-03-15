import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AppErrorsService {
  fatalError = signal<string>('');

  setFatalError(message: string): void {
    this.fatalError.set(message);
  }

  clearFatalError(): void {
    this.fatalError.set('');
  }
}

