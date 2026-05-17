import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RestaurantService } from '../../../core/restaurant.service';
import { TableService } from '../../../core/table.service';
import { Restaurant } from '../../../shared/models/restaurant.model';
import { Table, TableCreate } from '../../../shared/models/table.model';

@Component({
  selector: 'app-tables',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './tables.component.html',
})
export class TablesComponent implements OnInit {
  restaurant: Restaurant | null = null;
  tables: Table[] = [];
  loading = true;
  showForm = false;
  editingId: string | null = null;
  error = '';

  form = { name: '', capacity: 2, table_type: 'indoor' as 'indoor' | 'outdoor' | 'window', is_active: true };

  constructor(
    private restaurantService: RestaurantService,
    private tableService: TableService
  ) {}

  ngOnInit(): void {
    this.restaurantService.getMyRestaurant().subscribe({
      next: (r) => {
        this.restaurant = r;
        if (r) this.loadTables();
        else this.loading = false;
      },
      error: () => (this.loading = false),
    });
  }

  loadTables(): void {
    if (!this.restaurant) return;
    this.loading = true;
    this.tableService.getByRestaurant(this.restaurant.id).subscribe({
      next: (t) => { this.tables = t; this.loading = false; },
      error: () => (this.loading = false),
    });
  }

  openCreate(): void {
    this.form = { name: '', capacity: 2, table_type: 'indoor', is_active: true };
    this.editingId = null;
    this.showForm = true;
    this.error = '';
  }

  openEdit(t: Table): void {
    this.form = { name: t.name, capacity: t.capacity, table_type: t.table_type, is_active: t.is_active };
    this.editingId = t.id;
    this.showForm = true;
    this.error = '';
  }

  save(): void {
    if (!this.restaurant) return;
    this.error = '';
    if (this.editingId) {
      this.tableService.update(this.restaurant.id, this.editingId, this.form).subscribe({
        next: () => { this.showForm = false; this.loadTables(); },
        error: (e) => (this.error = e.error?.detail || 'Hiba'),
      });
    } else {
      this.tableService.create(this.restaurant.id, this.form as TableCreate).subscribe({
        next: () => { this.showForm = false; this.loadTables(); },
        error: (e) => (this.error = e.error?.detail || 'Hiba'),
      });
    }
  }

  remove(id: string): void {
    if (!this.restaurant) return;
    this.tableService.delete(this.restaurant.id, id).subscribe({ next: () => this.loadTables() });
  }

  typeLabel(t: string): string {
    return { indoor: 'Belső', outdoor: 'Terasz', window: 'Ablak melletti' }[t] || t;
  }
}
