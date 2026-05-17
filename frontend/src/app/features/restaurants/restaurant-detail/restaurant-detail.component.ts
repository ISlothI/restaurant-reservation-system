import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { RestaurantService } from '../../../core/restaurant.service';
import { TableService } from '../../../core/table.service';
import { SlotService } from '../../../core/slot.service';
import { AuthService } from '../../../core/auth.service';
import { Restaurant } from '../../../shared/models/restaurant.model';
import { Table } from '../../../shared/models/table.model';
import { ReservationSlot } from '../../../shared/models/slot.model';

@Component({
  selector: 'app-restaurant-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './restaurant-detail.component.html',
})
export class RestaurantDetailComponent implements OnInit {
  restaurant: Restaurant | null = null;
  tables: Table[] = [];
  slots: ReservationSlot[] = [];
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private restaurantService: RestaurantService,
    private tableService: TableService,
    private slotService: SlotService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.restaurantService.getById(id).subscribe({
      next: (r) => {
        this.restaurant = r;
        this.loading = false;
        this.tableService.getByRestaurant(id).subscribe((t) => (this.tables = t));
        this.slotService.getByRestaurant(id, 'open').subscribe((s) => (this.slots = s));
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  serviceLabel(service: string): string {
    const map: Record<string, string> = {
      outdoor_seating: 'Terasz',
      vegan_options: 'Vegán ételek',
      gluten_free_options: 'Gluténmentes',
      wheelchair_accessible: 'Akadálymentes',
      pet_friendly: 'Kisállatbarát',
    };
    return map[service] || service;
  }

  tableTypeLabel(t: string): string {
    const map: Record<string, string> = { indoor: 'Belső', outdoor: 'Terasz', window: 'Ablak melletti' };
    return map[t] || t;
  }

  getTableName(tableId: string): string {
    const t = this.tables.find((x) => x.id === tableId);
    return t ? t.name : tableId;
  }
}
