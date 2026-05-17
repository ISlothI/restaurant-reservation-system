import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RestaurantService } from '../../../core/restaurant.service';
import { TableService } from '../../../core/table.service';
import { SlotService } from '../../../core/slot.service';
import { Restaurant } from '../../../shared/models/restaurant.model';
import { Table } from '../../../shared/models/table.model';
import { ReservationSlot, SlotCreate } from '../../../shared/models/slot.model';

@Component({
  selector: 'app-slots',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './slots.component.html',
})
export class SlotsComponent implements OnInit {
  restaurant: Restaurant | null = null;
  tables: Table[] = [];
  slots: ReservationSlot[] = [];
  loading = true;
  showForm = false;
  editingId: string | null = null;
  error = '';

  form = { table_id: '', start_at: '', end_at: '', status: 'open' as 'open' | 'closed' };

  constructor(
    private restaurantService: RestaurantService,
    private tableService: TableService,
    private slotService: SlotService
  ) {}

  ngOnInit(): void {
    this.restaurantService.getMyRestaurant().subscribe({
      next: (r) => {
        this.restaurant = r;
        if (r) {
          this.tableService.getByRestaurant(r.id).subscribe((t) => (this.tables = t));
          this.loadSlots();
        } else {
          this.loading = false;
        }
      },
      error: () => (this.loading = false),
    });
  }

  loadSlots(): void {
    if (!this.restaurant) return;
    this.loading = true;
    this.slotService.getByRestaurant(this.restaurant.id).subscribe({
      next: (s) => { this.slots = s; this.loading = false; },
      error: () => (this.loading = false),
    });
  }

  openCreate(): void {
    this.form = { table_id: '', start_at: '', end_at: '', status: 'open' };
    this.editingId = null;
    this.showForm = true;
    this.error = '';
  }

  openEdit(s: ReservationSlot): void {
    this.form = {
      table_id: s.table_id,
      start_at: s.start_at.slice(0, 16),
      end_at: s.end_at.slice(0, 16),
      status: s.status,
    };
    this.editingId = s.id;
    this.showForm = true;
    this.error = '';
  }

  save(): void {
    if (!this.restaurant) return;
    this.error = '';
    const payload = { ...this.form };
    if (this.editingId) {
      this.slotService.update(this.restaurant.id, this.editingId, payload).subscribe({
        next: () => { this.showForm = false; this.loadSlots(); },
        error: (e) => (this.error = e.error?.detail || 'Hiba'),
      });
    } else {
      this.slotService.create(this.restaurant.id, payload as SlotCreate).subscribe({
        next: () => { this.showForm = false; this.loadSlots(); },
        error: (e) => (this.error = e.error?.detail || 'Hiba'),
      });
    }
  }

  remove(id: string): void {
    if (!this.restaurant) return;
    this.slotService.delete(this.restaurant.id, id).subscribe({ next: () => this.loadSlots() });
  }

  getTableName(id: string): string {
    return this.tables.find((t) => t.id === id)?.name || id;
  }
}
