import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { SlotService } from '../../../core/slot.service';
import { ReservationService } from '../../../core/reservation.service';
import { RestaurantService } from '../../../core/restaurant.service';
import { TableService } from '../../../core/table.service';
import { ReservationSlot } from '../../../shared/models/slot.model';
import { Restaurant } from '../../../shared/models/restaurant.model';
import { Table } from '../../../shared/models/table.model';

interface TimeGroup {
  key: string;
  label: string;
  slots: ReservationSlot[];
}

@Component({
  selector: 'app-book',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './book.component.html',
})
export class BookComponent implements OnInit {
  restaurantId = '';
  restaurant: Restaurant | null = null;
  slots: ReservationSlot[] = [];
  tables: Table[] = [];

  timeGroups: TimeGroup[] = [];
  selectedTimeKey = '';
  availableSlots: ReservationSlot[] = [];
  selectedSlotId = '';

  partySize = 1;
  specialOccasion: string | null = null;
  guestNote = '';
  error = '';
  success = '';
  loading = false;

  occasions = [
    { value: null, label: 'Nincs' },
    { value: 'birthday', label: 'Születésnap' },
    { value: 'anniversary', label: 'Évforduló' },
    { value: 'date_night', label: 'Romantikus vacsora' },
    { value: 'engagement', label: 'Eljegyzés' },
    { value: 'business_dinner', label: 'Üzleti vacsora' },
    { value: 'family_celebration', label: 'Családi ünnepség' },
  ];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private slotService: SlotService,
    private reservationService: ReservationService,
    private restaurantService: RestaurantService,
    private tableService: TableService
  ) {}

  ngOnInit(): void {
    this.restaurantId = this.route.snapshot.paramMap.get('restaurantId')!;
    this.restaurantService.getById(this.restaurantId).subscribe((r) => (this.restaurant = r));
    this.tableService.getByRestaurant(this.restaurantId).subscribe((t) => (this.tables = t));
    this.slotService.getByRestaurant(this.restaurantId, 'open').subscribe((s) => {
      this.slots = s;
      this.buildTimeGroups();
    });
  }

  private buildTimeGroups(): void {
    const groups = new Map<string, ReservationSlot[]>();
    for (const s of this.slots) {
      const key = `${s.start_at}|${s.end_at}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(s);
    }
    this.timeGroups = Array.from(groups.entries()).map(([key, slots]) => {
      const start = new Date(slots[0].start_at);
      const end = new Date(slots[0].end_at);
      const datePart = start.toLocaleDateString('hu-HU', { year: 'numeric', month: '2-digit', day: '2-digit' });
      const startTime = start.toLocaleTimeString('hu-HU', { hour: '2-digit', minute: '2-digit' });
      const endTime = end.toLocaleTimeString('hu-HU', { hour: '2-digit', minute: '2-digit' });
      return { key, label: `${datePart} ${startTime} – ${endTime}`, slots };
    });
  }

  onTimeChange(): void {
    this.selectedSlotId = '';
    const group = this.timeGroups.find((g) => g.key === this.selectedTimeKey);
    this.availableSlots = group ? group.slots : [];
  }

  getTable(tableId: string): Table | undefined {
    return this.tables.find((t) => t.id === tableId);
  }

  getTableLabel(tableId: string): string {
    const t = this.getTable(tableId);
    if (!t) return tableId;
    const typeLabel = { indoor: 'Belső', outdoor: 'Terasz', window: 'Ablak melletti' }[t.table_type] || t.table_type;
    return `${t.name} (${typeLabel}, ${t.capacity} fő)`;
  }

  onSubmit(): void {
    this.loading = true;
    this.error = '';
    this.success = '';
    this.reservationService
      .create({
        restaurant_id: this.restaurantId,
        slot_id: this.selectedSlotId,
        party_size: this.partySize,
        special_occasion: this.specialOccasion,
        guest_note: this.guestNote,
      })
      .subscribe({
        next: () => {
          this.loading = false;
          this.success = 'Foglalás sikeresen létrehozva!';
          setTimeout(() => this.router.navigate(['/my-reservations']), 1500);
        },
        error: (err) => {
          this.loading = false;
          this.error = err.error?.detail || 'Foglalás sikertelen';
        },
      });
  }
}
