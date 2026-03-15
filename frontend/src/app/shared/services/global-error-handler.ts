import { ErrorHandler, Injectable } from '@angular/core';
import { AppErrorsService } from './app-errors';

@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  constructor(private errors: AppErrorsService) {}

  handleError(error: unknown): void {
    console.error(error);
    const message =
      "Une erreur est survenue côté interface. Recharge la page, et si ça revient reconnecte-toi.";
    this.errors.setFatalError(message);
  }
}

