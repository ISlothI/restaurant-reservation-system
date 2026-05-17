import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReservationService } from '../../../core/reservation.service';
import { Reservation } from '../../../shared/models/reservation.model';

@Component({
  selector: 'app-my-reservations',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './my-reservations.component.html',
})
export class MyReservationsComponent implements OnInit {
  reservations: Reservation[] = [];
  loading = true;

  constructor(private reservationService: ReservationService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading = true;
    this.reservationService.getMy().subscribe({
      next: (data) => {
        this.reservations = data;
        this.loading = false;
      },
      error: () => (this.loading = false),
    });
  }

  cancel(id: string): void {
    this.reservationService.update(id, { status: 'cancelled' }).subscribe({
      next: () => this.load(),
    });
  }

  statusLabel(s: string): string {
    const map: Record<string, string> = {
      pending: 'Függőben',
      confirmed: 'Visszaigazolva',
      cancelled: 'Lemondva',
    };
    return map[s] || s;
  }

  statusClass(s: string): string {
    const map: Record<string, string> = {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
    };
    return map[s] || '';
  }

  occasionLabel(o: string | null): string {
    if (!o) return '';
    const map: Record<string, string> = {
      birthday: 'Születésnap',
      anniversary: 'Évforduló',
      date_night: 'Romantikus vacsora',
      engagement: 'Eljegyzés',
      business_dinner: 'Üzleti vacsora',
      family_celebration: 'Családi ünnepség',
    };
    return map[o] || o;
  }

  tableTypeLabel(t: string | undefined): string {
    if (!t) return '';
    return { indoor: 'Belső', outdoor: 'Terasz', window: 'Ablak melletti' }[t] || t;
  }
}
