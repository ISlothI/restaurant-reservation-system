import { Routes } from '@angular/router';
import { authGuard, adminGuard } from './core/auth.guard';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./features/restaurants/restaurant-list/restaurant-list.component').then(m => m.RestaurantListComponent) },
  { path: 'login', loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent) },
  { path: 'register', loadComponent: () => import('./features/auth/register/register.component').then(m => m.RegisterComponent) },
  { path: 'restaurants/:id', loadComponent: () => import('./features/restaurants/restaurant-detail/restaurant-detail.component').then(m => m.RestaurantDetailComponent) },
  {
    path: 'my-reservations',
    canActivate: [authGuard],
    loadComponent: () => import('./features/reservations/my-reservations/my-reservations.component').then(m => m.MyReservationsComponent),
  },
  {
    path: 'profile',
    canActivate: [authGuard],
    loadComponent: () => import('./features/profile/profile.component').then(m => m.ProfileComponent),
  },
  {
    path: 'book/:restaurantId',
    canActivate: [authGuard],
    loadComponent: () => import('./features/reservations/book/book.component').then(m => m.BookComponent),
  },
  {
    path: 'admin',
    canActivate: [adminGuard],
    children: [
      { path: '', loadComponent: () => import('./features/admin/dashboard/dashboard.component').then(m => m.DashboardComponent) },
      { path: 'tables', loadComponent: () => import('./features/admin/tables/tables.component').then(m => m.TablesComponent) },
      { path: 'slots', loadComponent: () => import('./features/admin/slots/slots.component').then(m => m.SlotsComponent) },
      { path: 'reservations', loadComponent: () => import('./features/admin/admin-reservations/admin-reservations.component').then(m => m.AdminReservationsComponent) },
    ],
  },
  { path: '**', redirectTo: '' },
];
