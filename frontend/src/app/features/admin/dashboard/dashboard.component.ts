import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RestaurantService } from '../../../core/restaurant.service';
import { Restaurant, RestaurantCreate, RestaurantUpdate } from '../../../shared/models/restaurant.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  restaurant: Restaurant | null = null;
  loading = true;
  editing = false;
  creating = false;
  error = '';

  form: any = {
    name: '', description: '', address: '', contact: '',
    opening_hours: '', services: [] as string[], is_active: true,
  };

  allServices = [
    { value: 'outdoor_seating', label: 'Terasz' },
    { value: 'vegan_options', label: 'Vegán ételek' },
    { value: 'gluten_free_options', label: 'Gluténmentes' },
    { value: 'wheelchair_accessible', label: 'Akadálymentes' },
    { value: 'pet_friendly', label: 'Kisállatbarát' },
  ];

  constructor(private restaurantService: RestaurantService) {}

  ngOnInit(): void {
    this.loadRestaurant();
  }

  loadRestaurant(): void {
    this.loading = true;
    this.restaurantService.getMyRestaurant().subscribe({
      next: (r) => {
        this.restaurant = r;
        this.loading = false;
        if (!r) this.creating = true;
      },
      error: () => (this.loading = false),
    });
  }

  startEdit(): void {
    if (!this.restaurant) return;
    this.form = {
      name: this.restaurant.name,
      description: this.restaurant.description,
      address: this.restaurant.address,
      contact: this.restaurant.contact,
      opening_hours: this.restaurant.opening_hours,
      services: [...this.restaurant.services],
      is_active: this.restaurant.is_active,
    };
    this.editing = true;
  }

  toggleService(val: string): void {
    const idx = this.form.services.indexOf(val);
    if (idx >= 0) this.form.services.splice(idx, 1);
    else this.form.services.push(val);
  }

  save(): void {
    this.error = '';
    if (this.creating) {
      this.restaurantService.create(this.form as RestaurantCreate).subscribe({
        next: () => {
          this.creating = false;
          this.loadRestaurant();
        },
        error: (err) => (this.error = err.error?.detail || 'Hiba'),
      });
    } else if (this.editing && this.restaurant) {
      this.restaurantService.update(this.restaurant.id, this.form as RestaurantUpdate).subscribe({
        next: () => {
          this.editing = false;
          this.loadRestaurant();
        },
        error: (err) => (this.error = err.error?.detail || 'Hiba'),
      });
    }
  }

  cancel(): void {
    this.editing = false;
    this.creating = !this.restaurant;
  }
}
