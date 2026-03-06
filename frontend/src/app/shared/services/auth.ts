import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  isLoggedIn = signal<boolean>(!!localStorage.getItem('token'));

  login(token: string) {
    localStorage.setItem('token', token);
    this.isLoggedIn.set(true);
  }

  logout() {
    localStorage.removeItem('token');
    this.isLoggedIn.set(false);
  }
}
