import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth';

export const adminGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const user = auth.currentUser();
  if (!auth.isLoggedIn() || !user) return router.parseUrl('/login');
  return user.role === 'admin' ? true : router.parseUrl('/');
};

