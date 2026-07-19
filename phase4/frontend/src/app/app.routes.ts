import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Callback } from './pages/callback/callback';
import { Dashboard } from './pages/dashboard/dashboard';

export const routes: Routes = [
  { path: '', component: Login },
  { path: 'auth/callback', component: Callback },
  { path: 'dashboard', component: Dashboard },
  { path: '**', redirectTo: '' },
];
