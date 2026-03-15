import { ApplicationConfig, ErrorHandler } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
// @ts-ignore
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './shared/services/auth-interceptor';
import { GlobalErrorHandler } from './shared/services/global-error-handler';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor])),
    { provide: ErrorHandler, useClass: GlobalErrorHandler }
  ]
};
