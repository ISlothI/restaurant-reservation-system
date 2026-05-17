import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RestaurantService } from '../../../core/restaurant.service';
import { ReservationService } from '../../../core/reservation.service';
import { SlotService } from '../../../core/slot.service';
import { TableService } from '../../../core/table.service';
import { Restaurant } from '../../../shared/models/restaurant.model';
import { Reservation } from '../../../shared/models/reservation.model';
import { ReservationSlot } from '../../../shared/models/slot.model';
import { Table } from '../../../shared/models/table.model';

interface TimeGroup { key: string; label: string; slots: ReservationSlot[]; }

@Component({
  selector: 'app-admin-reservations',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-reservations.component.html',
})
export class AdminReservationsComponent implements OnInit {
  restaurant: Restaurant | null = null;
  reservations: Reservation[] = [];
  slots: ReservationSlot[] = [];
  tables: Table[] = [];
  loading = true;

  // filter
  filterDate = '';
  filterPeriod = '';

  // edit
  editingId: string | null = null;
  editOriginalSlotId = '';
  editForm = {
    party_size: 1, special_occasion: null as string | null,
    guest_note: '', status: 'pending' as string,
    selectedTimeKey: '', slot_id: '',
  };
  editTimeGroups: TimeGroup[] = [];
  editAvailableSlots: ReservationSlot[] = [];
  editError = '';

  // create
  showCreate = false;
  createForm = { slot_id: '', party_size: 1, special_occasion: null as string | null, guest_note: '', selectedTimeKey: '' };
  createTimeGroups: TimeGroup[] = [];
  createAvailableSlots: ReservationSlot[] = [];
  createError = '';

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
    private restaurantService: RestaurantService,
    private reservationService: ReservationService,
    private slotService: SlotService,
    private tableService: TableService
  ) {}

  ngOnInit(): void {
    this.restaurantService.getMyRestaurant().subscribe({
      next: (r) => {
        this.restaurant = r;
        if (r) {
          this.tableService.getByRestaurant(r.id).subscribe((t) => (this.tables = t));
          this.slotService.getByRestaurant(r.id, 'open').subscribe((s) => (this.slots = s));
          this.loadReservations();
        } else {
          this.loading = false;
        }
      },
      error: () => (this.loading = false),
    });
  }

  loadReservations(): void {
    if (!this.restaurant) return;
    this.loading = true;
    this.slotService.getByRestaurant(this.restaurant.id, 'open').subscribe((s) => (this.slots = s));
    let dateFrom: string | undefined;
    let dateTo: string | undefined;
    if (this.filterDate) {
      const base = this.filterDate;
      if (this.filterPeriod === 'morning') { dateFrom = `${base}T06:00:00`; dateTo = `${base}T12:00:00`; }
      else if (this.filterPeriod === 'afternoon') { dateFrom = `${base}T12:00:00`; dateTo = `${base}T18:00:00`; }
      else if (this.filterPeriod === 'evening') { dateFrom = `${base}T18:00:00`; dateTo = `${base}T23:59:59`; }
      else { dateFrom = `${base}T00:00:00`; dateTo = `${base}T23:59:59`; }
    }
    this.reservationService.getByRestaurant(this.restaurant.id, undefined, dateFrom, dateTo).subscribe({
      next: (data) => { this.reservations = data; this.loading = false; },
      error: () => (this.loading = false),
    });
  }

  applyFilter(): void { this.loadReservations(); }
  clearFilter(): void { this.filterDate = ''; this.filterPeriod = ''; this.loadReservations(); }

  // === Create ===
  openCreate(): void {
    this.showCreate = true;
    this.createForm = { slot_id: '', party_size: 1, special_occasion: null, guest_note: '', selectedTimeKey: '' };
    this.createError = '';
    this.createTimeGroups = this.buildTimeGroups(this.slots);
    this.createAvailableSlots = [];
  }

  onCreateTimeChange(): void {
    this.createForm.slot_id = '';
    const g = this.createTimeGroups.find((x) => x.key === this.createForm.selectedTimeKey);
    this.createAvailableSlots = g ? g.slots : [];
  }

  saveCreate(): void {
    if (!this.restaurant) return;
    this.createError = '';
    this.reservationService.create({
      restaurant_id: this.restaurant.id,
      slot_id: this.createForm.slot_id,
      party_size: this.createForm.party_size,
      special_occasion: this.createForm.special_occasion,
      guest_note: this.createForm.guest_note,
    }).subscribe({
      next: () => { this.showCreate = false; this.loadReservations(); },
      error: (e) => (this.createError = e.error?.detail || 'Hiba'),
    });
  }

  // === Edit ===
  confirm(id: string): void {
    this.reservationService.update(id, { status: 'confirmed' }).subscribe({ next: () => this.loadReservations() });
  }

  cancel(id: string): void {
    this.reservationService.update(id, { status: 'cancelled' }).subscribe({ next: () => this.loadReservations() });
  }

  openEdit(r: Reservation): void {
    this.editingId = r.id;
    this.editOriginalSlotId = r.slot_id;
    if (!this.restaurant) return;
    this.slotService.getByRestaurant(this.restaurant.id).subscribe((allSlots) => {
      this.editTimeGroups = this.buildTimeGroups(allSlots);
      const currentSlot = allSlots.find((s) => s.id === r.slot_id);
      const timeKey = currentSlot ? `${currentSlot.start_at}|${currentSlot.end_at}` : '';
      this.editForm = {
        party_size: r.party_size, special_occasion: r.special_occasion,
        guest_note: r.guest_note, status: r.status,
        selectedTimeKey: timeKey, slot_id: r.slot_id,
      };
      this.onEditTimeChange();
      this.editError = '';
    });
  }

  onEditTimeChange(): void {
    const g = this.editTimeGroups.find((x) => x.key === this.editForm.selectedTimeKey);
    this.editAvailableSlots = g ? g.slots : [];
    if (!this.editAvailableSlots.find((s) => s.id === this.editForm.slot_id)) {
      this.editForm.slot_id = '';
    }
  }

  cancelEdit(): void { this.editingId = null; this.editError = ''; }

  saveEdit(): void {
    if (!this.editingId) return;
    this.editError = '';
    const payload: any = {
      party_size: this.editForm.party_size,
      special_occasion: this.editForm.special_occasion,
      guest_note: this.editForm.guest_note,
      status: this.editForm.status,
    };
    if (this.editForm.slot_id && this.editForm.slot_id !== this.editOriginalSlotId) {
      payload.slot_id = this.editForm.slot_id;
    }
    this.reservationService.update(this.editingId, payload).subscribe({
      next: () => { this.editingId = null; this.loadReservations(); },
      error: (e) => (this.editError = e.error?.detail || 'Hiba a mentés során'),
    });
  }

  // === Helpers ===
  private buildTimeGroups(slots: ReservationSlot[]): TimeGroup[] {
    const groups = new Map<string, ReservationSlot[]>();
    for (const s of slots) {
      const key = `${s.start_at}|${s.end_at}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(s);
    }
    return Array.from(groups.entries()).map(([key, sl]) => {
      const start = new Date(sl[0].start_at);
      const end = new Date(sl[0].end_at);
      const d = start.toLocaleDateString('hu-HU', { year: 'numeric', month: '2-digit', day: '2-digit' });
      const st = start.toLocaleTimeString('hu-HU', { hour: '2-digit', minute: '2-digit' });
      const et = end.toLocaleTimeString('hu-HU', { hour: '2-digit', minute: '2-digit' });
      return { key, label: `${d} ${st} – ${et}`, slots: sl };
    });
  }

  getTableLabel(tableId: string): string {
    const t = this.tables.find((x) => x.id === tableId);
    if (!t) return tableId;
    const typeLabel = { indoor: 'Belső', outdoor: 'Terasz', window: 'Ablak melletti' }[t.table_type] || t.table_type;
    return `${t.name} (${typeLabel}, ${t.capacity} fő)`;
  }

  tableTypeLabel(t: string | undefined): string {
    if (!t) return '';
    return { indoor: 'Belső', outdoor: 'Terasz', window: 'Ablak melletti' }[t] || t;
  }

  statusLabel(s: string): string {
    return { pending: 'Függőben', confirmed: 'Visszaigazolva', cancelled: 'Lemondva' }[s] || s;
  }

  statusClass(s: string): string {
    return {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
    }[s] || '';
  }

  occasionLabel(o: string | null): string {
    if (!o) return '-';
    const map: Record<string, string> = {
      birthday: 'Születésnap', anniversary: 'Évforduló', date_night: 'Romantikus vacsora',
      engagement: 'Eljegyzés', business_dinner: 'Üzleti vacsora', family_celebration: 'Családi ünnepség',
    };
    return map[o] || o;
  }
}
